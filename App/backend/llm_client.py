from dotenv import load_dotenv
from groq import Groq
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
#MODEL_NAME = "llama-3.3-70b-versatile"
MODEL_NAME = "llama-3.3-70b-versatile"

