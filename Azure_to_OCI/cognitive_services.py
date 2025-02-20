import pandas as pd
from pymongo import MongoClient

def process_cognitiveServices(df):
    pricing_rules = [
    {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE OPENAI' and 'GPT' in row['meterName'],
        'unit_price': 0.0156,
        'comments': "Large Cohere 10,000 trasactions",
        'multiplier':1000,
        'usage_divisor': 10000,
        'sku_id':'B108077'
    },
    {
        'condition': lambda row: row['meterSubCategory'] == 'AZURE OPENAI' and 'EMBEDDING' in row['meterName'],
        'unit_price': 0.001,
        'comments': "Embed Cohere 10,000 trasactions",
        'multiplier':1000,
        'usage_divisor': 10000, 
        'sku_id':'B108079'
    },
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                df.at[index, 'OCI Service'] = 'OCI Generative AI'
                df.at[index, 'SKU_ID'] = rule['sku_id']
                df.at[index, 'OCI SKU UnitPrice'] = rule['unit_price']
                df.at[index, 'OCI TotalCost'] = row['usage'] * rule['unit_price'] * rule['multiplier'] / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = 'https://www.oracle.com/artificial-intelligence/generative-ai/generative-ai-service/pricing/'
                break

    return df