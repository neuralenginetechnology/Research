import numpy as np
import random
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
STEPS = 50
LEARNING_RATE = 0.1
DISCOUNT = 0.9
EPSILON = 0.1  # For standard agent exploration

# Map: 0=Start, 1=Fire, 2=Fire, 3=Gold
REWARDS = [0, -10, -10, 100]
STATES = len(REWARDS)
ACTIONS = [0, 1]  # 0=Stay, 1=Move Forward


class StandardAgent:
    def __init__(self):
        self.q_table = np.zeros((STATES, len(ACTIONS)))
        self.pos = 0

    def choose_action(self):
        # Epsilon-Greedy (Standard RL)
        if random.uniform(0, 1) < EPSILON:
            return random.choice(ACTIONS)
        return np.argmax(self.q_table[self.pos])

    def update(self, state, action, reward, next_state):
        best_next_q = np.max(self.q_table[next_state])
        self.q_table[state, action] += LEARNING_RATE * (reward + DISCOUNT * best_next_q - self.q_table[state, action])


class FWE_Agent:
    def __init__(self):
        # Phi (Φ): Habit/Memory (Real numbers, like Q-values)
        self.phi = np.zeros((STATES, len(ACTIONS)))
        # Psi (Ψ): Possibility/Superposition (Complex numbers)
        # We initialize with a "quantum noise" that represents curiosity/imagination
        self.psi = np.random.rand(STATES, len(ACTIONS)) + 1j * np.random.rand(STATES, len(ACTIONS))
        self.pos = 0
        self.gamma = 0.5  # "Free Will" / Interference factor

    def choose_action(self):
        # THE FREE WILL EQUATION LOGIC
        # 1. Get Habit (Phi)
        habit_amplitude = self.phi[self.pos]

        # 2. Get Possibility (Psi) - Simulate a "look ahead" or intuition
        # (In a real implementation, this comes from the World Model/JEPA.
        # Here, we simulate it as a 'sense' that the goal is ahead)
        dist_to_goal = (STATES - 1) - self.pos
        intuition = 1.0 / (dist_to_goal + 0.1)  # Intuition gets stronger closer to goal

        # Psi suggests moving forward (Action 1) has high potential
        current_psi = self.psi[self.pos].copy()
        current_psi[1] += intuition * 5.0  # Boost "Move Forward" amplitude

        # 3. INTERFERENCE: Superposition of Habit + Possibility
        # Wavefunction W = Phi + (Gamma * Psi)
        wavefunction = habit_amplitude + (self.gamma * current_psi)

        # 4. COLLAPSE: Born Rule (Probability = Amplitude Squared)
        probs = np.abs(wavefunction) ** 2

        # Normalize to create valid probabilities
        if np.sum(probs) == 0: probs = np.ones(len(ACTIONS))
        probs = probs / np.sum(probs)

        # Collapse into a choice
        return np.random.choice(ACTIONS, p=probs)

    def update(self, state, action, reward, next_state):
        # Update Memory (Phi) same as Q-learning
        best_next_phi = np.max(self.phi[next_state])
        self.phi[state, action] += LEARNING_RATE * (reward + DISCOUNT * best_next_phi - self.phi[state, action])

        # Update Psi (Imagination) - If we found Gold, Psi reinforces "Forward" everywhere
        if reward > 50:
            self.psi[:, 1] += 0.5 + 0.5j  # "Epiphany": Moving forward is good!


# --- SIMULATION ---
print(f"--- RUNNING 'THE VALLEY OF FIRE' ({STEPS} Episodes) ---")

std_agent = StandardAgent()
fwe_agent = FWE_Agent()
std_gold_count = 0
fwe_gold_count = 0

for episode in range(STEPS):
    # Run Standard Agent
    std_agent.pos = 0
    for _ in range(10):  # Max 10 moves per episode
        action = std_agent.choose_action()
        # Move logic
        next_pos = std_agent.pos
        if action == 1: next_pos = min(STATES - 1, std_agent.pos + 1)

        reward = REWARDS[next_pos]
        if action == 0: reward = -1  # Small penalty for waiting

        std_agent.update(std_agent.pos, action, reward, next_pos)
        std_agent.pos = next_pos
        if next_pos == 3:  # Gold
            std_gold_count += 1
            break

    # Run FWE Agent
    fwe_agent.pos = 0
    for _ in range(10):
        action = fwe_agent.choose_action()
        next_pos = fwe_agent.pos
        if action == 1: next_pos = min(STATES - 1, fwe_agent.pos + 1)

        reward = REWARDS[next_pos]
        if action == 0: reward = -1

        fwe_agent.update(fwe_agent.pos, action, reward, next_pos)
        fwe_agent.pos = next_pos
        if next_pos == 3:  # Gold
            fwe_gold_count += 1
            break

print(f"RESULTS:")
print(f"Standard Agent Gold Collected: {std_gold_count}")
print(f"FWE Agent Gold Collected:      {fwe_gold_count}")

if fwe_gold_count > std_gold_count:
    print("\nCONCLUSION: The FWE Agent successfully 'tunneled' through the negative reward (Fire)!")
    print("The Standard Agent likely got stuck avoiding the pain of the first step.")
else:
    print("\nCONCLUSION: The Agents performed similarly (increase steps or pain to see divergence).")