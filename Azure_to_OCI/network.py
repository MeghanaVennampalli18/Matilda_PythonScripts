import pandas as pd
from pymongo import MongoClient

def process_network(df, collection):
    pricing_rules = [
    {
        'condition': lambda row: ('DATA TRANSFER OUT' in row['meterName'] or 'EGRESS' in row['meterName']) and row['region'] in  ['USEAST', 'USEAST2', 'USCENTRAL', 'USNORTHCENTRAL', 'USSOUTHCENTRAL', 'USWEST', 'USWEST2', 'USWEST3', 'CANCENTRAL', 'CANEAST', 'EUNORTH', 'EUWEST', 'FRCENTRAL', 'FRSOUTH', 'DEWESTCENTRAL', 'DENORTH', 'NOEAST', 'NOWEST', 'SECENTRAL', 'CHNORTH', 'CHWEST', 'UKSOUTH', 'UKWEST'],
        'query': {"name": "Outbound Data Transfer - Originating in North America, Europe, and UK"},
        'unit_price_field': 'pricePerGBPerMonth',
        'comments': "Outbound Data Transfer - Originating in North America, Europe, and UK",
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: ('DATA TRANSFER OUT' in row['meterName'] or 'EGRESS' in row['meterName']) and row['region'] in  ['EASIA', 'SEASIA', 'AUEAST', 'AUSEAST', 'AUCENTRAL', 'AUCENTRAL2', 'JAEAST', 'JAWEST', 'BRSOUTH', 'BRSE'],
        'query': {"name": "Outbound Data Transfer - Originating in APAC, Japan, and South America"},
        'unit_price_field': 'pricePerGBPerMonth',
        'comments': "Outbound Data Transfer - Originating in APAC, Japan and South America",
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: ('DATA TRANSFER OUT' in row['meterName'] or 'EGRESS' in row['meterName']) and row['region'] in  ['QACENTRAL', 'UAECENTRAL', 'UAENORTH', 'SANORTH', 'SAWEST'],
        'query':{"name": "Outbound Data Transfer - Originating in Middle East and Africa"},
        'unit_price_field': 'pricePerGBPerMonth',
        'comments': "Outbound Data Transfer - Originating in Middle East and Africa", 
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: 'DATA TRANSFER IN' in row['meterName'] or 'INGRESS' in row['meterName'],
        'query': {},
        'unit_price_field': '',
        'comments': "Inbound data transfer is Free",
        'usage_divisor': 1,
        'multiplier':0,
        'sku_id':'',
        'Reference':'',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: row['meterSubCategory']=='LOAD BALANCER' and 'LB RULES' in row['meterName'],
        'query': {"name": "Load Balancer Bandwidth"},
        'unit_price_field': 'pricePerGBPerMonthBase',
        'comments': "$0.0113 for Oracle Cloud Infrastructure - Load Balancer Base - Load Balancer Hour", 
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifierBase',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: 'QUERIES' in row['meterName'],
        'query': {"tfService": "dnsTrafficmanagement"},
        'unit_price_field': 'pricePerGBPerMonthDNS',
        'comments': "Networking - DNS", 
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifierDNS',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    },
    {
        'condition': lambda row: 'QUERIES' in row['meterName'],
        'query': {"tfService": "dnsTrafficmanagement"},
        'unit_price_field': 'pricePerGBPerMonthTrafficManagement',
        'comments': "Networking - DNS", 
        'multiplier':1,
        'usage_divisor': 1,
        'sku_id':'serviceIdentifierTrafficManagement',
        'Reference':'https://www.oracle.com/cloud/networking/pricing/',
        'service':'OCI Networking'
    }, 
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                document = collection.find_one(rule['query'])
                unit_price = document.get(rule['unit_price_field'], 0)
                df.at[index, 'OCI Service'] = rule['service']
                df.at[index, 'SKU_ID'] = document.get(rule['sku_id'],'')
                df.at[index, 'OCI Unit Price'] = unit_price
                df.at[index, 'OCI Cost'] = row['usage'] * unit_price * rule['multiplier'] / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = rule['Reference']
                break

    return df