import pandas as pd
import os


def read_supplier_file(file_path):
    """
    Reads supplier CSV file and returns dataframe
    with source file information
    """
    try:
        df = pd.read_csv(file_path)

        # Add source file name for traceability
        df["source_file"] = os.path.basename(file_path)

        return df

    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None



def load_all_supplier_files():
    """
    Loads all supplier input files
    """

    supplier_files = {
        "supplier_a": "data/input/supplier_a.csv",
        "supplier_b": "data/input/supplier_b.csv",
        "supplier_c": "data/input/supplier_c.csv"
    }

    supplier_data = {}

    for supplier, file_path in supplier_files.items():
        data = read_supplier_file(file_path)
        supplier_data[supplier] = data

    return supplier_data