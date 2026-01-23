import random
import numpy as np
from dotenv import load_dotenv
from qiskit.circuit.library import efficient_su2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qrmi.primitives import QRMIService
from qrmi.primitives.ibm import SamplerV2, get_target

# Create QRMI
load_dotenv()
service = QRMIService()

resources = service.resources()
if len(resources) == 0:
    raise ValueError("No quantum resource is available.")

# Randomly select QR
qrmi = resources[random.randrange(len(resources))]
print(qrmi.metadata())

# Generate transpiler target from backend configuration & properties
target = get_target(qrmi)

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
    target=target,
)
isa_circuit = pm.run(circuit)
print(f">>> Circuit ops (ISA): {isa_circuit.count_ops()}")

# Initialize QRMI Sampler
options = {
    "default_shots": 10000,
}
sampler = SamplerV2(qrmi, options=options)

# Next, invoke the run() method to generate the output. The circuit and optional
# parameter value sets are input as primitive unified bloc (PUB) tuples.
job = sampler.run([(isa_circuit, param_values)])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")
result = job.result()

# Get results for the first (and only) PUB
pub_result = result[0]
print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")
