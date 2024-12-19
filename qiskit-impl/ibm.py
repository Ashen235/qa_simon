import numpy as np
import argparse
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer


def simon_function(s: str):
    """
    Create a QuantumCircuit implementing a query gate for Simon problem obeying the promise for the hidden string `s`
    """
    n = len(s)
    qc = QuantumCircuit(2 * n)

    # Define a random permutation of all n-bit strings. This will effectively hide the string s.
    pi = np.random.permutation(2**n)

    # Define a query gate that satisfies Simon's promise
    query_gate = np.zeros((2**(2 * n), 2**(2 * n)), dtype=complex)
    for x in range(2**n):
        for y in range(2**n):
            z = y ^ pi[min(x, x ^ int(s, 2))]
            query_gate[x + 2**n * z, x + 2**n * y] = 1

    # Check if the matrix is unitary
    if not np.allclose(query_gate @ query_gate.conj().T, np.eye(2**(2 * n))):
        raise ValueError("Matrix is not unitary. Something went wrong.")

    # Add the unitary to the circuit
    qc.unitary(query_gate, range(2 * n))

    # Return the circuit
    return qc


def simon_measurements(problem: QuantumCircuit, k: int):
    """
    Quantum part of Simon's algorithm. Given a `QuantumCircuit` that
    implements f, get `k` measurements to be post-processed later.
    """
    n = problem.num_qubits // 2

    qc = QuantumCircuit(2 * n, n)
    qc.h(range(n))  # Apply Hadamard gates on the first n qubits
    qc.compose(problem, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))

    # Simulate the circuit
    result = AerSimulator().run(qc, shots=k, memory=True).result()
    return result.get_memory()


def main():
    # Example hidden string '11011' with 12 measurements

        # Parse arguments
    parser = argparse.ArgumentParser(description="Simon's Algorithm with Qiskit")
    parser.add_argument("--hidden_string", type=str, required=True, help="The hidden binary string used in Simon's problem (e.g., '11011').")
    parser.add_argument("--shots", type=int, default=1024, help="Number of measurement shots for simulation.")
    args = parser.parse_args()

    hidden_string = args.hidden_string
    num_measurements = args.shots

    # Generate the Simon function circuit
    try:
        query_circuit = simon_function(hidden_string)
    except ValueError as e:
        print(e)
        return

    print("Quantum Circuit for the Query:")
    print(query_circuit.draw())

    # Perform measurements
    measurements = simon_measurements(query_circuit, num_measurements)
    print("\nMeasurement Results:")
    print(measurements)


if __name__ == "__main__":
    main()
    
