#------------Program Using Classes--------------#


import pandas as pd
import os

class CloudWatch_PricingRule:
    """
    Represents a pricing rule with a condition, unit price, comments, and a usage divisor.
    """
    def __init__(self, condition, unit_price, comments, usage_divisor):
        self.condition = condition
        self.unit_price = unit_price
        self.comments = comments
        self.usage_divisor = usage_divisor

    def applies_to(self, row):
        """
        Checks if the rule applies to a given row.
        """
        return self.condition(row)


class CloudWatch_PricingEngine:
    """
    Encapsulates the pricing logic and applies pricing rules to a DataFrame.
    """
    def __init__(self, dataframe, pricing_rules):
        self.dataframe = dataframe
        self.pricing_rules = pricing_rules

    def apply_rules(self):
        """
        Applies the pricing rules to the DataFrame.
        """
        for index, row in self.dataframe.iterrows():
            for rule in self.pricing_rules:
                if rule.applies_to(row):
                    self.dataframe.at[index, 'OCI Unit Price'] = rule.unit_price
                    self.dataframe.at[index, 'OCI Cost'] = (
                        row['SUM(line_item_usage_amount)'] * rule.unit_price / rule.usage_divisor
                    )
                    self.dataframe.at[index, 'Comments'] = rule.comments
                    break 
                else:
                    continue


def CloudWatch_main():
    # Load the input file
    file_path = "Cloudwatch_excelfile.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    
    # Add default columns
    df['OCI Service'] = "OCI Monitoring & OCI Logging"
    df['Reference'] = "https://www.oracle.com/manageability/pricing/"

    # Define pricing rules
    pricing_rules = [
        CloudWatch_PricingRule(
            condition=lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
                                  row['line_item_operation'] in ['GetMetricData', 'GetMetricWidgetImage'],
            unit_price=0.0015,
            comments="$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
            usage_divisor=1000000
        ),
        CloudWatch_PricingRule(
            condition=lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
                                  row['line_item_operation'] in [
                                      'MetricUpdate', 'MetricStorage', 'MetricStorage:AWS/Logs-EMF',
                                      'MetricStorage:AWS/EC2', 'MetricStorage:AWS/S3', 'MetricStorage:AWS/SES',
                                      'MetricStorage:AWS/Beanstalk', 'MetricStorage:AWS/CloudWatchLogs',
                                      'MetricStorage:AWS/ApiGateway', 'MetricStorage:AWS/Kinesis', 'MetricStorage:AWS/CloudFront','MetricStorage:AWS/Kafka'
                                  ],
            unit_price=0.0025,
            comments="$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
            usage_divisor=1000000
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Requests' and 
                                  row['line_item_operation'] in ['GetMetricStatistics', 'ListDashboards', 
                                                                 'GetDashboard', 'ListMetrics'],
            unit_price= 0.0015,
            comments= "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
            usage_divisor= 1000000
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Requests' and 
                                row['line_item_operation'] in ['PutMetricData', 'PutDashboard'],
            unit_price= 0.0025,
            comments= "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
            usage_divisor= 1000000
        ),

        CloudWatch_PricingRule(
            condition=lambda row: row['pricing_unit'] == 'Requests' and 
                                  row['line_item_operation'] == 'DeleteDashboards',
            unit_price=0,
            comments="Dashboards are free in OCI",
            usage_divisor=1
        ),
        CloudWatch_PricingRule(
            condition=lambda row: row['pricing_unit'] == 'GB' or row['pricing_unit'] == 'GB-Mo',
            unit_price=0.05,
            comments="$0.05 for Over 10 gigabytes log storage per month",
            usage_divisor=1
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Alarms',
            unit_price= 0.0015,
            comments= "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
            usage_divisor= 1000000
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Dashboards',
            unit_price= 0,
            comments= "Dashboards are free in OCI",
            usage_divisor= 1
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Minutes',
            unit_price= 0,
            comments= "Free",
            usage_divisor= 1
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Observations',
            unit_price= 0.0025,
            comments= "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
            usage_divisor= 1000000
        ),
        CloudWatch_PricingRule(
            condition= lambda row: row['pricing_unit'] == 'Runs',
            unit_price= 0.1,
            comments= "Synthetic Test Runs are billed in units of 10",
            usage_divisor= 1
        ),
    ]

    # Create the CloudWatch_PricingEngine and apply rules
    cw_pricing_engine = CloudWatch_PricingEngine(df, pricing_rules)
    cw_pricing_engine.apply_rules()

    # Save the updated DataFrame to an Excel file
    cw_output_file_path = "CloudWatch_Output.xlsx"
    df.to_excel(cw_output_file_path, index=False, engine="openpyxl")
    print("Excel file updated successfully!")

    # Open the file
    os.startfile(cw_output_file_path)


if __name__ == "__main__":
    CloudWatch_main()



#########################################################################################################################

#-------------Program Using Functions-------------------#


# import pandas as pd
# import os

# file_path = "Cloudwatch_excelfile.xlsx"
# df = pd.read_excel(file_path, engine="openpyxl")
# df['OCI Service'] = "OCI Monitoring & OCI Logging"
# df['Reference'] = "https://www.oracle.com/manageability/pricing/"


# pricing_rules = [
#     {
#         'condition': lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
#                                   row['line_item_operation'] in ['GetMetricData', 'GetMetricWidgetImage'],
#         'unit_price': 0.0015,
#         'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
#         'usage_divisor': 1000000
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] in ['Metric Update', 'Metrics'] and 
#                                   row['line_item_operation'] in [
#                                       'MetricUpdate', 'MetricStorage', 'MetricStorage:AWS/Logs-EMF',
#                                       'MetricStorage:AWS/EC2', 'MetricStorage:AWS/S3', 'MetricStorage:AWS/SES',
#                                       'MetricStorage:AWS/Beanstalk', 'MetricStorage:AWS/CloudWatchLogs',
#                                       'MetricStorage:AWS/ApiGateway'
#                                   ],
#         'unit_price' :0.0025,
#         'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
#         'usage_divisor': 1000000
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Requests' and 
#                                   row['line_item_operation'] in ['GetMetricStatistics', 'ListDashboards', 
#                                                                  'GetDashboard', 'ListMetrics'],
#         'unit_price': 0.0015,
#         'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
#         'usage_divisor': 1000000
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Requests' and 
#                                   row['line_item_operation'] in ['PutMetricData', 'PutDashboard'],
#         'unit_price': 0.0025,
#         'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
#         'usage_divisor': 1000000
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Requests' and 
#                                   row['line_item_operation'] == 'DeleteDashboards',
#         'unit_price': 0,
#         'comments': "Dashboards are free in OCI",
#         'usage_divisor': 1
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'GB' or row['pricing_unit'] == 'GB-Mo',
#         'unit_price': 0.05,
#         'comments': "$0.05 for Over 10 gigabytes log storage per month",
#         'usage_divisor': 1
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Alarms',
#         'unit_price': 0.0015,
#         'comments': "$0.0015 for Retrieval - Over 1 Billion Datapoints(1 request can have any num of datapoints)",
#         'usage_divisor': 1
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Dashboards',
#         'unit_price': 0,
#         'comments': "Dashboards are free in OCI",
#         'usage_divisor': 1
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'minutes',
#         'unit_price': 0,
#         'comments': "Free",
#         'usage_divisor': 1
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Observations',
#         'unit_price': 0.0025,
#         'comments': "$0.0025 for Ingestion - Over 500 Million Datapoints(1 Request can have any num of datapoints)",
#         'usage_divisor': 1000000
#     },
#     {
#         'condition': lambda row: row['pricing_unit'] == 'Runs',
#         'unit_price': 0.1,
#         'comments': "Synthetic Test Runs are billed in units of 10",
#         'usage_divisor': 1
#     },
# ]


# for index, row in df.iterrows():
#     for rule in pricing_rules:
#         if rule['condition'](row):
#             df.at[index, 'OCI Unit Price'] = rule['unit_price']
#             df.at[index, 'OCI Cost'] = row['SUM(line_item_usage_amount)'] * rule['unit_price'] / rule['usage_divisor']
#             df.at[index, 'Comments'] = rule['comments']
#             break 
#         else:
#             continue 


# df.to_excel("CloudWatch_Output.xlsx", index=False, engine="openpyxl")

# print("Excel file updated successfully!")

# os.startfile("CloudWatch_Output.xlsx")


#########################################################################################################################






