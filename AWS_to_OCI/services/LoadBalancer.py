import pandas as pd
import os

class LoadBalancer_PricingRule:
    """
    Represents a pricing rule with a condition, unit price, comments, and a usage divisor.
    """
    def __init__(self, condition, unit_price, comments, usage_divisor, is_lcu_rule=False):
        self.condition = condition
        self.unit_price = unit_price
        self.comments = comments
        self.usage_divisor = usage_divisor
        self.is_lcu_rule = is_lcu_rule

    def applies_to(self, row):
        """
        Checks if the rule applies to a given row.
        """
        return self.condition(row)


class LoadBalancer_PricingEngine:
    """
    Encapsulates the pricing logic and applies pricing rules to a DataFrame.
    """
    def __init__(self, dataframe, pricing_rules):
        self.dataframe = dataframe
        self.pricing_rules = pricing_rules

    def calculate_bandwidth_cost(self, usage_amount):
        """
        Calculates bandwidth cost for LCU-Hrs based on 2.27 Mbps/GB rate.
        """
        return usage_amount * 2.27 * 0.0001  # Bandwidth cost calculation    

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

                    # if rule.is_lcu_rule and row['pricing_unit'] == 'LCU-Hrs':
                    #     self.dataframe.at[index, 'OCI Cost'] = (
                    #         row['SUM(line_item_usage_amount)'] * rule.unit_price / rule.usage_divisor
                    #     ) + self.calculate_bandwidth_cost(row['SUM(line_item_usage_amount)'])
                    # else:
                    #     self.dataframe.at[index, 'OCI Cost'] = (
                    #         row['SUM(line_item_usage_amount)'] * rule.unit_price / rule.usage_divisor
                    # )

                    self.dataframe.at[index, 'Comments'] = rule.comments
                    break
                else:
                    continue

def LoadBalancer_main():
    # Load the input file
    file_path = "LoadBalancer_excelfile.xlsx"
    df = pd.read_excel(file_path, engine="openpyxl")
    
    # Add default columns
    df['OCI Service'] = "OCI Load Balancer"
    df['Reference'] = "https://www.oracle.com/cloud/networking/pricing/"

    # Define pricing rules
    pricing_rules = [
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation'] in ['LoadBalancing:Network','LoadBalancing-NLB-PublicIP-In'],
            unit_price=0,
            comments="Network Load Balancer is Free in OCI",
            usage_divisor=1
        ),
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation'] == 'LoadBalancing-PublicIP-In',
            unit_price=0,
            comments="Inbound Data Transfer is Free in OCI",
            usage_divisor=1
        ),
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation'] in ['LoadBalancing:Application','LoadBalancing'] and row['pricing_unit'] in ['Hrs','LCU-Hrs'],
            unit_price=0.0113,
            comments="$0.0113 for Oracle Cloud Infrastructure - Load Balancer Base - Load Balancer Hour",
            usage_divisor=1
        ),
        # LoadBalancer_PricingRule(
        #     condition=lambda row: row['line_item_operation'] in ['LoadBalancing:Application','LoadBalancing'] and row['pricing_unit'] == 'LCU-Hrs',
        #     unit_price=0.0113,
        #     comments="$0.0113 for Load Balancer Hour + $0.0001 for Bandwidth mbps",
        #     usage_divisor=1,
        #     is_lcu_rule=True
        # ),
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation'] in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                                  row['line_item_usage_type'].startswith(('US', 'EU', 'DA', 'CA')) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
            unit_price=0.0085,
            comments="Outbound Data Transfer - Originating in North America, Europe, and UK",
            usage_divisor=1000000
        ),
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation']  in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                                  row['line_item_usage_type'].startswith(('AP','SA')) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
            unit_price=0.025,
            comments="Outbound Data Transfer - Originating in APAC, Japan, and South America",
            usage_divisor=1000000
        ),
        LoadBalancer_PricingRule(
            condition=lambda row: row['line_item_operation'] in ['LoadBalancing','LoadBalancing-NLB-PublicIP-Out','LoadBalancing-PublicIP-Out'] and 
                                  row['line_item_usage_type'].startswith(('AF','ME' )) and row['pricing_unit']=='GB' and 'regional' not in row['line_item_line_item_description'],
            unit_price=0.05,
            comments="Outbound Data Transfer - Originating in Middle East and Africa",
            usage_divisor=1000000
        ),
        LoadBalancer_PricingRule(
            condition=lambda row: 'regional' in row['line_item_line_item_description'],
            unit_price=0,
            comments="Regional Data Transfer is free in OCI",
            usage_divisor=1
        ),
    ]

    # Create the LoadBalancer_PricingEngine and apply rules
    elb_pricing_engine = LoadBalancer_PricingEngine(df, pricing_rules)
    elb_pricing_engine.apply_rules()

    # Save the updated DataFrame to an Excel file
    elb_output_file_path = "LoadBalancer_Output.xlsx"
    df.to_excel(elb_output_file_path, index=False, engine="openpyxl")
    print("Excel file updated successfully!")

    # Open the file
    os.startfile(elb_output_file_path)


if __name__ == "__main__":
    LoadBalancer_main()

