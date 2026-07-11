"""
Kusto/KQL Query Execution Utility
"""
import pandas as pd
from datetime import datetime, timedelta
import random

def execute_kql_query(query, use_demo=True):
    """
    Execute KQL query against Kusto cluster
    
    Args:
        query: KQL query string
        use_demo: Whether to use demo data (True) or real cluster (False)
    
    Returns:
        pandas DataFrame with results
    """
    
    if use_demo:
        # Return sample data for demo/testing
        return get_sample_data_for_query(query)
    else:
        # Real Kusto connection (requires azure-kusto-data package)
        return execute_real_kusto_query(query)

def execute_real_kusto_query(query):
    """
    Execute query against real Kusto cluster
    Requires: pip install azure-kusto-data azure-kusto-ingest
    """
    try:
        from azure.kusto.data import KustoClient, KustoConnectionStringBuilder
        
        # Connection configuration (should be in .env)
        cluster = "https://help.kusto.windows.net"
        database = "Samples"
        
        # Build connection string
        kcsb = KustoConnectionStringBuilder.with_aad_device_authentication(cluster)
        
        # Create client
        client = KustoClient(kcsb)
        
        # Execute query
        response = client.execute(database, query)
        
        # Convert to DataFrame
        return pd.DataFrame(response.primary_results[0])
        
    except ImportError:
        raise Exception(
            "azure-kusto-data package not installed. "
            "Install with: pip install azure-kusto-data"
        )
    except Exception as e:
        raise Exception(f"Query execution failed: {str(e)}")

def get_sample_data_for_query(query):
    """
    Generate sample data based on query type
    This simulates query execution for demo purposes
    """
    
    query_lower = query.lower()
    
    # Detect query type and return appropriate sample data
    if 'stormevents' in query_lower:
        return generate_storm_events_data()
    elif 'securityevent' in query_lower:
        return generate_security_events_data()
    elif 'count()' in query_lower and 'summarize' in query_lower:
        return generate_aggregation_data()
    elif 'timechart' in query_lower or 'render' in query_lower:
        return generate_time_series_data()
    else:
        return generate_generic_data()

def generate_storm_events_data():
    """Generate sample storm events data"""
    states = ['TEXAS', 'CALIFORNIA', 'FLORIDA', 'NEW YORK', 'ILLINOIS']
    event_types = ['Tornado', 'Hurricane', 'Flood', 'Hail', 'Lightning']
    
    data = []
    for i in range(20):
        data.append({
            'EventId': f'EV{1000 + i}',
            'State': random.choice(states),
            'EventType': random.choice(event_types),
            'StartTime': datetime.now() - timedelta(days=random.randint(1, 30)),
            'EndTime': datetime.now() - timedelta(days=random.randint(0, 29)),
            'DamageProperty': random.randint(0, 1000000),
            'InjuriesDirect': random.randint(0, 10),
            'DeathsDirect': random.randint(0, 3)
        })
    
    return pd.DataFrame(data)

def generate_security_events_data():
    """Generate sample security events data"""
    event_types = ['LogonSuccess', 'LogonFailure', 'AccountCreated', 'PasswordChanged']
    users = ['john.doe', 'jane.smith', 'admin', 'system', 'user123']
    
    data = []
    for i in range(25):
        data.append({
            'TimeGenerated': datetime.now() - timedelta(hours=random.randint(1, 72)),
            'EventType': random.choice(event_types),
            'User': random.choice(users),
            'Computer': f'COMPUTER-{random.randint(1, 10)}',
            'IPAddress': f'192.168.1.{random.randint(1, 254)}',
            'Status': random.choice(['Success', 'Failure']),
            'EventID': random.randint(4624, 4648)
        })
    
    return pd.DataFrame(data)

def generate_aggregation_data():
    """Generate sample aggregation results"""
    states = ['TEXAS', 'CALIFORNIA', 'FLORIDA', 'NEW YORK', 'ILLINOIS']
    
    data = []
    for state in states:
        data.append({
            'State': state,
            'EventCount': random.randint(50, 500),
            'TotalDamage': random.randint(1000000, 10000000)
        })
    
    df = pd.DataFrame(data)
    return df.sort_values('EventCount', ascending=False)

def generate_time_series_data():
    """Generate sample time series data"""
    data = []
    current_date = datetime.now()
    
    for i in range(30):
        date = current_date - timedelta(days=29-i)
        data.append({
            'StartTime': date,
            'EventCount': random.randint(10, 100)
        })
    
    return pd.DataFrame(data)

def generate_generic_data():
    """Generate generic sample data"""
    data = []
    for i in range(15):
        data.append({
            'Id': i + 1,
            'Name': f'Item_{i+1}',
            'Value': random.randint(1, 100),
            'Category': random.choice(['A', 'B', 'C']),
            'Timestamp': datetime.now() - timedelta(hours=random.randint(1, 48))
        })
    
    return pd.DataFrame(data)

def get_sample_data():
    """Get pre-loaded sample dataset"""
    return generate_storm_events_data()

def validate_kql_syntax(query):
    """
    Basic KQL syntax validation
    
    Args:
        query: KQL query string
    
    Returns:
        tuple: (is_valid, error_message)
    """
    
    # Basic validation checks
    query = query.strip()
    
    if not query:
        return False, "Query is empty"
    
    # Check for common syntax errors
    if query.count('|') > 0 and not any(op in query.lower() for op in ['where', 'project', 'take', 'summarize', 'extend']):
        return False, "Pipe operator used but no valid operator found"
    
    # Check for balanced parentheses
    if query.count('(') != query.count(')'):
        return False, "Unbalanced parentheses"
    
    # Check for balanced quotes
    if query.count('"') % 2 != 0:
        return False, "Unbalanced quotes"
    
    return True, "Query syntax looks valid"

def get_query_statistics(df):
    """
    Get statistics about query results
    
    Args:
        df: Result DataFrame
    
    Returns:
        dict with statistics
    """
    if df is None or df.empty:
        return {
            'row_count': 0,
            'column_count': 0,
            'columns': []
        }
    
    return {
        'row_count': len(df),
        'column_count': len(df.columns),
        'columns': list(df.columns),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024,  # KB
        'dtypes': df.dtypes.to_dict()
    }

def format_query_result(df, format_type='table'):
    """
    Format query results for display
    
    Args:
        df: Result DataFrame
        format_type: 'table', 'json', 'csv'
    
    Returns:
        Formatted string or DataFrame
    """
    if df is None or df.empty:
        return "No results"
    
    if format_type == 'json':
        return df.to_json(orient='records', indent=2)
    elif format_type == 'csv':
        return df.to_csv(index=False)
    else:  # table
        return df

# Sample datasets for learning
SAMPLE_DATASETS = {
    'StormEvents': {
        'description': 'Historical storm and weather event data',
        'columns': ['EventId', 'State', 'EventType', 'StartTime', 'EndTime', 'DamageProperty', 'InjuriesDirect'],
        'sample_queries': [
            "StormEvents | take 10",
            "StormEvents | where State == 'TEXAS'",
            "StormEvents | summarize count() by EventType"
        ]
    },
    'SecurityEvent': {
        'description': 'Security log events',
        'columns': ['TimeGenerated', 'EventType', 'User', 'Computer', 'IPAddress', 'Status'],
        'sample_queries': [
            "SecurityEvent | where EventType == 'LogonFailure'",
            "SecurityEvent | summarize FailedLogins=count() by User",
            "SecurityEvent | where TimeGenerated > ago(1h)"
        ]
    }
}

def get_dataset_info(dataset_name):
    """Get information about a sample dataset"""
    return SAMPLE_DATASETS.get(dataset_name, {
        'description': 'Unknown dataset',
        'columns': [],
        'sample_queries': []
    })

def list_available_datasets():
    """List all available sample datasets"""
    return list(SAMPLE_DATASETS.keys())
