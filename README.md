# Dungeon Explorer

A text-based dungeon exploration game powered by LLM technology. The game dynamically generates story content, characters, and player choices using OpenAI's GPT-3.5 model.

## Features

- Procedurally generated dungeon adventures
- Dynamic storytelling that adapts to player choices
- Character interactions that evolve based on game state
- Inventory management
- Text-based interface through the terminal

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```
   
   On Windows:
   ```
   set OPENAI_API_KEY=your-api-key-here
   ```

## How to Play

Run the game with:
```
python main.py
```

The game will:
1. Generate a unique dungeon adventure
2. Create a player character for you
3. Present you with choices as you explore
4. Track your inventory and progress
5. Adapt the story based on your decisions

## Game Mechanics

- You'll be presented with 4 choices at each step
- Your inventory affects what actions are available
- Characters you meet may help or hinder your progress
- The game keeps track of your history and adapts accordingly

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for LLM API calls)

## Note

This game makes API calls to OpenAI's services, which may incur costs depending on your usage and OpenAI's pricing model. 