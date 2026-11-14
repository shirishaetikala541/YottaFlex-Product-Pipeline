# System Architecture

## Overview

The YottaFlex Supplier Data Pipeline follows a modular ETL (Extract, Transform, Load) architecture.

The pipeline collects product feeds from multiple suppliers with different schemas, transforms them into a unified format, validates data quality, resolves conflicts, and publishes a standardized product dataset with source traceability.

---

## Architecture Flow

Supplier A CSV  
        |  
Supplier B CSV  
        |  
Supplier C CSV  
        |  
        ↓  
Data Ingestion  
        |  
        ↓  
Data Transformation  
Schema Standardization  
        |  
        ↓  
Data Validation  
        |  
        ↓  
Conflict Resolution  
Supplier Priority Handling  
        |  
        ↓  
Reject Handling  
        |  
        ↓  
Output Dataset  
products.csv  
        |  
        ↓  
Run Metrics  
JSON Reports  

---

# System Components

## 1. Data Ingestion Module

File:

src/ingestion.py

Responsibilities:

- Reads product data from multiple supplier CSV files.
- Loads raw supplier data into the pipeline.
- Supports different supplier input formats.
- Maintains source file information for traceability.

---

## 2. Data Transformation Module

File:

src/transformation.py

Responsibilities:

- Maps different supplier column names.
- Converts supplier-specific schemas into a common schema.
- Standardizes product attributes.

Example:

Supplier formats:

Supplier A:
product_id, name, category, price, stock

Supplier B:
sku, product_name, type, cost, availability

Supplier C:
item_code, title, group_name, amount, quantity

Converted into:

product_id  
product_name  
category  
price  
stock_quantity  
source_supplier  
source_file  

---

## 3. Data Validation Module

File:

src/validation.py

Responsibilities:

- Checks mandatory fields.
- Validates product price.
- Detects invalid records.
- Identifies duplicate product IDs.

Validation rules:

- product_name cannot be empty.
- category cannot be empty.
- price must be greater than zero.
- Missing product IDs are rejected.
- Duplicate product IDs are detected and handled.

---

## 4. Conflict Resolution Module

Handled by:

src/pipeline.py

Responsibilities:

- Handles duplicate product records from multiple suppliers.
- Applies supplier priority rules.
- Selects the preferred product record.

Supplier priority:

supplier_a > supplier_b > supplier_c

This ensures consistent product selection when multiple suppliers provide the same product.

---

## 5. Reject Handling

Invalid records are identified during validation.

Rejected records contain:

- Product identifier.
- Validation failure reason.

Examples:

- Missing product name
- Invalid price
- Duplicate product_id

Rejected records are stored in:

data/quarantine/rejected_records.csv

---

## 6. Output Publishing

The final standardized dataset is generated as:

data/output/products.csv

Output schema:

product_id  
product_name  
category  
price  
stock_quantity  
source_supplier  
source_file  

The source_supplier and source_file fields maintain data lineage and identify the original source of each record.

---

## 7. Database Storage

The pipeline stores processed product data in SQLite database.

Database location:

data/product_pipeline.db

Database table:

products

Table columns:

product_id  
product_name  
category  
price  
stock_quantity  
source_supplier  
source_file  

---

## 8. Monitoring and Run Metrics

The pipeline generates monitoring files:

data/output/run_metrics.json

data/output/reconciliation_report.json

The metrics file contains:

- run_id
- execution status
- start time
- end time
- input record count
- output record count
- rejected record count
- execution time
- error details

The reconciliation report verifies:

Input Records = Output Records + Rejected Records + Duplicate Records Removed

This ensures reconciliation accounts for validation failures
and conflict resolution removals.
---

# Data Flow

1. Supplier systems provide product CSV feeds.
2. Data ingestion module reads supplier files.
3. Transformation module converts different schemas into a common format.
4. Validation module checks data quality rules.
5. Conflict resolution applies supplier priority rules.
6. Valid records are published as the final product dataset.
7. Processed data is stored in SQLite database.
8. Execution metrics and reconciliation reports are generated.

---

# Architecture Benefits

- Modular and maintainable design.
- Clear separation of responsibilities.
- Easy addition of new suppliers.
- Better data quality control.
- Source-level traceability.
- Easy testing and debugging.
- Supports future scalability.

---

# Future Scalability

The architecture can be extended with:

- API-based supplier ingestion.
- Cloud deployment.
- Distributed data processing systems.
- Advanced conflict resolution mechanisms.
- Enterprise database integration.
- Real-time data processing pipelines.