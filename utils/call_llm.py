from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Learn more about calling the LLM: https://the-pocket.github.io/PocketFlow/utility_function/llm.html
def call_llm(prompt):    
    # Use AI_BUILDER_TOKEN for ai-builders.space platform
    api_key = os.getenv("AI_BUILDER_TOKEN")
    if not api_key:
        raise ValueError("AI_BUILDER_TOKEN not found. Please set it in your .env file.")
    
    client = OpenAI(
    api_key=os.getenv("AI_BUILDER_TOKEN"),
    base_url="https://space.ai-builders.com/backend/v1"
    )
    r = client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}]
    )
    return r.choices[0].message.content
    
if __name__ == "__main__":
    prompt = "What is the meaning of life?"
    print(call_llm(prompt))
