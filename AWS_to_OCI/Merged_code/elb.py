import pandas as pd
from pymongo import MongoClient

def process_elb(df, collection):
    pricing_rules = [
            {
        'condition': lambda row: row['line_item_operation'] in ['LoadBalancing:Network','LoadBalancing-NLB-PublicIP-In'],
        'query': {"name": "NetworkLoadBalancer"},
        'unit_price_field': 'pricePerUnitPerMonth', 
        'comments': "Network Load Balancer is Free in OCI",
        'usage_divisor': 1
    },

    {
        'condition': lambda row: row['line_item_operation'] == 'LoadBalancing-PublicIP-In',
        'query': {"name": "NetworkLoadBalancer"},
        'unit_price_field': 'pricePerUnitPerMonth', 
        'comments': "Inbound Data Transfer is Free in OCI",
        'usage_divisor': 1
    },
    {
        'condition': lambda row: row['line_item_operation'] in ['LoadBalancing:Application','LoadBalancing'] and row['pricing_unit'] in ['Hrs','LCU-Hrs'],
        'query': {"name": "Load Balancer Bandwidth"},
        'unit_price_field': 'pricePerGBPerMonthBase', 
        'comments': "$0.0113 for Oracle Cloud Infrastructure - Load Balancer Base - Load Balancer Hour",
        'usage_divisor': 1
    },
    {
        'condition': lambda row: row['line_item_operation'] in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                    row['line_item_usage_type'].startswith(('US', 'EU', 'DA', 'CA')) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
        'query': {"name": "Outbound Data Transfer - Originating in North America, Europe, and UK"},
        'unit_price_field': 'pricePerGBPerMonth', 
        'comments': "Outbound Data Transfer - Originating in North America, Europe, and UK",
        'usage_divisor': 1000000
    },
    {
        'condition': lambda row: row['line_item_operation']  in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                    row['line_item_usage_type'].startswith(('AP','SA')) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
        'query': {"name": "Outbound Data Transfer - Originating in APAC, Japan, and South America"},
        'unit_price_field': 'pricePerGBPerMonth', 
        'comments': "Outbound Data Transfer - Originating in APAC, Japan, and South America",
        'usage_divisor': 1000000
    },
    {
        'condition': lambda row: row['line_item_operation'] in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                    row['line_item_usage_type'].startswith(('AF','ME' )) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
        'query': {"name": "Outbound Data Transfer - Originating in Middle East and Africa"},
        'unit_price_field': 'pricePerGBPerMonth', 
        'comments': "Outbound Data Transfer - Originating in Middle East and Africa",
        'usage_divisor': 1000000
    },
    {
        'condition': lambda row: 'regional' in row['line_item_line_item_description'],
        'query': {"name": "NetworkLoadBalancer"},
        'unit_price_field': 'pricePerUnitPerMonth', 
        'comments': "Regional Data Transfer is free in OCI",
        'usage_divisor': 1
    }
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                document = collection.find_one(rule['query'])
                unit_price = document.get(rule['unit_price_field'], 0)
                df.at[index, 'OCI Service'] = 'OCI Load Balancer'
                df.at[index, 'OCI Unit Price'] = unit_price
                df.at[index, 'OCI Cost'] = row['SUM(line_item_usage_amount)'] * unit_price / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = 'https://www.oracle.com/cloud/networking/pricing/'
                break

    return df