import streamlit as st
from simpledspy import pipe
import json
import os
import dspy
from dspy.teleprompt import BootstrapFewShot

st.set_page_config(layout="wide", page_title="Text Improvement Assistant")

DATA_FILE = 'data.json'

# Initialize LM
dspy.settings.configure(lm=dspy.LM('openrouter/deepseek/deepseek-chat'))

def load_data():
    if not os.path.exists(DATA_FILE):
        initial_data = {
            'instruction': '',
            'few_shot_examples': []
        }
        save_data(initial_data)
        return initial_data
        
    try:
        with open(DATA_FILE) as f:
            data = json.load(f)
            if 'few_shot_examples' not in data:
                data['few_shot_examples'] = []
            return data
    except json.JSONDecodeError:
        st.error("Error reading data file. Creating new one.")
        initial_data = {
            'instruction': '',
            'few_shot_examples': []
        }
        save_data(initial_data)
        return initial_data

def save_data(data):
    # Load existing data first
    existing_data = {}
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE) as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            pass
    
    # Update with new data while preserving existing examples
    data_to_save = {
        'instruction': data.get('instruction', existing_data.get('instruction', '')),
        'few_shot_examples': existing_data.get('few_shot_examples', []) + data.get('few_shot_examples', [])
    }
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data_to_save, f, indent=2)

def main():
    st.title("SimpleDSPY Interface")
    
    data = load_data()
    
    with st.sidebar:
        st.header("Settings")
        instruction = st.text_area("Add instruction", value=data['instruction'])
        if instruction != data['instruction']:
            data['instruction'] = instruction
            save_data(data)
            
        num_completions = st.number_input("Number of completions", min_value=1, max_value=5, value=3)
        
        st.header("Current Examples")
        examples = data.get('few_shot_examples', [])
        st.write(f"Number of examples: {len(examples)}")
        
        if examples:
            for i, example in enumerate(examples, 1):
                with st.expander(f"Example {i}", expanded=False):
                    st.text_area("Input", value=example['input_text'], disabled=True, height=100)
                    st.text_area("Reasoning", value=example['reasoning'], disabled=True, height=100)
                    st.text_area("Issues", value=example['issues'], disabled=True, height=100)
                    st.text_area("Improved", value=example['improved_text'], disabled=True, height=100)
        else:
            st.info("No examples yet. Add some completions to build up your examples!")
    
    input_col, *completion_cols = st.columns([1] + [1] * num_completions)
    
    with input_col:
        input_text = st.text_area("Enter your text:", height=150, key="input")
    
    if input_text:
        completions = []
        for i in range(num_completions):
            reasoning, issues, improved_text = pipe(
                data['few_shot_examples'], 
                data['instruction'], 
                input_text
            )
            completions.append((reasoning, issues, improved_text))
        
        for i, (reasoning, issues, improved_text) in enumerate(completions):
            with completion_cols[i]:
                st.markdown(f"### Completion {i+1}")
                
                with st.expander("Reasoning", expanded=True):
                    st.write(reasoning)
                
                with st.expander("Issues", expanded=True):
                    st.write(issues)
                
                with st.expander("Improved Text", expanded=True):
                    st.text_area("", value=improved_text, height=100, key=f"improved_{i}")
                    st.button("Copy", key=f"copy_{i}", help="Copy improved text to clipboard")
                
                if st.button(f"Add to Examples", key=f"add_{i}"):
                    example = {
                        'input_text': input_text,
                        'reasoning': reasoning,
                        'issues': issues,
                        'improved_text': improved_text
                    }
                    # Create new data dict with just this example
                    new_data = {
                        'instruction': data['instruction'],
                        'few_shot_examples': [example]
                    }
                    save_data(new_data)
                    st.success(f"Added completion {i+1} to examples!")
                    st.experimental_rerun()  # Refresh to show new example
                
                st.markdown("---")

if __name__ == '__main__':
    main()
