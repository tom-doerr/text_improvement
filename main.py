#!/usr/bin/env python3

from simpledspy import pipe
import json
import os

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        save_data({
            'instruction': '',
            'few_shot_examples': [],
        })
    with open(DATA_FILE) as f:
        data = json.load(f)
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def execute_instruction(data, input_text):
    if input_text.startswith('\\note'):
        note = input_text[6:]
        data['instruction'] += note 
        save_data(data)
        return 'Instruction saved.'

    if input_text == '\\add':
        if 'few_shot_examples' not in data:
            data['few_shot_examples'] = []
        data['few_shot_examples'].append(data['last_run'])
        save_data(data)
        return 'Example added.'

def main():
    data = load_data()
    while True:
        input_text = input('Enter your text: ')
        if input_text.startswith('\\'):
            result = execute_instruction(data, input_text)
            print(result)
            continue
            
        reasoning, issues, improved_text = pipe(
            data['few_shot_examples'], 
            data['instruction'], 
            input_text
        )
        print("Reasoning:", reasoning)
        print("Issues:", issues)
        print("Improved text:", improved_text)
        
        data['last_run'] = {
            'input_text': input_text,
            'reasoning': reasoning,
            'issues': issues,
            'improved_text': improved_text
        }

if __name__ == '__main__':
    main()
