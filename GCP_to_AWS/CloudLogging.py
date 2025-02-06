import pandas as pd
import os
import region_mapping

class CloudWatch_PricingRule:
    """
    Represents a pricing rule with a condition, unit price, comments, and a usage divisor.
    """
    def __init__(self, region, configuration,condition, unit_price, comments, usage_divisor):
        self.region = region
        self.configuration = configuration
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
                    self.dataframe.at[index, 'AWS Unit Price'] = rule.unit_price
                    self.dataframe.at[index, 'AWS Cost'] = (
                        row['UsageAmount'] * rule.unit_price / rule.usage_divisor
                    )
                    self.dataframe.at[index, 'Comments'] = rule.comments
                    break 
                else:
                    continue

CLOUDWATCH_LOGS_STORAGE_PRICING = {
    'us-east-1': 0.50,      # US East (N. Virginia)
    'us-east-2': 0.50,      # US East (Ohio)
    'us-west-1': 0.67,      # US West (N. California)
    'us-west-2': 0.50,
    'ca-central-1': 0.55, 
    'ca-west-1': 0.55,
    'mx-central-1': 0.50,
    'us-gov-east-1': 0.675,  # AWS GovCloud (US-East)
    'us-gov-west-1': 0.675,      # US West (Oregon)
    'af-south-1': 0.63,     # Africa (Cape Town)
    'ap-east-1': 0.80,      # Asia Pacific (Hong Kong)
    'ap-south-2': 0.67, 
    'ap-southeast-3': 0.70, 
    'ap-southeast-5': 0.50, 
    'ap-southeast-4': 0.67,
    'ap-south-1': 0.67, 
    'ap-northeast-1': 0.76,  # Asia Pacific (Tokyo)
    'ap-northeast-2': 0.76,  # Asia Pacific (Seoul)
    'ap-northeast-3': 0.76,  # Asia Pacific (Osaka)
    'ap-southeast-1': 0.70,  # Asia Pacific (Singapore)
    'ap-southeast-2': 0.67,  # Asia Pacific (Sydney)
      # Canada (Central)
    'eu-central-1': 0.57,   # Europe (Frankfurt)
    'eu-west-1': 0.54,      # Europe (Ireland)
    'eu-west-2': 0.57,      # Europe (London)
    'eu-west-3': 0.57,      # Europe (Paris)
    'eu-north-1': 0.52,     # Europe (Stockholm)
    'eu-south-1': 0.57,     # Europe (Milan)
    'me-south-1': 0.60,     # Middle East (Bahrain)
    'sa-east-1': 0.65,  
      # AWS GovCloud (US-West)
}

def CloudWatch_main():
    # Load the input file
    file_path = "CloudLogging_excelfile.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    
    # Add default columns
    df['AWS Service'] = "Amazon Cloudwatch"
    df['Reference'] = "https://aws.amazon.com/cloudwatch/pricing/"
    df['AWS Region'] = df['Region'].map(region_mapping.gcp_aws_region_mapping)

    # Define pricing rules
    pricing_rules = [
        CloudLogging_PricingRule(   
            configuration = "Logs-Standard Storage" 
            condition=lambda row: row['SKUDescription'] in ['Log Storage cost'],                    
            unit_price=0.5,
            comments="standard Storage",
            usage_divisor=1
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