"""
Home page for the KQL Learning App
"""
import streamlit as st
from utils.session_state import get_progress_percentage, update_streak
from utils.theme_manager import get_badge_emoji

def render_home():
    """Render the home page with dashboard and quick start"""
    
    # Update streak on home page visit
    update_streak()
    
    # Hero section
    st.markdown("""
    # 🔍 Welcome to Must Learn KQL Learning Hub
    
    Your interactive companion for mastering **Kusto Query Language (KQL)** - the powerful 
    language for querying and analyzing data in Azure, Microsoft 365, and more.
    """)
    
    if st.session_state.first_time_user:
        st.info("👋 Welcome! This is your first time here. Let's get you started!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎓 Start Learning Tour", use_container_width=True, key="start_tour_btn"):
                st.session_state.first_time_user = False
                st.session_state.current_module_id = 'introduction'
                st.session_state.selected_page = "Learn KQL"
                st.rerun()
        
        with col2:
            if st.button("🚀 Jump Right In", use_container_width=True, key="jump_in_btn"):
                st.session_state.first_time_user = False
                st.rerun()
    
    st.markdown("---")
    
    # Dashboard - 3 columns for key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Progress</h3>
            <h1>{get_progress_percentage():.0f}%</h1>
            <p>{len(st.session_state.completed_modules)} modules completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>⭐ Points</h3>
            <h1>{st.session_state.total_points}</h1>
            <p>Keep learning to earn more!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        streak_emoji = "🔥" if st.session_state.current_streak > 0 else "💤"
        st.markdown(f"""
        <div class="metric-card">
            <h3>{streak_emoji} Streak</h3>
            <h1>{st.session_state.current_streak}</h1>
            <p>{'day' if st.session_state.current_streak == 1 else 'days'} in a row</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Two column layout for main content
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.subheader("🚀 Quick Start")
        
        # Quick action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📚 Continue Learning", use_container_width=True):
                st.session_state.selected_page = "Learn KQL"
                st.rerun()
        
        with col2:
            if st.button("💻 Open Query Lab", use_container_width=True):
                st.session_state.selected_page = "Query Lab"
                st.rerun()
        
        with col3:
            if st.button("🤖 Ask AI Tutor", use_container_width=True):
                st.session_state.selected_page = "AI Tutor"
                st.rerun()
        
        st.markdown("### 📖 Learning Path")
        
        # Progress through learning levels
        beginner_modules = [
            {"name": "Introduction", "id": "introduction"},
            {"name": "Basic Operators", "id": "basic_operators"},
            {"name": "Search & Filter", "id": "search_filter"}
        ]
        intermediate_modules = [
            {"name": "Aggregations", "id": "aggregations"},
            {"name": "Joins", "id": "joins"},
            {"name": "Time Series", "id": "time_series"}
        ]
        advanced_modules = [
            {"name": "Functions", "id": "functions"},
            {"name": "Advanced Analytics", "id": "advanced_analytics"},
            {"name": "Optimization", "id": "optimization"}
        ]
        
        # Start buttons for each module
        with st.expander("🌱 Beginner (3 modules)", expanded=True):
            for module in beginner_modules:
                completed = module["id"] in st.session_state.completed_modules
                icon = "✅" if completed else "⬜"
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{icon} {module['name']}")
                with col2:
                    if st.button("Start", key=f"start_beginner_{module['id']}", use_container_width=True):
                        st.session_state.current_module_id = module["id"]
                        st.session_state.selected_page = "Learn KQL"
                        st.rerun()
        
        with st.expander("📊 Intermediate (3 modules)"):
            for module in intermediate_modules:
                completed = module["id"] in st.session_state.completed_modules
                icon = "✅" if completed else "⬜"
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{icon} {module['name']}")
                with col2:
                    if st.button("Start", key=f"start_intermediate_{module['id']}", use_container_width=True):
                        st.session_state.current_module_id = module["id"]
                        st.session_state.selected_page = "Learn KQL"
                        st.rerun()
        
        with st.expander("🏆 Advanced (3 modules)"):
            for module in advanced_modules:
                completed = module["id"] in st.session_state.completed_modules
                icon = "✅" if completed else "⬜"
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{icon} {module['name']}")
                with col2:
                    if st.button("Start", key=f"start_advanced_{module['id']}", use_container_width=True):
                        st.session_state.current_module_id = module["id"]
                        st.session_state.selected_page = "Learn KQL"
                        st.rerun()
                        st.session_state.navigation_target = "Learn KQL"
                        st.rerun()
        
        st.markdown("### 📝 Recent Activity")
        
        if st.session_state.query_history:
            for i, query in enumerate(st.session_state.query_history[:3]):
                with st.container():
                    st.markdown(f"""
                    <div class="query-result">
                        <small>{query['timestamp'].strftime('%Y-%m-%d %H:%M')}</small><br>
                        <code>{query['query'][:80]}...</code>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No recent queries yet. Head to the Query Lab to get started!")
    
    with right_col:
        st.subheader("🏆 Your Badges")
        
        if st.session_state.badges:
            for badge in st.session_state.badges:
                emoji = get_badge_emoji(badge)
                st.markdown(f'<span class="badge">{emoji} {badge}</span>', unsafe_allow_html=True)
        else:
            st.info("Complete modules and queries to earn badges!")
        
        st.markdown("---")
        
        st.subheader("💡 Daily Tip")
        
        tips = [
            "Use `take 10` to quickly preview the first 10 rows of your results.",
            "The `where` operator is your best friend for filtering data!",
            "Combine multiple operators with the pipe `|` symbol.",
            "Use `summarize` to aggregate data and gain insights.",
            "Remember: KQL queries are case-insensitive for keywords!",
            "Add comments with `//` to document your queries.",
            "Use `project` to select only the columns you need.",
            "The `extend` operator adds calculated columns without removing existing ones.",
        ]
        
        import random
        daily_tip = random.choice(tips)
        st.info(f"💡 {daily_tip}")
        
        st.markdown("---")
        
        st.subheader("📚 Resources")
        
        st.markdown("""
        - [KQL Reference](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/)
        - [Sample Queries](https://github.com/rod-trent/MustLearnKQL)
        - [Community Forum](#)
        - [Report an Issue](#)
        """)
        
        st.markdown("---")
        
        # Settings and admin
        with st.expander("⚙️ Settings"):
            st.checkbox("Enable keyboard shortcuts", value=True)
            st.checkbox("Show query execution time", value=True)
            st.checkbox("Auto-save queries", value=True)
            
            if st.button("🔄 Reset All Progress", use_container_width=True):
                if st.button("⚠️ Confirm Reset"):
                    from utils.session_state import reset_progress
                    reset_progress()
                    st.rerun()
    
    st.markdown("---")
    
    # Featured content section
    st.subheader("🌟 Featured Content")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="module-card">
            <h4>🔍 Search Operator</h4>
            <p>Master the fundamental search operator for finding data quickly and efficiently.</p>
            <small>Beginner • 15 min</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="module-card">
            <h4>📊 Aggregations</h4>
            <p>Learn to summarize and analyze large datasets with powerful aggregation functions.</p>
            <small>Intermediate • 25 min</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="module-card">
            <h4>🚀 Query Optimization</h4>
            <p>Advanced techniques to make your queries faster and more efficient.</p>
            <small>Advanced • 30 min</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Community leaderboard (mock data for now)
    st.subheader("🏅 Community Leaderboard (This Week)")
    
    leaderboard_data = [
        {"rank": 1, "name": "You", "points": st.session_state.total_points, "is_user": True},
        {"rank": 2, "name": "KQLMaster", "points": 1250, "is_user": False},
        {"rank": 3, "name": "DataWizard", "points": 980, "is_user": False},
        {"rank": 4, "name": "QueryNinja", "points": 875, "is_user": False},
        {"rank": 5, "name": "LogAnalyst", "points": 790, "is_user": False},
    ]
    
    for entry in leaderboard_data:
        highlight = "background-color: #fef3c7;" if entry["is_user"] else ""
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; padding: 10px; 
                    margin: 5px 0; border-radius: 5px; {highlight}">
            <span><strong>#{entry['rank']}</strong> {entry['name']}</span>
            <span><strong>{entry['points']}</strong> pts</span>
        </div>
        """, unsafe_allow_html=True)
