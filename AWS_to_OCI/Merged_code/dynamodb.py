import pandas as pd
from pymongo import MongoClient

def process_dynamodb(df, collection):
    pricing_rules = [
            {
        'condition': lambda row: row['pricing_unit'] == 'ReplicatedWriteCapacityUnit-Hrs',
        'query': {"serviceName" : "DatabaseNoSQLProvisioned"},
        'unit_price_field': 'regionalReplicatedWritePricePerMonth', 
        'comments': "$0.36/744 per hour for provisioned capacity - Regional Replicated Write",
        'usage_divisor': 744
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'ReplicatedWriteRequestUnits',
        'query': {"serviceName" : "DatabaseNoSQL"},
        'unit_price_field': 'regionalReplicatedWritePricePerMonth', 
        'comments': "$0.36 for On Demand Capacity - Regional Replicated Write",
        'usage_divisor': 1000000
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'WriteCapacityUnit-Hrs',
        'query': {"serviceName" : "DatabaseNoSQLProvisioned"},
        'unit_price_field': 'writePricePerMonth', 
        'comments': "$0.1254/744 for Provisioned Capacity – Write",
        'usage_divisor': 744
    },
    {
        'condition': lambda row: row['pricing_unit'] in ['WriteRequestUnits','ChangeDataCaptureUnits'],
        'query': {"serviceName" : "DatabaseNoSQL"},
        'unit_price_field': 'writeAutoPricePerMonth', 
        'comments': "$3.135 for on Demand Capacity – Write",
        'usage_divisor':1000000
    },
    {
        'condition':lambda row: row['pricing_unit'] == 'ReadCapacityUnit-Hrs',
        'query': {"serviceName" : "DatabaseNoSQLProvisioned"},
        'unit_price_field': 'readPricePerMonth', 
        'comments': "$0.0064/744 per hour for Provisioned Capacity-Read",
        'usage_divisor': 744
    },
    {
        'condition': lambda row: row['pricing_unit'] in ['ReadRequestUnits', 'Requests'],
        'query': {"serviceName" : "DatabaseNoSQL"},
        'unit_price_field': 'readAutoPricePerMonth', 
        'comments': "$0.16 for On-Demand Capacity – Read",
        'usage_divisor': 1000000
    },
    {
        'condition': lambda row: row['pricing_unit'] in ['GB-Mo', 'GB','GB-Month'],
        'query': {"serviceName" : "DatabaseNoSQL"},
        'unit_price_field': 'storagePricePerGBPerMonth', 
        'comments': "$0.066 for on demand capacity - Storage ",
        'usage_divisor': 1
    },
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                document = collection.find_one(rule['query'])
                unit_price = document.get(rule['unit_price_field'], 0)
                df.at[index, 'OCI Service'] = 'OCI NoSQL Database'
                df.at[index, 'OCI Unit Price'] = unit_price
                df.at[index, 'OCI Cost'] = row['SUM(line_item_usage_amount)'] * unit_price / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = 'https://www.oracle.com/database/nosql/pricing/#on-demand-capacity-pricing'
                break

    return df