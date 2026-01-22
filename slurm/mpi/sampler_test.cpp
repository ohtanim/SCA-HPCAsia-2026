/*
# This code is part of Qiskit.
#
# (C) Copyright IBM 2026.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
*/

// Example of Quantum workload + MPI

#define _USE_MATH_DEFINES
#include <mpi.h>
#include <iostream>
#include <cstdint>
#include <cstdlib>
#include <cmath>
#include <fstream>
#include <vector>

#include "circuit/quantumcircuit.hpp"
#include "primitives/backend_sampler_v2.hpp"
#include "providers/qrmi_backend.hpp"
#include "compiler/transpiler.hpp"

#include "qrmi.h"

#include <nlohmann/json.hpp>
using json = nlohmann::json;

using namespace Qiskit;
using namespace Qiskit::circuit;
using namespace Qiskit::providers;
using namespace Qiskit::primitives;
using namespace Qiskit::compiler;

using Sampler = BackendSamplerV2;

const uint32_t BITLEN = 10;
const uint32_t MAXVAL = 1 << BITLEN;

static std::vector<std::string> _split(const std::string &s, char delim) {
    std::vector<std::string> elems;
    std::string item;
    for (char ch: s) {
        if (ch == delim) {
            if (!item.empty())
                elems.push_back(item);
                item.clear();
        }
        else {
            item += ch;
        }
    }
    if (!item.empty())
        elems.push_back(item);
    return elems;
}

static std::vector<std::string> _split(const std::string &s, char delim) {
    std::cerr <<  s << "  " << delim << std::endl;
    std::vector<std::string> elems;
    std::string item;
    for (char ch: s) {
        if (ch == delim) {
            if (!item.empty())
                elems.push_back(item);
                item.clear();
        }
        else {
            item += ch;
        }
    }
    if (!item.empty())
        elems.push_back(item);
    return elems;
}


int main(int argc, char** argv)
{
    MPI_Init(&argc, &argv);
    int rank = 0, size = 0;
    // Get the rank of the process
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    // Get the number of processes
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    // Print a message from each process
    std::cout <<  "Hello from processor, rank " << rank << " of " << size << " processes" << std::endl;

    uint32_t total_count = 0;
    std::vector<uint32_t> data;

    if (rank == 0) {

        // Map the problem - Create QuantumCircuit
        int num_qubits = BITLEN;
        int shots = 10000;
        auto qreg = QuantumRegister(num_qubits);
        auto creg = ClassicalRegister(num_qubits, std::string("meas"));
        QuantumCircuit circ(std::vector<QuantumRegister>({qreg,}), std::vector<ClassicalRegister>({creg,}));

        // GHZ circuit
        circ.h(0);
        for (int i = 0; i < num_qubits - 1; i++) {
            circ.cx(0, i + 1);
        }
        circ.measure(qreg, creg);
      
        // Build Qiskit backend with QRMI instance
        auto qpu_resources = _split(getenv("SLURM_JOB_QPU_RESOURCES"), ',');
        std::string name = qpu_resources[0];
        QrmiResourceType type_ = QRMI_RESOURCE_TYPE_QISKIT_RUNTIME_SERVICE;
        std::shared_ptr<QrmiQuantumResource> qrmi(qrmi_resource_new(name.c_str(), type_), qrmi_resource_free);
        Qiskit::providers::QRMIBackend backend(name, qrmi);


        // Optimize - Transpile the circuit
        auto transpiled_circ = transpile(circ, backend);

        // Execute
        auto sampler = Sampler(backend, shots);
        auto job = sampler.run({SamplerPub(transpiled_circ)});
        if (job == nullptr)
            return -1;
        auto result = job->result();

        // Processing the result
        auto pub_result = result[0];
        auto meas_bits = pub_result.data("meas");
        auto bits = meas_bits.get_bitstrings();

        data.reserve(bits.size());
        total_count = bits.size();

        for (const auto& b : bits) {
            uint32_t value = static_cast<uint32_t>(std::stoul(b, nullptr, 2));
            data.push_back(value);
        }

        // for debug
        std::ofstream ofs("input.bin", std::ios::binary);
        ofs.write(reinterpret_cast<const char*>(data.data()),
            data.size() * sizeof(uint32_t));
        ofs.close();
    }

    MPI_Bcast(&total_count, 1, MPI_UNSIGNED, 0, MPI_COMM_WORLD);

    uint32_t local_n = total_count / size;
    std::vector<uint32_t> local_data(local_n);

    MPI_Scatter(rank == 0 ? data.data() : nullptr, local_n, MPI_UNSIGNED,
        local_data.data(), local_n, MPI_UNSIGNED,
        0, MPI_COMM_WORLD);

    std::vector<int> local_hist(MAXVAL, 0);
    for (auto v : local_data) {
        if (v < MAXVAL) local_hist[v]++;
    }

    std::vector<int> global_hist;
    if (rank == 0) global_hist.resize(MAXVAL, 0);

    MPI_Reduce(local_hist.data(),
        rank == 0 ? global_hist.data() : nullptr,
        MAXVAL, MPI_INT, MPI_SUM, 0, MPI_COMM_WORLD);

    if (rank == 0) {
        std::ofstream fout("output.json");
        fout << "{";
        bool first = true;
        for (uint32_t i = 0; i < MAXVAL; ++i) {
            if (global_hist[i] > 0) {
                if (!first) fout << ",";
                fout << "\"" << i << "\":" << global_hist[i];
                first = false;
            }
        }
        fout << "}\n";
        fout.close();
    }

    MPI_Finalize();
    std::cout <<  "Completed, rank " << rank << " of " << size << " processes" << std::endl;
    return 0;
}

