import os
from groq import Groq

def get_answer(question, api_key):
    client = Groq(
        api_key=api_key,
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful coding assistant. Provide only the code or the direct answer requested. If code is requested, output it in a format suitable for saving directly to a file (e.g., no markdown backticks if the user asks for a raw python file, or keep them if it's a text explanation). However, since the user is outputting to a file like answer.py, prefer raw code without markdown formatting if the output file extension suggests code."
            },
            {
                "role": "user",
                "content": question,
            }
        ],
        model="openai/gpt-oss-20b",
    )

    return chat_completion.choices[0].message.content
