# QubitPresimulated
Library of premade qubits made in Qiskit Metal. Ask for a set of target parameters, and we'll give you a few close choices.

# Usage
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

