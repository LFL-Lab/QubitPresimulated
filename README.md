# QubitPresimulated
Library of modular pre-designed superconducting Qubits using Qiskit Metal. Speed up your the design and simulation phase of fabrication. Ask for a set of target parameters, and we'll give you a few close choices.

## Instalation
Must have `qiskit-metal` by IBM Quantum installed.

## Usage
See tutorials for the full story. But here's some pseduo-code if you're in a rush.
```
# Run a sweep
analyzer = QAnalysis
parameters_to_sweep = dict() # in structure of QComponent.options
component_name = QComponent.name

sweeper = QSweeper(QAnalysis)
sweeper.run_sweep(component_name, parameter_to_sweep, etc.)

# See results
print(sweeper.librarian.qoptions_data)
print(sweeper.librarian.simulations_data)
```

# To Do
- Make tutorial for `QLibrary`, specifically selecting the best choice
- Implement complete support for LOM and ScatteringSim

