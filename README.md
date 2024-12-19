# Simon's Algorithm Implementations

*Figure: Histogram of Measurement Results for Simon's Algorithm*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Implementations](#implementations)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Example](#example)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Introduction

Simon's Algorithm demonstrates exponential speedup over classical algorithms for identifying a hidden binary string in a black-box function . This repository includes multiple implementations of Simon's Algorithm using:

- **Cirq**
- **Qiskit**
- **Amazon Braket**

Each implementation showcases unique features, enabling developers to explore Simon's Algorithm across different quantum platforms.

## Features

- **Multi-platform Implementations**:
  - Cirq-based simulation for constructing and running Simon's Algorithm locally.
  - Qiskit-based implementation for creating quantum circuits and running them using Qiskit's simulators.
  - Amazon Braket-based implementation for executing Simon's Algorithm on cloud quantum simulators.
- **Dynamic Oracle Generation**:
  - Automatically creates oracles based on the hidden binary string .
- **Scalability**:
  - Supports custom qubit counts.
- **Visualization**:
  - Includes histograms and circuit visualizations for result analysis.
- **Utility Functions**:
  - Shared utility functions to streamline oracle creation and simulation.

## Implementations

1. **Cirq Implementation**

   - Cirq implementation to simulate Simon's Algorithm locally using Cirq's tools.
   - Dynamically generated quantum circuits for Simon's Algorithm.

2. **Qiskit Implementation**

   - Quantum circuits implemented with Qiskit.
   - Qiskit implementation to simulate quantum circuits using AerSimulator.

3. **Amazon Braket Implementation**

   - Uses Amazon Braket's `LocalSimulator` for circuit execution.
   - Simon's oracle subroutine is registered for modular use.

4. **Shared Utilities**

   - `simons_utils.py` contains reusable components like the oracle subroutine for Braket.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.7 or later**: [Download Python](https://www.python.org/downloads/)
- **Cirq**: Quantum simulation library.
- **Qiskit**: Quantum Information Toolkit.
- **Amazon Braket SDK**: For quantum circuit simulation and execution.
- **Matplotlib**: For result visualization.
- **SymPy**: For symbolic mathematics.

## Installation

Follow these steps to set up the development environment for Simon's Algorithm.

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/simons-algorithm.git
cd simons-algorithm
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv env

# Activate the virtual environment
# On Windows:
env\Scripts\activate
# On Unix/Linux/macOS:
source env/bin/activate
```

### 3. Install Required Packages

Install all necessary Python packages using `pip`.

```bash
pip install cirq matplotlib sympy qiskit amazon-braket-sdk
```

### 4. Verify Installation

Run the following Python commands to ensure everything is installed correctly.

```python
import cirq
import matplotlib
import sympy
from qiskit import Aer
from braket.circuits import Circuit

print("Cirq version:", cirq.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("SymPy version:", sympy.__version__)
```

## Usage

### 1. **Cirq Implementation**

Run the `google.py` implementation:

```bash
python google.py --hidden_string 11011 --shots 1024 -n 5
```

All the parameters are optional and can be used as wished. The defaults are n = 5, shots = 8192, and if hidden_string is not provided, a random one will be generated with length $\(n\)$.

### 2. **Qiskit Implementation**

Run the `ibm.py` script:

```bash
python ibm.py --hidden_string 11011 --shots 1024
```

Replace `11011` with your desired hidden string and specify the number of shots.

### 3. **Amazon Braket Implementation**

Run the `aws.py` script:

```bash
python aws.py --hidden_string 11011 --shots 1024
```

Replace `11011` with your desired hidden string and specify the number of shots.

## Project Structure

```
simons-algorithm/
├── cirq-impl/             # Cirq-based implementation
│   ├── google.py          # Cirq implementation
│   ├── google.ipynb       # Jupyter Notebook for Cirq
├── braket-impl/           # Amazon Braket-based implementation
│   ├── aws.py             # Amazon Braket implementation
│   └── simons_utils.py    # Shared utilities for Braket
├── qiskit-impl/           # Qiskit-based implementation
│   └── ibm.py             # Qiskit implementation
├── assets/                # Assets for the README
│   └── SimonCircuitExample.jpeg # Example circuit image for README
├── README.md               # Project documentation
└── requirements.txt        # List of dependencies
```

## Example

Here's an example for Simon's Algorithm with :

### Cirq Implementation

```python
python google.py
```

### Qiskit Implementation

```bash
python ibm.py --hidden_string 1011 --shots 512
```

### Amazon Braket Implementation

```bash
python aws.py --hidden_string 111 --shots 256
```

## Troubleshooting

If you encounter issues:

1. **Circular Import Errors**:

   - Ensure your file names don’t conflict with library names (e.g., `cirq.py`, `qiskit.py`).
   - Rename conflicting files and clear `__pycache__`.

2. **Incorrect Secret Extraction**:

   - Verify the oracle implementation.
   - Increase the number of shots.

3. **Dependencies Not Found**:

   - Ensure all required libraries are installed. Reinstall missing dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## Contributing

Contributions are welcome! Open an issue or submit a pull request if you have suggestions or fixes.

1. **Fork the Repository**

2. **Create a Feature Branch**:

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Changes**:

   ```bash
   git commit -m "Add Your Feature"
   ```

4. **Push to the Branch**:

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Cirq Documentation](https://quantumai.google/cirq)
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Amazon Braket Documentation](https://docs.aws.amazon.com/braket/index.html)

