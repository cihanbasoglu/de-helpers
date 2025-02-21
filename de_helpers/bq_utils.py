import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import json

def get_bq_credentials(file_path: str):
    """Load BigQuery service account credentials from a file."""
    with open(file_path, "r") as f:
        service_account_info = json.load(f)
    return service_account.Credentials.from_service_account_info(service_account_info)

def upload_to_bq(df, project, dataset, table, credentials, if_exists="replace"):
    """Upload a Pandas DataFrame to BigQuery."""
    df.to_gbq(f'{dataset}.{table}', project_id=project, credentials=credentials, if_exists=if_exists)
    print(f"Data uploaded to {project}.{dataset}.{table}")

def delete_bq_table(credentials, project, dataset, table, not_found_ok=True):
    """Delete a table in BigQuery."""
    client = bigquery.Client(credentials=credentials)
    table_id = f"{project}.{dataset}.{table}"
    client.delete_table(table_id, not_found_ok=not_found_ok)
    print(f"Deleted table: {table_id}")

def query_bq_to_df(query: str, client):
    """Run a query in BigQuery and return a Pandas DataFrame."""
    query_job = client.query(query)
    return pd.DataFrame([dict(row) for row in query_job])

def run_bq_query(query: str, client):
    """Execute a query in BigQuery without returning results."""
    try:
        query_job = client.query(query)
        query_job.result()
        print(f"Query executed successfully. Job ID: {query_job.job_id}, State: {query_job.state}")
        return query_job
    except Exception as e:
        print(f"Failed to execute query. Error: {e}")
        return None