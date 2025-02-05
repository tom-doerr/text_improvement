import streamlit as st
from typing import List, Set
from ..models.example import Example
from ..services.data_service import DataService

class ExampleView:
    def __init__(self, data_service: DataService):
        self.data_service = data_service
        if 'to_delete' not in st.session_state:
            st.session_state.to_delete = set()
        if 'modified' not in st.session_state:
            st.session_state.modified = False

    def render_sidebar_examples(self, examples: List[Example]):
        """Render examples in the sidebar"""
        st.header("Current Examples")
        st.write(f"Number of examples: {len(examples)}")
        
        if examples:
            for i, example in enumerate(examples, 1):
                with st.expander(f"Example {i}", expanded=False):
                    st.text_area("Input", value=example.input_text, disabled=True, height=100, key=f"view_input_{i}")
                    st.text_area("Reasoning", value=example.reasoning, disabled=True, height=100, key=f"view_reasoning_{i}")
                    st.text_area("Issues", value=example.issues, disabled=True, height=100, key=f"view_issues_{i}")
                    st.text_area("Improved", value=example.improved_text, disabled=True, height=100, key=f"view_improved_{i}")
        else:
            st.info("No examples yet. Add some completions to build up your examples!")

    def render_example_editor(self, example: Example, index: int) -> Example:
        """Render editor for a single example"""
        modified = False
        
        new_input = st.text_area("Input", value=example.input_text, key=f"edit_input_{index}", height=100)
        new_reasoning = st.text_area("Reasoning", value=example.reasoning, key=f"edit_reasoning_{index}", height=100)
        new_issues = st.text_area("Issues", value=example.issues, key=f"edit_issues_{index}", height=100)
        new_improved = st.text_area("Improved", value=example.improved_text, key=f"edit_improved_{index}", height=100)
        
        if (new_input != example.input_text or 
            new_reasoning != example.reasoning or 
            new_issues != example.issues or 
            new_improved != example.improved_text):
            modified = True
            example = Example(
                input_text=new_input,
                reasoning=new_reasoning,
                issues=new_issues,
                improved_text=new_improved
            )
        
        if st.button("Delete Example", key=f"delete_{index}"):
            st.session_state.to_delete.add(index)
            modified = True
            
        return example, modified

    def render(self):
        """Render the example management interface"""
        st.header("Edit Examples")
        examples = self.data_service.get_examples()
        
        if not examples:
            st.info("No examples to edit.")
            return
            
        modified = False
        for i, example in enumerate(examples):
            if i in st.session_state.to_delete:
                continue
                
            with st.expander(f"Edit Example {i+1}", expanded=False):
                new_example, was_modified = self.render_example_editor(example, i)
                if was_modified:
                    examples[i] = new_example
                    modified = True
        
        # Auto-save changes when modifications are detected
        if modified:
            # Remove examples marked for deletion
            examples = [ex for i, ex in enumerate(examples) 
                       if i not in st.session_state.to_delete]
            
            # Save updated examples
            self.data_service.save_data({
                'instruction': self.data_service.get_instruction(),
                'few_shot_examples': [ex.to_dict() for ex in examples]
            })
            st.session_state.to_delete = set()
            st.rerun()
