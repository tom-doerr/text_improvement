import streamlit as st
from .completion_view import CompletionView
from .example_view import ExampleView
from ..services.completion_service import CompletionService
from ..services.data_service import DataService
from ..services.llm_service import LLMService

class MainView:
    def __init__(self):
        st.set_page_config(layout="wide", page_title="Text Improvement Assistant")
        
        # Initialize services
        self.data_service = DataService()
        self.llm_service = LLMService()
        self.completion_service = CompletionService(self.llm_service, self.data_service)
        
        # Initialize views
        self.completion_view = CompletionView(self.completion_service, self.data_service)
        self.example_view = ExampleView(self.data_service)

    def render_sidebar(self):
        """Render the sidebar with settings and examples"""
        with st.sidebar:
            st.header("Settings")
            
            # Instruction editor
            instruction = st.text_area(
                "Add instruction", 
                value=self.data_service.get_instruction()
            )
            if instruction != self.data_service.get_instruction():
                self.data_service.set_instruction(instruction)
            
            # Number of completions setting
            num_completions = st.number_input(
                "Number of completions",
                min_value=1,
                max_value=5,
                value=3
            )
            
            # Show examples in sidebar
            self.example_view.render_sidebar_examples(self.data_service.get_examples())
            
            return num_completions

    def render(self):
        """Render the main application interface"""
        num_completions = self.render_sidebar()
        
        # Main content tabs
        tab1, tab2 = st.tabs(["Generate", "Manage Examples"])
        
        with tab1:
            self.completion_view.render(num_completions)
            
        with tab2:
            self.example_view.render()
