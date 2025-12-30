import numpy as np
import random
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
EPISODES = 80
CHANGE_POINT = 40
GRID_SIZE = 7
START = (0, 0)
GOAL = (6, 6)
DOOR_LOC = (3, 3)

# The Wall with a "Long Path" gap at (3,6)
WALLS = [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5)]

ACTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right


class MazeEnv:
    def __init__(self):
        self.door_locked = True

    def step(self, state, action_idx):
        move = ACTIONS[action_idx]
        next_r = state[0] + move[0]
        next_c = state[1] + move[1]
        next_state = (next_r, next_c)

        if not (0 <= next_r < GRID_SIZE and 0 <= next_c < GRID_SIZE):
            return state, -1, False
        if next_state in WALLS:
            return state, -1, False
        if next_state == GOAL:
            return next_state, 100, True
        if next_state == DOOR_LOC and self.door_locked:
            return state, -10, False  # Painful bump
        return next_state, -1, False


class StandardAgent:
    def __init__(self):
        self.q_table = {}
        self.epsilon = 0.1

    def get_q(self, state):
        if state not in self.q_table: self.q_table[state] = np.zeros(4)
        return self.q_table[state]

    def choose_action(self, state):
        if random.random() < self.epsilon: return random.randint(0, 3)
        return np.argmax(self.get_q(state))

    def update(self, state, action, reward, next_state):
        old_q = self.get_q(state)[action]
        max_next = np.max(self.get_q(next_state))
        self.q_table[state][action] = old_q + 0.1 * (reward + 0.95 * max_next - old_q)


class FWE_Agent:
    def __init__(self):
        self.phi = {}  # Habit (Memory)
        self.gamma = 1.5  # Willpower Intensity

    def get_phi(self, state):
        if state not in self.phi: self.phi[state] = np.zeros(4)
        return self.phi[state]

    def get_psi(self, state):
        # --- THE FIX: HEURISTIC PSI ---
        # Psi acts like a "Compass" pointing to the Goal.
        # It creates a vector that says "I WANT to go towards (6,6)"
        psi_vector = np.zeros(4, dtype=complex)

        goal_r, goal_c = GOAL
        curr_r, curr_c = state

        # Calculate pull towards goal
        if goal_r > curr_r: psi_vector[1] += 1.0  # Pull Down
        if goal_r < curr_r: psi_vector[0] += 1.0  # Pull Up
        if goal_c > curr_c: psi_vector[3] += 1.0  # Pull Right
        if goal_c < curr_c: psi_vector[2] += 1.0  # Pull Left

        return psi_vector

    def choose_action(self, state):
        phi = self.get_phi(state)
        psi = self.get_psi(state)

        # INTERFERENCE: Memory + (Will * Compass)
        wavefunction = phi + (self.gamma * psi)

        probs = np.abs(wavefunction) ** 2
        if np.sum(probs) == 0: return random.randint(0, 3)
        probs = probs / np.sum(probs)
        return np.random.choice(4, p=probs)

    def update(self, state, action, reward, next_state):
        # Update Memory (Phi) normally
        max_next = np.max(self.get_phi(next_state))
        self.phi[state][action] += 0.1 * (reward + 0.95 * max_next - self.phi[state][action])


# --- RUN ---
print("--- RUNNING FIXED EXPERIMENT (Heuristic Psi) ---")
env = MazeEnv()
std_agent = StandardAgent()
fwe_agent = FWE_Agent()

std_log = []
fwe_log = []

for ep in range(EPISODES):
    if ep == CHANGE_POINT:
        print(f"Ep {ep}: *** DOOR UNLOCKS ***")
        env.door_locked = False

    # Standard
    s, steps = START, 0
    while s != GOAL and steps < 100:
        a = std_agent.choose_action(s)
        ns, r, d = env.step(s, a)
        std_agent.update(s, a, r, ns)
        s = ns
        steps += 1
    std_log.append(steps)

    # FWE
    s, steps = START, 0
    while s != GOAL and steps < 100:
        a = fwe_agent.choose_action(s)
        ns, r, d = env.step(s, a)
        fwe_agent.update(s, a, r, ns)
        s = ns
        steps += 1
    fwe_log.append(steps)

# --- RESULTS ---
print(f"Avg Steps Phase 2 (Standard): {np.mean(std_log[CHANGE_POINT:]):.1f}")
print(f"Avg Steps Phase 2 (FWE):      {np.mean(fwe_log[CHANGE_POINT:]):.1f}")

plt.figure(figsize=(10, 6))
plt.plot(std_log, 'r--', label='Standard Agent (Habit)', linewidth=2)
plt.plot(fwe_log, 'b-', label='FWE Agent (Will)', linewidth=2)
plt.axvline(x=CHANGE_POINT, color='g', label='Door Unlocks')
plt.title('Cognitive Flexibility: Unlearning the Long Path')
plt.xlabel('Episodes')
plt.ylabel('Steps (Lower is Better)')
plt.legend()
plt.show()