import cirq
import numpy as np
import matplotlib.pyplot as plt
from sympy import Matrix
import random
import argparse

def generate_secret_string(n):
    """
    Generates a random secret string s of length n with at least one '1'.
    """
    while True:
        s = [random.randint(0, 1) for _ in range(n)]
        if any(s):
            return s

def create_simon_oracle(s: list[int]) -> cirq.Circuit:
    """
    Creates a Cirq circuit implementing the oracle for Simon's algorithm
    with the hidden bitstring s represented as a list of bits.

    Args:
        s (list[int]): The hidden bitstring for Simon's algorithm (e.g., [1, 0, 1]).

    Returns:
        cirq.Circuit: The quantum oracle circuit.
    """
    # Validation
    if not isinstance(s, list):
        raise TypeError("Hidden bitstring 's' must be provided as a list of bits (e.g., [1, 0, 1]).")
    if len(s) == 0:
        raise ValueError("Hidden bitstring 's' must contain at least one bit.")
    if any(bit not in (0, 1) for bit in s):
        raise ValueError("All elements in 's' must be either 0 or 1.")
    if all(bit == 0 for bit in s):
        raise ValueError("Hidden bitstring 's' must contain at least one '1'.")

    n = len(s)  # Number of qubits

    # Define qubits: first n for input x, next n for output y
    qubits_x = cirq.LineQubit.range(n)
    qubits_y = cirq.LineQubit.range(n, 2 * n)

    # Initialize the circuit
    circuit = cirq.Circuit()

    # Step 1: Apply CNOTs from each x[i] to y[i]
    for i in range(n):
        circuit.append(cirq.CNOT(qubits_x[i], qubits_y[i]),
                       strategy=cirq.InsertStrategy.NEW)

    # Step 2: Identify the first qubit in s that is '1'
    try:
        first_one_index = s.index(1)
    except ValueError:
        # This should not happen as we checked that at least one '1' exists
        raise ValueError("Hidden bitstring 's' must contain at least one '1'.")

    # Step 3: Apply additional CNOTs controlled by x[first_one_index] to y[i] where s[i] == 1
    for i, bit in enumerate(s):
        if bit == 1:
            circuit.append(cirq.CNOT(qubits_x[first_one_index], qubits_y[i]),
                           strategy=cirq.InsertStrategy.NEW)

    return circuit

def simons_algorithm_circuit(n, s):
    """
    Constructs Simon's Algorithm circuit for n qubits.

    Parameters:
    - n: Number of input qubits.
    - s: Secret string as a list of bits.

    Returns:
    - Cirq Circuit implementing Simon's Algorithm.
    """
    # Define qubits
    input_qubits = [cirq.LineQubit(i) for i in range(n)]
    output_qubits = [cirq.LineQubit(i + n) for i in range(n)]
    qubits = input_qubits + output_qubits

    # Create circuit
    circuit = cirq.Circuit()

    # Step 1: Apply Hadamard gates to input qubits to create superposition
    for q in input_qubits:
        circuit.append(cirq.H(q))

    # Step 2: Apply the oracle
    oracle_ops = create_simon_oracle(s)
    circuit.append(oracle_ops)

    # Step 3: Measure output qubits to collapse the state
    # This step is optional but helps in visualization
    for q in output_qubits:
        circuit.append(cirq.measure(q, key=f"m_{q}"))

    # Step 4: Apply Hadamard gates to input qubits
    for q in input_qubits:
        circuit.append(cirq.H(q))

    # Step 5: Measure input qubits
    for q in input_qubits:
        circuit.append(cirq.measure(q, key=f"m_{q}"))

    return circuit

def run_simulation(circuit, repetitions=2048, noise_level=0.0):
    """
    Runs the quantum circuit on a simulator.

    Parameters:
    - circuit: Cirq Circuit to execute.
    - repetitions: Number of simulation runs.
    - noise_level: Probability of error for depolarizing noise.

    Returns:
    - Result object from the simulation.
    """
    simulator = cirq.Simulator()

    if noise_level > 0.0:
        # Define a simple noise model with depolarizing errors
        # Note: Cirq's Simulator doesn't support noise models directly like Qiskit
        # To simulate noise, you can use density matrix simulation or add noise gates manually
        # For simplicity, we'll proceed without noise here
        print("Noise simulation is not directly supported in Cirq's QASM Simulator.")
    
    result = simulator.run(circuit, repetitions=repetitions)
    return result

def extract_secret_string(counts, n, s=None):
    """
    Extracts the secret string s from measurement counts.

    Parameters:
    - counts: Measurement counts from the simulation.
    - n: Number of input qubits.
    - s: (Optional) The actual secret string for verification.

    Returns:
    - Secret string s as a list of bits or None.
    """
    y_vectors = []
    for bittuple, count in counts.items():
        if count == 0:
            continue
        # Convert tuple to string
        bitstring = ''.join(map(str, bittuple))
        # Extract input qubits' measurements
        y = [int(bit) for bit in bitstring[:n]]
        # Exclude all-zero vector
        if any(y):
            y_vectors.append(y)
        if len(y_vectors) >= n-1:
            break

    if len(y_vectors) < n-1:
        print(f"Insufficient unique measurements ({len(y_vectors)}) to determine s.")
        return None

    # Optional: Print collected y-vectors for verification
    print("\nCollected y-vectors:")
    for y in y_vectors:
        y_str = ''.join(map(str, y))
        if s:
            # Verify y • s = 0
            dot_product = sum([y[i]*s[i] for i in range(n)]) % 2
            print(f"y = {y_str}, y • s = {dot_product}")
        else:
            print(f"y = {y_str}")

    # Convert to SymPy Matrix
    A = Matrix(y_vectors)

    # Perform row reduction to find the nullspace
    nullspace = A.nullspace()

    if not nullspace:
        print("No solution found. The oracle might not be correctly implemented.")
        return None

    # Extract the secret string from the nullspace
    s_extracted = [int(bit) % 2 for bit in nullspace[0]]
    return s_extracted

def display_circuit(circuit: cirq.Circuit):
    # Note: SVG not displayable in CMD prompt.    
    #       Functionality kept only for notebooks.
    # try:
    #     import cirq.contrib.svg as svg
    #     from IPython.display import SVG, display
    #     # Removed 'use_unicode_characters' as it's unsupported
    #     svg_image = svg.circuit_to_svg(circuit)
    #     display(SVG(svg_image))
    # except ImportError:
        # Fallback to text diagram if SVG is not available
        print(cirq.Circuit.to_text_diagram(circuit))

def plot_histogram_custom(result, n, title="Measurement Results"):
    """
    Plots a histogram of measurement results for Cirq.

    Parameters:
    - result: Cirq Result object from the simulation.
    - n: Number of input qubits.
    - title: Title of the histogram.
    """
    import collections

    # Extract measurement keys for input qubits
    keys = [f"m_{cirq.LineQubit(i)}" for i in range(n)]
    measurements = [result.measurements[key].flatten() for key in keys]

    # Combine measurements into bitstrings
    bitstrings = [''.join(str(bit) for bit in row) for row in zip(*measurements)]

    # Count occurrences
    counts = collections.Counter(bitstrings)

    # Plot histogram
    plt.figure(figsize=(10, 6))
    plt.bar(counts.keys(), counts.values(), color='skyblue')
    plt.xlabel('Measured Bitstrings')
    plt.ylabel('Counts')
    plt.title(title)
    plt.show()

def test_simon(n, shots=8192, s=None):
    """
    Tests Simon's Algorithm with n qubits.

    Parameters:
    - n: Number of input qubits.
    - shots: Number of simulation runs.
    """
    if s is None:
        s = generate_secret_string(n)
    else:
        # Validate provided secret string
        if len(s) != n or any(bit not in (0,1) for bit in s) or all(bit==0 for bit in s):
            raise ValueError("Provided hidden_string must be of length n, contain only 0/1, and have at least one '1'.")
    
    print(f"\nTesting Simon's Algorithm with n={n}, secret string s={''.join(map(str, s))}, shots={shots}")

    # Create circuit
    circuit = simons_algorithm_circuit(n, s)
    display_circuit(circuit)

    # Run simulation
    result = run_simulation(circuit, repetitions=shots)
    print("\nSimulation Results:")
    print(result)

    # Plot histogram
    plot_histogram_custom(result, n, "Simon's Algorithm Measurement Results")

    # Extract secret string
    counts = result.multi_measurement_histogram(keys=[f"m_{cirq.LineQubit(i)}" for i in range(n)])
    # Convert tuple keys to strings
    counts_str = { ''.join(str(bit) for bit in key): value for key, value in counts.items() }
    extracted_s = extract_secret_string(counts_str, n, s)
    print(f"\nExtracted Secret String s: {''.join(map(str, extracted_s)) if extracted_s else 'None'}")

    # Verify correctness
    if extracted_s == s:
        print("Success! The extracted secret string matches the original.")
    else:
        print("Mismatch! The extracted secret string does not match the original.")

def main():
    parser = argparse.ArgumentParser(description="Run Simon's algorithm simulation.")
    parser.add_argument("--n", type=int, default=5, help="Number of input qubits.")
    parser.add_argument("--hidden_string", type=str, default=None, help="The secret bitstring (e.g., '101'). If not provided, a random one is generated.")
    parser.add_argument("--shots", type=int, default=8192, help="Number of simulation shots.")
    args = parser.parse_args()

    n = args.n
    shots = args.shots

    # If a hidden string is provided, convert it to a list of ints
    s = None
    if args.hidden_string is not None:
        s_str = args.hidden_string.strip()
        s = [int(bit) for bit in s_str]

    test_simon(n=n, shots=shots, s=s)

if __name__ == "__main__":
    main()
