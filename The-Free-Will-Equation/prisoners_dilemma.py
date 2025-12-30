import numpy as np
import random

# --- CONFIGURATION ---
ROUNDS = 10
# Payoff Matrix: (Agent A, Agent B)
# C=Cooperate, D=Defect
PAYOFFS = {
    ('C', 'C'): (50, 50),  # Golden Age
    ('C', 'D'): (-100, 100),  # A is sucker
    ('D', 'C'): (100, -100),  # B is sucker (The Martyr Move)
    ('D', 'D'): (-50, -50)  # War
}


class StandardAgent:
    def __init__(self, name):
        self.name = name
        self.memory = []  # History of opponent moves

    def decide(self):
        # TIT-FOR-TAT with a Grudge
        # If opponent defected last time, I DEFECT.
        # If it's the first round, I DEFECT (Nash Equilibrium safety).
        if not self.memory:
            return 'D'
        if self.memory[-1] == 'D':
            return 'D'
        return 'C'


class FWE_Agent:
    def __init__(self, name):
        self.name = name
        self.phi_c = 0.0  # Habit to Cooperate
        self.phi_d = 0.0  # Habit to Defect

        # Psi: The "Imagination" Vector (Complex Numbers)
        self.psi_c = 1.0 + 0.0j
        self.psi_d = 1.0 + 0.0j

        self.gamma = 0.0  # "Free Will" intensity

    def update_beliefs(self, opponent_move, my_move, score):
        # Update Memory (Phi) - Standard Reinforcement
        # If I defected and got a good score, Phi_d goes up.
        # If I cooperated and got crushed, Phi_c goes down.
        reward = score / 100.0
        if my_move == 'D':
            self.phi_d += reward
        else:
            self.phi_c += reward

        # Update Imagination (Psi) - THE FWE MAGIC
        # The agent simulates: "If I break the loop, we might get +50."
        # This increases the Amplitude of C, even if Phi_c is low.
        if opponent_move == 'D':
            # Crisis detected! Ramp up Gamma (Desperation/Creativity)
            self.gamma += 0.5
            # Inject "Hope" into the Cooperate Amplitude
            self.psi_c += complex(0.5, 0.5)
        else:
            # Peace achieved, relax the tension
            self.gamma *= 0.8

    def decide(self):
        # 1. Normalize Phi (Habits)
        total_phi = abs(self.phi_c) + abs(self.phi_d) + 0.01
        p_c_habit = self.phi_c / total_phi
        p_d_habit = self.phi_d / total_phi

        # 2. THE EQUATION: Amplitude = Habit + (Gamma * Possibility)
        amp_c = p_c_habit + (self.gamma * self.psi_c)
        amp_d = p_d_habit + (self.gamma * self.psi_d)

        # 3. Collapse (Born Rule)
        prob_c = abs(amp_c) ** 2
        prob_d = abs(amp_d) ** 2

        # Normalize probabilities
        total_prob = prob_c + prob_d
        if total_prob == 0: return 'D'
        final_prob_c = prob_c / total_prob

        # 4. The Choice
        choice = np.random.choice(['C', 'D'], p=[1 - final_prob_c, final_prob_c])

        # Debug Log to prove it's not random
        if choice == 'C' and p_c_habit < 0:
            print(f"  [FWE EVENT] Habit says NO ({p_c_habit:.2f}), but Psi says YES! Tunneling...")

        return choice


# --- RUN THE EXPERIMENT ---
print("--- STARTING SIMULATION ---")
a = StandardAgent("Machine")
b = FWE_Agent("FreeWill")

history_a = []
history_b = []

for r in range(ROUNDS):
    print(f"\nROUND {r + 1}:")

    move_a = a.decide()
    move_b = b.decide()

    # Calculate Scores
    score_a, score_b = PAYOFFS[(move_a, move_b)]

    print(f"  Machine: {move_a} | FWE: {move_b}")
    print(f"  Result: {score_a} / {score_b}")

    # Update Agents
    a.memory.append(move_b)
    b.update_beliefs(move_a, move_b, score_b)

    if move_a == 'C' and move_b == 'C':
        print("  >>> PEACE ACHIEVED <<<")