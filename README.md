# 🚀 Spaceship Arcade Game

A classic arcade game built with **Pygame** — control your spaceship, dodge meteorites, and collect stars to beat your high score!

## 🎮 Gameplay

- **Up/Down arrows** — move the spaceship
- **Avoid** incoming meteorites
- **Collect** stars for +100 bonus points
- **+10 points** every second you survive
- Press **Pause** to take a break
- Check the **Leaderboard** to see top scores

## 🛠 Tech Stack

- Python 3
- Pygame
- Simple file-based score persistence

## 🚀 How to Run

```bash
pip install pygame
python main.py
```

> Note: game background music file is optional — the game works with or without it.

## 📁 Project Structure

```
mygame/
├── main.py         # Main game logic
├── data/           # Images and assets
│   ├── ship0.png
│   ├── ship1.png
│   ├── ship2.png
│   ├── asteroid.png
│   ├── star.png
│   └── background.jpg
└── records.txt     # High scores
```