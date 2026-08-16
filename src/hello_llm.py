import os, sys
from dotenv import load_dotenv
from openai import OpenAI

# Load OPENAI_API_KEY from the environment — never hard-code keys
load_dotenv()
client = OpenAI()

def ask(question):
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are concise."},
            {"role": "user",   "content": question},
        ],
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python hello_llm.py "your question here"')
        sys.exit(1)
    question = sys.argv[1]
    answer =  ask(question)    
    print(answer)