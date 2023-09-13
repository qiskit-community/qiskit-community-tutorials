from openfermion import QubitOperator
from qiskit.quantum_info import SparsePauliOp

def convert_openfermion_to_qiskit(openfermion_operator: QubitOperator, num_qubits: int) -> SparsePauliOp:
    terms = openfermion_operator.terms

    labels = []
    coefficients = []

    for term, constant in terms.items():
        # Default set to identity
        operator = list('I' * num_qubits)

        # Iterate through PauliSum and replace I with Pauli
        for index, pauli in term:
            operator[index] = pauli
        label = ''.join(operator)
        labels.append(label)
        coefficients.append(constant)
    
    return SparsePauliOp(labels, coefficients)