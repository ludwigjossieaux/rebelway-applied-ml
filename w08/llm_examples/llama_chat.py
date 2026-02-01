import os
import subprocess
import sys
from pathlib import Path
from llama_cpp import Llama
from assistant import create_dcc_assistant

def chat_with_llama(model_path):
    llm = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=os.cpu_count(),
        chat_format="llama-2"
    )
    
    print("\nLlama Chat Interface")
    print("Type 'exit' to quit.\n")
    print("-" * 40)
    
    messages = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'exit':
            print("Exiting chat.")
            break
        
        messages.append({"role": "user", "content": user_input})
        
        response = llm.create_chat_completion(messages)
        assistant_message = response['choices'][0]['message']['content']        
        messages.append({"role": "assistant", "content": assistant_message})
        
        print(f"Llama: {assistant_message}\n")
        print("-" * 40)
        
if __name__ == "__main__":
    model_file = "llama-2-7b-chat.Q4_K_M.gguf"  # Update with your model file name
    model_path =  Path("/data2/models/gguf/") / model_file
    
    if not model_path.exists():
        print(f"Model file not found at {model_path}. Please ensure the model is downloaded and placed in the 'models' directory.")
        sys.exit(1)
    
    #chat_with_llama(str(model_path))
    create_dcc_assistant(str(model_path), str(sys.argv[1]), device='cuda')