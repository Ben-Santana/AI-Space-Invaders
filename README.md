# Tomo

*By: Benjamin Santana, Madhav Lodha, Brendan Peters, Alejandro*

## Project Overview

Tomo brings a fresh take on the arcade classic by incorporating AI-driven adaptability. With each new level, ChatGPT dynamically generates new game mechanics, ensuring that no two playthroughs are ever the same. Built using Python and Pygame, this project leverages the power of language models to push the boundaries of traditional gameplay, delivering innovative and unpredictable challenges.

## Features

- **AI-Powered Game Evolution**: Each level introduces unique mechanics, coded in real-time, thanks to the integration of a large language model.
- **Classic Arcade Feel**: Retains the iconic gameplay of Space Invaders while adding layers of complexity and creativity.
- **Infinite Replayability**: With procedurally generated features, each game session brings new surprises and challenges.

## How It Works

1. **Starting the Game**: At each level, the LLM (ChatGPT) analyzes the current game state and introduces new mechanics. This can range from new enemy behaviors to player abilities.
2. **Player vs AI Creativity**: The game evolves based on AI-generated code, allowing for a continuous, non-repetitive gameplay experience.

## Installation

To get started, clone the repository and install the required packages:

```bash
git clone https://github.com/Ben-Santana/Tomo.git
cd tomo
```

## Running the Game

Run the main game script:

```bash
python game.py
```

Our main branch implements a leap motion hand tracker to control the player using hand movements, if you would like to play with keyboard inputs, I would recommend checking out the BensTweaks branch.

## License

This project is licensed under the MIT License.
