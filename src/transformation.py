import pandas as pd


def transform_supplier_a(df):
    transformed = pd.DataFrame()

    transformed["product_id"] = df["product_id"]
    transformed["product_name"] = df["name"]
    transformed["category"] = df["category"]
    transformed["price"] = df["price"]
    transformed["stock_quantity"] = df["stock"]

    transformed["source_supplier"] = "supplier_a"
    transformed["source_file"] = df["source_file"]

    return transformed



def transform_supplier_b(df):
    transformed = pd.DataFrame()

    transformed["product_id"] = df["sku"]
    transformed["product_name"] = df["product_name"]
    transformed["category"] = df["type"]
    transformed["price"] = df["cost"]
    transformed["stock_quantity"] = df["availability"]

    transformed["source_supplier"] = "supplier_b"
    transformed["source_file"] = df["source_file"]

    return transformed



def transform_supplier_c(df):
    transformed = pd.DataFrame()

    transformed["product_id"] = df["item_code"]
    transformed["product_name"] = df["title"]
    transformed["category"] = df["group_name"]
    transformed["price"] = df["amount"]
    transformed["stock_quantity"] = df["quantity"]

    transformed["source_supplier"] = "supplier_c"
    transformed["source_file"] = df["source_file"]

    return transformed