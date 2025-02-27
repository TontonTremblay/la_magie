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
llm = llmlite.LLM(model="gpt-4o", api_key=OPENAI_API_KEY)

class Game:
    def __init__(self):
        self.game_state = {
            "story_context": {},
            "player": {},
            "current_location": "",
            "inventory": [],
            "characters_met": [],
            "current_goal": "",
            "completed_goals": [],
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
        5. failure_cases: At least 5 ways the player might fail
        6. main_goal: A clear, specific main goal for the player to accomplish
        7. initial_goal: The first immediate goal the player should focus on to start their journey
        """
        
        story_context = llm.generate_json(prompt)
        if story_context:
            self.game_state["story_context"] = story_context
            # Set the initial goal for the player
            if "initial_goal" in story_context:
                self.game_state["current_goal"] = story_context["initial_goal"]
            else:
                self.game_state["current_goal"] = "Explore the area and discover your purpose"
            game_utils.slow_print("Game context generated successfully!")
        else:
            game_utils.slow_print("Error generating game context. Using default game context.")
            self.game_state["story_context"] = self._get_default_game_context()
            self.game_state["current_goal"] = "Find the source of the monsters and deal with the artifact"
    
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
            ],
            "main_goal": "Find and deal with the cursed artifact to stop the monster invasion",
            "initial_goal": "Explore the temple entrance and find clues about the artifact's location"
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
        
        IMPORTANT: At least 2 of these actions should help the player progress toward their current goal: "{self.game_state.get('current_goal', '')}"
        
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
        6. Evaluating if the current goal has been completed
        7. Providing a new goal if the current one is completed
        
        Format your response with these fields:
        - action_result: A paragraph describing what happens
        - new_location (optional): If the player moved to a new location
        - location_description (optional): Description of the new location
        - items_gained (optional): List of items the player gained
        - items_lost (optional): List of items the player lost
        - character_encountered (optional): Name of any character encountered
        - character_interaction (optional): Description of the interaction
        - goal_completed (optional): Set to true if the current goal was completed
        - new_goal (optional): A new goal for the player if the current one was completed
        
        if a character appears, please make sure it was caused by an action. 
        Make sure all action makes the narrative move forward, make sure there are not circular interactions. 
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
            
            # Update goal if completed
            if "goal_completed" in action_result and action_result["goal_completed"]:
                completed_goal = self.game_state["current_goal"]
                if completed_goal and completed_goal not in self.game_state["completed_goals"]:
                    self.game_state["completed_goals"].append(completed_goal)
                    game_utils.slow_print(f"\n✅ Goal completed: {completed_goal}")
                
                if "new_goal" in action_result and action_result["new_goal"]:
                    self.game_state["current_goal"] = action_result["new_goal"]
                    game_utils.slow_print(f"\n📋 New goal: {action_result['new_goal']}")
            
            # Display and narrate result to player
            result_text = action_result["action_result"]
            game_utils.slow_print("\n" + result_text + "\n", delay=0.02)
            game_utils.narrate(result_text, llm)
            
        else:
            game_utils.slow_print("\nYou tried that, but nothing significant happened.\n")
            self.game_state["history"].append({
                "action": action,
                "result": "Nothing significant happened."
            })
    
    def display_game_status(self):
        """Display current game status to the player"""
        # Get game title
        if "custom_title" in self.game_state:
            title1 = self.game_state["custom_title"]["title1"]
            title2 = self.game_state["custom_title"]["title2"]
            game_title = f"{title1} {title2}".strip()
        else:
            game_title = "DUNGEON EXPLORER"
            
        print(f"\n--- {game_title}: {self.game_state['current_location']} ---")
        location_desc = self.game_state.get("location_description", "")
        game_utils.slow_print(location_desc, delay=0.02)
        game_utils.narrate(location_desc, llm)
        
        # Display current goal
        current_goal = self.game_state.get("current_goal", "")
        if current_goal:
            print("\n📋 Current Goal:", current_goal)
        
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
    
    def toggle_narration(self):
        """Toggle narration on/off"""
        is_enabled = game_utils.toggle_narration()
        if is_enabled:
            game_utils.slow_print("Narration enabled.")
        else:
            game_utils.slow_print("Narration disabled.")
    
    def change_narration_voice(self):
        """Change the narration voice"""
        voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
        print("\nAvailable voices:")
        for i, voice in enumerate(voices, 1):
            print(f"{i}. {voice}")
        
        try:
            choice = int(input("\nSelect a voice (1-6): "))
            if 1 <= choice <= len(voices):
                voice = voices[choice-1]
                if game_utils.set_narration_voice(voice):
                    game_utils.slow_print(f"Voice changed to {voice}.")
                    # Provide a sample of the new voice
                    sample_text = f"This is the {voice} voice. How does it sound?"
                    game_utils.narrate(sample_text, llm)
                else:
                    game_utils.slow_print("Failed to change voice.")
            else:
                game_utils.slow_print("Invalid choice.")
        except ValueError:
            game_utils.slow_print("Please enter a number.")
        
    def view_goal_history(self):
        """Display the player's goal history"""
        print("\n--- Goal History ---")
        
        # Show main goal from story context
        story_context = self.game_state["story_context"]
        if "main_goal" in story_context:
            print(f"\nUltimate Mission: {story_context['main_goal']}")
        
        # Show completed goals
        completed_goals = self.game_state.get("completed_goals", [])
        if completed_goals:
            print("\nCompleted Goals:")
            for i, goal in enumerate(completed_goals, 1):
                print(f"{i}. ✅ {goal}")
        else:
            print("\nNo goals completed yet.")
        
        # Show current goal
        current_goal = self.game_state.get("current_goal", "")
        if current_goal:
            print(f"\nCurrent Objective: 📋 {current_goal}")
        
        input("\nPress Enter to continue...")
    
    def customize_game_title(self):
        """Allow the player to customize the game title"""
        print("\n--- Customize Game Title ---")
        
        # Show current title
        if "custom_title" in self.game_state:
            current_title1 = self.game_state["custom_title"]["title1"]
            current_title2 = self.game_state["custom_title"]["title2"]
            current_title = f"{current_title1} {current_title2}".strip()
        else:
            current_title = "DUNGEON EXPLORER"
        
        print(f"Current title: {current_title}")
        print("\nOptions:")
        print("1. Enter new title")
        print("2. Reset to default (DUNGEON EXPLORER)")
        print("0. Cancel")
        
        try:
            option = int(input("\nSelect option (0-2): "))
            
            if option == 0:
                game_utils.slow_print("Title customization cancelled.")
                return
            elif option == 2:
                # Reset to default
                self.game_state["custom_title"] = {
                    "title1": "DUNGEON",
                    "title2": "EXPLORER"
                }
                game_utils.slow_print("Title reset to default: DUNGEON EXPLORER")
                
                # Show preview
                print("\nTitle Preview:")
                print(game_utils.get_fancy_game_banner("DUNGEON", "EXPLORER"))
                
                input("\nPress Enter to continue...")
                return
            elif option != 1:
                game_utils.slow_print("Invalid option. Title customization cancelled.")
                return
        except ValueError:
            game_utils.slow_print("Invalid input. Title customization cancelled.")
            return
        
        # Option 1: Enter new title
        print("\nEnter new title (two words recommended, leave blank to cancel):")
        new_title = input("> ").strip()
        if not new_title:
            game_utils.slow_print("Title customization cancelled.")
            return
        
        # Split the title into two parts if possible
        title_parts = new_title.split(maxsplit=1)
        if len(title_parts) == 1:
            title1 = title_parts[0]
            title2 = ""
        else:
            title1, title2 = title_parts
        
        # Show preview
        print("\nTitle Preview:")
        print(game_utils.get_fancy_game_banner(title1, title2))
        
        # Ask for confirmation
        confirm = input("Use this title? (y/n): ").lower()
        if confirm.startswith('y'):
            # Store the custom title in game state
            self.game_state["custom_title"] = {
                "title1": title1,
                "title2": title2
            }
            game_utils.slow_print("Game title updated!")
        else:
            game_utils.slow_print("Title customization cancelled.")
        
        input("\nPress Enter to continue...")
    
    def run_game(self):
        """Main game loop"""
        game_utils.clear_screen()
        
        # Use the fancy banner with custom title if available
        if "custom_title" in self.game_state:
            title1 = self.game_state["custom_title"]["title1"]
            title2 = self.game_state["custom_title"]["title2"]
            print(game_utils.get_fancy_game_banner(title1, title2))
            game_title = f"{title1} {title2}".strip()
        else:
            # Use default title
            print(game_utils.get_fancy_game_banner())
            game_title = "Dungeon Explorer"
        
        game_utils.slow_print(f"\nWelcome to {game_title}!\n", delay=0.05)
        
        # Ask to load saved game
        if os.path.exists("savegame.json"):
            load_choice = input("Would you like to load a saved game? (y/n): ").lower()
            if load_choice.startswith('y'):
                if self.load_saved_game():
                    player = self.game_state["player"]
                    welcome_back = f"\nWelcome back, {player['name']}!"
                    game_utils.slow_print(welcome_back)
                    game_utils.narrate(welcome_back, llm)
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
            print("6. Toggle narration")
            print("7. Change narration voice")
            print("8. View goal history")
            print("9. Customize game title")
            print("0. Quit game")
            
            # Get player input
            try:
                choice_num = int(input("\nEnter your choice (0-9): "))
                if choice_num == 0:
                    game_utils.slow_print("\nThanks for playing!")
                    break
                elif choice_num == 5:
                    self.save_current_game()
                elif choice_num == 6:
                    self.toggle_narration()
                elif choice_num == 7:
                    self.change_narration_voice()
                elif choice_num == 8:
                    self.view_goal_history()
                elif choice_num == 9:
                    self.customize_game_title()
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
        
        # Ensure default title is set if not customized
        if "custom_title" not in self.game_state:
            self.game_state["custom_title"] = {
                "title1": "DUNGEON",
                "title2": "EXPLORER"
            }
        
        # Introduction
        player = self.game_state["player"]
        welcome_text = f"\nWelcome, {player['name']}!"
        background_text = f"Background: {player['background']}"
        adventure_text = "\nYour adventure begins...\n"
        
        game_utils.slow_print(welcome_text)
        game_utils.narrate(welcome_text, llm)
        
        game_utils.slow_print(background_text)
        game_utils.narrate(background_text, llm)
        
        # Introduce the main goal and initial goal
        story_context = self.game_state["story_context"]
        if "main_goal" in story_context:
            main_goal_text = f"\nYour ultimate mission: {story_context['main_goal']}"
            game_utils.slow_print(main_goal_text)
            game_utils.narrate(main_goal_text, llm)
        
        if "current_goal" in self.game_state and self.game_state["current_goal"]:
            initial_goal_text = f"\nYour current objective: {self.game_state['current_goal']}"
            game_utils.slow_print(initial_goal_text)
            game_utils.narrate(initial_goal_text, llm)
        
        game_utils.slow_print(adventure_text)
        game_utils.narrate("Your adventure begins...", llm)

if __name__ == "__main__":
    game = Game()
    game.run_game()
