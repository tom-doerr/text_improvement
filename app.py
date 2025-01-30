import streamlit as st
from simpledspy import pipe
import json
import os
import dspy
from dspy.teleprompt import BootstrapFewShot
from copy import deepcopy
import pyperclip

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
    
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
        st.session_state.modified = False
        st.session_state.to_delete = set()
    
    data = st.session_state.data
    
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
                    st.text_area("Input", value=example['input_text'], disabled=True, height=100, key=f"view_input_{i}")
                    st.text_area("Reasoning", value=example['reasoning'], disabled=True, height=100, key=f"view_reasoning_{i}")
                    st.text_area("Issues", value=example['issues'], disabled=True, height=100, key=f"view_issues_{i}")
                    st.text_area("Improved", value=example['improved_text'], disabled=True, height=100, key=f"view_improved_{i}")
        else:
            st.info("No examples yet. Add some completions to build up your examples!")
    
    tab1, tab2 = st.tabs(["Generate", "Manage Examples"])
    
    with tab1:
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
                try:
                    result = pipe(
                        data['few_shot_examples'], 
                        data['instruction'], 
                        input_text
                    )
                    
                    # Handle different return types
                    if isinstance(result, tuple):
                        reasoning, issues, improved_text = result
                    elif isinstance(result, dict):
                        reasoning = result.get('reasoning', '')
                        issues = result.get('issues', '')
                        improved_text = result.get('improved_text', reasoning)
                    else:
                        # Handle string or other return types
                        reasoning = str(result)
                        issues = ''
                        improved_text = str(result)
                    
                    with placeholders[i].container():
                        with st.spinner("Processing..."):
                            with st.expander("Reasoning", expanded=True):
                                st.write(reasoning)
                        
                            with st.expander("Issues", expanded=True):
                                st.write(issues)
                        
                            with st.expander("Improved Text", expanded=True):
                                st.text_area("Improved Text", value=improved_text, height=100, key=f"improved_{i}", label_visibility="collapsed")
                                if st.button("Copy to Clipboard", key=f"copy_{i}"):
                                    try:
                                        pyperclip.copy(improved_text)
                                        st.success("Copied to clipboard!")
                                    except Exception as e:
                                        st.error(f"Failed to copy: {str(e)}")
                                
                                if st.button(f"Add to Fewshot", key=f"add_{i}"):
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
                except Exception as e:
                    st.error(f"Error processing completion {i+1}: {str(e)}")
    
    @st.fragment
    def edit_examples(examples, data):
        st.header("Edit Examples")
        if examples:
            for i, example in enumerate(examples):
                    if i in st.session_state.to_delete:
                        continue
                        
                    with st.expander(f"Edit Example {i+1}", expanded=False):
                        new_input = st.text_area("Input", value=example['input_text'], key=f"edit_input_{i}", height=100)
                        new_reasoning = st.text_area("Reasoning", value=example['reasoning'], key=f"edit_reasoning_{i}", height=100)
                        new_issues = st.text_area("Issues", value=example['issues'], key=f"edit_issues_{i}", height=100)
                        new_improved = st.text_area("Improved", value=example['improved_text'], key=f"edit_improved_{i}", height=100)
                        
                        if (new_input != example['input_text'] or 
                            new_reasoning != example['reasoning'] or 
                            new_issues != example['issues'] or 
                            new_improved != example['improved_text']):
                            examples[i] = {
                                'input_text': new_input,
                                'reasoning': new_reasoning,
                                'issues': new_issues,
                                'improved_text': new_improved
                            }
                            st.session_state.modified = True
                        
                        if st.button("Delete Example", key=f"delete_{i}"):
                            st.session_state.to_delete.add(i)
                            st.session_state.modified = True
            
            # Auto-save changes when modifications are detected
            if st.session_state.modified:
                # Remove examples marked for deletion
                examples = [ex for i, ex in enumerate(examples) if i not in st.session_state.to_delete]
                
                # Save updated examples
                new_data = {
                    'instruction': data['instruction'],
                    'few_shot_examples': examples
                }
                save_data(new_data)
                st.session_state.data = new_data
                st.session_state.modified = False
                st.session_state.to_delete = set()
        else:
            st.info("No examples to edit.")
    
    with tab2:
        edit_examples(examples, data)

if __name__ == '__main__':
    main()
