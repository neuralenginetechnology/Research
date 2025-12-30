# The Free Will Equation (FWE)
**Modeling Agency via Quantum-Inspired Interference in Reinforcement Learning**

![Status](https://img.shields.io/badge/Status-Complete-green.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

This repository contains the reference implementation for the paper **"The Free Will Equation."** It demonstrates how separating "Habit" (Memory) from "Possibility" (Will) allows AI agents to escape local optima that trap standard Reinforcement Learning algorithms.

## 📄 The Core Concept
Standard AI maximizes reward based on history ($\Phi$).
**FWE agents maximize amplitude based on history + potential ($\Phi + \gamma\Psi$).**

This architecture enables:
1. **Tunneling:** Crossing negative reward valleys to find global optima.
2. **Sacrifice:** Taking short-term losses for long-term social trust.
3. **Innovation:** Exploring unstable regions to find "Black Swan" solutions.

---

## 🧪 Experiments

### 1. The Valley of Fire (Physical Endurance)
A simulation where an agent must walk through fire (-10 reward) to reach gold (+100 reward).
* **Result:** FWE Agent crosses the fire 100% of the time. Standard agent hesitates and fails.
* **Run:** `python valley_of_fire.py`

### 2. Prisoner's Dilemma (Social Trust)
An iterated game testing trust.
* **Result:** FWE Agent breaks the Nash Equilibrium by executing a "Sacrifice Move," signaling trust to a selfish opponent.
* **Run:** `python prisoners_dilemma.py`

### 3. Molecule Discovery (Creativity)
A symbolic chemical space with a "Valley of Instability."
* **Result:** FWE Agent ignores "Stability" warnings to find highly potent molecules (Score: 100.0), while standard AI gets stuck on local maxima.
* **Run:** `python molecule_discovery.py`

### 4. The Changed Labyrinth (Cognitive Flexibility)
A maze where a locked door secretly unlocks halfway through.
* **Result:** FWE Agent unlearns the "Locked Door" habit 30% faster than standard Q-Learning.
* **Run:** `python changed_labyrinth.py`

### 5. The Torture Test (Robustness)
The FWE Agent vs. a Random "ChaosBot."
* **Result:** FWE Agent correctly identifies the opponent is crazy and switches to defensive play, proving it is not blindly suicidal.
* **Run:** `python torture_test.py`

---

## 🛠️ Installation & Usage

1. **Clone the repo:**
    ```bash
    git clone [https://github.com/neuralenginetechnology/Research.git](https://github.com/neuralenginetechnology/Research.git)
    cd Research/The-Free-Will-Equation
    ```

2. **Install dependencies:**
    ```bash
    pip install numpy matplotlib
    ```

3. **Run an experiment:**
    ```bash
    python molecule_discovery.py
    ```

## 📜 Citation

```bibtex
@article{kabali2025freewill,
  title={The Free Will Equation: Modeling Agency via Quantum-Inspired Interference in Reinforcement Learning},
  author={Kabali, Rahul},
  journal={arXiv preprint arXiv:2507.14154},
  year={2025}
}
*Created by Rahul Kabali.*
