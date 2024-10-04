# Memory Card Game - Spaced Repetition Learning Tool

## Overview

The Memory Card Game is an educational tool designed to enhance learning through spaced repetition. The game presents questions on various topics, and users must provide answers, which are then evaluated by an AI bot. The goal is to encourage retention of information by adjusting the difficulty and frequency of questions based on user performance.

## Features
- **Spaced Repetition Algorithm**: Questions are presented based on a spaced repetition system, increasing the interval between questions as you answer correctly.
- **Interactive UI**: A user-friendly interface built with Tkinter, allowing easy topic selection, question display, and answer submission.
- **AI-Assisted Evaluation**: Uses a chatbot to evaluate answers and provide feedback, assigning a score based on correctness.
- **Dynamic Feedback**: Immediate feedback is provided after each answer submission, with explanations for incorrect answers.
- **Customizable Topics**: Users can add and select topics from JSON files, which contain predefined questions.

## Project Structure

1. **MemoryCard Class**: Represents a flashcard with a question, score, and interval. Tracks when the card was last answered.
2. **MemoryGame Class**: Manages the game logic, including loading topics, displaying questions, saving progress, and checking answers.
3. **MemoryGameUI Class**: Builds the Tkinter-based interface, allowing users to interact with the game (e.g., selecting topics, submitting answers).
4. **AI Integration**: A simple chatbot model evaluates user answers and assigns scores based on correctness.

## Getting Started

### Prerequisites
- Python 3.x
- Tkinter (included with most Python installations)
- External libraries:
  - `llamabot` (for the chatbot model)
  - `memory_game_ui`, `memory_card` (custom game logic modules)

### Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/memory-card-game.git
    ```
2. Navigate to the project directory:
    ```bash
    cd memory-card-game
    ```

3. Run the setup script to install necessary dependencies:
    ```bash
    ./setup.sh
    ```

The `setup.sh` file will:
- Install Ollama for the chatbot model:
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
- Pull the llama3.2 model:
    ```bash
    ollama pull llama3.2
    ```
- Install Python requirements:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Game
1. Ensure the `topics` directory contains JSON files with question data.
2. Run the main script:
    ```bash
    python main.py
    ```
3. The user interface will open. Choose a topic to start playing.

## JSON File Structure
Each topic is represented by a JSON file in the `topics/` directory. The structure is as follows:
```json
[
    {
        "question": "What is the capital of France?",
        "interval": 1,
        "score": 0,
        "last_answered": null
    },
    ...
]
```
- **question**: The question to ask the user.
- **interval**: The time interval before the question is shown again (spaced repetition).
- **score**: The user's current score for the question.
- **last_answered**: The timestamp of when the question was last answered.

## How the Game Works
1. **Topic Selection**: The user selects a topic from the dropdown menu.
2. **Show Question**: A random question is selected based on the spaced repetition system.
3. **Submit Answer**: The user submits an answer, which is evaluated by the chatbot.
4. **Feedback**: The AI provides feedback, scoring the answer and offering explanations if necessary. The question's interval is adjusted based on performance.
5. **Save Progress**: The game saves the user's progress (question score, interval, and last answered time) to the JSON file.

## Customization
- Add your own topics by creating JSON files in the `topics/` directory.
- Modify the chatbot model or change the evaluation logic by editing the `check_answer_with_LLM` method.

## Future Improvements
- Add more sophisticated question types (e.g., multiple-choice).
- Implement a scoring leaderboard or progress tracker.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
