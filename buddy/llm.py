import os
from groq import Groq

DEFAULT_MODEL = "openai/gpt-oss-20b"
DEFAULT_SYSTEM_PROMPT = "You are a helpful coding assistant. Provide only the code or the direct answer requested. If code is requested, output it in a format suitable for saving directly to a file (e.g., no markdown backticks if the user asks for a raw python file, or keep them if it's a text explanation). However, since the user is outputting to a file like answer.py, prefer raw code without markdown formatting if the output file extension suggests code."

def get_answer(question, api_key, model=None, system_prompt=None):
    client = Groq(
        api_key=api_key,
    )

    if model is None:
        model = DEFAULT_MODEL
    
    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content
