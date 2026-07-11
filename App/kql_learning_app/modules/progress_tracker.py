"""
Progress Tracking Module
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.session_state import get_progress_percentage
from utils.theme_manager import get_badge_emoji

def render_progress():
    """Render the progress tracking dashboard"""
    
    st.title("📊 Your Learning Progress")
    st.markdown("Track your journey to KQL mastery")
    
    # Overall progress section
    st.markdown("### 🎯 Overall Progress")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        progress_pct = get_progress_percentage()
        st.metric(
            "Completion",
            f"{progress_pct:.0f}%",
            delta=f"{len(st.session_state.completed_modules)} modules"
        )
    
    with col2:
        st.metric(
            "Total Points",
            st.session_state.total_points,
            delta="+50" if st.session_state.total_points > 0 else None
        )
    
    with col3:
        st.metric(
            "Current Streak",
            f"{st.session_state.current_streak} days",
            delta="🔥" if st.session_state.current_streak > 0 else None
        )
    
    with col4:
        st.metric(
            "Badges Earned",
            len(st.session_state.badges),
            delta=f"🏆"
        )
    
    # Progress bar
    st.progress(progress_pct / 100)
    
    st.markdown("---")
    
    # Two column layout
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        # Module completion status
        st.markdown("### 📚 Module Progress")
        
        modules = {
            'Beginner': [
                {'id': 'introduction', 'name': 'Introduction to KQL', 'points': 50},
                {'id': 'basic_operators', 'name': 'Basic Operators', 'points': 75},
                {'id': 'search_filter', 'name': 'Search & Filter', 'points': 75},
            ],
            'Intermediate': [
                {'id': 'aggregations', 'name': 'Aggregations', 'points': 100},
                {'id': 'joins', 'name': 'Join Operations', 'points': 100},
                {'id': 'time_series', 'name': 'Time Series Analysis', 'points': 100},
            ],
            'Advanced': [
                {'id': 'functions', 'name': 'User-Defined Functions', 'points': 150},
                {'id': 'advanced_analytics', 'name': 'Advanced Analytics', 'points': 150},
                {'id': 'optimization', 'name': 'Query Optimization', 'points': 150},
            ]
        }
        
        for level, module_list in modules.items():
            with st.expander(f"{level} Modules", expanded=(level == 'Beginner')):
                for module in module_list:
                    completed = module['id'] in st.session_state.completed_modules
                    
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        icon = "✅" if completed else "⬜"
                        st.write(f"{icon} **{module['name']}**")
                    
                    with col2:
                        st.caption(f"{module['points']} pts")
                    
                    with col3:
                        if not completed:
                            if st.button("Start", key=f"start_{module['id']}", use_container_width=True):
                                st.info(f"Starting {module['name']}...")
                        else:
                            st.success("Done")
        
        st.markdown("---")
        
        # Quiz scores
        st.markdown("### 📝 Quiz Scores")
        
        if st.session_state.quiz_scores:
            quiz_data = []
            for quiz_name, score in st.session_state.quiz_scores.items():
                quiz_data.append({
                    'Quiz': quiz_name,
                    'Score': f"{score['correct']}/{score['total']}",
                    'Percentage': f"{(score['correct']/score['total']*100):.0f}%"
                })
            
            df = pd.DataFrame(quiz_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No quizzes completed yet. Visit the Quizzes section to test your knowledge!")
        
        st.markdown("---")
        
        # Activity timeline
        st.markdown("### 📅 Recent Activity")
        
        activities = generate_activity_timeline()
        
        for activity in activities[:10]:
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background-color: rgba(59, 130, 246, 0.1); 
                        border-left: 3px solid #3b82f6; border-radius: 5px;">
                <small>{activity['timestamp'].strftime('%Y-%m-%d %H:%M')}</small><br>
                <strong>{activity['icon']} {activity['title']}</strong>
                {'<br><span style="color: #f59e0b;">+' + str(activity['points']) + ' points</span>' if activity.get('points') else ''}
            </div>
            """, unsafe_allow_html=True)
    
    with right_col:
        # Badges showcase
        st.markdown("### 🏆 Badges")
        
        if st.session_state.badges:
            for badge in st.session_state.badges:
                emoji = get_badge_emoji(badge)
                st.markdown(f"""
                <div style="padding: 15px; margin: 10px 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 10px; text-align: center; color: white;">
                    <div style="font-size: 40px;">{emoji}</div>
                    <div style="font-weight: bold; margin-top: 5px;">{badge}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Complete activities to earn badges!")
        
        # Available badges
        with st.expander("🎯 Available Badges"):
            all_badges = [
                {"name": "KQL Novice", "requirement": "Earn 100 points"},
                {"name": "KQL Practitioner", "requirement": "Earn 500 points"},
                {"name": "KQL Expert", "requirement": "Earn 1000 points"},
                {"name": "Week Warrior", "requirement": "7 day streak"},
                {"name": "Month Master", "requirement": "30 day streak"},
                {"name": "Query Master", "requirement": "Run 100 queries"},
                {"name": "Perfect Score", "requirement": "Get 100% on any quiz"},
                {"name": "First Query", "requirement": "Run your first query"},
            ]
            
            for badge in all_badges:
                earned = badge['name'] in st.session_state.badges
                icon = "✅" if earned else "🔒"
                st.write(f"{icon} **{badge['name']}**")
                st.caption(badge['requirement'])
        
        st.markdown("---")
        
        # Learning goals
        st.markdown("### 🎯 Goals")
        
        with st.expander("Set Learning Goals", expanded=False):
            goal_type = st.selectbox(
                "Goal type:",
                ["Daily queries", "Weekly modules", "Monthly points"]
            )
            
            goal_value = st.number_input("Target:", min_value=1, value=5)
            
            if st.button("Set Goal", use_container_width=True):
                st.success(f"Goal set: {goal_value} {goal_type}")
        
        # Current goals (mock data)
        st.write("**Active Goals:**")
        st.write("✓ Complete 3 beginner modules")
        st.write("⬜ Maintain 7-day streak")
        st.write("⬜ Score 80%+ on all quizzes")
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📈 Statistics")
        
        total_queries = len(st.session_state.query_history)
        favorite_count = len(st.session_state.favorite_queries)
        
        st.metric("Total Queries", total_queries)
        st.metric("Favorite Queries", favorite_count)
        st.metric("Average Score", "75%" if st.session_state.quiz_scores else "N/A")
        
        st.markdown("---")
        
        # Export progress
        if st.button("📥 Export Progress Report", use_container_width=True):
            generate_progress_report()
    
    st.markdown("---")
    
    # Charts section
    st.markdown("### 📊 Progress Charts")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Points Over Time")
        # Mock data for demonstration
        dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7, 0, -1)]
        points = [50, 75, 125, 175, 250, 350, st.session_state.total_points]
        
        chart_data = pd.DataFrame({
            'Date': dates,
            'Points': points
        })
        st.line_chart(chart_data.set_index('Date'))
    
    with chart_col2:
        st.markdown("#### Module Completion")
        completion_data = {
            'Beginner': 3,
            'Intermediate': 0,
            'Advanced': 0
        }
        st.bar_chart(completion_data)
    
    st.markdown("---")
    
    # Leaderboard comparison
    st.markdown("### 🏅 How You Compare")
    
    percentile = min(95, (st.session_state.total_points / 10))
    st.write(f"You're in the top **{100-percentile:.0f}%** of learners!")
    
    st.progress(percentile / 100)

def generate_activity_timeline():
    """Generate activity timeline from session state"""
    activities = []
    
    # Add module completions
    for module in st.session_state.completed_modules:
        activities.append({
            'timestamp': datetime.now() - timedelta(days=len(activities)),
            'icon': '📚',
            'title': f'Completed {module.replace("_", " ").title()}',
            'points': 50
        })
    
    # Add query executions (sample from history)
    for query in st.session_state.query_history[:5]:
        activities.append({
            'timestamp': query['timestamp'],
            'icon': '💻',
            'title': 'Executed KQL query',
            'points': 10
        })
    
    # Add badge earnings
    for badge in st.session_state.badges:
        activities.append({
            'timestamp': datetime.now() - timedelta(days=len(activities) * 2),
            'icon': '🏆',
            'title': f'Earned badge: {badge}',
            'points': 100
        })
    
    # Sort by timestamp
    activities.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return activities

def generate_progress_report():
    """Generate and download progress report"""
    report = f"""
# KQL Learning Progress Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Summary
- **Completion**: {get_progress_percentage():.0f}%
- **Total Points**: {st.session_state.total_points}
- **Current Streak**: {st.session_state.current_streak} days
- **Badges Earned**: {len(st.session_state.badges)}

## Completed Modules
{', '.join(st.session_state.completed_modules) if st.session_state.completed_modules else 'None yet'}

## Badges
{', '.join(st.session_state.badges) if st.session_state.badges else 'None yet'}

## Query Statistics
- Total queries executed: {len(st.session_state.query_history)}
- Favorite queries: {len(st.session_state.favorite_queries)}

## Recent Activity
"""
    
    activities = generate_activity_timeline()
    for activity in activities[:10]:
        report += f"- {activity['timestamp'].strftime('%Y-%m-%d')}: {activity['title']}\n"
    
    st.download_button(
        "Download Report",
        report,
        "kql_progress_report.md",
        "text/markdown"
    )
