# Getting started with Qiskit Sampler + QRMI

In this section, we take Qiskit’s [Getting started with Sampler](https://quantum.cloud.ibm.com/docs/en/guides/get-started-with-primitives#get-started-with-sampler) as our example and learn how to port the quantum program to run on Slurm using QRMI, and how to execute it.


## Setup your python environment

Refer [How to build and install QRMI Python package](https://github.com/qiskit-community/qrmi/blob/main/INSTALL.md#how-to-build--install-qrmi-python-package) to build wheel and install to your python venv.

Once you complete to setup your python environment, you will find ```qrmi``` in the result of ```pip list```.

```bash
pip list | grep qrmi
qrmi                      0.10.1
```

## Original Sampler code

Put the following code in an appropriate place within the shared volume.

```python
import numpy as np
from qiskit.circuit.library import efficient_su2
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2

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

# Initialize QRMI Sampler
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
```

## Port the program to run with QRMI

1. Replace the lines below with the following code block.
```python
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
```
to
```python
import random
from qrmi.primitives import QRMIService
from qrmi.primitives.ibm import SamplerV2, get_backend
```

2. Replace the lines below with the following code block.
```python
service = QiskitRuntimeService()
backend = service.least_busy(
    operational=True, simulator=False, min_num_qubits=127
)
```
to
```python
service = QRMIService()

resources = service.resources()
if len(resources) == 0:
    raise ValueError("No quantum resource is available.")

# Randomly select QR
qrmi = resources[random.randrange(len(resources))]
print(qrmi.metadata())

# Generate Qiskit backend from backend configuration & properties
backend = get_backend(qrmi)
```

3. Replace the lines below with the following code block.
```python
sampler = SamplerV2(mode=backend, options=options)
```
to
```python
sampler = SamplerV2(qrmi, options=options)
```

The files after porting can be found [here](./sampler_qrmi.py).

## Create Slurm script file

Create run_sampler.sh

```bash
#!/bin/bash

#SBATCH --job-name=sampler
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=qpu:1
#SBATCH --qpu=ibm_kingston

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Your script goes here
source /shared/tutorial/pyenv/bin/activate
srun python /shared/tutorial/getting_started/sampler_qrmi.py
```

The ```--qpu``` directive is required. This option specifies the quantum resource you intend to use.
The environment variables necessary for execution must be defined in ```/etc/slurm/qrmi_config.json```.

```json
{
  "resources": [
    {
      "name": "ibm_kingston",
      "type": "qiskit-runtime-service",
      "environment": {
        "QRMI_IBM_QRS_ENDPOINT": "https://quantum.cloud.ibm.com/api/v1",
        "QRMI_IBM_QRS_IAM_ENDPOINT": "https://iam.cloud.ibm.com",
        "QRMI_IBM_QRS_IAM_APIKEY": "*******",
        "QRMI_IBM_QRS_SERVICE_CRN": "crn:v1:bluemix:public:quantum-computing:us-east:a/*********::"
      }
    }
  ]
}
```

## Submit a job

```bash
sbatch sampler_qrmi.sh
```

The environment variable values defined in ```qrmi_config.json``` can be overridden by setting them in the shell where sbatch is executed, as shown below. This is useful when you want to use values you have obtained personally, such as an API key.

```bash
export ibm_kingston_QRMI_IBM_QRS_IAM_APIKEY=<my API key>
sbatch sampler_qrmi.sh
```

## Monitor your job status

```bash
squeue
```

## Review the result

```slurm-N.out``` file is generated once job is finished. You must see some log messages and binary string as Sampler result.
```txt
Starting at Fri Jan 23 10:14:04 UTC 2026
Running on hosts: c1
Running on 1 nodes.
Running 1 tasks.
Current working directory is /shared/job_scripts/qrmi
{'backend_name': 'ibm_kingston', 'session_id': 'a01b9d67-2b65-404c-8f92-1839f723239c'}
>>> Circuit ops (ISA): OrderedDict({'rz': 3030, 'sx': 753, 'rx': 511, 'cz': 378, 'measure': 127, 'barrier': 1})
>>> Job ID: d5pkjs9dgvjs73dbt0e0
>>> Job Status: JobStatus.QUEUED
Counts for the 'meas' output register: {'1000010000101110011100000000000001010110110001110010001010100011011011001111010110101011010101000001100010101101011101111100010': 1,
```

You have now successfully executed a simple Qiskit Sampler program on Slurm.

   
