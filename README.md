# QAI Labs Quantum Computing & AI/ML Internship — Day 1

This repository contains the **Day 1** deliverable for the **QAI Labs Quantum Computing & AI/ML Internship**.  
It demonstrates the creation, simulation, and verification of the **four Bell states** (maximally entangled two-qubit states) using **Qiskit 2.3.0** (modern API: `AerSimulator`, `transpile`).

> **Reference:** Official "Day_1_Bell_state.pdf" by **Rajiv Kumar Yadav** (QAI Labs).

---

## 1. Repository Structure

```text
QAI-Labs-Internship/
├── assets/                          # Output screenshots (generated after running the script)
│   ├── phi_plus_output.png          # |Φ⁺⟩ measurement histogram
│   ├── phi_minus_output.png         # |Φ⁻⟩ measurement histogram
│   ├── psi_plus_output.png          # |Ψ⁺⟩ measurement histogram
│   └── psi_minus_output.png         # |Ψ⁻⟩ measurement histogram
├── bell_states_verification.py      # Main Python script (complete code below)
├── requirements.txt                 # Pinned dependencies
└── README.md                        # This file
```

---

## 2. Technical Context

| Item | Detail |
|------|--------|
| **Framework** | Qiskit 2.3.0 (modern API) |
| **Simulator** | `AerSimulator` (replaces deprecated `BasicAer`/`Aer.get_backend`) |
| **Compilation** | `transpile(circuit, backend)` — required in Qiskit ≥ 1.0 |
| **Shots** | 1000 per Bell state |
| **Measurement Basis** | Computational (Z) basis — `measure_all()` |
| **Expected Outcome** | Each Bell state yields **exactly two outcomes** with ~50 % probability each (e.g., `00` & `11` for \|Φ⁺⟩). |

---

## 3. Requirements

Create a virtual environment and install the pinned dependencies:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install --no-cache-dir -r requirements.txt
```

**requirements.txt** (exact contents):

```text
qiskit==2.3.0
qiskit-aer==0.17.2
matplotlib
```

> **Note:** Only the three packages above are required for this Day 1 task.  
> `scipy`, `pennylane`, etc. are **not** needed here.

---

## 4. Full Python Code — `bell_states_verification.py`

Copy the code below into `bell_states_verification.py` and run it:

```python
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
```

### Run the script

```bash
python bell_states_verification.py
```

---

## 5. Expected Output

Running the script prints the measurement counts for each Bell state (example output with 1000 shots):

```text
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2: {'00': 502, '11': 498}
|Φ⁻⟩ = (|00⟩ - |11⟩)/√2: {'00': 511, '11': 489}
|Ψ⁺⟩ = (|01⟩ + |10⟩)/√2: {'01': 503, '10': 497}
|Ψ⁻⟩ = (|01⟩ - |10⟩)/√2: {'01': 495, '10': 505}

All histograms saved to assets/
```

**Interpretation:** Each Bell state produces **exactly two computational-basis outcomes** with near-equal probability (~50 % each), confirming maximal entanglement.

---

## 6. Bell State Results (Embedded Histograms)

### |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
![Phi Plus Output](assets/phi_plus_output.png)

### |Φ⁻⟩ = (|00⟩ - |11⟩)/√2
![Phi Minus Output](assets/phi_minus_output.png)

### |Ψ⁺⟩ = (|01⟩ + |10⟩)/√2
![Psi Plus Output](assets/psi_plus_output.png)

### |Ψ⁻⟩ = (|01⟩ - |10⟩)/√2
![Psi Minus Output](assets/psi_minus_output.png)

---

## Quick Reference

| Bell State | Circuit | Outcomes (Z-basis) |
|------------|---------|-------------------|
| \|Φ⁺⟩ | H(0) → CX(0,1) | `00`, `11` |
| \|Φ⁻⟩ | H(0) → CX(0,1) → Z(0) | `00`, `11` |
| \|Ψ⁺⟩ | H(0) → CX(0,1) → X(1) | `01`, `10` |
| \|Ψ⁻⟩ | H(0) → CX(0,1) → X(1) → Z(0) | `01`, `10` |

---

**End of Day 1 Deliverable** — Ready for submission to QAI Labs.
