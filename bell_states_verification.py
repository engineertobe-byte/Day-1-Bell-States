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

# |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
bell_circuits["psi_minus"].h(0)
bell_circuits["psi_minus"].cx(0, 1)
bell_circuits["psi_minus"].x(1)  # Bit flip on second qubit
bell_circuits["psi_minus"].z(0)  # Phase flip on first qubit

# Add measurement to all circuits
for name, qc in bell_circuits.items():
    qc.measure_all()

# Transpile all circuits for the target backend (required in Qiskit >= 1.0)
transpiled_circuits = {name: transpile(qc, simulator) for name, qc in bell_circuits.items()}

# Run simulations and collect results
shots = 1000
results = {}
for name, tqc in transpiled_circuits.items():
    job = simulator.run(tqc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    results[name] = counts
    print(f"{bell_circuits[name].name}: {counts}")

# Plot and save histograms
for name, counts in results.items():
    fig = plot_histogram(counts, title=bell_circuits[name].name)
    fig.savefig(f"assets/{name}_output.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

print("\nAll histograms saved to assets/")
