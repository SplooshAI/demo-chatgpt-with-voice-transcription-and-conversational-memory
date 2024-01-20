# Manages the interaction with the GPT model
from openai import OpenAI

def communicate_with_gpt(client, model, messages, temperature=0.75):
    response = client.chat.completions.create(model=model, temperature=temperature, messages=messages, stream=True)
    full_response_content = ""
    for chunk in response:
        choice = chunk.choices[0]
        if choice.delta and choice.delta.content:
            response_content = choice.delta.content
            full_response_content += response_content
    return full_response_content.strip()
