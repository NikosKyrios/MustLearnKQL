"""
Theme management for the KQL Learning App
"""
import streamlit as st

def apply_custom_theme():
    """Apply custom CSS based on theme selection"""
    
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'dark':
        custom_css = """
        <style>
            /* Dark theme customizations */
            .main {
                background-color: #0e1117;
                color: #fafafa;
            }
            
            .stAlert {
                border-radius: 10px;
            }
            
            .query-editor {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
                color: white;
            }
            
            .badge {
                display: inline-block;
                padding: 5px 12px;
                margin: 5px;
                border-radius: 20px;
                background-color: #f59e0b;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            
            .module-card {
                background-color: #1e293b;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #3b82f6;
                margin: 10px 0;
                transition: transform 0.2s;
            }
            
            .module-card:hover {
                transform: translateX(5px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }
            
            .query-result {
                background-color: #1e293b;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
            }
            
            .success-banner {
                background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
                padding: 15px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                text-align: center;
                margin: 10px 0;
            }
            
            .error-banner {
                background: linear-gradient(90deg, #ef4444 0%, #f87171 100%);
                padding: 15px;
                border-radius: 8px;
                color: white;
                font-weight: bold;
                text-align: center;
                margin: 10px 0;
            }
            
            .ai-message {
                background-color: #1e293b;
                border-left: 4px solid #8b5cf6;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
            
            .user-message {
                background-color: #1e3a8a;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                text-align: right;
            }
            
            .progress-bar-container {
                background-color: #1e293b;
                border-radius: 10px;
                padding: 5px;
                margin: 10px 0;
            }
            
            .cheat-sheet-item {
                background-color: #1e293b;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border-left: 3px solid #f59e0b;
            }
            
            /* Accessibility improvements */
            .stButton>button {
                border-radius: 8px;
                font-weight: 600;
                transition: all 0.3s ease;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            }
            
            /* Code highlighting */
            code {
                background-color: #1e293b;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                color: #60a5fa;
            }
            
            /* Responsive design improvements */
            @media (max-width: 768px) {
                .module-card {
                    padding: 15px;
                }
                
                .metric-card {
                    padding: 15px;
                }
            }
        </style>
        """
    else:  # Light theme
        custom_css = """
        <style>
            /* Light theme customizations */
            .main {
                background-color: #ffffff;
                color: #1f2937;
            }
            
            .query-editor {
                background-color: #f9fafb;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
            }
            
            .metric-card {
                background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
                padding: 20px;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                color: white;
            }
            
            .badge {
                display: inline-block;
                padding: 5px 12px;
                margin: 5px;
                border-radius: 20px;
                background-color: #f59e0b;
                color: white;
                font-weight: bold;
                font-size: 14px;
            }
            
            .module-card {
                background-color: #f9fafb;
                padding: 20px;
                border-radius: 10px;
                border-left: 4px solid #3b82f6;
                margin: 10px 0;
                transition: transform 0.2s;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }
            
            .module-card:hover {
                transform: translateX(5px);
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.2);
            }
            
            .query-result {
                background-color: #f9fafb;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
                border: 1px solid #e5e7eb;
            }
            
            .ai-message {
                background-color: #f3f4f6;
                border-left: 4px solid #8b5cf6;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
            }
            
            .user-message {
                background-color: #dbeafe;
                padding: 15px;
                border-radius: 8px;
                margin: 10px 0;
                text-align: right;
            }
            
            .cheat-sheet-item {
                background-color: #fef3c7;
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                border-left: 3px solid #f59e0b;
            }
            
            code {
                background-color: #f3f4f6;
                padding: 2px 6px;
                border-radius: 4px;
                font-family: 'Courier New', monospace;
                color: #1e40af;
            }
        </style>
        """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def get_badge_emoji(badge_name):
    """Return appropriate emoji for badge"""
    badge_emojis = {
        "KQL Novice": "🌱",
        "KQL Practitioner": "📊",
        "KQL Expert": "🏆",
        "Week Warrior": "🔥",
        "Month Master": "👑",
        "Query Master": "⚡",
        "Perfect Score": "💯",
        "First Query": "🎯",
        "Speed Demon": "🚀",
        "Data Detective": "🔍"
    }
    return badge_emojis.get(badge_name, "🏅")
