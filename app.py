import streamlit as st
from simpledspy import pipe
import json
import os
import dspy
from dspy.teleprompt import BootstrapFewShot

st.set_page_config(layout="wide", page_title="Text Improvement Assistant")

DATA_FILE = 'data.json'

# Initialize LM
dspy.settings.configure(lm=dspy.LM('openrouter/deepseek/deepseek-chat', temperature=1.5, cache=False))

def load_data():
    print(f"\nDEBUG: Checking if {DATA_FILE} exists")
    if not os.path.exists(DATA_FILE):
        print("DEBUG: File doesn't exist, creating initial data")
        initial_data = {
            'instruction': '',
            'few_shot_examples': []
        }
        save_data(initial_data)
        return initial_data
        
    try:
        print("DEBUG: Loading existing data file")
        with open(DATA_FILE) as f:
            data = json.load(f)
            print(f"DEBUG: Loaded data: {json.dumps(data, indent=2)}")
            if 'few_shot_examples' not in data:
                print("DEBUG: No few_shot_examples found, initializing empty list")
                data['few_shot_examples'] = []
            print(f"DEBUG: Number of examples: {len(data['few_shot_examples'])}")
            return data
    except json.JSONDecodeError as e:
        print(f"DEBUG: JSON decode error: {e}")
        st.error("Error reading data file. Creating new one.")
        initial_data = {
            'instruction': '',
            'few_shot_examples': []
        }
        save_data(initial_data)
        return initial_data

def save_data(data):
    print("\nDEBUG: Saving data")
    # Load existing data first
    existing_data = {}
    if os.path.exists(DATA_FILE):
        try:
            print("DEBUG: Loading existing data before save")
            with open(DATA_FILE) as f:
                existing_data = json.load(f)
                print(f"DEBUG: Existing data: {json.dumps(existing_data, indent=2)}")
        except json.JSONDecodeError as e:
            print(f"DEBUG: Error loading existing data: {e}")
    
    # Update with new data while preserving existing examples
    existing_examples = existing_data.get('few_shot_examples', [])
    new_examples = data.get('few_shot_examples', [])
    print(f"DEBUG: Existing examples: {len(existing_examples)}")
    print(f"DEBUG: New examples: {len(new_examples)}")
    
    data_to_save = {
        'instruction': data.get('instruction', existing_data.get('instruction', '')),
        'few_shot_examples': existing_examples + new_examples
    }
    
    print(f"DEBUG: Saving final data: {json.dumps(data_to_save, indent=2)}")
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
        
        tab1, tab2 = st.tabs(["View Examples", "Manage Examples"])
        
        with tab1:
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
        
        with tab2:
            st.header("Edit Examples")
            if examples:
                to_delete = []
                for i, example in enumerate(examples):
                    with st.expander(f"Edit Example {i+1}", expanded=False):
                        modified = False
                        new_input = st.text_area("Input", value=example['input_text'], key=f"edit_input_{i}", height=100)
                        new_reasoning = st.text_area("Reasoning", value=example['reasoning'], key=f"edit_reasoning_{i}", height=100)
                        new_issues = st.text_area("Issues", value=example['issues'], key=f"edit_issues_{i}", height=100)
                        new_improved = st.text_area("Improved", value=example['improved_text'], key=f"edit_improved_{i}", height=100)
                        
                        if (new_input != example['input_text'] or 
                            new_reasoning != example['reasoning'] or 
                            new_issues != example['issues'] or 
                            new_improved != example['improved_text']):
                            modified = True
                            examples[i] = {
                                'input_text': new_input,
                                'reasoning': new_reasoning,
                                'issues': new_issues,
                                'improved_text': new_improved
                            }
                        
                        if st.button("Delete Example", key=f"delete_{i}"):
                            to_delete.append(i)
                            st.warning("Example will be deleted after saving")
                
                if modified or to_delete:
                    if st.button("Save Changes"):
                        # Remove examples marked for deletion
                        for index in sorted(to_delete, reverse=True):
                            del examples[index]
                        
                        # Save updated examples
                        new_data = {
                            'instruction': data['instruction'],
                            'few_shot_examples': examples
                        }
                        save_data(new_data)
                        st.success("Changes saved!")
                        st.rerun()
            else:
                st.info("No examples to edit.")
    
    input_col, *completion_cols = st.columns([1] + [1] * num_completions)
    
    with input_col:
        input_text = st.text_area("Enter your text:", height=150, key="input")
    
    if input_text:
        placeholders = []
        for i in range(num_completions):
            with completion_cols[i]:
                st.markdown(f"### Completion {i+1}")
                placeholders.append(st.empty())
        
        for i in range(num_completions):
            reasoning, issues, improved_text = pipe(
                data['few_shot_examples'], 
                data['instruction'], 
                input_text
            )
            
            with placeholders[i].container():
                
                with st.spinner("Processing..."):
                    with st.expander("Reasoning", expanded=True):
                        st.write(reasoning)
                    
                    with st.expander("Issues", expanded=True):
                        st.write(issues)
                    
                    with st.expander("Improved Text", expanded=True):
                        st.text_area("Improved Text", value=improved_text, height=100, key=f"improved_{i}", label_visibility="collapsed")
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
                    st.rerun()  # Updated from experimental_rerun
                
                st.markdown("---")

if __name__ == '__main__':
    main()
