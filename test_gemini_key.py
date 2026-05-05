"""
Quick test to verify Gemini API key configuration
Run: python test_gemini_key.py
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config import settings
import google.generativeai as genai

print("=" * 60)
print("Gemini API Key Test")
print("=" * 60)

# Check if key is set
api_key = settings.GEMINI_API_KEY
print(f"\n1. API Key found: {bool(api_key)}")
print(f"   Key length: {len(api_key) if api_key else 0}")
print(f"   Key format: {'AIza...' if api_key and api_key.startswith('AIza') else 'INVALID FORMAT'}")

# Try to configure
print(f"\n2. Attempting to configure Gemini with model: {settings.GEMINI_MODEL}")
try:
    genai.configure(api_key=api_key)
    print("   ✓ Configuration successful")
except Exception as e:
    print(f"   ✗ Configuration failed: {type(e).__name__}: {e}")
    sys.exit(1)

# Try to create model
print(f"\n3. Creating GenerativeModel...")
try:
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    print("   ✓ Model created successfully")
except Exception as e:
    print(f"   ✗ Model creation failed: {type(e).__name__}: {e}")
    sys.exit(1)

# Try a simple test request
print(f"\n4. Testing with a simple request...")
try:
    response = model.generate_content("Say 'Hello' in one word.")
    print(f"   ✓ API call successful")
    print(f"   Response: {response.text[:50]}...")
except Exception as e:
    print(f"   ✗ API call failed: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ All tests passed! Gemini API is working correctly.")
print("=" * 60)
