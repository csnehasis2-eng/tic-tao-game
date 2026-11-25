# 🎮 Tic Tac Toe — Classic Logic, Modern Experience

<p align="center">
  <strong>A classic two-player Tic Tac Toe game built with Python and NumPy, featuring both a terminal-based version and a modern interactive Streamlit gaming interface.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/NumPy-Array%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy">
  <img src="https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Status-Completed-22C55E?style=for-the-badge" alt="Status">
</p>

---

## ✨ Overview

Tic Tac Toe is a classic two-player strategy game where players take turns marking a 3×3 grid with **X** and **O**.

This project started as a simple Python terminal game and was extended into an interactive web-based gaming experience using Streamlit.

It demonstrates how the same core game logic can power two different interfaces while using NumPy for efficient board representation and winner detection.

## 🚀 Features

### 🖥️ Terminal Version — `main.py`

- Interactive command-line gameplay.
- Two-player turn-based system.
- NumPy-powered 3×3 game board.
- Automatic winner detection.
- Row, column and diagonal checking.
- Draw detection.
- Input-based player interaction.

### 🌐 Streamlit Version — `app.py`

- Modern dark gaming interface.
- Interactive 3×3 game board.
- Neon-inspired styling and visual effects.
- Dynamic player turn indicators.
- Animated winning line across matching symbols.
- Winner celebration with balloons.
- Draw celebration effect.
- Match scoreboard tracking X wins, O wins and draws.
- Play Again and Reset Match controls.
- Responsive layout for different screen sizes.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NumPy | Game board and array-based winner detection |
| Streamlit | Interactive web application |
| HTML & CSS | Custom UI design and styling |
| SVG | Animated winning-line effect |

## 📁 Project Structure

```text
tic-tao-game/
│
├── main.py       # Original terminal-based game
├── app.py        # Modern Streamlit gaming interface
└── README.md     # Project documentation
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/csnehasis2-eng/tic-tao-game.git
```

### 2. Navigate to the project directory

```bash
cd tic-tao-game
```

### 3. Install dependencies

```bash
pip install numpy streamlit
```

### 4. Run the terminal version

```bash
python main.py
```

### 5. Run the Streamlit version

```bash
streamlit run app.py
```

Your browser will open the interactive Tic Tac Toe application.

## 🎯 How to Play

1. The game is played between two players: X and O.
2. Player X starts first.
3. Players take turns selecting an empty cell.
4. The first player to align three identical symbols horizontally, vertically or diagonally wins.
5. If all nine cells are occupied without a winner, the game ends in a draw.

## 🧠 What I Learned

Building this project helped me practice:

- Working with NumPy arrays and matrix operations.
- Using `np.zeros
