import os

def read_initial_prompt(base_path):
    gpt_prompt_path = os.path.join(base_path, 'data/prompts/gpt_prompt.txt')
    if os.path.exists(gpt_prompt_path):
        with open(gpt_prompt_path, 'r', errors="ignore") as file:
            return file.read().strip()
    return ""
