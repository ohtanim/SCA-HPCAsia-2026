# SCA/HPCAsia 2026 Tutorial - Workload and workflow management in quantum-classical HPC

## Abstract
Quantum computing has the potential to elevate heterogeneous high-performance computers to tackle problems that are intractable for purely classical supercomputers.
Integrating quantum processing units (QPUs) into a heterogeneous compute infrastructure, referred to as the quantum-centric supercomputing (QCSC) model, involves
CPUs, GPUs, and other specialized accelerators (AIUs, etc.). Achieving this requires collaboration across multiple industries to align efforts in integrating hardware and
software.

IBM and our HPC/Quantum partners have developed software components to enable the handling of QPU workloads within the Slurm workload manager in HPC environments. This
tutorial session will provide a comprehensive overview of the architecture, demonstrate how to create Slurm jobs for executing quantum workloads, and discuss the execution of
Quantum-Classical hybrid workloads. Participants will gain hands-on experience though live demonstrations, exploring the integration of quantum workloads into existing HPC
systems.

Efficient scheduling is only part of the solution. In the second half of the session, we will address the orchestration challenges unique to hybrid Quantum-Classical workloads—
such as iterative execution, hyperparameter tuning, and backend instability. Participants will learn how to build scalable, fault-tolerant pipelines using Python-based workflow
tools like Prefect. Key features such as checkpointing, automatic retries, and real-time observability will be demonstrated live, equipping attendees with the skills to manage
complex quantum workloads and prepare for future challenges in scalability and reproducibility.


## Tutorial Agenda
- Date: Mon, January 26, 2026
- Time: 13:30 - 16:30
- Room: 1007

| Time | | Theme | Presenter |
|----|----|----|----|
|1:30pm - 1:35pm|5min|Opening|Yoonho Park|
|1:35pm - 2:45pm|70min|Towards the Integration of HPC and Quantum Computing|Munetaka Ohtani|
|2:45pm - 3:15pm|30min|Coffee Break||
|3:15pm - 4:25pm|70min|Workflow and Workload Management in Quantum-Classical HPC|Shweta Salaria|
|4:25pm - 4:30pm|5min|Closing|Yoonho Park|

## Presenters

- Yoonho Park (yoonho@us.ibm.com) is a Principal Research Scientist at IBM Research-Yorktown with experience in operating systems, distributed systems, HPC, and cloud infrastructure. He led the IBM Research software teams during the delivery of the CORAL supercomputers, Summit and Sierra. He then led the delivery of on-premise AI cloud to IBM Research partners. His current focus is HPC-Quantum integration.

- Munetaka Ohtani(ohtanim@jp.ibm.com) is a Senior Software Engineer at IBM Quantum, IBM Research-Tokyo, with extensive experience in distributed computing, cloud infrastructure, and analytics, the
author has contributed to the development of global-scale software products for over a decade. Since 2020, he has been working at IBM Quantum, focusing on monitoring and observability tools for quantum systems. In 2023, his work shifted toward developing software for HPC-Quantum integration, enabling seamless access to quantum computers in on-premises environments. His recent efforts include building tools that allow quantum workloads to run on Slurm-based HPC eco systems, bridging classical and quantum computing. The presenter is passionate about advancing hybrid computing architectures and making quantum technologies more accessible to researchers and engineers.

- Shweta Salaria(Shweta.Salaria@ibm.com) is a Research Scientist at IBM Research since 2022, working on benchmarking large language models and enabling their deployment on large-scale clusters. She holds a PhD from Tokyo Institute of Technology, with doctoral research focused on cross-architecture performance modeling and analysis of CPU and GPU-based HPC applications. At IBM, she has contributed to the enablement of IBM Watson Code Assistant for Z, powered by Granite foundation models, and received an Outstanding Technical Achievement award for her contributions to enable HPC and AI Workloads on IBM Cloud. Her current research focuses on understanding the performance characteristics of HPC-Quantum workloads and enabling their deployment at large-scale.

## References

- [QRMI](https://github.com/qiskit-community/qrmi)
- [SPANK Plugin](https://github.com/qiskit-community/spank-plugins/tree/main)
- [Demonstration of SQD using the Qiskit C API](https://github.com/qiskit-community/qiskit-c-api-demo)
- [QRMI Examples](https://github.com/qiskit-community/qrmi/tree/main/examples)
- [Slurm Docker Cluster](https://github.com/qiskit-community/spank-plugins/tree/main/demo/qrmi/slurm-docker-cluster)

