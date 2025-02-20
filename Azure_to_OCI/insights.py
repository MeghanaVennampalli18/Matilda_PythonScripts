import pandas as pd
from pymongo import MongoClient

def process_insights(df, collection):
    pricing_rules = [
    {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE MONITOR' and row['meterName'] == 'EMAILS',
        'query': {"name": "Notifications - Email Delivery"},
        'unit_price_field': 'pricePerUnitfrom1',
        'comments': "$0.02 for 1000 Emails sent",
        'multiplier':1,
        'usage_divisor': 1000,
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/cloud/cloud-native/notifications/pricing/'
    },
    {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE MONITOR' and row['meterName'] == 'NOTIFICATIONS WEB HOOK',
        'query': {"name": "Notifications - HTTPS Delivery"},
        'unit_price_field': 'pricePerUnitfrom1',
        'comments': "$0.60 for million Delivery Operations",
        'multiplier':10,
        'usage_divisor': 1000000, 
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/cloud/cloud-native/notifications/pricing/'
    },
    {
        'condition': lambda row: row['meterSubCategory'] in ['LOG ANALYTICS', 'INSIGHT AND ANALYTICS'],
        'query': {"name": "Logging Analytics - Active Storage"},
        'unit_price_field': 'pricePermonth',
        'comments': "$372 for first 35 Logging Analytics Storage Unit per month(1 Storage Unit=300 GB of logs during the month",
        'usage_divisor': 300,
        'multiplier':1,
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/manageability/logging-analytics/pricing/'
    },
        {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE MONITOR' and 'INGESTION' in row['meterName'],
        'query': {"name": "Monitoring - Ingestion"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0025 for Monitoring Ingestion per Million Datapoints",
        'multiplier':1,
        'usage_divisor': 1000000, 
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/manageability/pricing/#monitoring'
    },
        {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE MONITOR' and 'RETRIVAL' in row['meterName'],
        'query': {"name": "Monitoring - Retrieval"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0015 for Monitoring Retrieval per Million Datapoints",
        'multiplier':1,
        'usage_divisor': 1000000, 
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/manageability/pricing/#monitoring'
    },
    {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE MONITOR' and 'ALERTS' in row['meterName'],
        'query': {},
        'unit_price_field': '',
        'comments': "No price for Alarms in OCI",
        'usage_divisor': 1,
        'multiplier':0,
        'sku_id':'',
        'Reference':''
    },
    
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                document = collection.find_one(rule['query'])
                unit_price = document.get(rule['unit_price_field'], 0)
                df.at[index, 'OCI Service'] = 'OCI Observability and Management Services'
                df.at[index, 'SKU_ID'] = document.get(rule['sku_id'],'')
                df.at[index, 'OCI Unit Price'] = unit_price
                df.at[index, 'OCI Cost'] = row['usage'] * unit_price * rule['multiplier'] / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = rule['Reference']
                break

    return df