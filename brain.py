import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

# Fetch API key from .env
API = os.getenv("GEMINI_API_KEY")

# Read system instruction from file
file_path = "System_inst.txt"
with open(file_path, "r") as file:
    SYSTEM_INSTRUCTION = file.read()

def get_response(prompt):
    client = genai.Client(api_key=API)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.7,
            top_p=0.9
        ),
    )
    return response.text

# Test the function
print(get_response("The robot is moving forward and detects an obstacle in front of it. The left side is clear."))
