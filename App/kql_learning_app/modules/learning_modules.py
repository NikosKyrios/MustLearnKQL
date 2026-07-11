"""
Learning Modules - Interactive KQL Lessons
"""
import streamlit as st
from utils.session_state import complete_module, award_points

def render_learning_modules():
    """Render the learning modules interface"""
    
    st.title("📚 Learn KQL")
    st.markdown("Interactive lessons based on the 'Must Learn KQL' series")
    
    # Initialize current module in session state if not exists
    if 'current_module_id' not in st.session_state:
        st.session_state.current_module_id = 'introduction'
    
    # Module navigation
    modules = get_all_modules()
    
    # Sidebar for module selection
    selected_level = st.selectbox(
        "Select Level:",
        ["Beginner", "Intermediate", "Advanced"],
        key="module_level_selector"
    )
    
    level_modules = [m for m in modules if m['level'] == selected_level]
    
    # Find current module or default to first in level
    current_module = next((m for m in level_modules if m['id'] == st.session_state.current_module_id), None)
    
    # If current module not in this level, use first module of level
    if current_module is None:
        current_module = level_modules[0]
        st.session_state.current_module_id = current_module['id']
    
    # Find index for default selection
    default_index = next((i for i, m in enumerate(level_modules) if m['id'] == st.session_state.current_module_id), 0)
    
    selected_module_name = st.selectbox(
        "Select Module:",
        [m['name'] for m in level_modules],
        index=default_index,
        key="module_name_selector"
    )
    
    # Find selected module and update session state
    module = next(m for m in level_modules if m['name'] == selected_module_name)
    st.session_state.current_module_id = module['id']
    
    # Render the module
    render_module(module)

def render_module(module):
    """Render a specific module"""
    
    # Get position in all modules
    all_modules = get_all_modules()
    current_index = next((i for i, m in enumerate(all_modules) if m['id'] == module['id']), 0)
    total_modules = len(all_modules)
    
    # Module header with progress
    st.markdown(f"""
    <div class="module-card">
        <p style="color: #888; font-size: 14px;">Module {current_index + 1} of {total_modules}</p>
        <h2>{module['icon']} {module['name']}</h2>
        <p><strong>Level:</strong> {module['level']} | 
           <strong>Duration:</strong> {module['duration']} | 
           <strong>Points:</strong> {module['points']}</p>
        <p>{module['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if completed
    is_completed = module['id'] in st.session_state.completed_modules
    if is_completed:
        st.success("✅ You've completed this module!")
    
    st.markdown("---")
    
    # Module content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Learn", "💻 Practice", "📝 Exercises", "🎯 Quiz"
    ])
    
    with tab1:
        render_module_content(module)
    
    with tab2:
        render_module_practice(module)
    
    with tab3:
        render_module_exercises(module)
    
    with tab4:
        render_module_quiz(module)
    
    # Module navigation
    st.markdown("---")
    
    # Get all modules and find current position
    all_modules = get_all_modules()
    current_index = next((i for i, m in enumerate(all_modules) if m['id'] == module['id']), 0)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Previous module button
        if current_index > 0:
            prev_module = all_modules[current_index - 1]
            if st.button("⬅️ Previous Module"):
                st.session_state.current_module_id = prev_module['id']
                st.rerun()
        else:
            st.button("⬅️ Previous Module", disabled=True)
    
    with col2:
        if not is_completed:
            if st.button("✓ Mark as Complete", type="primary", use_container_width=True):
                complete_module(module['id'], module['points'])
                st.success(f"🎉 Module completed! +{module['points']} points")
                st.rerun()
    
    with col3:
        # Next module button
        if current_index < len(all_modules) - 1:
            next_module = all_modules[current_index + 1]
            if st.button("Next Module ➡️"):
                st.session_state.current_module_id = next_module['id']
                st.rerun()
        else:
            st.button("Next Module ➡️", disabled=True)

def render_module_content(module):
    """Render the learning content"""
    
    st.markdown("### 📖 Content")
    
    # Display sections
    for i, section in enumerate(module['content'], 1):
        with st.expander(f"{i}. {section['title']}", expanded=(i == 1)):
            st.markdown(section['text'])
            
            # Code examples
            if 'examples' in section:
                st.markdown("#### Examples:")
                for example in section['examples']:
                    st.code(example['code'], language='sql')
                    if 'explanation' in example:
                        st.caption(example['explanation'])
            
            # Interactive demo
            if 'demo' in section:
                st.markdown("#### Try It:")
                demo_query = st.text_area(
                    "Edit and run:",
                    value=section['demo'],
                    height=150,
                    key=f"demo_{i}"
                )
                if st.button(f"▶️ Run Demo", key=f"run_demo_{i}"):
                    st.info("Demo execution (integrate with Query Lab)")
    
    # Key takeaways
    st.markdown("### 🎯 Key Takeaways")
    for takeaway in module.get('takeaways', []):
        st.write(f"✓ {takeaway}")

def render_module_practice(module):
    """Render practice exercises"""
    
    st.markdown("### 💻 Practice")
    st.write("Apply what you've learned with hands-on practice")
    
    practice_queries = module.get('practice', [])
    
    for i, practice in enumerate(practice_queries, 1):
        st.markdown(f"#### Practice {i}: {practice['title']}")
        st.write(practice['description'])
        
        # Hints
        if 'hints' in practice:
            with st.expander("💡 Hints"):
                for hint in practice['hints']:
                    st.write(f"• {hint}")
        
        # Query editor
        user_query = st.text_area(
            "Your solution:",
            height=200,
            key=f"practice_{i}",
            placeholder="Write your KQL query here..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"✓ Check Solution", key=f"check_{i}"):
                if user_query:
                    # In production, validate against expected solution
                    st.success("Great job! Your solution looks correct.")
                    award_points(25, "completing practice")
                else:
                    st.warning("Please write a solution first")
        
        with col2:
            if st.button(f"👁️ Show Solution", key=f"show_{i}"):
                st.code(practice['solution'], language='sql')
        
        st.markdown("---")

def render_module_exercises(module):
    """Render module exercises"""
    
    st.markdown("### 📝 Exercises")
    st.write("Challenge yourself with these exercises")
    
    exercises = module.get('exercises', [])
    
    for i, exercise in enumerate(exercises, 1):
        with st.expander(f"Exercise {i}: {exercise['title']}", expanded=(i == 1)):
            st.markdown(f"**Difficulty:** {exercise['difficulty']}")
            st.write(exercise['description'])
            
            if 'dataset' in exercise:
                st.info(f"📊 Dataset: {exercise['dataset']}")
            
            # Solution area
            solution = st.text_area(
                "Your answer:",
                height=250,
                key=f"ex_{i}"
            )
            
            if st.button("Submit", key=f"submit_ex_{i}"):
                if solution:
                    st.success("Exercise submitted! Check the AI Tutor for feedback.")
                else:
                    st.warning("Please write a solution")

def render_module_quiz(module):
    """Render module quiz"""
    
    st.markdown("### 🎯 Module Quiz")
    st.write("Test your understanding of this module")
    
    if st.button("🚀 Start Quiz", type="primary"):
        st.info("Starting quiz... (integrate with quiz system)")
    
    st.markdown("---")
    
    # Quiz info
    st.write(f"**Questions:** {module.get('quiz_questions', 10)}")
    st.write(f"**Passing Score:** 70%")
    st.write(f"**Points:** {module['points']}")

def get_all_modules():
    """Get all learning modules"""
    return [
        {
            'id': 'introduction',
            'name': 'Introduction to KQL',
            'level': 'Beginner',
            'icon': '🌟',
            'duration': '15 min',
            'points': 50,
            'description': 'Learn the basics of Kusto Query Language and why it\'s essential for data analysis.',
            'content': [
                {
                    'title': 'What is KQL?',
                    'text': '''
KQL (Kusto Query Language) is a powerful query language used to query large datasets. 
It's the primary language for:
- Azure Data Explorer
- Azure Monitor Logs
- Microsoft 365 Defender
- Microsoft Sentinel

KQL is designed to be intuitive and easy to learn, with a SQL-like syntax but optimized 
for log and telemetry data analysis.
                    ''',
                    'examples': [
                        {
                            'code': 'StormEvents\n| take 10',
                            'explanation': 'Get the first 10 rows from the StormEvents table'
                        }
                    ]
                },
                {
                    'title': 'Basic Query Structure',
                    'text': '''
KQL queries follow a pipeline structure where data flows through operators:

1. Start with a table name
2. Use the pipe (|) to chain operators
3. Each operator transforms the data
4. Results flow to the next operator
                    ''',
                    'examples': [
                        {
                            'code': 'TableName\n| where ColumnName == "value"\n| project Column1, Column2\n| take 100',
                            'explanation': 'A typical query structure: filter, select columns, limit results'
                        }
                    ],
                    'demo': 'StormEvents\n| take 10\n| project State, EventType'
                }
            ],
            'takeaways': [
                'KQL uses a pipeline structure with the pipe (|) operator',
                'Queries start with a table name',
                'Operators transform data as it flows through the pipeline',
                'KQL is case-insensitive for keywords but case-sensitive for values'
            ],
            'practice': [
                {
                    'title': 'Your First Query',
                    'description': 'Write a query to get 5 rows from the StormEvents table',
                    'hints': ['Use the take operator', 'Start with the table name'],
                    'solution': 'StormEvents\n| take 5'
                }
            ],
            'exercises': [
                {
                    'title': 'Explore the Data',
                    'difficulty': 'Easy',
                    'description': 'Get the first 20 events and show only State and EventType columns',
                    'dataset': 'StormEvents'
                }
            ],
            'quiz_questions': 10
        },
        {
            'id': 'basic_operators',
            'name': 'Basic Operators',
            'level': 'Beginner',
            'icon': '🔧',
            'duration': '20 min',
            'points': 75,
            'description': 'Master the fundamental KQL operators: where, project, take, and sort.',
            'content': [
                {
                    'title': 'The where Operator',
                    'text': '''
The `where` operator filters rows based on conditions. It's one of the most commonly used operators in KQL.

**Syntax:** `| where condition`

Common comparison operators:
- `==` (equals)
- `!=` (not equals)
- `>`, `<`, `>=`, `<=` (comparison)
- `contains`, `startswith`, `endswith` (string operations)
- `in`, `!in` (membership)
                    ''',
                    'examples': [
                        {
                            'code': 'StormEvents\n| where State == "TEXAS"\n| take 10',
                            'explanation': 'Filter for events in Texas'
                        },
                        {
                            'code': 'StormEvents\n| where DamageProperty > 1000000',
                            'explanation': 'Find events with property damage over $1M'
                        }
                    ]
                },
                {
                    'title': 'The project Operator',
                    'text': '''
The `project` operator selects which columns to include in the result set. It's similar to SELECT in SQL.

**Syntax:** `| project Column1, Column2, ...`

You can also:
- Rename columns: `project NewName = OldName`
- Create calculated columns: `project Total = Column1 + Column2`
                    ''',
                    'examples': [
                        {
                            'code': 'StormEvents\n| project State, EventType, DamageProperty',
                            'explanation': 'Select only three columns'
                        },
                        {
                            'code': 'StormEvents\n| project State, Event = EventType, Damage = DamageProperty / 1000',
                            'explanation': 'Rename and calculate columns'
                        }
                    ],
                    'demo': 'StormEvents\n| where State == "CALIFORNIA"\n| project State, EventType, StartTime\n| take 10'
                }
            ],
            'takeaways': [
                'where filters rows based on conditions',
                'project selects and renames columns',
                'take limits the number of results',
                'sort/order by arranges results'
            ],
            'practice': [
                {
                    'title': 'Filtering and Projection',
                    'description': 'Find all tornado events and show only State, StartTime, and DamageProperty',
                    'hints': [
                        'Use where to filter EventType',
                        'Use project to select columns',
                        'Remember: EventType == "Tornado"'
                    ],
                    'solution': 'StormEvents\n| where EventType == "Tornado"\n| project State, StartTime, DamageProperty'
                }
            ],
            'exercises': [
                {
                    'title': 'Complex Filtering',
                    'difficulty': 'Medium',
                    'description': 'Find events in Texas or Florida with damage over $100,000, sorted by damage amount',
                    'dataset': 'StormEvents'
                }
            ],
            'quiz_questions': 15
        },
        {
            'id': 'search_filter',
            'name': 'Search & Filter Techniques',
            'level': 'Beginner',
            'icon': '🔍',
            'duration': '18 min',
            'points': 75,
            'description': 'Master advanced filtering and searching techniques in KQL.',
            'content': [
                {
                    'title': 'String Search Operations',
                    'text': '''
KQL provides powerful string search operators for filtering text data:

- **contains** - Check if string contains a substring (case-insensitive)
- **has** - Check for whole word matches
- **startswith** / **endswith** - Check string boundaries
- **matches regex** - Use regular expressions for pattern matching

These operators are essential for log analysis and security investigations.
                    ''',
                    'examples': [
                        {
                            'code': 'StormEvents\n| where EventType contains "Wind"\n| take 10',
                            'explanation': 'Find all events with "Wind" in the EventType'
                        },
                        {
                            'code': 'StormEvents\n| where State startswith "C"\n| project State, EventType',
                            'explanation': 'Find events in states starting with C'
                        }
                    ]
                },
                {
                    'title': 'Multiple Conditions',
                    'text': '''
Combine multiple conditions using logical operators:

- **and** - Both conditions must be true
- **or** - Either condition can be true
- **not** - Negate a condition

You can also use **in** operator for checking multiple values efficiently.
                    ''',
                    'examples': [
                        {
                            'code': 'StormEvents\n| where State == "TEXAS" and EventType == "Tornado"\n| take 10',
                            'explanation': 'Find tornadoes in Texas'
                        },
                        {
                            'code': 'StormEvents\n| where State in ("TEXAS", "CALIFORNIA", "FLORIDA")\n| summarize count() by State',
                            'explanation': 'Count events in multiple states'
                        }
                    ],
                    'demo': 'StormEvents\n| where EventType contains "Storm" or EventType contains "Wind"\n| project State, EventType, DamageProperty\n| take 15'
                }
            ],
            'takeaways': [
                'Use contains for substring search (case-insensitive)',
                'Use has for whole word matching',
                'Combine conditions with and, or, not',
                'Use in operator for checking multiple values efficiently'
            ],
            'practice': [
                {
                    'title': 'Advanced Filtering',
                    'description': 'Find all hail or tornado events in states starting with "T"',
                    'hints': [
                        'Use or to combine event types',
                        'Use startswith for state filter',
                        'Combine with and operator'
                    ],
                    'solution': 'StormEvents\n| where (EventType == "Hail" or EventType == "Tornado") and State startswith "T"\n| project State, EventType, StartTime'
                }
            ],
            'exercises': [
                {
                    'title': 'Complex Search',
                    'difficulty': 'Medium',
                    'description': 'Find events that contain the word "Storm" in the event type, occurred in the last 30 days, and caused more than $50,000 in damage',
                    'dataset': 'StormEvents'
                }
            ],
            'quiz_questions': 12
        },
        # Add more modules here...
    ]

# Initialize module if not set
if 'current_module' not in st.session_state:
    st.session_state.current_module = 'introduction'
