import pandas as pd
import random
import os


random.seed(42)


def generate_supplier_data(records=100, supplier="supplier_a"):
    """
    Generates synthetic supplier product data
    with supplier-specific schemas.
    """

    products = [
        "Laptop",
        "Mobile",
        "Headphones",
        "Keyboard",
        "Mouse",
        "Monitor"
    ]

    categories = [
        "Electronics",
        "Accessories"
    ]

    data = []

    for i in range(records):

        product_number = i + 1

        if supplier == "supplier_a":

            row = {
                "product_id": f"A{product_number}",
                "name": random.choice(products),
                "category": random.choice(categories),
                "price": random.randint(500, 60000),
                "stock": random.randint(1, 100)
            }

            # Inject invalid records for validation testing
            if product_number == 10:
                row["price"] = -500

            if product_number == 20:
                row["name"] = ""

            if product_number == 30:
                row["category"] = "INVALID_CATEGORY"


        elif supplier == "supplier_b":

            row = {
                "sku": f"A{product_number}" if product_number <= 100 else f"B{product_number}",
                "product_name": random.choice(products),
                "type": random.choice(categories),
                "cost": random.randint(500, 60000),
                "availability": random.randint(1, 100)
            }


        elif supplier == "supplier_c":

            row = {
                "item_code": f"A{product_number}" if product_number <= 100 else f"C{product_number}",
                "title": random.choice(products),
                "group_name": random.choice(categories),
                "amount": random.randint(500, 60000),
                "quantity": random.randint(1, 100)
            }


        else:
            raise ValueError(
                "Invalid supplier name. Use supplier_a, supplier_b, or supplier_c."
            )

        data.append(row)

    return pd.DataFrame(data)



def generate_dataset(records=100000):
    """
    Generates supplier CSV files for testing the pipeline.
    """

    os.makedirs(
        "data/input",
        exist_ok=True
    )

    supplier_a = generate_supplier_data(
        records,
        "supplier_a"
    )

    supplier_b = generate_supplier_data(
        records,
        "supplier_b"
    )

    supplier_c = generate_supplier_data(
        records,
        "supplier_c"
    )


    supplier_a.to_csv(
        "data/input/supplier_a.csv",
        index=False
    )

    supplier_b.to_csv(
        "data/input/supplier_b.csv",
        index=False
    )

    supplier_c.to_csv(
        "data/input/supplier_c.csv",
        index=False
    )


    print(
        f"Generated {records} records for each supplier."
    )

    print(
        "Files created: supplier_a.csv, supplier_b.csv, supplier_c.csv"
    )



if __name__ == "__main__":

    generate_dataset(100000)