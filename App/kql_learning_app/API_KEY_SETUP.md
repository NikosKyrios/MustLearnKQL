# Quick Setup - Getting Your Grok API Key

## Step 1: Get Your Grok API Key

1. Visit https://x.ai
2. Sign up or log in
3. Navigate to API settings
4. Generate a new API key
5. Copy the key (starts with `xai-`)

## Step 2: Configure the App

1. In the app folder, copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` in a text editor

3. Find the **Grok xAI API Configuration** section:
   ```env
   # Grok xAI API Configuration
   XAI_API_KEY=your_grok_api_key_here
   ```

4. Replace `your_grok_api_key_here` with your actual key:
   ```env
   # Grok xAI API Configuration
   XAI_API_KEY=xai-your-actual-key-here
   ```

5. Save the file

## Step 3: Run the App

```bash
# Install dependencies (first time only)
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Or use the convenience scripts:
- **Windows:** Double-click `start.bat`
- **Mac/Linux:** Run `./start.sh`

## ✅ Verify It's Working

1. App starts without errors
2. Navigate to "AI Tutor" page
3. Try asking a question
4. If you get a response, the API is configured correctly!

**Note:** The app uses the `grok-3` model (latest as of January 2026). If you see errors about model availability, the model name may have changed. Check https://x.ai for current model names.

## 🔧 Troubleshooting

**Error: "AI Error: API key not found"**
- Check that `.env` file exists (not `.env.example`)
- Verify the key is on the line with `XAI_API_KEY=`
- Make sure there are no spaces around the `=`
- Key should look like: `xai-xxxxxxxxxxxxx`

**Error: "Invalid API key"**
- Key might be incorrect or expired
- Generate a new key at https://x.ai
- Copy and paste carefully (no extra spaces)

**AI features not working**
- Check you have internet connection
- Verify API key is valid
- Try restarting the app

## 💡 Demo Mode

The app works without a Grok API key! You can:
- ✅ Use the Query Lab
- ✅ Complete learning modules
- ✅ Take quizzes
- ✅ Track progress

But these features require the API key:
- ❌ AI Tutor chat
- ❌ Query generation
- ❌ Concept explainer
- ❌ Error explanations

---

**Need more help?** Check SETUP.md or README.md for detailed instructions.
