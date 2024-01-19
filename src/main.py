# src/main.py
import os
from dotenv import load_dotenv
from pynput import keyboard
import wave
import sounddevice as sd
import time
from openai import OpenAI
import re

# Load .env file from the same directory as main.py
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Read OPENAI_API_KEY from environment
openai_api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_api_key)
