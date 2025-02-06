import pandas as pd
import os
from pymongo import MongoClient
from dynamodb import process_dynamodb
from cloudwatch import process_cloudwatch
from elb import process_elb

def main():
    # Connect to MongoDB
    client = MongoClient("mongodb://admin:Matilda7%23@172.24.6.190:30020")
    db = client['matildacost']
    collection = db['mcost_oci']

    # Read the main input Excel file
    input_file = "Main_Input.xlsx"
    output_file = "Main_Output.xlsx"

    # Read all sheets into a dictionary of DataFrames
    sheets_dict = pd.read_excel(input_file, sheet_name=None, engine="openpyxl")

    # Process each sheet
    for sheet_name, df in sheets_dict.items():
        df['SUM(line_item_usage_amount)'] = pd.to_numeric(df['SUM(line_item_usage_amount)'], errors='coerce').fillna(0)

        if sheet_name == "dynamodb":
            df = process_dynamodb(df, collection)
        elif sheet_name == "cloudwatch":
            df = process_cloudwatch(df, collection)
        elif sheet_name == "elb":
            df = process_elb(df, collection)

        # Update the sheet in the dictionary
        sheets_dict[sheet_name] = df

    # Write all sheets to a new Excel file
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        for sheet_name, df in sheets_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

    print("Excel file updated successfully!")
    os.startfile(output_file)

    # Close the MongoDB connection
    client.close()

if __name__ == "__main__":
    main()