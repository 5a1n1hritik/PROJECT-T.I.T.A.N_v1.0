# t_core.py
import json
import os

MEMORY_FILE = "memory.json"

# Load or initialize memory
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as file:
        return json.load(file)

def save_memory(input_text: str, output_text: str):
    memory = load_memory()
    memory[input_text] = output_text
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=2)

def recall_memory(input_text: str):
    memory = load_memory()
    return memory.get(input_text, None)
