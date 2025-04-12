# 🐉 Three-Dragon Ante AI

This project implements an AI agent that plays **Three-Dragon Ante (3DA)**, a strategic fantasy card game of bluffing and risk. The AI uses **Monte Carlo Tree Search (MCTS)** and **Bayesian inference** to make intelligent, forward-looking decisions during gameplay.

---

## 🎮 Game Summary

Three-Dragon Ante is a poker-style game where players:
- **Ante** a card at the start of each gambit
- Take turns playing dragon cards into their **flight**
- Trigger **powers** based on the type and color of cards
- Win or lose gold based on total flight strength and triggered effects

The game continues across multiple gambits until a player is eliminated or a winning condition is met.

---

## 🤖 AI Features

The AI plays as one of the players in the game and makes decisions based on simulations and predictions. It can:
- Choose which **card to ante**
- Decide whether to **give up a card or gold** when prompted by card effects
- Select which **card to play** during its turn
- **Predict opponent card strength** using a Bayesian model based on cards already played

---

## 🧠 AI Architecture

### 🧩 Game State Representation

Each simulation node contains a full game state, represented by a `TDA` object that tracks:
- Each player's **gold**, **card count**, and **flight**
- The AI player's **hand** and **gold**
- The current **ante** (cards + gold)
- Whose **turn** it is
- The **last played card**

All simulations **deep copy** this state to avoid side effects.

### 🌀 MCTS Overview

- Each node corresponds to a full game state
- Simulations run until the **end of the current gambit**
- **Random card draws** are handled via sampling or averaged value (e.g., strength = 7)
- Only **AI turns are used for node selection and backpropagation**
- Scoring is based on:
  ```
  score = coins + estimated coin value of cards remaining in hand
  ```

### 📊 Opponent Modeling

Opponent card strength is estimated using Bayesian updates:
- Initial distribution assumes a mean of 7 (values from 1 to 13)
- Each played card updates the posterior
- AI uses this to predict likely future card values for opponents

---

## 📁 Project Structure

```plaintext
3DA/
├── game/
│   ├── AIPlayer.py       # AI-specific player logic
│   ├── Player.py         # Base player class
│   ├── TDA.py            # Game state and rule enforcement
│   ├── Cards.py          # Dragon card powers (basic colors)
│   ├── Card.py           # Card base class
│   ├── Ante.py           # Ante mechanics
│   ├── Flight.py         # Flight logic and resolution
│   └── __init__.py
├── MCTS/
│   ├── MCTS.py           # Core MCTS algorithm
│   ├── Node.py           # Tree node representation
│   └── __init__.py
├── game.py               # Main entry point to play a full game
├── gameTests.py          # Basic test harness
└── README.md             # You're here
```

---

## 🛠️ Requirements

- Python 3.10+
- No external dependencies

---

## 🚀 Running the Project

To run a full AI game simulation:

```bash
python3 game.py
```

To run any tests or debug gameplay behavior:

```bash
python3 gameTests.py
```

---

## ⚠️ Limitations

- Deck is currently assumed to be **infinite** (drawn cards may repeat)
- **Legendary and Mortal** card types are not yet implemented
- Opponents use **random or simple heuristics**
- Some card interactions may be simplified for now

---

## 🛣️ Future Improvements

- Implement **finite deck mechanics**
- Add full support for **Legendary and Mortal** cards
- Improve opponent behavior using **learned policies or heuristics**
- Expand power resolution to support edge cases and chaining
- Visualize game state and MCTS decision tree for debugging

---

## 📬 Contributions

Open to ideas, contributions, or feedback! Feel free to fork this repo, open issues, or suggest improvements.
