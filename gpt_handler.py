import os
import openai
# from config import OPENAI_API_KEY
from dotenv import load_dotenv

# openai.api_key = OPENAI_API_KEY
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ask_titan_gpt(prompt):
    try:
        client = openai.OpenAI(api_key=openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Or use "gpt-3.5-turbo", "gpt-4"
            messages=[
                {"role": "system", "content": "You are TITAN, an intelligent, helpful AI assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        return reply
    except Exception as e:
        return f"Error contacting TITAN->GPT: {str(e)}"
