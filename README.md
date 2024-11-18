# **AI-2048 Game**

## **Overview**
This project is an AI implementation of the classic 2048 game. The AI autonomously plays the game using intelligent decision-making strategies to maximize its score.

## **Features**
- Playable version of 2048 with AI-controlled gameplay.
- Intelligent agents implement strategies like Minimax or Expectimax.
- Modular design with separate components for grid management, AI logic, and display functionalities.

## **Project Structure**
Here’s a breakdown of the key files:

- **`BaseAI.py`**: Base class for AI agents to inherit common functionality.
- **`ComputerAI.py`**: Logic for simulating computer moves in the game.
- **`GameManager.py`**: Manages the game flow, alternating between AI and computer turns.
- **`BaseDisplayer.py`**: Base functionality for displaying the game board.
- **`Displayer.py`**: Visual representation of the game board.
- **`Grid.py`**: Manages the game grid, including tile placement and updates.
- **`IntelligentAgent.py`**: Core AI logic, implementing strategies to optimize gameplay.
- **`README.md`**: Documentation for the project (this file).

## **Installation**
Clone the repository:
git clone https://github.com/yourusername/ai-2048.git
cd ai-2048
run: python GameManager.py


