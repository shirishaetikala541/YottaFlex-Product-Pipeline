from src.database import get_connection, create_tables


def load_products_to_db(products):

    create_tables()

    connection = get_connection()

    # Clear existing data for idempotent reruns
    connection.execute(
        "DELETE FROM products"
    )

    connection.commit()

    products.to_sql(
        "products",
        connection,
        if_exists="append",
        index=False
    )

    connection.close()

    print(
        "Products loaded into SQLite database successfully."
    )