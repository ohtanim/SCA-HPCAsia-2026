# Write Quantum Program in C++

We will now implement a C++ version of a program similar to the one used in the previous tutorial.
For executing the quantum workload, we will use [Qiskit‑cpp](https://github.com/Qiskit/qiskit-cpp). Qiskit‑cpp can be run using the QRMI libraries.


## Prerequisites

### Prepare Qiskit and Qiskit C extension
```bash
git clone git@github.com:Qiskit/qiskit.git
cd qiskit
make c
```

### Prepare QRMI
```bash
git clone git@github.com:qiskit-community/qrmi.git
cd qrmi
cargo build --release
```

### Prepare Qiskit C++
```bash
git clone git@github.com:Qiskit/qiskit-cpp.git
```

### Create a directory for this tutorial

```bash
cd qiskit-cpp
mkdir -p tutorial
cd tutorial
```

## Create C++ program

[sampler_test.cpp](./sampler_test.cpp)

The quantum workload is executed by the MPI process with rank 0. The quantum workload executed on rank 0 is based on this sample program, with the following code replaced by the code shown below so that it operates using the environment variables set by the Spank plugin.

```CPP
// Build Qiskit backend with QRMI instance
auto qpu_resources = _split(getenv("SLURM_JOB_QPU_RESOURCES"), ',');
std::string name = qpu_resources[0];
QrmiResourceType type_ = QRMI_RESOURCE_TYPE_QISKIT_RUNTIME_SERVICE;
std::shared_ptr<QrmiQuantumResource> qrmi(qrmi_resource_new(name.c_str(), type_), qrmi_resource_free);
Qiskit::providers::QRMIBackend backend(name, qrmi);
```

Post processing(get counts) is exactly same as one in previous tutorial.

## Build

```bash
mkdir build
cmake -DQISKIT_ROOT=<Qiskit source tree> -DQRMI_ROOT=<QRMI source tree> ..
make
```

## Create Slurm script for sampler_test

[sampler_test.sh](./sampler_test.sh)

4 MPI Ranks will be created.

```bash
#!/bin/bash
#SBATCH --job-name=sampler_test  # Job name
#SBATCH --nodes=2                # Request 2 nodes
#SBATCH --ntasks-per-node=2      # 4 MPI tasks per node
#SBATCH --time=00:05:00          # Time limit (hh:mm:ss)
#SBATCH -p normal
#SBATCH --gres=qpu:1
#SBATCH --qpu=ibm_torino

echo "Starting at `date`"
echo "Running on hosts: $SLURM_NODELIST"
echo "Running on $SLURM_NNODES nodes."
echo "Running $SLURM_NTASKS tasks."
echo "Current working directory is `pwd`"

# Run the MPI program using srun or mpirun
# srun is often the preferred method with Slurm
srun ./sampler_test
# Alternatively, you could use mpirun:
# mpirun ./sampler_test
```

## Run a jobs

```bash
sbatch sampler_test.sh
```

The environment variable values defined in ```qrmi_config.json``` can be overridden by setting them in the shell where sbatch is executed, as shown below. This is useful when you want to use values you have obtained personally, such as an API key.

```bash
export ibm_kingston_QRMI_IBM_QRS_IAM_APIKEY=<my API key>
sbatch sampler_test.sh
```

## Review the result

You must find the files similar to [slurm-43.out](./slurm-43.out) and [output.json](./output.json).


You have now successfully created a simple classical-quantum workroad in C++ and executed on Slurm.
