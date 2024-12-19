# Imports and Setup
import matplotlib.pyplot as plt
import numpy as np

from braket.circuits import Circuit
from braket.devices import LocalSimulator

from simons_utils import simons_oracle  # noqa: F401
import argparse



# Sets the device to run the circuit on
def simons_algo(s, shots):
    device = LocalSimulator()


    

    # Other examples to try:
    # s = '011'
    # s = '00000'
    # s = '1'
    # Generate a random string of random length from 1 to 10:
    # s="".join(str(np.random.randint(2)) for _ in range(np.random.randint(1,10)))

    print("The secret string is: " + s)

    n = len(s)

    circ = Circuit()

    # Apply Hadamard gates to first n qubits
    circ.h(range(n))

    # Now apply the Oracle for f
    circ.simons_oracle(s)

    # Apply Hadamard gates to the first n qubits
    circ.h(range(n))


    print(circ)


    task = device.run(circ, shots)

    result = task.result()

    counts = result.measurement_counts
    plt.bar(counts.keys(), counts.values())
    plt.xlabel("bit strings")
    plt.ylabel("counts")
    plt.xticks(rotation=90)
    plt.show()

    result = task.result()

    counts = result.measurement_counts
    plt.bar(counts.keys(), counts.values())
    plt.xlabel("bit strings")
    plt.ylabel("counts")
    plt.xticks(rotation=90)
    plt.show()

    new_results = {}
    for bitstring, count in result.measurement_counts.items():
        # Only keep the outcomes on first n qubits
        trunc_bitstring = bitstring[:n]
        # Add the count to that of the of truncated bit string
        new_results[trunc_bitstring] = new_results.get(trunc_bitstring, 0) + count

    plt.bar(new_results.keys(), new_results.values())
    plt.xlabel("bit strings")
    plt.ylabel("counts")
    plt.xticks(rotation=70)
    plt.show()




def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="Simon's Algorithm with Amazon Braket")
    parser.add_argument("--hidden_string", type=str, required=True, help="The hidden binary string used in Simon's problem (e.g., '11011').")
    parser.add_argument("--shots", type=int, default=12, help="Number of measurement shots for simulation.")
    args = parser.parse_args()

    hidden_string = args.hidden_string
    num_measurements = args.shots

    # Generate the Simon function circuit
    try:
        query_circuit = simons_algo(hidden_string, num_measurements)
    except ValueError as e:
        print(e)
        return
    

if __name__ == "__main__":
    main()
