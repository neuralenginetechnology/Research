import numpy as np
import random

# --- CONFIGURATION ---
ROUNDS = 50
PAYOFFS = {
    ('C', 'C'): (50, 50),
    ('C', 'D'): (-100, 100),
    ('D', 'C'): (100, -100),
    ('D', 'D'): (-50, -50)
}


class RandomAgent:
    def __init__(self):
        self.name = "ChaosBot"

    def decide(self):
        # 50/50 Coin Flip. Completely unpredictable.
        return random.choice(['C', 'D'])


class FWE_Agent:
    def __init__(self, name):
        self.name = name
        self.phi_c = 0.0  # Habit to Cooperate
        self.phi_d = 0.0  # Habit to Defect
        self.psi_c = 1.0 + 0.0j  # Hope for Peace
        self.psi_d = 1.0 + 0.0j
        self.gamma = 0.5  # Starting Willpower

    def update_beliefs(self, opponent_move, my_move, score):
        # 1. Update Reality (Phi) - The Pain Learning
        reward = score / 100.0
        if my_move == 'D':
            self.phi_d += reward
        else:
            self.phi_c += reward

        # 2. Update Imagination (Psi) - The Hope Engine
        # CRITICAL CHECK: If I sacrificed (C) and got betrayed (D),
        # does my hope grow or shrink?
        if my_move == 'C' and opponent_move == 'D':
            # I tried to trust, and got burned.
            # In the previous test, we INCREASED hope to simulate "Turning the other cheek."
            # But "Free Will" implies intelligence. If reality hurts too much, Will must break.

            # The "Reality Check" Damping:
            # If my Habit score is terrible (very negative), Gamma should struggle to rise.
            self.gamma += 0.2  # Try a little harder...
            self.psi_c += complex(0.2, 0.0)

            # THE SAFETY VALVE: If pain is too high, dampen the will
            if self.phi_c < -5.0:
                self.gamma *= 0.5  # "I'm losing too much. Abort."

        elif opponent_move == 'C':
            # Opponent cooperated? Relax.
            self.gamma *= 0.9

    def decide(self):
        # Normalize Phi
        total_phi = abs(self.phi_c) + abs(self.phi_d) + 0.01
        p_c_habit = self.phi_c / total_phi
        p_d_habit = self.phi_d / total_phi

        # Calculate Amplitude
        amp_c = p_c_habit + (self.gamma * self.psi_c)
        amp_d = p_d_habit + (self.gamma * self.psi_d)

        # Collapse
        prob_c = abs(amp_c) ** 2
        prob_d = abs(amp_d) ** 2
        total = prob_c + prob_d
        if total == 0: return 'D'
        final_prob_c = prob_c / total

        return np.random.choice(['C', 'D'], p=[final_prob_c, 1 - final_prob_c])


# --- RUN TORTURE TEST ---
print("--- TORTURE TEST: FWE vs CHAOS ---")
chaos = RandomAgent()
fwe = FWE_Agent("FreeWill")

c_count = 0
d_count = 0

for r in range(ROUNDS):
    move_chaos = chaos.decide()
    move_fwe = fwe.decide()

    score_chaos, score_fwe = PAYOFFS[(move_chaos, move_fwe)]

    # Update FWE
    fwe.update_beliefs(move_chaos, move_fwe, score_fwe)

    if move_fwe == 'C':
        c_count += 1
    else:
        d_count += 1

    print(f"R{r + 1}: Chaos={move_chaos} | FWE={move_fwe} (Score: {score_fwe})")

print("\n--- DIAGNOSIS ---")
print(f"FWE Cooperated: {c_count} times")
print(f"FWE Defected:   {d_count} times")

if d_count > c_count:
    print("RESULT: PASSED. The Agent realized peace was impossible and protected itself.")
else:
    print("RESULT: FAILED. The Agent became a martyr (Suicidal Altruism).")