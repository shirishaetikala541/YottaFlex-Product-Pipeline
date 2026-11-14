import pandas as pd


def validate_products(df):

    errors = []

    # Handle empty dataframe
    if df.empty:

        errors.append({
            "product_id": None,
            "error": "Empty input data"
        })

        return pd.DataFrame(errors)


    # Duplicate product ID check
    duplicates = df[
        df.duplicated(
            subset=["product_id"],
            keep=False
        )
    ]


    for _, row in duplicates.iterrows():

        errors.append({

            "product_id": row["product_id"],

            "error": "Duplicate product_id"

        })


    valid_categories = [
        "Electronics",
        "Accessories"
    ]


    for _, row in df.iterrows():


        if pd.isna(row["product_id"]) or str(row["product_id"]).strip() == "":

            errors.append({

                "product_id": row["product_id"],

                "error": "Missing product_id"

            })


        if pd.isna(row["product_name"]) or str(row["product_name"]).strip() == "":

            errors.append({

                "product_id": row["product_id"],

                "error": "Missing product name"

            })


        if pd.isna(row["price"]) or row["price"] <= 0:

            errors.append({

                "product_id": row["product_id"],

                "error": "Invalid price"

            })


        if pd.isna(row["category"]) or str(row["category"]).strip() == "":

            errors.append({

                "product_id": row["product_id"],

                "error": "Missing category"

            })

        elif row["category"] not in valid_categories:

            errors.append({

                "product_id": row["product_id"],

                "error": "Invalid category"

            })


    return pd.DataFrame(errors)