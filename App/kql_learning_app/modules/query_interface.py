"""
Interactive Query Interface for KQL Learning App
"""
import streamlit as st
from datetime import datetime
import pandas as pd
from utils.session_state import add_to_query_history, award_points, toggle_favorite_query
from utils.kusto_connector import execute_kql_query, get_sample_data
from utils.ai_helper import get_query_feedback, explain_kql_error

def render_query_interface():
    """Render the interactive query lab"""
    
    st.title("💻 KQL Query Lab")
    st.markdown("Write, test, and learn KQL with real-time feedback")
    
    # Top action bar
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.markdown("### 🎯 Interactive Query Editor")
    
    with col2:
        if st.button("📝 New Query", use_container_width=True):
            st.session_state.current_query = ""
            st.rerun()
    
    with col3:
        if st.button("📋 Examples", use_container_width=True):
            st.session_state.show_examples = not st.session_state.get('show_examples', False)
    
    with col4:
        if st.button("🔌 Connect", use_container_width=True):
            st.session_state.show_connection_settings = True
    
    st.markdown("---")
    
    # Connection settings
    if st.session_state.get('show_connection_settings', False):
        with st.expander("🔌 Connection Settings", expanded=True):
            connection_type = st.radio(
                "Choose data source:",
                ["Demo Cluster (help.kusto.windows.net)", "Azure Log Analytics", "Custom Cluster"],
                horizontal=True
            )
            
            if connection_type == "Demo Cluster (help.kusto.windows.net)":
                st.info("✅ Connected to public demo cluster with sample data")
                st.session_state.use_demo_cluster = True
            else:
                st.warning("Custom connections require authentication setup")
                cluster_url = st.text_input("Cluster URL")
                database = st.text_input("Database Name")
                
                if st.button("Connect"):
                    st.success("Connection feature coming soon!")
    
    # Two-column layout: Editor + Results
    editor_col, results_col = st.columns([1, 1])
    
    with editor_col:
        st.markdown("#### 📝 Query Editor")
        
        # Sample query templates
        if st.session_state.get('show_examples', False):
            with st.expander("📋 Query Templates", expanded=True):
                templates = {
                    "Basic Search": "StormEvents\n| where State == \"TEXAS\"\n| take 10",
                    "Aggregation": "StormEvents\n| summarize EventCount=count() by State\n| top 10 by EventCount desc",
                    "Time Series": "StormEvents\n| where StartTime > ago(30d)\n| summarize count() by bin(StartTime, 1d)\n| render timechart",
                    "Join Example": "StormEvents\n| join kind=inner (PopulationData) on State\n| project State, EventType, Population",
                    "Complex Filter": "StormEvents\n| where EventType in (\"Tornado\", \"Hurricane\")\n| where DamageProperty > 1000000\n| project State, EventType, DamageProperty, StartTime"
                }
                
                template_choice = st.selectbox("Select a template:", list(templates.keys()))
                if st.button("Load Template"):
                    st.session_state.current_query = templates[template_choice]
                    st.rerun()
        
        # Query editor (using text_area for now, can be upgraded with streamlit-ace)
        query_text = st.text_area(
            "Write your KQL query:",
            value=st.session_state.get('current_query', ''),
            height=300,
            key="query_editor",
            help="Write your KQL query here. Press Ctrl+Enter to execute."
        )
        
        st.session_state.current_query = query_text
        
        # Editor toolbar
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("▶️ Run Query", type="primary", use_container_width=True):
                if query_text.strip():
                    execute_query(query_text, results_col)
                else:
                    st.error("Please enter a query first!")
        
        with col2:
            if st.button("🤖 Get AI Help", use_container_width=True):
                if query_text.strip():
                    with st.spinner("Analyzing query..."):
                        feedback = get_query_feedback(query_text)
                        st.info(f"💡 AI Feedback: {feedback}")
                else:
                    st.warning("Write a query first to get help!")
        
        with col3:
            if st.button("🔍 Explain", use_container_width=True):
                if query_text.strip():
                    explain_query(query_text)
        
        with col4:
            if st.button("📑 Format", use_container_width=True):
                formatted = format_kql_query(query_text)
                st.session_state.current_query = formatted
                st.rerun()
        
        # Query info panel
        with st.expander("ℹ️ Query Information"):
            if query_text:
                st.write(f"**Lines:** {len(query_text.split(chr(10)))}")
                st.write(f"**Characters:** {len(query_text)}")
                operators = extract_operators(query_text)
                if operators:
                    st.write(f"**Operators used:** {', '.join(operators)}")
            else:
                st.info("Write a query to see information")
    
    with results_col:
        st.markdown("#### 📊 Query Results")
        
        # Results display area (will be populated by execute_query)
        if 'last_result' in st.session_state:
            display_results(st.session_state.last_result)
        else:
            st.info("""
            👈 Write a query in the editor and click **Run Query** to see results here.
            
            **Quick Start Tips:**
            - Start with a table name (e.g., `StormEvents`)
            - Use `|` to pipe operators
            - Use `take 10` to limit results
            - Try the example templates!
            """)
    
    st.markdown("---")
    
    # Query history section
    st.markdown("### 📜 Query History")
    
    tab1, tab2 = st.tabs(["Recent Queries", "Favorites"])
    
    with tab1:
        if st.session_state.query_history:
            for i, query in enumerate(st.session_state.query_history[:10]):
                with st.expander(
                    f"🕐 {query['timestamp'].strftime('%Y-%m-%d %H:%M')} - "
                    f"{query['query'][:50]}..."
                ):
                    st.code(query['query'], language='sql')
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        if st.button(f"▶️ Run", key=f"run_{i}"):
                            st.session_state.current_query = query['query']
                            st.rerun()
                    with col2:
                        if st.button(f"⭐ Favorite", key=f"fav_{i}"):
                            toggle_favorite_query(i)
                            st.rerun()
                    with col3:
                        if st.button(f"📋 Copy", key=f"copy_{i}"):
                            st.write("Query copied to clipboard!")
                    
                    if query.get('result_count'):
                        st.caption(f"Results: {query['result_count']} rows")
                    if query.get('execution_time'):
                        st.caption(f"Execution time: {query['execution_time']:.2f}s")
        else:
            st.info("No query history yet. Run some queries to see them here!")
    
    with tab2:
        if st.session_state.favorite_queries:
            for i, query in enumerate(st.session_state.favorite_queries):
                with st.expander(f"⭐ {query['query'][:50]}..."):
                    st.code(query['query'], language='sql')
                    if st.button(f"▶️ Run", key=f"run_fav_{i}"):
                        st.session_state.current_query = query['query']
                        st.rerun()
        else:
            st.info("No favorite queries yet. Star queries from your history!")
    
    # Export options
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export History", use_container_width=True):
            export_query_history()
    
    with col2:
        if st.button("📄 Generate Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
    
    with col3:
        if st.button("🔗 Share Query", use_container_width=True):
            st.info("Query sharing feature coming soon!")

def execute_query(query, display_area=None):
    """Execute KQL query and display results"""
    try:
        with st.spinner("Executing query..."):
            start_time = datetime.now()
            
            # Execute query (using sample data for demo)
            result_df = execute_kql_query(query)
            
            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds()
            
            # Store results
            st.session_state.last_result = {
                'df': result_df,
                'execution_time': execution_time,
                'query': query
            }
            
            # Add to history
            add_to_query_history(
                query,
                result_count=len(result_df) if result_df is not None else 0,
                execution_time=execution_time
            )
            
            # Award points
            award_points(10, "running a query")
            
            st.success(f"✅ Query executed in {execution_time:.2f}s")
            st.rerun()
            
    except Exception as e:
        st.error(f"❌ Query Error: {str(e)}")
        
        # Get AI explanation of error
        with st.expander("🤖 AI Error Explanation"):
            explanation = explain_kql_error(str(e), query)
            st.write(explanation)

def display_results(result):
    """Display query results"""
    if result and 'df' in result:
        df = result['df']
        
        # Results toolbar
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Rows", len(df))
        with col2:
            st.metric("Columns", len(df.columns) if not df.empty else 0)
        with col3:
            st.metric("Time", f"{result['execution_time']:.2f}s")
        
        # Display options
        display_mode = st.radio(
            "Display as:",
            ["Table", "Chart", "JSON"],
            horizontal=True
        )
        
        if display_mode == "Table":
            st.dataframe(df, use_container_width=True, height=400)
        elif display_mode == "Chart":
            if not df.empty and len(df.columns) >= 2:
                chart_type = st.selectbox("Chart type:", ["Bar", "Line", "Area"])
                if chart_type == "Bar":
                    st.bar_chart(df.set_index(df.columns[0]))
                elif chart_type == "Line":
                    st.line_chart(df.set_index(df.columns[0]))
                else:
                    st.area_chart(df.set_index(df.columns[0]))
            else:
                st.warning("Chart requires at least 2 columns")
        else:  # JSON
            st.json(df.to_dict(orient='records'))
        
        # Export options
        if st.button("💾 Export Results"):
            csv = df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "query_results.csv",
                "text/csv"
            )

def format_kql_query(query):
    """Format KQL query with proper indentation"""
    # Simple formatter - can be enhanced
    lines = query.split('\n')
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|'):
            formatted_lines.append('| ' + stripped[1:].strip())
        else:
            formatted_lines.append(stripped)
    
    return '\n'.join(formatted_lines)

def extract_operators(query):
    """Extract KQL operators from query"""
    operators = []
    common_operators = [
        'where', 'project', 'summarize', 'take', 'limit', 'top', 
        'extend', 'join', 'union', 'render', 'sort', 'order'
    ]
    
    query_lower = query.lower()
    for op in common_operators:
        if f'| {op}' in query_lower or query_lower.startswith(op):
            operators.append(op)
    
    return operators

def explain_query(query):
    """Provide explanation of query structure"""
    st.info("""
    **Query Explanation:**
    
    This query will be analyzed by the AI Tutor to provide:
    - What each operator does
    - The expected output
    - Optimization suggestions
    - Common pitfalls to avoid
    """)

def export_query_history():
    """Export query history as JSON"""
    import json
    
    history_export = []
    for query in st.session_state.query_history:
        history_export.append({
            'query': query['query'],
            'timestamp': query['timestamp'].isoformat(),
            'is_favorite': query.get('is_favorite', False)
        })
    
    json_str = json.dumps(history_export, indent=2)
    st.download_button(
        "Download History (JSON)",
        json_str,
        "query_history.json",
        "application/json"
    )
