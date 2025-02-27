"""
Utility functions for the Dungeon Explorer game
"""

import os
import time
import random
from typing import List, Dict, Any, Optional

# Global configuration
NARRATION_ENABLED = False
NARRATION_VOICE = "nova"  # Options: alloy, echo, fable, onyx, nova, shimmer

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text: str, delay: float = 0.03):
    """Print text with a typing effect"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def narrate(text: str, llm=None):
    """Narrate text using text-to-speech if enabled"""
    if NARRATION_ENABLED and llm:
        llm.text_to_speech(text, voice=NARRATION_VOICE)

def format_list(items: List[str]) -> str:
    """Format a list of items as a readable string"""
    if not items:
        return "nothing"
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return ", ".join(items[:-1]) + f", and {items[-1]}"

def dice_roll(sides: int = 6, num_dice: int = 1) -> int:
    """Simulate rolling dice"""
    return sum(random.randint(1, sides) for _ in range(num_dice))

def chance(probability: float) -> bool:
    """Return True with the given probability (0.0 to 1.0)"""
    return random.random() < probability

def get_game_banner(title1: str = "DUNGEON", title2: str = "EXPLORER") -> str:
    """
    Generate ASCII art banner for the game with customizable title text.
    
    Args:
        title1: First line of the title (default: "DUNGEON")
        title2: Second line of the title (default: "EXPLORER")
    
    Returns:
        A string containing the ASCII art banner
    """
    # Create the border
    border_top = "    ╔" + "═" * 59 + "╗"
    border_bottom = "    ╚" + "═" * 59 + "╝"
    empty_line = "    ║" + " " * 59 + "║"
    
    # Generate the banner
    banner = [
        "",
        border_top,
        empty_line
    ]
    
    # Add the first title line (if provided)
    if title1:
        title1_centered = title1.center(59)
        banner.append(f"    ║   {title1_centered}   ║")
    
    # Add spacing between titles
    banner.append(empty_line)
    
    # Add the second title line (if provided)
    if title2:
        title2_centered = title2.center(59)
        banner.append(f"    ║   {title2_centered}   ║")
    
    # Complete the banner
    banner.extend([
        empty_line,
        border_bottom,
        ""
    ])
    
    return "\n".join(banner)

def get_fancy_game_banner(title1: str = "DUNGEON", title2: str = "EXPLORER") -> str:
    """
    Generate a fancy ASCII art banner for the game with customizable title text.
    
    Args:
        title1: First line of the title (default: "DUNGEON")
        title2: Second line of the title (default: "EXPLORER")
    
    Returns:
        A string containing the fancy ASCII art banner
    """
    # ASCII art letters for each character (simplified version)
    ascii_letters = {
        'A': [
            "  █████  ",
            " ██   ██ ",
            "███████  ",
            "██   ██ ",
            "██   ██ "
        ],
        'B': [
            "██████  ",
            "██   ██ ",
            "██████  ",
            "██   ██ ",
            "██████  "
        ],
        'C': [
            " ██████ ",
            "██      ",
            "██      ",
            "██      ",
            " ██████ "
        ],
        'D': [
            "██████  ",
            "██   ██ ",
            "██   ██ ",
            "██   ██ ",
            "██████  "
        ],
        'E': [
            "███████ ",
            "██      ",
            "█████   ",
            "██      ",
            "███████ "
        ],
        'F': [
            "███████ ",
            "██      ",
            "█████   ",
            "██      ",
            "██      "
        ],
        'G': [
            " ██████  ",
            "██       ",
            "██   ███ ",
            "██    ██ ",
            " ██████  "
        ],
        'H': [
            "██   ██ ",
            "██   ██ ",
            "███████ ",
            "██   ██ ",
            "██   ██ "
        ],
        'I': [
            "███     ",
            " ██     ",
            " ██     ",
            " ██     ",
            "███     "
        ],
        'J': [
            "     ██ ",
            "     ██ ",
            "     ██ ",
            "██   ██ ",
            " █████  "
        ],
        'K': [
            "██   ██ ",
            "██  ██  ",
            "█████   ",
            "██  ██  ",
            "██   ██ "
        ],
        'L': [
            "██      ",
            "██      ",
            "██      ",
            "██      ",
            "███████ "
        ],
        'M': [
            "███    ███ ",
            "████  ████ ",
            "██ ████ ██ ",
            "██  ██  ██ ",
            "██      ██ "
        ],
        'N': [
            "███    ██ ",
            "████   ██ ",
            "██ ██  ██ ",
            "██  ██ ██ ",
            "██   ████ "
        ],
        'O': [
            " ██████  ",
            "██    ██ ",
            "██    ██ ",
            "██    ██ ",
            " ██████  "
        ],
        'P': [
            "██████  ",
            "██   ██ ",
            "██████  ",
            "██      ",
            "██      "
        ],
        'Q': [
            " ██████  ",
            "██    ██ ",
            "██    ██ ",
            "██ ▄▄ ██ ",
            " ██████  "
        ],
        'R': [
            "██████  ",
            "██   ██ ",
            "██████  ",
            "██   ██ ",
            "██   ██ "
        ],
        'S': [
            " ██████  ",
            "██       ",
            " ██████  ",
            "      ██ ",
            " ██████  "
        ],
        'T': [
            "████████ ",
            "   ██    ",
            "   ██    ",
            "   ██    ",
            "   ██    "
        ],
        'U': [
            "██    ██ ",
            "██    ██ ",
            "██    ██ ",
            "██    ██ ",
            " ██████  "
        ],
        'V': [
            "██    ██ ",
            "██    ██ ",
            "██    ██ ",
            " ██  ██  ",
            "  ████   "
        ],
        'W': [
            "██     ██ ",
            "██     ██ ",
            "██  █  ██ ",
            "██ ███ ██ ",
            " ███ ███  "
        ],
        'X': [
            "██   ██ ",
            " ██ ██  ",
            "  ███   ",
            " ██ ██  ",
            "██   ██ "
        ],
        'Y': [
            "██    ██ ",
            " ██  ██  ",
            "  ████   ",
            "   ██    ",
            "   ██    "
        ],
        'Z': [
            "███████ ",
            "    ██  ",
            "   ██   ",
            "  ██    ",
            "███████ "
        ],
        ' ': [
            "        ",
            "        ",
            "        ",
            "        ",
            "        "
        ]
    }
    
    # Create the border
    border_top = "    ╔" + "═" * 59 + "╗"
    border_bottom = "    ╚" + "═" * 59 + "╝"
    empty_line = "    ║" + " " * 59 + "║"
    
    # Generate the banner
    banner = [
        "",
        border_top,
        empty_line
    ]
    
    # Convert titles to uppercase
    title1 = title1.upper()
    title2 = title2.upper()
    
    # Generate ASCII art for the first title
    if title1:
        title1_ascii = ["", "", "", "", ""]
        for char in title1:
            if char in ascii_letters:
                for i in range(5):
                    title1_ascii[i] += ascii_letters[char][i]
            else:
                for i in range(5):
                    title1_ascii[i] += "        "
        
        # Center and add the first title
        for line in title1_ascii:
            centered_line = line.center(59)
            banner.append(f"    ║{centered_line}║")
    
    # Add spacing between titles
    banner.append(empty_line)
    
    # Generate ASCII art for the second title
    if title2:
        title2_ascii = ["", "", "", "", ""]
        for char in title2:
            if char in ascii_letters:
                for i in range(5):
                    title2_ascii[i] += ascii_letters[char][i]
            else:
                for i in range(5):
                    title2_ascii[i] += "        "
        
        # Center and add the second title
        for line in title2_ascii:
            centered_line = line.center(59)
            banner.append(f"    ║{centered_line}║")
    
    # Complete the banner
    banner.extend([
        empty_line,
        border_bottom,
        ""
    ])
    
    return "\n".join(banner)

def toggle_narration():
    """Toggle narration on/off"""
    global NARRATION_ENABLED
    NARRATION_ENABLED = not NARRATION_ENABLED
    return NARRATION_ENABLED

def set_narration_voice(voice: str):
    """Set the narration voice"""
    global NARRATION_VOICE
    valid_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    if voice.lower() in valid_voices:
        NARRATION_VOICE = voice.lower()
        return True
    return False

def save_game(game_state: Dict[str, Any], filename: str = "savegame.json") -> bool:
    """Save the current game state to a file"""
    import json
    try:
        with open(filename, 'w') as f:
            json.dump(game_state, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving game: {e}")
        return False

def load_game(filename: str = "savegame.json") -> Optional[Dict[str, Any]]:
    """Load a game state from a file"""
    import json
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading game: {e}")
        return None 