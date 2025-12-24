# Flappy Bird AI - Genetic Algorithm

A Flappy Bird game where AI agents learn to play using a genetic algorithm and neural networks.

## Overview

This project implements an AI that learns to play Flappy Bird through evolutionary learning. Multiple birds (agents) play simultaneously, and the best performers are selected to create the next generation through:
- **Selection**: Tournament selection to pick the fittest birds
- **Crossover**: Combining neural network weights from two parents
- **Mutation**: Random weight adjustments for genetic diversity
- **Elitism**: Keeping the best performers unchanged

## Features

- 🧠 **Neural Network Brain**: Each bird has a feedforward neural network that decides when to jump
- 🧬 **Genetic Algorithm**: Population evolves over generations to improve performance
- 📊 **Real-time Statistics**: See generation number, alive birds, current score, and best score
- ⚡ **Speed Control**: Press SPACE to toggle between 1x and 5x speed
- 👁️ **Visibility Toggle**: Press V to show/hide all birds (shows only the best bird when hidden)

## Requirements

- Python 3.x
- pygame-ce
- numpy

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Flappy_bird
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
```

3. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`

4. Install dependencies:
```bash
pip install pygame-ce numpy
```

## Usage

Run the game:
```bash
python flappy_bird_ai/main.py
```

### Controls

- **SPACE**: Toggle speed (1x / 5x)
- **V**: Toggle bird visibility (all birds / best bird only)
- **ESC**: Quit

## How It Works

### Neural Network
Each bird has a neural network with:
- **Input Layer**: 5 neurons (bird Y position, bird velocity, pipe X position, pipe top Y, pipe bottom Y)
- **Hidden Layer**: 8 neurons with ReLU activation
- **Output Layer**: 1 neuron with sigmoid activation (jump if > 0.5)

### Genetic Algorithm
1. **Population**: 50 birds start each generation
2. **Fitness**: Based on survival time and score (pipes passed)
3. **Selection**: Tournament selection picks the best parents
4. **Crossover**: Uniform crossover combines parent weights
5. **Mutation**: 10% chance to mutate each weight with Gaussian noise
6. **Elitism**: Top 5 birds survive unchanged to the next generation

## Project Structure

```
flappy_bird_ai/
├── bird.py              # Bird class with neural network brain
├── config.py            # Game configuration and parameters
├── genetic_algorithm.py # Genetic algorithm implementation
├── main.py              # Main game loop
├── neural_network.py    # Neural network implementation
└── pipe.py              # Pipe class and collision detection
```

## Parameters

You can adjust these parameters in `config.py`:
- `POPULATION_SIZE`: Number of birds per generation (default: 50)
- `MUTATION_RATE`: Probability of weight mutation (default: 0.1)
- `MUTATION_STRENGTH`: Magnitude of mutations (default: 0.5)
- `ELITISM_COUNT`: Number of best birds to keep (default: 5)
- `HIDDEN_SIZE`: Neural network hidden layer size (default: 8)

## License

This project is open source and available for educational purposes.

## Acknowledgments

Inspired by the classic Flappy Bird game and evolutionary learning techniques.

[Game Screenshot](Screenshots-Flappy/Screenshot 2025-12-15 140132.png)
[Game Screenshot](Screenshots-Flappy/Screenshot 2025-12-15 140649.png)
[Game Screenshot](Screenshots-Flappy/Screenshot 2025-12-15 140918.png
