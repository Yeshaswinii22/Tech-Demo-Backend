import requests
import os
from dotenv import load_dotenv
import json
import sys
from dotenv import load_dotenv
from datetime import datetime, timedelta
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AZURE_SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

if not all([AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_SUBSCRIPTION_ID]):
    print(" Missing Azure credentials in .env file")
    exit()

# Step 1: Get OAuth2 Access Token
def get_access_token():
    token_url = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/oauth2/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": AZURE_CLIENT_ID,
        "client_secret": AZURE_CLIENT_SECRET,
        "resource": "https://management.azure.com/"
    }

    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code == 200:
        access_token = token_response.json().get("access_token")
        print("Access Token Retrieved Successfully")
        print(f" Access Token: {access_token[:30]}... (truncated for security)")
        return access_token
    else:
        print(" Failed to get token:", token_response.json())
        exit()

# Step 2: Define the API Request
def fetch_cost_data(access_token):
    api_url = f"https://management.azure.com/subscriptions/{AZURE_SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "type": "ActualCost",
        "timeframe": "Last30Days",
        "dataset": {
            "granularity": "Daily",
            "aggregation": {"totalCost": {"name": "Cost", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}
            ]
        
        }
    }

    # Step 3: Make the API Request
    response = requests.post(api_url, headers=headers, json=payload)

    # Step 4: Print the Response
    if response.status_code == 200:
        print(" Cost Data Retrieved Successfully")
        print(response.json())
    else:
        print(" Error Fetching Cost Data:", response.status_code, response.json())

# Execute the functions
access_token = get_access_token()
fetch_cost_data(access_token)

def get_cost_data(access_token):
    """Retrieve cost data from Azure Cost Management API"""
    # Calculate date range (e.g., last 30 days)
    today = datetime.now().date()
    from_date = today - timedelta(days=30)
    to_date = today
    
    api_url= f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.CostManagement/query?api-version=2023-03-01"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'type': 'Usage',
        'timeframe': 'Custom',
        'timePeriod': {
            'from': from_date.strftime('%Y-%m-%dT00:00:00+00:00'),
            'to': to_date.strftime('%Y-%m-%dT23:59:59+00:00')
        },
        'dataset': {
            'granularity': 'Daily',
            'aggregation': {
                'totalCost': {
                    'name': 'Cost',
                    'function': 'Sum'
                }
            },
            'grouping': [
                {
                    'type': 'Dimension',
                    'name': 'ServiceName'
                },
                {
                    'type': 'Dimension',
                    'name': 'UsageDate'
                }
            ],
            'include': ['Currency']
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    return response.json()


def store_data_in_db(subscription_id, cost_data):
    """Store Azure Cost Data in PostgreSQL."""
    conn = psycopg2.connect(**DB_PARAMS)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO azure_cost_data (subscription_id, cost, usage_date, service_name, currency)
    VALUES (%s, %s, %s, %s, %s)
    """

    for row in cost_data:
        cost, usage_date, service_name, currency = row
        usage_date = datetime.strptime(str(usage_date), "%Y%m%d").date()  # Convert date format

        cursor.execute(insert_query, (subscription_id, cost, usage_date, service_name, currency))

    conn.commit()
    cursor.close()
    conn.close()
    print("Cost data stored successfully.")

if __name__ == "__main__":
    fetch_cost_data()
    
