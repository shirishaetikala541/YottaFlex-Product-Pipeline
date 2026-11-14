import pandas as pd

from src.pipeline import (
    run_pipeline,
    resolve_product_conflicts
)

from src.validation import validate_products



def test_pipeline_output():

    result = run_pipeline()

    assert result is not None

    required_columns = [
        "product_id",
        "product_name",
        "category",
        "price",
        "stock_quantity",
        "source_supplier",
        "source_file"
    ]

    for column in required_columns:
        assert column in result.columns

    assert len(result) > 0



def test_duplicate_product_id():

    data = pd.DataFrame(
        {
            "product_id": ["A101", "A101"],
            "product_name": ["Laptop", "Laptop"],
            "category": [
                "Electronics",
                "Electronics"
            ],
            "price": [
                50000,
                50000
            ],
            "stock_quantity": [
                10,
                10
            ]
        }
    )

    errors = validate_products(data)

    assert (
        "Duplicate product_id"
        in errors["error"].values
    )



def test_missing_product_name():

    data = pd.DataFrame(
        {
            "product_id": ["A102"],
            "product_name": [""],
            "category": [
                "Electronics"
            ],
            "price": [
                30000
            ],
            "stock_quantity": [
                5
            ]
        }
    )

    errors = validate_products(data)

    assert (
        "Missing product name"
        in errors["error"].values
    )



def test_invalid_price():

    data = pd.DataFrame(
        {
            "product_id": ["A103"],
            "product_name": [
                "Mobile"
            ],
            "category": [
                "Electronics"
            ],
            "price": [
                -100
            ],
            "stock_quantity": [
                5
            ]
        }
    )

    errors = validate_products(data)

    assert (
        "Invalid price"
        in errors["error"].values
    )



def test_empty_input():

    empty_data = pd.DataFrame(
        columns=[
            "product_id",
            "product_name",
            "category",
            "price",
            "stock_quantity"
        ]
    )

    errors = validate_products(empty_data)

    assert (
        "Empty input data"
        in errors["error"].values
    )



def test_malformed_record():

    data = pd.DataFrame(
        {
            "product_id": ["A104"],
            "product_name": [
                "Laptop"
            ],
            "price": [
                50000
            ]
        }
    )

    try:
        validate_products(data)
        assert False

    except KeyError:
        assert True



def test_null_product_id():

    data = pd.DataFrame(
        {
            "product_id": [None],
            "product_name": [
                "Laptop"
            ],
            "category": [
                "Electronics"
            ],
            "price": [
                50000
            ],
            "stock_quantity": [
                10
            ]
        }
    )

    errors = validate_products(data)

    assert (
        "Missing product_id"
        in errors["error"].values
    )



def test_unexpected_schema_change():

    data = pd.DataFrame(
        {
            "wrong_id": [
                "A105"
            ],
            "name": [
                "Mobile"
            ],
            "cost": [
                20000
            ]
        }
    )

    try:
        validate_products(data)
        assert False

    except KeyError:
        assert True



def test_conflict_resolution_priority():

    data = pd.DataFrame(
        {
            "product_id": [
                "A101",
                "A101",
                "A101"
            ],
            "product_name": [
                "Laptop",
                "Laptop",
                "Laptop"
            ],
            "category": [
                "Electronics",
                "Electronics",
                "Electronics"
            ],
            "price": [
                51000,
                52000,
                50000
            ],
            "stock_quantity": [
                10,
                10,
                10
            ],
            "source_supplier": [
                "supplier_c",
                "supplier_b",
                "supplier_a"
            ]
        }
    )


    result = resolve_product_conflicts(data)


    assert len(result) == 1

    assert (
        result.iloc[0]["source_supplier"]
        ==
        "supplier_a"
    )