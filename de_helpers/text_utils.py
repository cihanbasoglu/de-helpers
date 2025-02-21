import re

def convert_to_snake_case(text):
    """Convert a string to snake_case."""
    text = re.sub(r'[\s\W]+', '_', text)
    text = re.sub(r'Retention Day (\d+)', r'retention_day_\1', text)
    return text.lower()
