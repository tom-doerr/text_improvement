import concurrent.futures
from typing import List
import streamlit as st
from ..models.completion import CompletionResult
from ..models.example import Example
from .llm_service import LLMService
from .data_service import DataService

class CompletionService:
    def __init__(self, llm_service: LLMService, data_service: DataService):
        self.llm_service = llm_service
        self.data_service = data_service

    def generate_single_completion(self, input_text: str, index: int) -> CompletionResult:
        """Generate a single completion"""
        try:
            print(f"\nDEBUG: Starting completion {index+1}")
            
            examples = self.data_service.get_examples()
            instruction = self.data_service.get_instruction()
            
            print(f"DEBUG: Input length: {len(input_text)}")
            print(f"DEBUG: Number of examples: {len(examples)}")
            
            reasoning, issues, improved_text = self.llm_service.generate_completion(
                examples,
                instruction,
                input_text
            )
            
            print(f"DEBUG: Completion {index+1} successful")
            print(f"DEBUG: Reasoning length: {len(reasoning)}")
            print(f"DEBUG: Issues length: {len(issues)}")
            print(f"DEBUG: Improved text length: {len(improved_text)}")
            
            return CompletionResult.success(index, reasoning, issues, improved_text)
            
        except Exception as e:
            print(f"\nDEBUG: Error in completion {index+1}: {str(e)}")
            return CompletionResult.failure(index, f"Generation failed: {str(e)}")

    def generate_completions(
        self,
        input_text: str,
        num_completions: int,
        progress_callback=None
    ) -> List[CompletionResult]:
        """Generate multiple completions in parallel"""
        print("\nDEBUG: Starting parallel completion generation")
        print(f"DEBUG: Requesting {num_completions} completions")
        
        results = []
        completed = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_completions) as executor:
            futures = {
                executor.submit(self.generate_single_completion, input_text, i): i 
                for i in range(num_completions)
            }
            
            for future in concurrent.futures.as_completed(futures):
                i = futures[future]
                completed += 1
                if progress_callback:
                    progress_callback(completed / num_completions)
                
                try:
                    result = future.result(timeout=60)  # 60 second timeout
                    results.append(result)
                    print(f"DEBUG: Completion {i+1} finished processing")
                except concurrent.futures.TimeoutError:
                    print(f"\nDEBUG: Completion {i+1} timed out")
                    results.append(
                        CompletionResult.failure(i, "Generation timed out after 60 seconds")
                    )
                except Exception as e:
                    print(f"\nDEBUG: Error processing completion {i+1}: {str(e)}")
                    results.append(
                        CompletionResult.failure(i, f"Processing failed: {str(e)}")
                    )
        
        return sorted(results, key=lambda r: r.index)
