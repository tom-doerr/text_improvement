import streamlit as st
from simpledspy import pipe
import json
import os
import dspy
from dspy.teleprompt import BootstrapFewShot

DATA_FILE = 'data.json'

# Initialize LM
dspy.settings.configure(lm=dspy.LM('gpt-4-mini'))

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
        st.header("Instructions")
        instruction = st.text_area("Add instruction", value=data['instruction'])
        if instruction != data['instruction']:
            data['instruction'] = instruction
            save_data(data)
    
    input_text = st.text_area("Enter your text:", height=150)
    
    if st.button("Process"):
        if input_text:
            reasoning, issues, improved_text = pipe(
                data['few_shot_examples'], 
                data['instruction'], 
                input_text
            )
            
            st.subheader("Results")
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
