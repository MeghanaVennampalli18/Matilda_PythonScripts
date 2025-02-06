import pandas as pd
import os

class DynamoDB_PricingRule:
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


class DynamoDB_PricingEngine:
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
                        row['usageAmount'] * rule.unit_price / rule.usage_divisor
                    )
                    self.dataframe.at[index, 'Comments'] = rule.comments
                    break 
                else:
                    continue


def DynamoDB_main():
    # Load the input file
    file_path = "DynamoDB_excelfile.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    
    # Add default columns
    df['OCI Service'] = "OCI NoSQL Database"
    df['Reference'] = "https://www.oracle.com/database/nosql/pricing/#on-demand-capacity-pricing"

    # Define pricing rules
    pricing_rules = [
        DynamoDB_PricingRule(
            condition=lambda row: row['BillingUnit'] in ['GB-Mo', 'GB','GB-Month'],
            unit_price=0.066,
            comments="$0.066 for on demand capacity - Storage ",
            usage_divisor=1
        ),
        DynamoDB_PricingRule(
            condition=lambda row: row['BillingUnit'] in ['Read Requests', 'Requests'],
            unit_price=0.16,
            comments="$0.16 for On-Demand Capacity – Read",
            usage_divisor=1000000
        ),
        DynamoDB_PricingRule(
            condition= lambda row: row['BillingUnit'] == 'ReadCapacityUnit-Hrs',
            unit_price= 0.0064,
            comments= "$0.0064/744 per hour for Provisioned Capacity-Read",
            usage_divisor= 744
        ),
        DynamoDB_PricingRule(
            condition= lambda row: row['BillingUnit'] in ['Write Requests','ChangeDataCaptureUnits'],
            unit_price= 3.135,
            comments= "$3.135 for on Demand Capacity – Write",
            usage_divisor= 1000000
        ),

        DynamoDB_PricingRule(
            condition=lambda row: row['BillingUnit'] == 'WriteCapacityUnit-Hrs',
            unit_price=0.1254,
            comments="$0.1254/744 for Provisioned Capacity – Write",
            usage_divisor=744
        ),
        DynamoDB_PricingRule(
            condition=lambda row: row['BillingUnit'] == 'ReplicatedWriteRequestUnits',
            unit_price=0.36,
            comments="$0.36 for On Demand Capacity - Regional Replicated Write",
            usage_divisor=1000000
        ),
        DynamoDB_PricingRule(
            condition= lambda row: row['BillingUnit'] == 'ReplicatedWriteCapacityUnit-Hrs',
            unit_price= 0.36,
            comments= "$0.36/744 per hour for provisioned capacity - Regional Replicated Write",
            usage_divisor= 744
        ),
    ]

    # Create the DynamoDB_PricingEngine and apply rules
    dynamodb_pricing_engine = DynamoDB_PricingEngine(df, pricing_rules)
    dynamodb_pricing_engine.apply_rules()

    # Save the updated DataFrame to an Excel file
    dynamodb_output_file_path = "DynamoDB_Output.xlsx"
    df.to_excel(dynamodb_output_file_path, index=False, engine="openpyxl")
    print("Excel file updated successfully!")

    # Open the file
    os.startfile(dynamodb_output_file_path)


if __name__ == "__main__":
    DynamoDB_main()