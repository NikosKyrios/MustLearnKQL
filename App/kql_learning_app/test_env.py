"""
Diagnostic Script - Test Environment Configuration
Run this to verify your .env file is being loaded correctly
"""

import os
from dotenv import load_dotenv
from pathlib import Path

print("=" * 60)
print("Must Learn KQL Learning Hub - Environment Diagnostics")
print("=" * 60)
print()

# Get current directory
current_dir = Path(__file__).parent
print(f"📁 Current directory: {current_dir}")
print()

# Check if .env file exists
env_file = current_dir / ".env"
env_example = current_dir / ".env.example"

print("📄 File Check:")
print(f"  .env exists: {env_file.exists()}")
print(f"  .env.example exists: {env_example.exists()}")
print()

# Load .env file
print("🔄 Loading .env file...")
load_dotenv()
print("  ✓ Load attempted")
print()

# Check for API key
api_key = os.getenv('XAI_API_KEY', '')

print("🔑 API Key Status:")
if not api_key:
    print("  ❌ XAI_API_KEY not found!")
    print("  → Make sure you have a .env file with XAI_API_KEY=your-key")
elif api_key == 'your_grok_api_key_here':
    print("  ⚠️  XAI_API_KEY found but not configured!")
    print("  → Replace 'your_grok_api_key_here' with your actual API key")
else:
    print(f"  ✅ XAI_API_KEY found!")
    print(f"  → Key starts with: {api_key[:10]}...")
    print(f"  → Key ends with: ...{api_key[-8:]}")
    print(f"  → Key length: {len(api_key)} characters")
print()

# Test Grok API connection
print("🌐 Testing Grok API Connection:")
try:
    from openai import OpenAI
    
    if not api_key or api_key == 'your_grok_api_key_here':
        print("  ⏭️  Skipped (no valid API key)")
    else:
        print("  → Creating client...")
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        print("  ✓ Client created successfully")
        
        print("  → Testing API call...")
        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "user", "content": "Say 'API test successful' if you receive this."}
            ],
            max_tokens=20
        )
        
        result = response.choices[0].message.content
        print(f"  ✅ API Response: {result}")
        print()
        print("🎉 SUCCESS! Your API key is working correctly!")
        
except ImportError:
    print("  ❌ OpenAI library not installed!")
    print("  → Run: pip install openai")
except Exception as e:
    print(f"  ❌ API Error: {str(e)}")
    print()
    print("  Possible issues:")
    print("  1. API key is invalid or expired")
    print("  2. No internet connection")
    print("  3. Grok API service is down")
    print("  4. Rate limit exceeded")
    print()
    print("  → Get a new key from: https://x.ai")

print()
print("=" * 60)
print("Diagnostic complete!")
print()

# Show other environment variables
print("📋 Other Configuration:")
print(f"  APP_TITLE: {os.getenv('APP_TITLE', 'Not set')}")
print(f"  USE_DEMO_DATA: {os.getenv('USE_DEMO_DATA', 'Not set')}")
print(f"  APP_DEBUG: {os.getenv('APP_DEBUG', 'Not set')}")
print()

print("💡 Next Steps:")
if not api_key or api_key == 'your_grok_api_key_here':
    print("  1. Create/edit .env file in the app folder")
    print("  2. Add: XAI_API_KEY=xai-your-actual-key-here")
    print("  3. Save the file")
    print("  4. Run this script again to verify")
    print("  5. Then start the app: streamlit run app.py")
else:
    print("  ✓ Configuration looks good!")
    print("  → Run the app: streamlit run app.py")
print()
print("=" * 60)
