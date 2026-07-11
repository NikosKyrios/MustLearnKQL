"""
AI Helper Utility - Grok xAI API Integration
"""
import os
from openai import OpenAI

# Initialize Grok client
def get_grok_client():
    """Initialize and return Grok API client"""
    api_key = os.getenv('XAI_API_KEY', '')
    if not api_key or api_key == 'your_grok_api_key_here':
        raise ValueError("XAI_API_KEY not found or not configured. Please add your Grok API key to the .env file.")
    
    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        return client
    except Exception as e:
        raise ValueError(f"Failed to initialize Grok client: {str(e)}")

def chat_with_grok(message, context="", model="grok-3"):
    """
    Chat with Grok AI
    
    Args:
        message: User's message
        context: Previous conversation context
        model: Model to use (default: grok-3)
    
    Returns:
        AI response string
    """
    client = get_grok_client()
    
    if not client:
        return """**AI Tutor is not configured yet.**

To enable AI features:

1. Get a Grok API key from https://x.ai
2. Create a `.env` file in the app directory
3. Add this line: `XAI_API_KEY=your_key_here`
4. Restart the app

**In the meantime, here are some helpful KQL resources:**

- KQL Quick Reference: https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/
- Must Learn KQL Series: https://github.com/rod-trent/MustLearnKQL
- Practice queries in the Query Lab with sample data!

**Common KQL Operators:**
- `where` - Filter rows
- `project` - Select columns
- `summarize` - Aggregate data
- `take` - Limit results
- `sort` - Order results

Feel free to explore the Learning Modules for comprehensive lessons!"""
    
    try:
        # Build messages
        messages = [
            {
                "role": "system",
                "content": """You are an expert KQL (Kusto Query Language) tutor. 
                You help learners understand KQL concepts, write queries, debug errors, 
                and improve their skills. Always provide clear explanations with examples.
                Be encouraging and patient. Format code examples in KQL syntax."""
            }
        ]
        
        if context:
            messages.append({
                "role": "user",
                "content": f"Previous context: {context}"
            })
        
        messages.append({
            "role": "user",
            "content": message
        })
        
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        error_msg = str(e)
        
        # Check for model-specific errors
        if "404" in error_msg or "not found" in error_msg.lower() or "deprecated" in error_msg.lower():
            return f"""**AI Error:** Model not available

The model may have been deprecated or renamed. Current model: `{model}`

**Quick Fix:**
1. Check https://x.ai/docs for current model names
2. Update the model in `utils/ai_helper.py` if needed
3. Common models: `grok-3`, `grok-2`, `grok-vision`

**Error Details:** {error_msg}

**Alternative:** Use the Learning Modules for structured lessons without AI assistance."""
        
        return f"""**AI Error:** {error_msg}

**Troubleshooting:**
- Verify your XAI_API_KEY is correct
- Check your internet connection
- Ensure you have API credits remaining
- Model `{model}` must be available

**Alternative:** Use the Learning Modules for structured lessons without AI assistance."""

def generate_kql_query(goal, table_name="", include_viz=False, model="grok-3"):
    """
    Generate KQL query from natural language description
    
    Args:
        goal: Natural language description of what to query
        table_name: Optional table name to query
        include_viz: Whether to include render visualization
        model: Model to use
    
    Returns:
        Generated KQL query string
    """
    client = get_grok_client()
    
    if not client:
        return f"""// AI query generation requires API configuration
// Goal: {goal}
// 
// Example query structure for this goal:

StormEvents
| where <your_condition>
| project <columns_you_need>
| take 100

// Configure your XAI_API_KEY in .env to enable AI query generation
// In the meantime, try modifying this template or use the Query Lab templates!"""
    
    try:
        prompt = f"""Generate a KQL query for the following goal:
        
Goal: {goal}
{f'Table: {table_name}' if table_name else 'Choose an appropriate table name like StormEvents, SecurityEvent, etc.'}
{f'Include visualization with render operator' if include_viz else ''}

Requirements:
- Write syntactically correct KQL
- Use appropriate operators
- Include comments explaining key parts
- Follow KQL best practices
- Make the query efficient

Return ONLY the KQL query, no explanations."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a KQL query generator. Output only valid KQL code."},
                {"role": "user", "content": prompt}
            ]
        )
        
        query = response.choices[0].message.content.strip()
        
        # Clean up response (remove markdown code blocks if present)
        if query.startswith('```'):
            lines = query.split('\n')
            query = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)
        
        return query
        
    except Exception as e:
        return f"// Error generating query: {str(e)}\n// Please check API configuration"

def explain_concept(topic, category="", level="Intermediate", include_examples=True):
    """
    Explain a KQL concept
    
    Args:
        topic: The concept/operator to explain
        category: Category of the concept
        level: Difficulty level (Beginner/Intermediate/Advanced)
        include_examples: Whether to include code examples
    
    Returns:
        Explanation string
    """
    try:
        client = get_grok_client()
        
        prompt = f"""Explain the KQL concept: {topic}

Category: {category if category else 'General'}
Level: {level}
{'Include practical code examples' if include_examples else 'Brief explanation only'}

Provide:
1. What it is and what it does
2. Syntax and usage
{'3. Practical examples with comments' if include_examples else ''}
4. Common use cases
5. Tips and best practices

Keep it clear and educational for someone learning KQL."""

        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are an expert KQL educator. Explain concepts clearly with examples."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error generating explanation: {str(e)}"

def get_query_feedback(query, model="grok-3"):
    """
    Get AI feedback on a query
    
    Args:
        query: KQL query to analyze
        model: Model to use
    
    Returns:
        Feedback string
    """
    try:
        client = get_grok_client()
        
        prompt = f"""Analyze this KQL query and provide feedback:

```kql
{query}
```

Provide:
1. What the query does
2. Potential improvements or optimizations
3. Best practices to follow
4. Potential issues or warnings
5. Suggested enhancements

Be constructive and educational."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a KQL code reviewer. Provide helpful, constructive feedback."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing query: {str(e)}"

def explain_kql_error(error_message, query, model="grok-3"):
    """
    Explain a KQL error and suggest fixes
    
    Args:
        error_message: The error message
        query: The query that caused the error
        model: Model to use
    
    Returns:
        Explanation and suggestion string
    """
    try:
        client = get_grok_client()
        
        prompt = f"""A KQL query produced this error:

Error: {error_message}

Query:
```kql
{query}
```

Please:
1. Explain what caused the error in simple terms
2. Show the corrected query
3. Explain what was changed and why
4. Provide tips to avoid this error in the future

Be clear and helpful."""

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a KQL debugging expert. Help users understand and fix errors."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error explaining error: {str(e)}"

def generate_quiz_questions(topic, count=5, difficulty="Intermediate"):
    """
    Generate quiz questions for a topic
    
    Args:
        topic: The topic to generate questions about
        count: Number of questions to generate
        difficulty: Question difficulty level
    
    Returns:
        List of question dictionaries
    """
    try:
        client = get_grok_client()
        
        prompt = f"""Generate {count} multiple-choice quiz questions about: {topic}

Difficulty: {difficulty}

Format each question as JSON with:
- question: The question text
- options: List of 4 options (A, B, C, D)
- correct: The correct option letter
- explanation: Why that answer is correct

Return a valid JSON array only."""

        response = client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": "You are a KQL quiz generator. Output valid JSON only."},
                {"role": "user", "content": prompt}
            ]
        )
        
        import json
        questions = json.loads(response.choices[0].message.content)
        return questions
        
    except Exception as e:
        # Return fallback questions if API fails
        return [
            {
                "question": f"What does the {topic} operator do in KQL?",
                "options": ["A. Filters rows", "B. Selects columns", "C. Aggregates data", "D. Joins tables"],
                "correct": "A",
                "explanation": "This is a sample question. Enable AI for generated questions."
            }
        ]

# Fallback responses when API is not available
def get_fallback_response(query_type):
    """Return fallback responses when API is unavailable"""
    
    fallbacks = {
        'chat': "AI tutor is currently unavailable. Please check your API configuration or try again later.",
        'query': "// AI query generation unavailable\n// Please write your query manually or check API settings",
        'explain': "Concept explanation requires API access. Please configure your Grok API key in the .env file.",
        'feedback': "Query feedback requires API access. Manual review recommended.",
        'error': "Error explanation requires API access. Check the KQL documentation for common errors."
    }
    
    return fallbacks.get(query_type, "AI assistance unavailable")
