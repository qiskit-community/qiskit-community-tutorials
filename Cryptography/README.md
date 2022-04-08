# Quantum Cryptography
## QRandom --> Generates random numbers.
The random number is directly generated from a Hadamard gate using Qiskit Terra. It is similar to rolling an `n`-faced dice, where `n` is the number of qubits. It is the worst way to generate random numbers using a quantum computer but the sequence developed is truly random. 

For a more detailed example of generating random variates from various distributions using Qiskit aqua, take a look at [this tutorial](https://github.com/Qiskit/qiskit-tutorials/blob/master/qiskit/aqua/generating_random_variates.ipynb).

## Quantum Key Distribution
Quantum Key Distribution (also called the "BB84 Protocol") is a method of distributing cryptographic keys for symmetric key crytography. Of course, no real quantum communications channel exists for this to be used yet, so qubits that would have been transferred along a quantum channel are instead stored in an array in this notebook.
