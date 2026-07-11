"""
Session state management for the KQL Learning App
"""
import streamlit as st
from datetime import datetime

def initialize_session_state():
    """Initialize all session state variables"""
    
    # Theme settings
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # User progress tracking
    if 'completed_modules' not in st.session_state:
        st.session_state.completed_modules = []
    
    if 'current_module' not in st.session_state:
        st.session_state.current_module = 'introduction'
    
    if 'learning_level' not in st.session_state:
        st.session_state.learning_level = 'Beginner'
    
    # Query history
    if 'query_history' not in st.session_state:
        st.session_state.query_history = []
    
    if 'favorite_queries' not in st.session_state:
        st.session_state.favorite_queries = []
    
    # Quiz scores
    if 'quiz_scores' not in st.session_state:
        st.session_state.quiz_scores = {}
    
    # Points and gamification
    if 'total_points' not in st.session_state:
        st.session_state.total_points = 0
    
    if 'current_streak' not in st.session_state:
        st.session_state.current_streak = 0
    
    if 'last_activity_date' not in st.session_state:
        st.session_state.last_activity_date = None
    
    if 'badges' not in st.session_state:
        st.session_state.badges = []
    
    # AI tutor conversation
    if 'ai_messages' not in st.session_state:
        st.session_state.ai_messages = []
    
    # Onboarding
    if 'first_time_user' not in st.session_state:
        st.session_state.first_time_user = True
    
    # KQL connection settings
    if 'kusto_connected' not in st.session_state:
        st.session_state.kusto_connected = False
    
    if 'use_demo_cluster' not in st.session_state:
        st.session_state.use_demo_cluster = True

def update_streak():
    """Update user's learning streak"""
    today = datetime.now().date()
    
    if st.session_state.last_activity_date is None:
        st.session_state.current_streak = 1
    elif st.session_state.last_activity_date == today:
        # Already logged activity today
        return
    elif (today - st.session_state.last_activity_date).days == 1:
        # Consecutive day
        st.session_state.current_streak += 1
    else:
        # Streak broken
        st.session_state.current_streak = 1
    
    st.session_state.last_activity_date = today
    
    # Award streak badges
    if st.session_state.current_streak >= 7 and "Week Warrior" not in st.session_state.badges:
        award_badge("Week Warrior")
    if st.session_state.current_streak >= 30 and "Month Master" not in st.session_state.badges:
        award_badge("Month Master")

def award_points(points, reason=""):
    """Award points to the user"""
    st.session_state.total_points += points
    update_streak()
    
    # Check for point-based badges
    if st.session_state.total_points >= 100 and "KQL Novice" not in st.session_state.badges:
        award_badge("KQL Novice")
    if st.session_state.total_points >= 500 and "KQL Practitioner" not in st.session_state.badges:
        award_badge("KQL Practitioner")
    if st.session_state.total_points >= 1000 and "KQL Expert" not in st.session_state.badges:
        award_badge("KQL Expert")
    
    if reason:
        st.toast(f"🎉 +{points} points for {reason}!")

def award_badge(badge_name):
    """Award a badge to the user"""
    if badge_name not in st.session_state.badges:
        st.session_state.badges.append(badge_name)
        st.balloons()
        st.success(f"🏆 New Badge Unlocked: {badge_name}!")

def add_to_query_history(query, result_count=None, execution_time=None):
    """Add a query to the history"""
    history_entry = {
        'query': query,
        'timestamp': datetime.now(),
        'result_count': result_count,
        'execution_time': execution_time,
        'is_favorite': False
    }
    st.session_state.query_history.insert(0, history_entry)
    
    # Keep only last 50 queries
    if len(st.session_state.query_history) > 50:
        st.session_state.query_history = st.session_state.query_history[:50]

def toggle_favorite_query(query_index):
    """Toggle favorite status of a query"""
    if query_index < len(st.session_state.query_history):
        query = st.session_state.query_history[query_index]
        if query['is_favorite']:
            query['is_favorite'] = False
            if query in st.session_state.favorite_queries:
                st.session_state.favorite_queries.remove(query)
        else:
            query['is_favorite'] = True
            st.session_state.favorite_queries.append(query)

def complete_module(module_name, points=50):
    """Mark a module as completed"""
    if module_name not in st.session_state.completed_modules:
        st.session_state.completed_modules.append(module_name)
        award_points(points, f"completing {module_name}")

def get_progress_percentage():
    """Calculate overall progress percentage"""
    total_modules = 20  # Adjust based on actual module count
    completed = len(st.session_state.completed_modules)
    return (completed / total_modules) * 100

def reset_progress():
    """Reset all user progress (for testing or user request)"""
    st.session_state.completed_modules = []
    st.session_state.quiz_scores = {}
    st.session_state.total_points = 0
    st.session_state.current_streak = 0
    st.session_state.badges = []
    st.session_state.query_history = []
    st.session_state.favorite_queries = []
    st.success("Progress reset successfully!")
