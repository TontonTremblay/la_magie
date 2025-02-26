# Dungeon Explorer

A text-based dungeon exploration game powered by LLM technology. The game dynamically generates story content, characters, and player choices using OpenAI's GPT-4o model.

## Features

- Procedurally generated dungeon adventures
- Dynamic storytelling that adapts to player choices
- Character interactions that evolve based on game state
- Inventory management
- Text-based interface through the terminal
- Powered by OpenAI's advanced GPT-4o model
- **Voice narration** using OpenAI's text-to-speech technology

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   For Linux users, you may need to install an audio player:
   ```
   # Ubuntu/Debian
   sudo apt-get install mpg123
   
   # Fedora/RHEL
   sudo dnf install mpg123
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
6. Narrate the story with AI-generated voice

## Game Mechanics

- You'll be presented with 4 choices at each step
- Your inventory affects what actions are available
- Characters you meet may help or hinder your progress
- The game keeps track of your history and adapts accordingly

## Voice Narration

The game includes AI-powered voice narration for an immersive experience:

- Toggle narration on/off during gameplay
- Choose from 6 different voice options:
  - Alloy: A warm, natural voice
  - Echo: A deep, resonant voice
  - Fable: A mystical, enchanting voice
  - Onyx: A clear, authoritative voice (default)
  - Nova: A bright, energetic voice
  - Shimmer: A soft, gentle voice

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for LLM API calls and text-to-speech)
- Audio playback capability

## Note

This game makes API calls to OpenAI's services, which may incur costs depending on your usage and OpenAI's pricing model. The text-to-speech feature will use additional API credits. 