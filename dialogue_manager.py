import json
import time
from typing import TYPE_CHECKING

class DialogueOption:
    def __init__(self, text, next_node_id):
        self.text = text
        self.next_node_id = next_node_id

class DialogueNode:
    def __init__(self, node_id, speaker, text, options):
        self.node_id = node_id
        self.speaker = speaker
        self.text = text
        self.options = options  # List of DialogueOption objects

class DialogueManager:
    def __init__(self, filepath="dialogue_data.json"):
        self.filepath = filepath
        self.dialogue_map = None

    def _load_character_data(self, character_name):
        # Private helper to load and parse JSON nodes into objects.
        dialogue_map = {}
        try:
            with open(self.filepath, "r") as file:
                all_data = json.load(file)

            # FIX: Loop through the list to find the matching character dictionary
            char_data = None
            for item in all_data:
                if character_name in item:
                    char_data = item[character_name]
                    break # Found the character, exit the loop
            
            if not char_data:
                return None
                
            for node_id, node_content in char_data.items():
                parsed_options = []
                for opt in node_content.get("options", []):
                    parsed_options.append(DialogueOption(opt["text"], opt["next_node_id"]))
                    
                dialogue_map[node_id] = DialogueNode(
                    node_id=node_id,
                    speaker=node_content["speaker"],
                    text=node_content["text"],
                    options=parsed_options
                )
            return dialogue_map
        except FileNotFoundError:
            print(f"Error: Could not find {self.filepath}")
            return None

    def start_conversation(self, character_name):
        # Loads the character graph and assigns it to the instance map

        # Stores the loaded data directly onto the class instance variable
        self.dialogue_map = self._load_character_data(character_name)