"""
List available Gemini models for the configured API key
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config import settings
import google.generativeai as genai

print("Configuring Gemini...")
genai.configure(api_key=settings.GEMINI_API_KEY)

print("\nAvailable models:\n")
for model in genai.list_models():
    print(f"- {model.name}")
    if hasattr(model, 'supported_generation_methods'):
        print(f"  Supported methods: {model.supported_generation_methods}")
