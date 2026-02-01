import os
# import subprocess
# import sys
# from pathlib import Path
from llama_cpp import Llama

def create_dcc_assistant(model_path, dcc_type, device='cpu'):
    llm = Llama(
        model_path=model_path,
        n_ctx=4096,
        n_threads=os.cpu_count(),
        chat_format="llama-2",
        device=device
    )
    
    system_prompt = f"""You are a helpful assistant specialized in {dcc_type} with expertise in:
    - {dcc_type} design and implementation
    - {dcc_type} 3d topology
    - {dcc_type} testing and debugging
    - {dcc_type} performance optimization
    - {dcc_type} animation and rendering
    - {dcc_type} user interface and user experience
    - {dcc_type} shaders and pipelines
    - {dcc_type} lights and materials
    
    Provide clear and concise answers to user queries related to {dcc_type}, including:
    - What the {dcc_type} does
    - How the {dcc_type} is implemented
    - Why the {dcc_type} is important
    - How the {dcc_type} can be optimized for better performance
    - Best practices for using the {dcc_type} effectively
    """
    
    print(f"\nDCC {dcc_type} Chat Interface")
    print("Type 'exit' to quit.\n")
    print("-" * 40)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    while True:
        user_input = input("\nYou: ")
        
        if user_input.lower() == 'exit':
            print("Exiting chat.")
            break
        
        if user_input.lower() == 'reset':
            messages = [{"role": "system", "content": system_prompt}]
            print("Chat history reset.")
            continue
        
        messages.append({"role": "user", "content": user_input})
        
        response = llm.create_chat_completion(messages)
        assistant_message = response['choices'][0]['message']['content']        
        messages.append({"role": "assistant", "content": assistant_message})
        
        if len(messages) > 20:
            messages = [messages[0]] + messages[-18:]
        
        print(f"Llama: {assistant_message}\n")
        print("-" * 40)
