import pandas as pd
import os
from pymongo import MongoClient
from insights import process_insights
from network import process_network
from cognitive_services import process_cognitiveServices
from operational_insights import process_operationalInsights


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
        if sheet_name == "insights":
            df = process_insights(df, collection)
        elif sheet_name == "network":
            df = process_network(df, collection)
        elif sheet_name == "cognitiveServices":
            df = process_cognitiveServices(df)
        elif sheet_name == "operationalInsights":
            df = process_operationalInsights(df, collection)

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