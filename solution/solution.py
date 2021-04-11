from typing import List, Tuple

import numpy as np
import cirq


def matrix_to_sycamore_operations(
    target_qubits: List[cirq.GridQubit], matrix: np.ndarray
) -> Tuple[cirq.OP_TREE, List[cirq.GridQubit]]:
    """A method to convert a unitary matrix to a list of Sycamore operations.

    This method will return a list of `cirq.Operation`s using the qubits and (optionally) ancilla
    qubits to implement the unitary matrix `matrix` on the target qubits `qubits`.
    The operations are also supported by `cirq.google.gate_sets.SYC_GATESET`.

    Args:
        target_qubits: list of qubits the returned operations will act on. The qubit order defined by the list
            is assumed to be used by the operations to implement `matrix`.
        matrix: a matrix that is guaranteed to be unitary and of size (2**len(qs), 2**len(qs)).
    Returns:
        A tuple of operations and ancilla qubits allocated.
            Operations: In case the matrix is supported, a list of operations `ops` is returned.
                `ops` acts on `qs` qubits and for which `cirq.unitary(ops)` is equal to `matrix` up
                 to certain tolerance. In case the matrix is not supported, it might return NotImplemented to
                 reduce the noise in the judge output.
            Ancilla qubits: In case ancilla qubits are allocated a list of ancilla qubits. Otherwise
                an empty list.
        .
    """

    class Gate2(cirq.TwoQubitGate):
        
        def _unitary_(self):
            return  matrix
        
        def __str__(self):
            return 'ζ'
        
    class Gate1(cirq.SingleQubitGate):
        
        def _unitary_(self):
            return  matrix
        
        def __str__(self):
            return 'ζ'

    
    size = len(matrix)
    
    if size == 4: 
        cnt2 = Gate2()
        answer = cirq.google.ConvertToSycamoreGates().convert(cnt2(target_qubits[0],target_qubits[1]))
        #print(cirq.google.ConvertToSycamoreGates().convert(cnt2(target_qubits[0],target_qubits[1])))
        #circuit2 = cirq.Circuit(cirq.google.ConvertToSycamoreGates().convert(cnt2(target_qubits[0],target_qubits[1]) ) )
        #print(circuit2)
    
    if size == 2: 
        cnt1 = Gate1()
        answer = cirq.google.ConvertToSycamoreGates().convert(cnt1(target_qubits[0]))
        #print(cirq.google.ConvertToSycamoreGates().convert(cnt1(target_qubits[0]) ))
        #circuit1 = cirq.Circuit(cirq.google.ConvertToSycamoreGates().convert(cnt1(target_qubits[0]) ) )
        #print(circuit1)
        
    return (answer), []