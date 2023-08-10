from qiskit.circuit import ParameterVector, QuantumCircuit
from qiskit.opflow import PauliSumOp
from qiskit.quantum_info import SparsePauliOp

Ha_to_kcalmol = 627.503

H4_from_file = PauliSumOp(SparsePauliOp(['IIII', 'XXXX', 'YYXX', 'IXZX', 'ZXZX', 'IXIX', 'ZXIX', 'XXYY', 'YYYY', 'IIIZ', 'XZXZ', 'XIXZ', 'IIZZ', 'IZZZ', 'ZZZZ', 'ZIZZ', 'IZIZ', 'ZZIZ', 'ZIIZ', 'XZXI', 'XIXI', 'IIZI', 'IZZI', 'ZZZI', 'ZIZI', 'IZII', 'ZZII', 'ZIII'],
              coeffs=[-1.40343802e+01+0.j,  1.89666179e-02+0.j, -1.89666179e-02+0.j,
 -1.89666179e-02+0.j,  1.89666179e-02+0.j,  1.89666179e-02+0.j,
 -1.89666179e-02+0.j, -1.89666179e-02+0.j,  1.89666179e-02+0.j,
 -1.60527381e-01+0.j,  5.30165769e-03+0.j,  5.30165769e-03+0.j,
 -2.41584122e-01+0.j,  8.88184955e-02+0.j,  9.94831530e-02+0.j,
 -8.88798376e-02+0.j,  8.58722654e-02+0.j,  8.88184955e-02+0.j,
 -8.88184955e-02+0.j,  5.30165769e-03+0.j,  5.30165769e-03+0.j,
  2.41584122e-01+0.j, -8.88184955e-02+0.j, -8.88798376e-02+0.j,
  9.94831530e-02+0.j, -1.60527381e-01+0.j, -2.41584122e-01+0.j,
  2.41584122e-01+0.j]), coeff=1.0)

paulis_from_file = ['YIXI', 'YYYX', 'YIXI']
params_from_file = [0.19535462771567846, 12.167984734279953, 0.19535462771567846]
parameters = ParameterVector('θ', 3)

def swap_qubits(p,q,H,paulis):
    def swap_list(a,b,c):
        c[a],c[b] = c[b],c[a]
        return c
    def swap_string(a,b,c):
        c = list(c)
        c = swap_list(a,b,c)
        return ''.join(c)
    paulis = [swap_string(p,q,x) for x in paulis]
    for r in  range(H._primitive._pauli_list._z.shape[0]):
        H._primitive._pauli_list._z[r,:] = swap_list(p,q,H._primitive._pauli_list._z[r,:])
        H._primitive._pauli_list._x[r,:] = swap_list(p,q,H._primitive._pauli_list._x[r,:])
    return H,paulis

def append_pauli(circuit,param,p):
    idx = [j for j,pj in enumerate(p) if pj!='I']
    for j,pj in enumerate(p):
        if(pj=='X'): circuit.h(j)
        if(pj=='Y'): circuit.sdg(j); circuit.h(j)
    for R in range(len(idx)-1):
        circuit.cx(idx[R],idx[R+1])
    if(len(idx)==0):
        circuit.rz(param,0)
    else:
        circuit.rz(param,idx[len(idx)-1])
    for R in range(len(idx)-1)[::-1]:
        circuit.cx(idx[R],idx[R+1])
    for j,pj in enumerate(p):
        if(pj=='X'): circuit.h(j)
        if(pj=='Y'): circuit.h(j); circuit.s(j)
    return circuit

def retrieve_observable_and_ansatz():
    H4, paulis = swap_qubits(1,2,H4_from_file, paulis_from_file)
    qc4 = QuantumCircuit(4); qc4.x([0,1,2,3])
    for c,P in zip(parameters, paulis):
        qc4 = append_pauli(qc4,c,P)

    return (H4, qc4, params_from_file)

