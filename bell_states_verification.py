"""
Bell States Verification — QAI Labs Day 1
Author: Rajiv Kumar Yadav (reference implementation)
Qiskit Version: 2.3.0 (modern API: AerSimulator + transpile)
Shots: 1000 per state
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import os

# Ensure assets directory exists
os.makedirs("assets", exist_ok=True)

# Initialize the simulator (modern Qiskit API)
simulator = AerSimulator()

# Define the four Bell state preparation circuits
bell_circuits = {
    "phi_plus": QuantumCircuit(2, name="|Φ⁺⟩ = (|00⟩ + |11⟩)/√2"),
    "phi_minus": QuantumCircuit(2, name="|Φ⁻⟩ = (|00⟩ - |11⟩)/√2"),
    "psi_plus": QuantumCircuit(2, name="|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2"),
    "psi_minus": QuantumCircuit(2, name="|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2"),
}

# |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
bell_circuits["phi_plus"].h(0)
bell_circuits["phi_plus"].cx(0, 1)

# |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
bell_circuits["phi_minus"].h(0)
bell_circuits["phi_minus"].cx(0, 1)
bell_circuits["phi_minus"].z(0)  # Phase flip on first qubit

# |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
bell_circuits["psi_plus"].h(0)
bell_circuits["psi_plus"].cx(0, 1)
bell_circuits["psi_plus"].x(1)  # Bit flip on second qubit

# |Ψ⁻⟩ = (|01
