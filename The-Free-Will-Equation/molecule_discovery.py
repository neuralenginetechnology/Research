import numpy as np
import random
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
# We simulate a "Chemical Space" from 0 to 100.
# 0-30:  "Standard Drug" (Stable, Low Potency)
# 30-70: "The Valley of Instability" (Unstable, difficult to synthesize)
# 70-100: "The Black Swan" (Highly Potent, but requires crossing the valley)

EPISODES = 200
START_MOL = 10  # Start with a basic structure


def get_chemical_properties(structure_val):
    """
    Returns (Stability, Potency) based on the structure value (0-100).
    Phi = Stability (Safety preference)
    Psi = Potency (The goal)
    """
    # 1. Stability Curve (Phi): High at start, dips in middle, recovers slightly at end
    # It discourages crossing the gap (30-70).
    stability = np.exp(-0.5 * ((structure_val - 20) ** 2) / 400) * 1.0  # Peak at 20
    if structure_val > 60: stability += 0.2  # Slight stability at the end

    # 2. Potency Curve (Psi): Increases exponentially towards 100
    potency = (structure_val / 100.0) ** 2

    return stability, potency


class StandardChemist:
    def __init__(self):
        self.current_mol = START_MOL

    def optimize(self):
        # Hill Climbing on Stability (Safety First)
        # Tries to modify molecule slightly (+/- 5)
        proposal = np.clip(self.current_mol + random.randint(-5, 5), 0, 100)

        curr_stab, _ = get_chemical_properties(self.current_mol)
        prop_stab, _ = get_chemical_properties(proposal)

        # Only accept if Stability improves (or is very close)
        if prop_stab >= curr_stab - 0.05:
            self.current_mol = proposal
        return self.current_mol


class FWE_Chemist:
    def __init__(self):
        self.current_mol = START_MOL
        self.gamma = 10.0  # High Curiosity/Risk Tolerance

    def optimize(self):
        # Tries to modify molecule
        proposal = np.clip(self.current_mol + random.randint(-5, 5), 0, 100)

        # Calculate Current State
        c_stab, c_pot = get_chemical_properties(self.current_mol)
        c_amp = c_stab + (self.gamma * c_pot)  # The FWE Check

        # Calculate Proposal State
        p_stab, p_pot = get_chemical_properties(proposal)
        p_amp = p_stab + (self.gamma * p_pot)  # The FWE Check

        # Accept if Amplitude increases (Even if Stability drops!)
        if p_amp > c_amp:
            self.current_mol = proposal
        return self.current_mol


# --- RUN EXPERIMENT ---
print("--- RUNNING MOLECULE DISCOVERY ---")
std_agent = StandardChemist()
fwe_agent = FWE_Chemist()

std_log = []
fwe_log = []

for _ in range(EPISODES):
    std_log.append(std_agent.optimize())
    fwe_log.append(fwe_agent.optimize())

# --- ANALYSIS ---
print(f"Final Structure (Standard): {std_log[-1]:.1f} (Trapped in Safety)")
print(f"Final Structure (FWE):      {fwe_log[-1]:.1f} (Found Black Swan)")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(std_log, 'r--', label='Standard Agent (Optimizes Stability)')
plt.plot(fwe_log, 'b-', label='FWE Agent (Optimizes Amplitude)')
plt.axhspan(30, 70, color='gray', alpha=0.2, label='Valley of Instability')
plt.axhline(y=90, color='green', linestyle=':', label='Target Potency')
plt.ylabel('Molecule Complexity (0-100)')
plt.xlabel('Iterations')
plt.title('Experiment C: Crossing the "Valley of Instability"')
plt.legend()
plt.show()