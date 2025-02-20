import pandas as pd
from pymongo import MongoClient

def process_cloudwatch(df, collection):
    pricing_rules = [
        {
        'condition': lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
                                  row['line_item_operation'] in ['GetMetricData', 'GetMetricWidgetImage'],
        'query': {"name": "Monitoring - Retrieval"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
                                  row['line_item_operation'] in [
                                      'MetricUpdate', 'MetricStorage', 'MetricStorage:AWS/Logs-EMF',
                                      'MetricStorage:AWS/EC2', 'MetricStorage:AWS/S3', 'MetricStorage:AWS/SES',
                                      'MetricStorage:AWS/Beanstalk', 'MetricStorage:AWS/CloudWatchLogs',
                                      'MetricStorage:AWS/ApiGateway','MetricStorage:AWS/CloudFront'
                                  ],
        'query': {"name": "Monitoring - Ingestion"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Requests' and 
                                  row['line_item_operation'] in ['GetMetricStatistics', 'ListDashboards', 
                                                                 'GetDashboard', 'ListMetrics'],
        'query': {"name": "Monitoring - Retrieval"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Requests' and 
                                  row['line_item_operation'] in ['PutMetricData', 'PutDashboard'],
        'query': {"name": "Monitoring - Ingestion"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Requests' and 
                                  row['line_item_operation'] == 'DeleteDashboards',
        'query': {"name": "Application Performance Monitoring Service - Synthetic Usage - Free"},
        'unit_price_field': 'pricePerUnit',
        'comments': "Dashboards are free in OCI",
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'GB' or row['pricing_unit'] == 'GB-Mo',
        'query': {"name": "Oracle Cloud Infrastructure - Logging - Storage"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.05 for Over 10 gigabytes log storage per month",
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Alarms',
        'query': {"name": "Monitoring - Retrieval"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Dashboards',
        'query': {"name": "Application Performance Monitoring Service - Synthetic Usage - Free"},
        'unit_price_field': 'pricePerUnit',
        'comments': "Dashboards are free in OCI",
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier'
        
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'minutes',
        'query': {"name": "Application Performance Monitoring Service - Synthetic Usage - Free"},
        'unit_price_field': 'pricePerUnit',
        'comments': "Free",
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Observations',
        'query': {"name": "Monitoring - Ingestion"},
        'unit_price_field': 'pricePermonth',
        'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
        'usage_divisor': 1000000,
        'sku_id':'serviceIdentifier'
    },
    {
        'condition': lambda row: row['pricing_unit'] == 'Runs',
        'query': {"name": "Application Performance Monitoring Service - Synthetic Usage - Free"},
        'unit_price_field': 'pricePerUnit',
        'comments': "Free",
        'usage_divisor': 1,
        'sku_id':'serviceIdentifier'
    },
    ]

    for index, row in df.iterrows():
        for rule in pricing_rules:
            if rule['condition'](row):
                document = collection.find_one(rule['query'])
                unit_price = document.get(rule['unit_price_field'], 0)
                df.at[index, 'OCI Service'] = 'OCI Monitoring & OCI Logging'
                df.at[index, 'SKU_ID'] = document.get(rule['sku_id'],'')
                df.at[index, 'OCI Unit Price'] = unit_price
                df.at[index, 'OCI Cost'] = row['SUM(line_item_usage_amount)'] * unit_price / rule['usage_divisor']
                df.at[index, 'Comments'] = rule['comments']
                df.at[index, 'Reference'] = 'https://www.oracle.com/manageability/pricing/'
                break

    return df