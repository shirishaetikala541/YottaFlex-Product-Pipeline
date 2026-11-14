from src.ingestion import load_all_supplier_files


def test_load_all_supplier_files():

    data = load_all_supplier_files()

    assert data is not None

    assert "supplier_a" in data
    assert "supplier_b" in data
    assert "supplier_c" in data

    for supplier, df in data.items():

        assert df is not None
        assert len(df) > 0
        assert "source_file" in df.columns