import streamlit as st
import pyperclip
from typing import List, Callable
from ..models.completion import CompletionResult
from ..models.example import Example
from ..services.completion_service import CompletionService
from ..services.data_service import DataService

class CompletionView:
    def __init__(self, completion_service: CompletionService, data_service: DataService):
        self.completion_service = completion_service
        self.data_service = data_service

    def render_completion_result(
        self,
        result: CompletionResult,
        input_text: str,
        placeholder: st.empty
    ) -> None:
        """Render a single completion result"""
        if not result.success:
            st.error(f"Error processing completion {result.index+1}: {result.reasoning}")
            return

        with placeholder.container():
            with st.spinner("Processing..."):
                with st.expander("Reasoning", expanded=True):
                    st.write(result.reasoning)
                
                with st.expander("Issues", expanded=True):
                    st.write(result.issues)
                
                with st.expander("Improved Text", expanded=True):
                    st.text_area(
                        "Improved Text",
                        value=result.improved_text,
                        height=100,
                        key=f"improved_{result.index}",
                        label_visibility="collapsed"
                    )
                    
                    if st.button("Copy to Clipboard", key=f"copy_{result.index}"):
                        try:
                            pyperclip.copy(result.improved_text)
                            st.success("Copied to clipboard!")
                        except Exception as e:
                            st.error(f"Failed to copy: {str(e)}")
                    
                    if st.button(f"Add to Examples", key=f"add_{result.index}"):
                        example = Example(
                            input_text=input_text,
                            reasoning=result.reasoning,
                            issues=result.issues,
                            improved_text=result.improved_text
                        )
                        
                        # Check for duplicates
                        examples = self.data_service.get_examples()
                        is_duplicate = any(
                            ex.input_text == input_text and ex.improved_text == result.improved_text
                            for ex in examples
                        )
                        
                        if is_duplicate:
                            st.warning("This example already exists!")
                        else:
                            self.data_service.add_example(example)
                            st.success(f"Added completion {result.index+1} to examples!")
                            st.rerun()

    def render(self, num_completions: int = 3):
        """Render the completion generation interface"""
        input_col, *completion_cols = st.columns([1] + [1] * num_completions)
        
        with input_col:
            input_text = st.text_area("Enter your text:", height=150, key="input")
        
        if input_text:
            placeholders = []
            for i in range(num_completions):
                with completion_cols[i]:
                    st.markdown(f"### Completion {i+1}")
                    placeholders.append(st.empty())
            
            progress = st.progress(0)
            status = st.empty()
            
            results = self.completion_service.generate_completions(
                input_text,
                num_completions,
                progress_callback=lambda p: progress.progress(p)
            )
            
            progress.empty()
            status.empty()
            
            for result in results:
                self.render_completion_result(
                    result,
                    input_text,
                    placeholders[result.index]
                )
                st.markdown("---")
