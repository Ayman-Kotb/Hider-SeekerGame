# Hider-Seeker Game

A strategic game theory-based implementation of the classic Hide and Seek game, featuring optimal AI strategies using linear programming and game theory principles. Players can compete against AI opponents that use mathematically optimal mixed strategies.

## 🎮 Game Overview

The Hider-Seeker Game is a turn-based strategy game where:
- **Hider**: Chooses a location to hide on a grid-based world
- **Seeker**: Attempts to find the hider by selecting search locations
- **AI Opponent**: Uses game theory and linear programming to compute optimal mixed strategies

The game features dynamically generated worlds with varying difficulty levels and strategic depth through payoff matrices that consider distance relationships and terrain difficulty.

## ✨ Features

### Core Gameplay
- **Dynamic World Generation**: Randomly generated grid worlds with varying difficulty levels (Easy, Medium, Hard)
- **Strategic AI**: Computer opponents use optimal mixed strategies computed via linear programming
- **Flexible Game Modes**: Play as either the Hider or the Seeker against AI
- **Real-time Strategy Computation**: Live calculation of optimal probability distributions

### Game Mechanics
- **Distance-based Scoring**: Payoffs calculated using Manhattan distance and terrain difficulty
- **Multi-level Terrain**: Three difficulty levels affecting scoring multipliers
- **Neighbor Influence**: Adjacent cells have modified payoff values based on proximity
- **Score Tracking**: Real-time score updates for both players

### Simulation & Analysis
- **Batch Simulation**: Run multiple rounds of AI vs AI gameplay
- **Strategy Analysis**: View optimal probability distributions for both roles
- **Statistical Reporting**: Comprehensive win/loss statistics and performance metrics

## 🛠 Technology Stack

### Backend
- **Flask**: RESTful API server
- **NumPy**: Numerical computations and matrix operations
- **SciPy**: Linear programming optimization for strategy computation
- **Flask-CORS**: Cross-origin resource sharing support

### Frontend
- **React**: Modern web application interface
- **Interactive Grid**: Visual game board representation
- **Real-time Updates**: Live game state and strategy visualization

## 📋 Prerequisites

- Python 3.7+
- Node.js 14+
- npm or yarn

## 🚀 Installation

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ayman-Kotb/Hider-SeekerGame.git
   cd Hider-SeekerGame
   ```

2. **Install Python dependencies**
   ```bash
   pip install flask flask-cors numpy scipy
   ```

3. **Run the Flask server**
   ```bash
   python main.py
   ```
   The API server will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend  # Adjust path based on your structure
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the React development server**
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

## 🎯 API Endpoints

### Start New Game
**POST** `/api/start-game`

Initialize a new game session with specified parameters.

```json
{
  "rows": 3,
  "cols": 3,
  "gameMode": "human",
  "playerRole": "hider"
}
```

**Response:**
```json
{
  "gameWorld": [[0, 1, 2], [1, 0, 1], [2, 1, 0]],
  "payoff": [...],
  "probabilities": [0.1, 0.2, 0.15, ...]
}
```

### Play Round
**POST** `/api/play-round`

Execute a single game round with player and computer moves.

```json
{
  "playerRole": "hider",
  "playerMove": 4
}
```

**Response:**
```json
{
  "computerMove": 7,
  "hiderScore": 8,
  "seekerScore": -8,
  "probabilities": [0.1, 0.2, 0.15, ...]
}
```

### Simulate Games
**POST** `/api/simulate`

Run multiple rounds of AI vs AI simulation for analysis.

```json
{
  "rounds": 100
}
```

**Response:**
```json
{
  "probabilitiesOfHider": [...],
  "probabilitiesOfSeeker": [...],
  "playerWins": 45,
  "computerWins": 55,
  "playerScore": 120,
  "computerScore": -120,
  "totalRounds": 100,
  "roundsResults": [...]
}
```

### Health Check
**GET** `/api/health`

Verify API server status.

## 🎲 Game Rules

### World Generation
- Each cell has a difficulty level: **Easy (0)**, **Medium (1)**, or **Hard (2)**
- Payoff matrices are generated based on difficulty and distance relationships
- Neighboring cells have modified payoff values

### Scoring System
- **Perfect Find**: ±4 × |payoff value| when seeker finds hider exactly
- **Miss**: ±4 × |payoff value| when seeker doesn't find hider
- **Sign Convention**: Positive for hider advantage, negative for seeker advantage

### AI Strategy
- Uses **Linear Programming** to solve for optimal mixed strategies
- Computes **Nash Equilibrium** strategies for both roles
- Adapts strategy based on current game state and payoff matrix

## 🔧 Configuration

### World Size
- Minimum: 2×2 grid
- Maximum: Limited by computational resources
- Recommended: 3×3 to 5×5 for optimal gameplay

### Difficulty Levels
- **Easy (0)**: Higher payoffs, more forgiving gameplay
- **Medium (1)**: Balanced risk/reward
- **Hard (2)**: Higher penalties, strategic depth

## 🧮 Game Theory Implementation

The game implements classic game theory concepts:

- **Two-Player Zero-Sum Game**: One player's gain equals the other's loss
- **Mixed Strategies**: Probability distributions over pure strategies
- **Nash Equilibrium**: Optimal strategies where no player can improve unilaterally
- **Linear Programming**: Mathematical optimization for strategy computation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- Game theory concepts from classical literature
- SciPy optimization library for linear programming
- Flask framework for robust API development
- React ecosystem for modern web interfaces

---

**Made with ❤️ using React and Flask**
