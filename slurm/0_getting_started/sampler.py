import numpy as np
from qiskit.circuit.library import efficient_su2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_ibm_runtime import SamplerV2

service = QiskitRuntimeService()
backend = service.least_busy(
    operational=True, simulator=False, min_num_qubits=127
)

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

# Initialize the Qiskit Runtime Sampler
options = {
    "default_shots": 10000,
}
sampler = SamplerV2(mode=backend, options=options)

# Next, invoke the run() method to generate the output. The circuit and optional
# parameter value sets are input as primitive unified bloc (PUB) tuples.
job = sampler.run([(isa_circuit, param_values)])
print(f">>> Job ID: {job.job_id()}")
print(f">>> Job Status: {job.status()}")
result = job.result()

# Get results for the first (and only) PUB
pub_result = result[0]
print(f"Counts for the 'meas' output register: {pub_result.data.meas.get_counts()}")
