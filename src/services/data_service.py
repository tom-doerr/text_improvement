import json
import os
from typing import List, Dict, Any
from ..models.example import Example

class DataService:
    def __init__(self, data_file: str = 'data.json'):
        self.data_file = data_file

    def load_data(self) -> Dict[str, Any]:
        print(f"\nDEBUG: Checking if {self.data_file} exists")
        if not os.path.exists(self.data_file):
            print("DEBUG: File doesn't exist, creating initial data")
            initial_data = {
                'instruction': '',
                'few_shot_examples': []
            }
            self.save_data(initial_data)
            return initial_data
            
        try:
            print("DEBUG: Loading existing data file")
            with open(self.data_file) as f:
                data = json.load(f)
                print(f"DEBUG: Loaded data: {json.dumps(data, indent=2)}")
                if 'few_shot_examples' not in data:
                    print("DEBUG: No few_shot_examples found, initializing empty list")
                    data['few_shot_examples'] = []
                print(f"DEBUG: Number of examples: {len(data['few_shot_examples'])}")
                return data
        except json.JSONDecodeError as e:
            print(f"DEBUG: JSON decode error: {e}")
            initial_data = {
                'instruction': '',
                'few_shot_examples': []
            }
            self.save_data(initial_data)
            return initial_data

    def save_data(self, data: Dict[str, Any]) -> None:
        print("\nDEBUG: Saving data")
        print(f"DEBUG: Saving data: {json.dumps(data, indent=2)}")
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except (IOError, PermissionError) as e:
            print(f"ERROR: Failed to save data: {e}")
            raise RuntimeError(f"Failed to save data: {e}")

    def get_examples(self) -> List[Example]:
        data = self.load_data()
        return [Example.from_dict(ex) for ex in data['few_shot_examples']]

    def add_example(self, example: Example) -> None:
        data = self.load_data()
        examples = data['few_shot_examples']
        examples.append(example.to_dict())
        self.save_data(data)

    def remove_example(self, index: int) -> None:
        data = self.load_data()
        if 0 <= index < len(data['few_shot_examples']):
            data['few_shot_examples'].pop(index)
            self.save_data(data)

    def update_example(self, index: int, example: Example) -> None:
        data = self.load_data()
        if 0 <= index < len(data['few_shot_examples']):
            data['few_shot_examples'][index] = example.to_dict()
            self.save_data(data)

    def get_instruction(self) -> str:
        data = self.load_data()
        return data.get('instruction', '')

    def set_instruction(self, instruction: str) -> None:
        data = self.load_data()
        data['instruction'] = instruction
        self.save_data(data)
