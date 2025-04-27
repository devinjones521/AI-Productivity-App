from fastapi import HTTPException
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_user_log(log_text):
    """
    Takes a daily habit log and returns a summarized feedback.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a productivity coach. Summarize the user's day, highlight successes, and gently suggest one area of improvement."},
                {"role": "user", "content": log_text}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        # 🔥 Raise clean API exception
        raise HTTPException(status_code=500, detail=f"OpenAI summarization failed: {str(e)}")
