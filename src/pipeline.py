from src.ingestion import load_all_supplier_files

from src.transformation import (
    transform_supplier_a,
    transform_supplier_b,
    transform_supplier_c
)

from src.validation import validate_products

from src.db_loader import load_products_to_db

from src.logger import (
    create_run_metrics,
    create_reconciliation_report
)

import pandas as pd
import time
import os



def resolve_product_conflicts(df):
    """
    Resolves duplicate products using supplier priority.

    Priority:
    supplier_a > supplier_b > supplier_c
    """

    supplier_priority = {

        "supplier_a": 1,
        "supplier_b": 2,
        "supplier_c": 3

    }


    df["priority"] = df[
        "source_supplier"
    ].map(
        supplier_priority
    )


    df = df.sort_values(
        by=[
            "product_id",
            "priority"
        ]
    )


    df = df.drop_duplicates(
        subset=[
            "product_id"
        ],
        keep="first"
    )


    df = df.drop(
        columns=[
            "priority"
        ]
    )


    return df




def run_pipeline():

    start_time = time.time()


    os.makedirs(
        "data/output",
        exist_ok=True
    )


    os.makedirs(
        "data/quarantine",
        exist_ok=True
    )


    # -----------------------------
    # 1. Load supplier files
    # -----------------------------

    supplier_data = load_all_supplier_files()


    for supplier, data in supplier_data.items():

        if data is None:

            raise FileNotFoundError(
                f"Input file missing for {supplier}"
            )


    input_records = sum(
        len(df)
        for df in supplier_data.values()
    )



    # -----------------------------
    # 2. Transform supplier data
    # -----------------------------

    supplier_a = transform_supplier_a(
        supplier_data["supplier_a"]
    )


    supplier_b = transform_supplier_b(
        supplier_data["supplier_b"]
    )


    supplier_c = transform_supplier_c(
        supplier_data["supplier_c"]
    )


    combined_products = pd.concat(
        [
            supplier_a,
            supplier_b,
            supplier_c
        ],
        ignore_index=True
    )



    # -----------------------------
    # 3. Validation
    # -----------------------------

    errors = validate_products(
        combined_products
    )


    # Duplicate records are handled
    # during conflict resolution

    invalid_errors = errors[
        errors["error"] != "Duplicate product_id"
    ]


    rejected_records = len(
        invalid_errors
    )


    if not invalid_errors.empty:


        invalid_errors.to_csv(
            "data/quarantine/rejected_records.csv",
            index=False
        )


        rejected_ids = (
            invalid_errors["product_id"]
            .dropna()
            .unique()
        )


        valid_products = combined_products[
            ~combined_products["product_id"]
            .isin(rejected_ids)
        ]


    else:

        valid_products = combined_products.copy()



    # -----------------------------
    # 4. Conflict Resolution
    # -----------------------------

    final_products = resolve_product_conflicts(
        valid_products
    )


    output_records = len(
        final_products
    )


    duplicate_records = (
        input_records
        -
        rejected_records
        -
        output_records
    )



    # -----------------------------
    # 5. Save Output CSV
    # -----------------------------

    final_products.to_csv(
        "data/output/products.csv",
        index=False
    )



    # -----------------------------
    # 6. Load SQLite Database
    # -----------------------------

    load_products_to_db(
        final_products
    )



    # -----------------------------
    # 7. Generate Metrics
    # -----------------------------

    execution_time = round(
        time.time() - start_time,
        3
    )


    create_run_metrics(

        status="SUCCESS",

        input_records=input_records,

        output_records=output_records,

        rejected_records=rejected_records,

        execution_time_seconds=execution_time

    )


    create_reconciliation_report(

        input_records=input_records,

        output_records=output_records,

        rejected_records=rejected_records,

        duplicate_records=duplicate_records

    )



    print(
        "Output file created successfully."
    )


    print(
        f"Processed records: {output_records}"
    )


    return final_products