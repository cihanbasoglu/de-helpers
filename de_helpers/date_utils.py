import pandas as pd
from datetime import datetime, timedelta

def range_end(end_date, days, freq):
    """Generate date range tuples from an end_date by subtracting days."""
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    start_date = end_date - timedelta(days=days)
    date_ranges = pd.date_range(start=start_date, end=end_date, freq=f'{freq}D')

    ranges = [(date_ranges[i].strftime('%Y-%m-%d'), (date_ranges[i+1] - timedelta(days=1)).strftime('%Y-%m-%d')) 
              for i in range(len(date_ranges) - 1)]

    ranges.append((date_ranges[-1].strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    return ranges

def range_start_end(start_date, end_date, freq):
    """Generate date range tuples from start_date to end_date."""
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    date_ranges = pd.date_range(start=start_date, end=end_date, freq=f'{freq}D')

    ranges = [(date_ranges[i].strftime('%Y-%m-%d'), (date_ranges[i+1] - timedelta(days=1)).strftime('%Y-%m-%d')) 
              for i in range(len(date_ranges) - 1)]

    ranges.append((date_ranges[-1].strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
    return ranges

def convert_to_epoch_ms(timestamp_str):
    """Convert a timestamp string to epoch milliseconds."""
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp() * 1000)
    except ValueError as e:
        print(f"Error converting timestamp: {timestamp_str}. Error: {e}")
        return None