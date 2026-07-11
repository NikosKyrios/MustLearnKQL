"""
KQL Learning App - Interactive companion for "Must Learn KQL" series
"""
import streamlit as st
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add modules to path
sys.path.append(str(Path(__file__).parent))

from modules.home import render_home
from modules.query_interface import render_query_interface
from modules.ai_tutor import render_ai_tutor
from modules.progress_tracker import render_progress
from modules.quizzes import render_quizzes
from utils.session_state import initialize_session_state
from utils.theme_manager import apply_custom_theme

# Page configuration
st.set_page_config(
    page_title="Must Learn KQL Learning Hub",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
initialize_session_state()

# Apply custom theme
apply_custom_theme()

# Sidebar navigation
with st.sidebar:
    st.title("🔍 Must Learn KQL Learning Hub")
    st.markdown("---")
    
    # Initialize selected page
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "Home"
    
    st.subheader("Navigation")
    
    # Page options with icons
    page_options = ["Home", "Learn KQL", "Query Lab", "AI Tutor", "Quizzes", "Progress"]
    page_icons = {
        "Home": "🏠",
        "Learn KQL": "📚", 
        "Query Lab": "💻",
        "AI Tutor": "🤖",
        "Quizzes": "📝",
        "Progress": "📊"
    }
    
    # Create navigation using radio buttons (more reliable than option_menu)
    selected = st.radio(
        "Select page:",
        page_options,
        index=page_options.index(st.session_state.selected_page),
        format_func=lambda x: f"{page_icons[x]} {x}",
        key="nav_radio",
        label_visibility="collapsed"
    )
    
    # Update selected page whenever the radio changes
    st.session_state.selected_page = selected
    
    st.markdown("---")
    
    # Learning level selector
    st.subheader("Learning Level")
    level = st.radio(
        "Select your level:",
        ["Beginner", "Intermediate", "Advanced"],
        key="learning_level",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick search
    st.subheader("🔎 Quick Search")
    search_query = st.text_input(
        "Search operators, functions...",
        key="quick_search",
        label_visibility="collapsed"
    )
    
    if search_query:
        st.info(f"Searching for: {search_query}")
        # This will be implemented with actual search functionality
    
    st.markdown("---")
    
    # Theme toggle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark"):
            st.session_state.theme = "dark"
            st.rerun()
    with col2:
        if st.button("☀️ Light"):
            st.session_state.theme = "light"
            st.rerun()
    
    st.markdown("---")
    st.caption("📚 Based on 'Must Learn KQL' Series")
    st.caption("Built with ❤️ by Rod")

# Main content routing - use selected_page from session state
selected = st.session_state.selected_page

if selected == "Home":
    render_home()
elif selected == "Learn KQL":
    from modules.learning_modules import render_learning_modules
    render_learning_modules()
elif selected == "Query Lab":
    render_query_interface()
elif selected == "AI Tutor":
    render_ai_tutor()
elif selected == "Quizzes":
    render_quizzes()
elif selected == "Progress":
    render_progress()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; padding: 20px;'>
        <p>Must Learn KQL Learning Hub | Powered by Streamlit & Grok AI</p>
        <p>Need help? Use the AI Tutor or check the Documentation</p>
    </div>
    """,
    unsafe_allow_html=True
)
