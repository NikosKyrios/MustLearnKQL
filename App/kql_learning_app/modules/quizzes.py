"""
Interactive Quizzes Module
"""
import streamlit as st
from datetime import datetime
from utils.session_state import award_points, award_badge
from utils.ai_helper import generate_quiz_questions

def render_quizzes():
    """Render the quizzes interface"""
    
    st.title("📝 KQL Quizzes")
    st.markdown("Test your knowledge and reinforce what you've learned")
    
    # Quiz selection
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🎯 Select a Quiz")
    
    with col2:
        if st.button("🎲 Random Quiz", use_container_width=True):
            st.session_state.quiz_mode = 'random'
            st.rerun()
    
    # Quiz categories
    quiz_categories = {
        'Basics': {
            'quizzes': [
                {'id': 'intro', 'name': 'Introduction to KQL', 'questions': 10, 'difficulty': 'Beginner'},
                {'id': 'operators', 'name': 'Basic Operators', 'questions': 15, 'difficulty': 'Beginner'},
                {'id': 'syntax', 'name': 'KQL Syntax', 'questions': 12, 'difficulty': 'Beginner'},
            ]
        },
        'Intermediate': {
            'quizzes': [
                {'id': 'aggregations', 'name': 'Aggregation Functions', 'questions': 15, 'difficulty': 'Intermediate'},
                {'id': 'joins', 'name': 'Join Operations', 'questions': 12, 'difficulty': 'Intermediate'},
                {'id': 'time_functions', 'name': 'Time Functions', 'questions': 10, 'difficulty': 'Intermediate'},
            ]
        },
        'Advanced': {
            'quizzes': [
                {'id': 'optimization', 'name': 'Query Optimization', 'questions': 10, 'difficulty': 'Advanced'},
                {'id': 'advanced_functions', 'name': 'Advanced Functions', 'questions': 12, 'difficulty': 'Advanced'},
                {'id': 'best_practices', 'name': 'Best Practices', 'questions': 15, 'difficulty': 'Advanced'},
            ]
        }
    }
    
    # Display quiz categories
    for category, data in quiz_categories.items():
        with st.expander(f"📚 {category}", expanded=(category == 'Basics')):
            for quiz in data['quizzes']:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{quiz['name']}**")
                
                with col2:
                    st.caption(f"{quiz['questions']} Qs")
                
                with col3:
                    st.caption(quiz['difficulty'])
                
                with col4:
                    # Check if already completed
                    score = st.session_state.quiz_scores.get(quiz['id'])
                    if score:
                        st.success(f"{score['correct']}/{score['total']}")
                    else:
                        if st.button("Start", key=f"start_quiz_{quiz['id']}", use_container_width=True):
                            start_quiz(quiz)
                            st.rerun()
    
    st.markdown("---")
    
    # Active quiz
    if st.session_state.get('active_quiz'):
        render_active_quiz()
    else:
        # Quiz stats
        st.markdown("### 📊 Your Quiz Statistics")
        
        if st.session_state.quiz_scores:
            col1, col2, col3 = st.columns(3)
            
            total_quizzes = len(st.session_state.quiz_scores)
            total_correct = sum(s['correct'] for s in st.session_state.quiz_scores.values())
            total_questions = sum(s['total'] for s in st.session_state.quiz_scores.values())
            
            with col1:
                st.metric("Quizzes Completed", total_quizzes)
            
            with col2:
                avg_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
                st.metric("Average Score", f"{avg_score:.0f}%")
            
            with col3:
                perfect_scores = sum(1 for s in st.session_state.quiz_scores.values() if s['correct'] == s['total'])
                st.metric("Perfect Scores", perfect_scores)
            
            # Detailed scores table
            st.markdown("#### 📋 Detailed Scores")
            
            for quiz_id, score in st.session_state.quiz_scores.items():
                percentage = (score['correct'] / score['total'] * 100) if score['total'] > 0 else 0
                
                st.markdown(f"""
                <div style="padding: 10px; margin: 5px 0; background-color: rgba(59, 130, 246, 0.1); 
                            border-radius: 5px; display: flex; justify-content: space-between;">
                    <span><strong>{quiz_id.replace('_', ' ').title()}</strong></span>
                    <span><strong>{score['correct']}/{score['total']}</strong> ({percentage:.0f}%)</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Complete quizzes to see your statistics here!")
        
        st.markdown("---")
        
        # Practice mode
        st.markdown("### 🎯 Practice Mode")
        st.write("Generate custom quizzes on specific topics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.text_input("Topic:", placeholder="e.g., where operator")
        
        with col2:
            num_questions = st.slider("Number of questions:", 5, 20, 10)
        
        if st.button("🚀 Generate Practice Quiz", type="primary"):
            if topic:
                generate_practice_quiz(topic, num_questions)
            else:
                st.warning("Please enter a topic")

def start_quiz(quiz_info):
    """Start a new quiz"""
    # Load or generate questions
    questions = load_quiz_questions(quiz_info['id'])
    
    st.session_state.active_quiz = {
        'id': quiz_info['id'],
        'name': quiz_info['name'],
        'questions': questions,
        'current_question': 0,
        'answers': {},
        'start_time': datetime.now()
    }

def render_active_quiz():
    """Render the active quiz interface"""
    quiz = st.session_state.active_quiz
    current_q = quiz['current_question']
    questions = quiz['questions']
    
    # Progress bar
    progress = (current_q / len(questions)) * 100
    st.progress(progress / 100)
    st.caption(f"Question {current_q + 1} of {len(questions)}")
    
    st.markdown("---")
    
    # Question display
    question = questions[current_q]
    
    st.markdown(f"### Question {current_q + 1}")
    st.markdown(f"**{question['question']}**")
    
    # Answer options
    answer = st.radio(
        "Select your answer:",
        question['options'],
        key=f"q_{current_q}",
        label_visibility="collapsed"
    )
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if current_q > 0:
            if st.button("⬅️ Previous", use_container_width=True):
                quiz['current_question'] -= 1
                st.rerun()
    
    with col2:
        if st.button("✓ Submit Answer", type="primary", use_container_width=True):
            quiz['answers'][current_q] = answer
            
            if current_q < len(questions) - 1:
                quiz['current_question'] += 1
                st.rerun()
            else:
                # Quiz complete
                complete_quiz()
                st.rerun()
    
    with col3:
        if current_q < len(questions) - 1:
            if st.button("Next ➡️", use_container_width=True):
                quiz['answers'][current_q] = answer
                quiz['current_question'] += 1
                st.rerun()
    
    st.markdown("---")
    
    # Quit quiz button
    if st.button("❌ Quit Quiz"):
        st.session_state.active_quiz = None
        st.rerun()
    
    # Show answered questions
    with st.expander("📋 Question Navigator"):
        cols = st.columns(10)
        for i in range(len(questions)):
            with cols[i % 10]:
                status = "✅" if i in quiz['answers'] else "⬜"
                if st.button(f"{status} {i+1}", key=f"nav_{i}", use_container_width=True):
                    quiz['current_question'] = i
                    st.rerun()

def complete_quiz():
    """Complete the quiz and show results"""
    quiz = st.session_state.active_quiz
    questions = quiz['questions']
    answers = quiz['answers']
    
    # Calculate score
    correct = 0
    for i, question in enumerate(questions):
        user_answer = answers.get(i, '')
        if user_answer and user_answer[0] == question['correct']:
            correct += 1
    
    total = len(questions)
    percentage = (correct / total * 100) if total > 0 else 0
    
    # Save score
    st.session_state.quiz_scores[quiz['id']] = {
        'correct': correct,
        'total': total,
        'percentage': percentage,
        'date': datetime.now()
    }
    
    # Award points
    points = int(correct * 10)
    award_points(points, f"completing {quiz['name']}")
    
    # Award badges
    if percentage == 100 and "Perfect Score" not in st.session_state.badges:
        award_badge("Perfect Score")
    
    # Show results
    st.session_state.quiz_results = {
        'correct': correct,
        'total': total,
        'percentage': percentage,
        'questions': questions,
        'answers': answers
    }
    
    st.session_state.active_quiz = None
    st.session_state.show_results = True

def load_quiz_questions(quiz_id):
    """Load questions for a quiz"""
    # In production, load from database or file
    # For now, return sample questions
    
    sample_questions = {
        'intro': [
            {
                'question': 'What does KQL stand for?',
                'options': [
                    'A. Kusto Query Language',
                    'B. Kernel Query Language',
                    'C. Knowledge Query Language',
                    'D. Key Query Language'
                ],
                'correct': 'A',
                'explanation': 'KQL stands for Kusto Query Language, developed for Azure Data Explorer.'
            },
            {
                'question': 'Which operator is used to filter rows in KQL?',
                'options': [
                    'A. select',
                    'B. where',
                    'C. filter',
                    'D. find'
                ],
                'correct': 'B',
                'explanation': 'The where operator is used to filter rows based on conditions.'
            },
        ],
        'operators': [
            {
                'question': 'Which operator selects specific columns?',
                'options': [
                    'A. select',
                    'B. choose',
                    'C. project',
                    'D. columns'
                ],
                'correct': 'C',
                'explanation': 'The project operator selects which columns to include in results.'
            },
        ]
    }
    
    # Return questions for the quiz, or generate AI questions
    return sample_questions.get(quiz_id, generate_default_questions())

def generate_default_questions():
    """Generate default questions"""
    return [
        {
            'question': 'Sample question about KQL',
            'options': ['A. Option 1', 'B. Option 2', 'C. Option 3', 'D. Option 4'],
            'correct': 'A',
            'explanation': 'Sample explanation'
        }
    ] * 5

def generate_practice_quiz(topic, num_questions):
    """Generate a practice quiz using AI"""
    with st.spinner(f"Generating {num_questions} questions about {topic}..."):
        questions = generate_quiz_questions(topic, num_questions)
        
        if questions:
            st.session_state.active_quiz = {
                'id': f'practice_{topic}',
                'name': f'Practice: {topic}',
                'questions': questions,
                'current_question': 0,
                'answers': {},
                'start_time': datetime.now()
            }
            st.success("Quiz generated!")
            st.rerun()
        else:
            st.error("Failed to generate quiz. Please try again.")

# Show results if just completed
if st.session_state.get('show_results'):
    results = st.session_state.quiz_results
    
    st.balloons()
    
    st.markdown(f"""
    <div style="padding: 30px; text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px; color: white; margin: 20px 0;">
        <h1>🎉 Quiz Complete!</h1>
        <h2>{results['correct']} / {results['total']}</h2>
        <h3>{results['percentage']:.0f}%</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Review answers
    with st.expander("📝 Review Answers", expanded=True):
        for i, question in enumerate(results['questions']):
            user_answer = results['answers'].get(i, '')
            correct = user_answer and user_answer[0] == question['correct']
            
            icon = "✅" if correct else "❌"
            st.markdown(f"### {icon} Question {i+1}")
            st.write(question['question'])
            
            if user_answer:
                st.write(f"**Your answer:** {user_answer}")
            else:
                st.write("**Your answer:** Not answered")
            
            st.write(f"**Correct answer:** {question['correct']}")
            
            if 'explanation' in question:
                st.info(f"💡 {question['explanation']}")
            
            st.markdown("---")
    
    if st.button("🏠 Back to Quizzes", type="primary"):
        st.session_state.show_results = False
        st.rerun()
