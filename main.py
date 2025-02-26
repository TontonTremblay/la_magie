import os
import json
from typing import List, Dict, Any
import llmlite
import game_utils

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

# Initialize LLM client
llm = llmlite.LLM(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)

class Game:
    def __init__(self):
        self.game_state = {
            "story_context": {},
            "player": {},
            "current_location": "",
            "inventory": [],
            "characters_met": [],
            "history": []
        }
    
    def initialize_game(self):
        """Generate the initial game context using LLM"""
        game_utils.slow_print("Generating game world...", delay=0.05)
        
        prompt = """
        You are a game master. A new game is about to start and we need an outline.
        
        Please provide the following in JSON format:
        1. theme: A fantasy theme for the dungeon
        2. conflict: The main conflict or challenge
        3. possible_solutions: At least 3 different ways to resolve the conflict
        4. characters: At least 3 characters with their descriptions, motivations, and how they can help or hinder the player
        5. failure_cases: At least 2 ways the player might fail
        """
        
        story_context = llm.generate_json(prompt)
        if story_context:
            self.game_state["story_context"] = story_context
            game_utils.slow_print("Game context generated successfully!")
        else:
            game_utils.slow_print("Error generating game context. Using default game context.")
            self.game_state["story_context"] = self._get_default_game_context()
    
    def _get_default_game_context(self) -> Dict[str, Any]:
        """Fallback game context if LLM fails"""
        return {
            "theme": "Ancient cursed temple",
            "conflict": "A powerful artifact is causing monsters to appear",
            "possible_solutions": [
                "Destroy the artifact",
                "Return the artifact to its rightful place",
                "Use the artifact to seal the temple"
            ],
            "characters": [
                {
                    "name": "Old Sage",
                    "description": "A wise old man who knows the temple's history",
                    "motivation": "Wants to preserve knowledge",
                    "help": "Can provide information about the artifact"
                },
                {
                    "name": "Temple Guardian",
                    "description": "A magical construct protecting the temple",
                    "motivation": "Follows ancient orders to protect the artifact",
                    "hinder": "Will attack anyone trying to take the artifact"
                },
                {
                    "name": "Treasure Hunter",
                    "description": "A rival explorer seeking the artifact",
                    "motivation": "Wants to sell the artifact for profit",
                    "hinder": "Will try to steal the artifact from the player"
                }
            ],
            "failure_cases": [
                "Getting trapped in the temple forever",
                "Releasing an ancient evil by misusing the artifact"
            ]
        }
    
    def create_player(self):
        """Generate player character and starting location"""
        game_utils.slow_print("Creating your character...", delay=0.05)
        
        context = self.game_state["story_context"]
        prompt = f"""
        Based on this game context: {json.dumps(context)}
        
        Please create:
        1. A player character (name, brief background, starting items)
        2. A starting location in the dungeon
        
        Format your response with these fields:
        - player_name
        - player_background
        - starting_items (as a list)
        - starting_location
        - location_description
        """
        
        player_data = llm.generate_json(prompt)
        if player_data and "player_name" in player_data:
            self.game_state["player"] = {
                "name": player_data["player_name"],
                "background": player_data["player_background"]
            }
            self.game_state["inventory"] = player_data["starting_items"]
            self.game_state["current_location"] = player_data["starting_location"]
            self.game_state["location_description"] = player_data["location_description"]
        else:
            game_utils.slow_print("Error creating player. Using default player.")
            self._create_default_player()
    
    def _create_default_player(self):
        """Fallback player creation if LLM fails"""
        self.game_state["player"] = {
            "name": "Adventurer",
            "background": "A brave explorer seeking fortune and glory"
        }
        self.game_state["inventory"] = ["torch", "rope", "dagger"]
        self.game_state["current_location"] = "Temple Entrance"
        self.game_state["location_description"] = "A massive stone doorway covered in ancient runes. The air feels heavy with magic."
    
    def get_player_choices(self) -> List[str]:
        """Generate 4 possible actions for the player based on current game state"""
        game_state_str = json.dumps(self.game_state)
        prompt = f"""
        Based on the current game state: {game_state_str}
        
        Generate exactly 4 possible actions the player can take right now.
        These should be logical given the current location, inventory, and story context.
        
        Format your response with a single field "choices" containing an array of 4 strings.
        Each string should be a brief action description (5-10 words).
        """
        
        choices_data = llm.generate_json(prompt)
        if choices_data and "choices" in choices_data and len(choices_data["choices"]) == 4:
            return choices_data["choices"]
        else:
            game_utils.slow_print("Error generating choices. Using default choices.")
            return [
                "Explore deeper into the dungeon",
                "Search the current area",
                "Check your inventory",
                "Rest and recover"
            ]
    
    def process_player_action(self, action: str):
        """Process the player's chosen action and update game state"""
        game_utils.slow_print(f"You decide to {action.lower()}...", delay=0.05)
        
        game_state_str = json.dumps(self.game_state)
        prompt = f"""
        Based on the current game state: {game_state_str}
        
        The player has chosen to: "{action}"
        
        Please continue the game by:
        1. Describing what happens as a result of this action
        2. Updating the game state
        3. Determining if any new items were found or lost
        4. Determining if any characters were encountered
        5. Updating the current location if the player moved
        
        Format your response with these fields:
        - action_result: A paragraph describing what happens
        - new_location (optional): If the player moved to a new location
        - location_description (optional): Description of the new location
        - items_gained (optional): List of items the player gained
        - items_lost (optional): List of items the player lost
        - character_encountered (optional): Name of any character encountered
        - character_interaction (optional): Description of the interaction
        """
        
        action_result = llm.generate_json(prompt)
        if action_result and "action_result" in action_result:
            # Update game history
            self.game_state["history"].append({
                "action": action,
                "result": action_result["action_result"]
            })
            
            # Update location if player moved
            if "new_location" in action_result and action_result["new_location"]:
                self.game_state["current_location"] = action_result["new_location"]
                self.game_state["location_description"] = action_result.get("location_description", "")
            
            # Update inventory
            if "items_gained" in action_result and action_result["items_gained"]:
                gained_items = action_result["items_gained"]
                self.game_state["inventory"].extend(gained_items)
                if gained_items:
                    game_utils.slow_print(f"You gained: {game_utils.format_list(gained_items)}")
            
            if "items_lost" in action_result and action_result["items_lost"]:
                lost_items = action_result["items_lost"]
                for item in lost_items:
                    if item in self.game_state["inventory"]:
                        self.game_state["inventory"].remove(item)
                if lost_items:
                    game_utils.slow_print(f"You lost: {game_utils.format_list(lost_items)}")
            
            # Update characters met
            if "character_encountered" in action_result and action_result["character_encountered"]:
                character = action_result["character_encountered"]
                if character not in self.game_state["characters_met"]:
                    self.game_state["characters_met"].append(character)
                    game_utils.slow_print(f"You met: {character}")
            
            # Display result to player
            game_utils.slow_print("\n" + action_result["action_result"] + "\n", delay=0.02)
            
        else:
            game_utils.slow_print("\nYou tried that, but nothing significant happened.\n")
            self.game_state["history"].append({
                "action": action,
                "result": "Nothing significant happened."
            })
    
    def display_game_status(self):
        """Display current game status to the player"""
        print(f"\n--- {self.game_state['current_location']} ---")
        game_utils.slow_print(self.game_state.get("location_description", ""), delay=0.02)
        print("\nInventory:", game_utils.format_list(self.game_state["inventory"]))
    
    def save_current_game(self):
        """Save the current game state"""
        if game_utils.save_game(self.game_state):
            game_utils.slow_print("Game saved successfully!")
        else:
            game_utils.slow_print("Failed to save game.")
    
    def load_saved_game(self):
        """Load a saved game state"""
        loaded_state = game_utils.load_game()
        if loaded_state:
            self.game_state = loaded_state
            game_utils.slow_print("Game loaded successfully!")
            return True
        else:
            game_utils.slow_print("No saved game found or error loading game.")
            return False
        
    def run_game(self):
        """Main game loop"""
        game_utils.clear_screen()
        print(game_utils.get_game_banner())
        game_utils.slow_print("\nWelcome to Dungeon Explorer!\n", delay=0.05)
        
        # Ask to load saved game
        if os.path.exists("savegame.json"):
            load_choice = input("Would you like to load a saved game? (y/n): ").lower()
            if load_choice.startswith('y'):
                if self.load_saved_game():
                    player = self.game_state["player"]
                    game_utils.slow_print(f"\nWelcome back, {player['name']}!")
                    game_utils.slow_print("Your adventure continues...\n")
                else:
                    self._start_new_game()
            else:
                self._start_new_game()
        else:
            self._start_new_game()
        
        # Game loop
        while True:
            self.display_game_status()
            
            # Get player choices
            choices = self.get_player_choices()
            print("\nWhat would you like to do?")
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")
            print("5. Save game")
            print("0. Quit game")
            
            # Get player input
            try:
                choice_num = int(input("\nEnter your choice (0-5): "))
                if choice_num == 0:
                    game_utils.slow_print("\nThanks for playing!")
                    break
                elif choice_num == 5:
                    self.save_current_game()
                elif 1 <= choice_num <= len(choices):
                    self.process_player_action(choices[choice_num-1])
                else:
                    game_utils.slow_print("Invalid choice. Please try again.")
            except ValueError:
                game_utils.slow_print("Please enter a number.")
    
    def _start_new_game(self):
        """Start a new game"""
        game_utils.slow_print("Starting a new adventure...\n")
        self.initialize_game()
        self.create_player()
        
        # Introduction
        player = self.game_state["player"]
        game_utils.slow_print(f"\nWelcome, {player['name']}!")
        game_utils.slow_print(f"Background: {player['background']}")
        game_utils.slow_print("\nYour adventure begins...\n")

if __name__ == "__main__":
    game = Game()
    game.run_game()
