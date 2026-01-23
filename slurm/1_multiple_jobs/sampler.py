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
import random
import numpy as np
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qrmi.primitives import QRMIService
from qrmi.primitives.ibm import SamplerV2, get_target

# Create QRMI
service = QRMIService()

resources = service.resources()
if len(resources) == 0:
    raise ValueError("No quantum resource is available.")

# Randomly select QR
qrmi = resources[random.randrange(len(resources))]
print(qrmi.metadata())

# Generate transpiler target from backend configuration & properties
target = get_target(qrmi)

BITLEN=10

qc_ghz = QuantumCircuit(BITLEN)
qc_ghz.h(0)
qc_ghz.cx(0, range(1, BITLEN))
qc_ghz.measure_active()
pm = generate_preset_pass_manager(
        optimization_level=3,
        target=target,
        seed_transpiler=123,
    )
isa = pm.run(qc_ghz)
pub_like = (isa, )

# Initialize QRMI Sampler
options = {
    "default_shots": 10000,
}
sampler = SamplerV2(qrmi, options=options)

# Next, invoke the run() method to generate the output. The circuit and optional
# parameter value sets are input as primitive unified bloc (PUB) tuples.
job = sampler.run([pub_like])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")
results = job.result()

# Get results for the first (and only) PUB
pub_result = results[0]
print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")

bitstrings = results[0].data.meas.get_bitstrings()
print("bitstrings >>>> ", len(bitstrings))
u32int_array = np.array(
    [int(b, base=2) for b in bitstrings],
        dtype=np.uint32,
    )
print(u32int_array)
u32int_array.tofile("input.bin")
