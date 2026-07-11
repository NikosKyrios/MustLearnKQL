# Quick Start Guide

## Installation Steps

### 1. System Requirements
- Python 3.8 or higher
- 4GB RAM minimum
- Internet connection for AI features

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or use a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Grok API key:
```
XAI_API_KEY=your_actual_key_here
```

Get your Grok API key from: https://x.ai

### 4. Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser at http://localhost:8501

## First-Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed from requirements.txt
- [ ] .env file created with API key
- [ ] Application runs without errors
- [ ] Can navigate between pages
- [ ] AI features working (test in AI Tutor)
- [ ] Can execute sample queries in Query Lab

## Troubleshooting

### "Module not found" errors
```bash
pip install --upgrade -r requirements.txt
```

### API key not working
- Verify no extra spaces in .env file
- Key format: `XAI_API_KEY=xai-...` (no quotes)
- Check key is valid at x.ai

### Streamlit not found
```bash
pip install streamlit
```

### Port already in use
```bash
streamlit run app.py --server.port 8502
```

## Optional: Azure Kusto Setup

For connecting to real Azure Data Explorer clusters:

1. Install Azure CLI: https://docs.microsoft.com/cli/azure/install-azure-cli
2. Login: `az login`
3. Add credentials to .env:
```
KUSTO_CLUSTER=https://your-cluster.kusto.windows.net
KUSTO_DATABASE=YourDatabase
USE_DEMO_DATA=False
```

## Need Help?

1. Check the README.md for detailed documentation
2. Use the AI Tutor in the app
3. Visit the troubleshooting section in README
4. Check application logs in the console

## Next Steps

1. Complete the "Introduction to KQL" module
2. Try the Query Lab with sample queries
3. Ask questions in the AI Tutor
4. Take your first quiz
5. Track your progress!

Happy Learning! 🚀
