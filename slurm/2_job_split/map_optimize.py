# This code is part of Qiskit.
#
# (C) Copyright 2024, 2025 IBM. All Rights Reserved.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""SamplerV2 example with IBM Direct Access QRMI"""

# pylint: disable=invalid-name
import json
import random
import numpy as np
from qiskit import qasm3
from qiskit.circuit.library import efficient_su2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.primitives.containers.sampler_pub import SamplerPub
from qiskit_ibm_runtime.utils import RuntimeEncoder
from qrmi.primitives import QRMIService

# from qrmi.primitives.ibm import SamplerV2, get_backend
from qrmi.primitives.ibm import get_backend

# Create QRMI
service = QRMIService()

resources = service.resources()
if len(resources) == 0:
    raise ValueError("No quantum resource is available.")

# Randomly select QR
qrmi = resources[random.randrange(len(resources))]
print(qrmi.metadata())

# Generate transpiler target from backend configuration & properties
backend = get_backend(qrmi)

# Create a circuit - You need at least one circuit as the input to the Sampler primitive.
circuit = efficient_su2(127, entanglement="linear")
circuit.measure_all()
# The circuit is parametrized, so we will define the parameter values for execution
param_values = np.random.rand(circuit.num_parameters)

# The circuit and observable need to be transformed to only use instructions
# supported by the QPU (referred to as instruction set architecture (ISA) circuits).
# We'll use the transpiler to do this.
pm = generate_preset_pass_manager(
    optimization_level=1,
    backend=backend,
)
isa_circuit = pm.run(circuit)
print(f">>> Circuit ops (ISA): {isa_circuit.count_ops()}")

# Initialize QRMI Sampler
# options = {
#    "default_shots": 10000,
# }
# sampler = SamplerV2(qrmi, options=options)
#
# Next, invoke the run() method to generate the output. The circuit and optional
# parameter value sets are input as primitive unified bloc (PUB) tuples.
# job = sampler.run([(isa_circuit, param_values)])
# print(f">>> Job ID: {job.job_id()}")
# print(f">>> Job Status: {job.status()}")
# result = job.result()
#
# Get results for the first (and only) PUB
# pub_result = result[0]
# print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")

shots = 10000
pub = SamplerPub.coerce((isa_circuit, param_values), shots)
qasm3_str = qasm3.dumps(
    pub.circuit,
    disable_constants=True,
    allow_aliasing=True,
    experimental=qasm3.ExperimentalFeatures.SWITCH_CASE_V1,
)

param_array = pub.parameter_values.as_array(pub.circuit.parameters).tolist()

# Generates JSON representation of primitive job
input_json = {
    "pubs": [(qasm3_str, param_array)],
    "version": 2,
    "support_qiskit": True,
    "shots": shots,
    "options": {},
}


def dump(json_data: dict, filename: str) -> None:
    """Write json data to the specified file

    Args:
        json_data(dict): JSON data
        filename(str): output filename
    """
    print(json.dumps(json_data, cls=RuntimeEncoder, indent=2))
    with open(filename, "w", encoding="utf-8") as primitive_input_file:
        json.dump(json_data, primitive_input_file, cls=RuntimeEncoder, indent=2)


dump(
    {"parameters": input_json, "program_id": "sampler"},
    f"sampler_input_{backend.name}.json",
)
dump(input_json, f"sampler_input_{backend.name}_params_only.json")

print("done")
