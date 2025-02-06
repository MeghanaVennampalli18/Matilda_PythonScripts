import requests
import json

# Fetch the services index JSON
url = "https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/index.json"
response = requests.get(url)
data = response.json()

# Extract and print service pricing URLs
for service, details in data['offers'].items():
    service_name = details.get('offerCode', 'Unknown')
    pricing_url = f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service_name}/current/index.json"
    print(f"{service_name}: {pricing_url}")

