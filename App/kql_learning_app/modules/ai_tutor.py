"""
AI Tutor Module - Powered by Grok xAI API
"""
import streamlit as st
from utils.ai_helper import chat_with_grok, generate_kql_query, explain_concept

def render_ai_tutor():
    """Render the AI tutor chat interface"""
    
    st.title("🤖 AI Tutor - Your KQL Learning Assistant")
    st.markdown("Ask questions, get explanations, and generate queries with AI-powered help")
    
    # API connection test
    import os
    api_key = os.getenv('XAI_API_KEY', '')
    if not api_key or api_key == 'your_grok_api_key_here':
        st.error("⚠️ Grok API key not configured! AI features will not work.")
        st.info("📝 Please add your Grok API key to the `.env` file. See API_KEY_SETUP.md for instructions.")
        
        with st.expander("🔧 Quick Fix Instructions"):
            st.markdown("""
            1. Create a `.env` file in the app folder (copy from `.env.example`)
            2. Add your API key: `XAI_API_KEY=xai-your-key-here`
            3. Restart the app
            4. Get your key from: https://x.ai
            """)
    else:
        st.success(f"✅ API Key configured (ends with: ...{api_key[-8:]})")
    
    st.markdown("---")
    
    # Tabs for different AI features
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 Chat", "🔮 Query Generator", "📚 Concept Explainer", "📝 Exercise Solver"
    ])
    
    with tab1:
        render_chat_interface()
    
    with tab2:
        render_query_generator()
    
    with tab3:
        render_concept_explainer()
    
    with tab4:
        render_exercise_solver()

def render_chat_interface():
    """Render the main chat interface"""
    
    st.markdown("### 💬 Chat with Your AI Tutor")
    st.caption("Ask anything about KQL, get explanations, or request help with queries")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.ai_messages:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class="user-message">
                    <strong>You:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    <strong>🤖 AI Tutor:</strong><br>
                    {message['content']}
                </div>
                """, unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_message = st.text_input(
            "Ask your question:",
            key="chat_input",
            placeholder="e.g., How do I filter by date in KQL?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    if send_button and user_message:
        # Add user message
        st.session_state.ai_messages.append({
            'role': 'user',
            'content': user_message
        })
        
        # Get AI response
        with st.spinner("Thinking..."):
            response = chat_with_grok(
                user_message,
                context=get_conversation_context()
            )
            
            st.session_state.ai_messages.append({
                'role': 'assistant',
                'content': response
            })
        
        st.rerun()
    
    # Quick question buttons
    st.markdown("#### 🎯 Quick Questions")
    quick_questions = [
        "What is the difference between 'where' and 'project'?",
        "How do I join two tables in KQL?",
        "Explain the 'summarize' operator",
        "What are the best practices for query performance?",
        "How do I work with time in KQL?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_q_{i}", use_container_width=True):
                st.session_state.ai_messages.append({
                    'role': 'user',
                    'content': question
                })
                response = chat_with_grok(question, context=get_conversation_context())
                st.session_state.ai_messages.append({
                    'role': 'assistant',
                    'content': response
                })
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.ai_messages = []
        st.rerun()

def render_query_generator():
    """Render the query generator interface"""
    
    st.markdown("### 🔮 Natural Language to KQL Query")
    st.caption("Describe what you want to find, and AI will generate the KQL query")
    
    # User input
    goal_description = st.text_area(
        "Describe your goal:",
        placeholder="e.g., Find all failed login attempts from the last week",
        height=100
    )
    
    # Table/dataset selection
    col1, col2 = st.columns(2)
    
    with col1:
        table_name = st.text_input(
            "Table name (optional):",
            placeholder="e.g., SecurityEvent"
        )
    
    with col2:
        include_render = st.checkbox("Include visualization", value=False)
    
    if st.button("✨ Generate Query", type="primary"):
        if goal_description:
            with st.spinner("Generating KQL query..."):
                query = generate_kql_query(
                    goal_description,
                    table_name=table_name,
                    include_viz=include_render
                )
                
                st.success("Query generated successfully!")
                st.code(query, language='sql')
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📋 Copy to Editor"):
                        st.session_state.current_query = query
                        st.success("Query copied! Go to Query Lab to run it.")
                
                with col2:
                    if st.button("🔄 Refine Query"):
                        refinement = st.text_input("How should I refine it?")
                        if refinement:
                            refined = generate_kql_query(
                                f"{goal_description}. {refinement}",
                                table_name=table_name
                            )
                            st.code(refined, language='sql')
                
                with col3:
                    if st.button("📖 Explain Query"):
                        explanation = explain_query_components(query)
                        st.info(explanation)
        else:
            st.warning("Please describe what you want to query")
    
    # Examples section
    with st.expander("💡 Example Prompts"):
        st.markdown("""
        **Good prompts:**
        - "Find all events where the status code is 404"
        - "Count the number of logins per user in the last 24 hours"
        - "Show me the top 10 users by data volume"
        - "Get all failed transactions and show them in a time chart"
        
        **Tips:**
        - Be specific about time ranges
        - Mention if you want aggregations (count, sum, average)
        - Specify sorting or limiting preferences
        - Include visualization preferences if needed
        """)

def render_concept_explainer():
    """Render the concept explainer interface"""
    
    st.markdown("### 📚 KQL Concept Explainer")
    st.caption("Get detailed explanations of KQL operators, functions, and concepts")
    
    # Category selection
    category = st.selectbox(
        "Select a category:",
        [
            "Operators (where, project, extend, etc.)",
            "Aggregation Functions (count, sum, avg, etc.)",
            "Time Functions (ago, now, datetime, etc.)",
            "String Functions (contains, startswith, etc.)",
            "Join Operations",
            "Performance & Optimization",
            "Best Practices"
        ]
    )
    
    # Topic input
    topic = st.text_input(
        "Enter a specific operator or concept:",
        placeholder="e.g., summarize, join, bin"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        include_examples = st.checkbox("Include examples", value=True)
    
    with col2:
        difficulty_level = st.select_slider(
            "Explanation level:",
            options=["Beginner", "Intermediate", "Advanced"]
        )
    
    if st.button("📖 Explain", type="primary"):
        if topic:
            with st.spinner("Generating explanation..."):
                explanation = explain_concept(
                    topic,
                    category=category,
                    level=difficulty_level,
                    include_examples=include_examples
                )
                
                st.markdown(f"""
                <div class="ai-message">
                    {explanation}
                </div>
                """, unsafe_allow_html=True)
                
                # Related topics
                st.markdown("#### 🔗 Related Topics")
                related = get_related_concepts(topic)
                for rel in related:
                    if st.button(rel, key=f"related_{rel}"):
                        st.session_state.explain_topic = rel
                        st.rerun()
        else:
            st.warning("Please enter a topic to explain")
    
    # Common topics quick access
    st.markdown("#### 🎯 Common Topics")
    
    common_topics = [
        "where", "project", "summarize", "extend", "join",
        "take", "top", "sort", "render", "bin"
    ]
    
    cols = st.columns(5)
    for i, topic in enumerate(common_topics):
        with cols[i % 5]:
            if st.button(topic, key=f"common_{topic}", use_container_width=True):
                explanation = explain_concept(topic, include_examples=True)
                st.info(explanation)

def render_exercise_solver():
    """Render the exercise solver interface"""
    
    st.markdown("### 📝 Practice Exercises with AI Feedback")
    st.caption("Solve KQL challenges and get instant AI-powered feedback")
    
    # Exercise difficulty
    difficulty = st.select_slider(
        "Exercise difficulty:",
        options=["Beginner", "Intermediate", "Advanced"],
        value="Beginner"
    )
    
    # Generate or select exercise
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎲 Generate Random Exercise", use_container_width=True):
            exercise = generate_exercise(difficulty)
            st.session_state.current_exercise = exercise
            st.rerun()
    
    with col2:
        if st.button("📚 Load From Module", use_container_width=True):
            st.info("Exercise library feature coming soon!")
    
    # Display current exercise
    if 'current_exercise' in st.session_state:
        exercise = st.session_state.current_exercise
        
        st.markdown(f"""
        <div class="module-card">
            <h4>🎯 {exercise['title']}</h4>
            <p><strong>Difficulty:</strong> {exercise['difficulty']}</p>
            <p><strong>Challenge:</strong> {exercise['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Hints
        if 'hints' in exercise:
            with st.expander("💡 Hints"):
                for i, hint in enumerate(exercise['hints'], 1):
                    st.write(f"{i}. {hint}")
        
        # User solution
        st.markdown("#### ✍️ Your Solution")
        user_solution = st.text_area(
            "Write your query:",
            height=200,
            placeholder="Enter your KQL query here..."
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✓ Submit Solution", type="primary"):
                if user_solution:
                    with st.spinner("Evaluating your solution..."):
                        feedback = evaluate_solution(
                            user_solution,
                            exercise['expected_solution']
                        )
                        
                        if feedback['correct']:
                            st.success("🎉 Excellent! Your solution is correct!")
                            from utils.session_state import award_points
                            award_points(50, "solving an exercise")
                        else:
                            st.warning("Not quite right. Check the feedback below:")
                        
                        st.markdown(f"""
                        <div class="ai-message">
                            <strong>📊 Feedback:</strong><br>
                            {feedback['explanation']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Please write a solution first!")
        
        with col2:
            if st.button("💡 Get Help"):
                hint = "Try breaking down the problem into smaller steps. " \
                       "What operators do you need?"
                st.info(hint)
        
        with col3:
            if st.button("👁️ Show Solution"):
                st.code(exercise['expected_solution'], language='sql')
                st.caption("Study the solution and try to understand each part")
    else:
        st.info("Click 'Generate Random Exercise' to start practicing!")

def get_conversation_context():
    """Get context from recent messages"""
    recent_messages = st.session_state.ai_messages[-5:]  # Last 5 messages
    context = "\n".join([
        f"{msg['role']}: {msg['content']}"
        for msg in recent_messages
    ])
    return context

def explain_query_components(query):
    """Explain components of a generated query"""
    return f"""
    **Query Breakdown:**
    
    This query uses several KQL operators:
    - Each line starting with `|` is an operator
    - Operators are processed from top to bottom
    - The result of each operator feeds into the next
    
    AI will provide detailed explanation of each component.
    """

def get_related_concepts(topic):
    """Get related concepts to explore"""
    related_map = {
        'where': ['project', 'extend', 'search'],
        'join': ['union', 'lookup', 'mv-expand'],
        'summarize': ['count', 'sum', 'avg', 'bin'],
        'render': ['timechart', 'barchart', 'piechart']
    }
    return related_map.get(topic.lower(), ['where', 'project', 'summarize'])

def generate_exercise(difficulty):
    """Generate a practice exercise"""
    exercises = {
        'Beginner': {
            'title': 'Filter and Select',
            'difficulty': 'Beginner',
            'description': 'Write a query to find all events from California and show only the State, EventType, and StartTime columns. Limit to 10 results.',
            'hints': [
                'Use the where operator to filter',
                'Use project to select specific columns',
                'Use take to limit results'
            ],
            'expected_solution': "StormEvents\n| where State == 'CALIFORNIA'\n| project State, EventType, StartTime\n| take 10"
        },
        'Intermediate': {
            'title': 'Aggregation Challenge',
            'difficulty': 'Intermediate',
            'description': 'Count the number of events per state and show the top 5 states with the most events.',
            'hints': [
                'Use summarize with count()',
                'Group by State',
                'Use top operator to get top results'
            ],
            'expected_solution': "StormEvents\n| summarize EventCount=count() by State\n| top 5 by EventCount desc"
        },
        'Advanced': {
            'title': 'Time Series Analysis',
            'difficulty': 'Advanced',
            'description': 'Create a time chart showing the count of tornado events per day over the last 30 days.',
            'hints': [
                'Filter for tornado events',
                'Filter by time range using ago()',
                'Use summarize with bin() for time buckets',
                'Use render timechart for visualization'
            ],
            'expected_solution': "StormEvents\n| where EventType == 'Tornado'\n| where StartTime > ago(30d)\n| summarize count() by bin(StartTime, 1d)\n| render timechart"
        }
    }
    
    return exercises.get(difficulty, exercises['Beginner'])

def evaluate_solution(user_solution, expected_solution):
    """Evaluate user's solution against expected solution"""
    # In real implementation, this would use Grok API
    # For now, simple comparison
    
    user_clean = user_solution.strip().lower().replace(' ', '')
    expected_clean = expected_solution.strip().lower().replace(' ', '')
    
    if user_clean == expected_clean:
        return {
            'correct': True,
            'explanation': 'Perfect! Your solution matches the expected query exactly.'
        }
    else:
        return {
            'correct': False,
            'explanation': f"""
Your solution is different from the expected one. Here's some feedback:

**Your approach:** The structure looks good, but check:
- Are you using the right operators?
- Is the filtering condition correct?
- Are column names spelled correctly?

Try comparing your query with the solution (click 'Show Solution' to see it).
            """
        }
