import numpy as np

class QuantumGate:
    def __init__(self, matrix):
        self.matrix = matrix

    def apply(self, state_vector):
        return np.dot(self.matrix, state_vector)

class QuantumCircuit:
    def __init__(self):
        self.gates = []

    def add_gate(self, gate):
        self.gates.append(gate)

    def apply_gates(self, initial_state):
        state_vector = initial_state
        for gate in self.gates:
            state_vector = gate.apply(state_vector)
        return state_vector

class HadamardGate(QuantumGate):
    def __init__(self):
        matrix = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        super().__init__(matrix)

class PauliXGate(QuantumGate):
    def __init__(self):
        matrix = np.array([[0, 1], [1, 0]])
        super().__init__(matrix)

class PauliYGate(QuantumGate):
    def __init__(self):
        matrix = np.array([[0, -1j], [1j, 0]])
        super().__init__(matrix)

class PauliZGate(QuantumGate):
    def __init__(self):
        matrix = np.array([[1, 0], [0, -1]])
        super().__init__(matrix)

class QuantumMeasurement:
    def __init__(self):
        pass

    @staticmethod
    def measure(state_vector):
        probabilities = np.abs(state_vector) ** 2
        outcome = np.random.choice(len(state_vector), p=probabilities)
        return outcome

def run_quantum_simulation():
    # Initial qubit state |0>
    initial_state = np.array([1, 0])

    # Create quantum circuit
    circuit = QuantumCircuit()

    # Add gates to the circuit
    circuit.add_gate(HadamardGate())
    circuit.add_gate(PauliXGate())
    
    # Apply gates
    final_state = circuit.apply_gates(initial_state)
    
    # Measure
    measurement = QuantumMeasurement()
    outcome = measurement.measure(final_state)

    # Output the results
    print("Final state vector:", final_state)
    print("Measurement outcome:", outcome)

if __name__ == "__main__":
    run_quantum_simulation()
    
# More gates and functionality
class CNOTGate(QuantumGate):
    def __init__(self):
        self.matrix = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 0, 1],
                                [0, 0, 1, 0]])
        super().__init__(self.matrix)

class ToffoliGate(QuantumGate):
    def __init__(self):
        self.matrix = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
                                [0, 1, 0, 0, 0, 0, 0, 0],
                                [0, 0, 1, 0, 0, 0, 0, 0],
                                [0, 0, 0, 1, 0, 0, 0, 0],
                                [0, 0, 0, 0, 1, 0, 0, 0],
                                [0, 0, 0, 0, 0, 1, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 1],
                                [0, 0, 0, 0, 0, 0, 1, 0]])
        super().__init__(self.matrix)

def multi_qubit_run_simulation():
    # Initial two qubits state |00>
    initial_state = np.array([1, 0, 0, 0])

    circuit = QuantumCircuit()
    circuit.add_gate(HadamardGate())
    circuit.add_gate(CNOTGate())
    
    final_state = circuit.apply_gates(initial_state)
    
    measurement = QuantumMeasurement()
    outcome = measurement.measure(final_state)

    print("Multi-qubit final state vector:", final_state)
    print("Multi-qubit measurement outcome:", outcome)

def run_experiment(num_trials=1000):
    outcomes = {'0': 0, '1': 0}
    for _ in range(num_trials):
        initial_state = np.array([1, 0])
        circuit = QuantumCircuit()
        circuit.add_gate(HadamardGate())
        final_state = circuit.apply_gates(initial_state)
        measurement = QuantumMeasurement()
        outcome = measurement.measure(final_state)
        if outcome == 0:
            outcomes['0'] += 1
        else:
            outcomes['1'] += 1
    print("Outcome probabilities over trials:", {k: v/num_trials for k, v in outcomes.items()})

if __name__ == "__main__":
    print("Running single qubit simulation:")
    run_quantum_simulation()
    
    print("\nRunning multi-qubit simulation:")
    multi_qubit_run_simulation()
    
    print("\nRunning experiment for outcome probabilities:")
    run_experiment()