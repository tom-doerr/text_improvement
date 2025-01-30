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
        if data['few_shot_examples']:
            for i, example in enumerate(data['few_shot_examples'], 1):
                with st.expander(f"Example {i}"):
                    st.write("Input:", example['input_text'])
                    st.write("Reasoning:", example['reasoning'])
                    st.write("Issues:", example['issues'])
                    st.write("Improved:", example['improved_text'])
    
    input_text = st.text_area("Enter your text:", height=150, key="input")
    
    if input_text:
        st.subheader("Results")
        
        for i in range(num_completions):
            with st.container():
                reasoning, issues, improved_text = pipe(
                    data['few_shot_examples'], 
                    data['instruction'], 
                    input_text
                )
                
                with st.expander(f"Completion {i+1}", expanded=True):
                    st.write("Reasoning:", reasoning)
                    st.write("Issues:", issues)
                    st.write("Improved Text:", improved_text)
        
        data['last_run'] = {
            'input_text': input_text,
            'reasoning': reasoning,
            'issues': issues,
            'improved_text': improved_text
        }
        
        if st.button("Add to Examples"):
            if 'few_shot_examples' not in data:
                data['few_shot_examples'] = []
            data['few_shot_examples'].append(data['last_run'])
            save_data(data)
            st.success("Example added!")

if __name__ == '__main__':
    main()
