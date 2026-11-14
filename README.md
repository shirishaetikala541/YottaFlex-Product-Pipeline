
# YottaFlex Supplier Data Pipeline

## Project Overview

This project is a Python-based supplier data processing pipeline that combines product feeds from multiple suppliers with different schemas and formats.

The pipeline ingests supplier files, standardizes different schemas into a common structure, validates data quality, resolves conflicts, maintains source-level traceability, and publishes clean output datasets.

The solution is designed to be reproducible, testable, and capable of handling large supplier datasets efficiently.

---

# Architecture Workflow

Supplier Data Sources
        |
        v
Data Ingestion
        |
        v
Data Transformation
(Schema Standardization)
        |
        v
Validation and Quality Checks
        |
        v
Duplicate Conflict Resolution
        |
        v
Reject / Quarantine Handling
        |
        v
Output Publishing
        |
        +----------------+
        |                |
        v                v

    CSV Output      SQLite Database

        |
        v

Run Metrics and Reconciliation Reports

---

# Project Structure

YottaFlex-Product-Pipeline

|
├── data
│   ├── input
│   ├── output
│   └── quarantine
│
├── src
│   ├── ingestion.py
│   ├── transformation.py
│   ├── validation.py
│   ├── logger.py
│   ├── database.py
│   ├── db_loader.py
│   └── pipeline.py
│
├── tests
│   ├── test_pipeline.py
│   └── test_ingestion.py
│
├── docs
│   ├── architecture.md
│   ├── design_notes.md
│   ├── data_dictionary.md
│   └── ai_prompt_history.md
│
├── generate_data.py
├── run_pipeline.py
├── requirements.txt
├── AI_USAGE.md
└── README.md


Note:

- data/input, data/output, quarantine files, and database files are generated during execution.
- Generated runtime data is excluded from Git tracking using .gitignore.

---

# Features

- Reads multiple supplier product feeds
- Handles different supplier schemas
- Converts data into a standardized target schema
- Maintains source-level traceability
- Tracks source supplier and source file information
- Performs data validation checks
- Handles missing required fields
- Detects duplicate product identifiers
- Resolves supplier conflicts using priority rules
- Stores invalid records in quarantine
- Generates operational run metrics
- Generates reconciliation reports
- Supports idempotent reruns
- Supports large-scale synthetic dataset generation
- Stores standardized data in SQLite database
- Includes automated pytest tests

---

# Key Highlights

- Built an end-to-end ETL pipeline using Python and Pandas
- Processed 300K supplier records with validation, rejection handling, and conflict resolution
- Implemented schema validation and standardization
- Added supplier conflict resolution using priority rules
- Implemented automated testing using pytest
- Added idempotent rerun capability
- Generated reconciliation and operational reports
- Stored processed data in SQLite database

---

# Technologies Used

- Python
- Pandas
- SQLite
- Pytest
- CSV Data Processing
- JSON Report Generation
- Git

---
# Installation

Clone repository:

git clone <repository-url>

cd YottaFlex-Product-Pipeline

Create virtual environment:

python -m venv venv

Activate virtual environment:

Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

---

# Running the Pipeline

Generate supplier data:

python generate_data.py

Run pipeline:

python run_pipeline.py

Run automated tests:

pytest

---

# Data Generation

The project includes a synthetic supplier data generator.

Generate scalable supplier data:

python generate_data.py

Generate a small sample dataset for quick testing:

python -c "from generate_data import generate_dataset; generate_dataset(100)"

Generate a larger dataset for performance testing:

python generate_data.py

The generator creates:

- supplier_a.csv
- supplier_b.csv
- supplier_c.csv

The generated data uses a fixed random seed to ensure reproducible results.

---

# Generated Output

After successful execution, the pipeline generates the following outputs.

## CSV Output

Location:

data/output/products.csv

Contains the final standardized product dataset.

Sample output:

A small reproducible output sample is available at:

sample_output/products_sample.csv

The complete output is generated during pipeline execution at:

data/output/products.csv

---

## SQLite Database

Location:

data/product_pipeline.db

Stores standardized product records for analytical querying.

SQLite is used as a lightweight relational storage layer for processed product data.

---

## Run Metrics

Location:

data/output/run_metrics.json

Contains:

- run_id
- start_time
- end_time
- execution status
- input record count
- output record count
- rejected record count
- execution time
- failure details

---

## Reconciliation Report

Location:

data/output/reconciliation_report.json

Contains:

- input count
- output count
- rejected count
- reconciliation status

Sample reconciliation report:

A sample validation report is available at:

sample_output/reconciliation_report_sample.json

This report demonstrates input-output reconciliation and duplicate handling results.

---

## Quarantine Records

Location:

data/quarantine/rejected_records.csv

Stores invalid or rejected records with source traceability information.

---

# Output Schema

The standardized product schema contains:

| Column | Description |
|---|---|
| product_id | Unique product identifier |
| product_name | Standardized product name |
| category | Product category |
| price | Product price |
| stock_quantity | Available inventory quantity |
| source_supplier | Original supplier name |
| source_file | Original input file |

---

# Conflict Resolution

Duplicate products are resolved using supplier priority.

Priority:

supplier_a > supplier_b > supplier_c

Rules:

1. Duplicate product IDs are detected.
2. Supplier priority is evaluated.
3. Highest priority supplier record is retained.
4. Lower priority duplicate records are removed.

This ensures deterministic and repeatable results.

---

# Conflict Resolution Evidence

The test dataset included overlapping product identifiers across suppliers.

Detected overlapping product identifiers:

- Supplier A and Supplier B: 100 overlapping IDs
- Supplier A and Supplier C: 100 overlapping IDs
- Supplier B and Supplier C: 100 overlapping IDs

After applying supplier priority rules:

- Input records: 300000
- Output records: 299797
- Rejected records: 3
- Duplicate records removed: 200

Example:

Product ID A1 existed in multiple supplier feeds.

Since supplier_a has the highest priority, the supplier_a record was retained and lower priority duplicate records were removed.

---


**---**

# Idempotency and Recovery Behavior

The pipeline is designed to support safe reruns with the same input data.

Idempotency approach:

- Each execution generates a unique run_id for tracking.
- Product records are processed using deterministic transformation rules.
- Duplicate product identifiers are resolved consistently using supplier priority rules.
- Rerunning the same input does not create unintended duplicate output records.

Retry and restart behavior:

- Failed executions are captured through run metrics with failure details.
- The pipeline can be restarted from the beginning using the same input files.
- Previously generated outputs can be regenerated deterministically.

Backfill behavior:

- Historical supplier files can be reprocessed by placing them in the input directory and executing the pipeline again.
- Generated run metrics allow tracking of each execution separately.

---

# Performance Benchmark

The pipeline was tested using generated large-scale supplier data.

Dataset:

- 3 supplier files
- 100,000 records per supplier
- 300,000 total records

Execution Environment:

- Python
- Pandas
- SQLite
- Local development environment

Execution Result:

Input Records: 300000  
Output Records: 299797  
Rejected Records: 3  
Duplicates Removed: 200  
Status: SUCCESS

The pipeline successfully processes large datasets while maintaining validation, conflict resolution, source traceability, and consistent output generation.

---

# Performance Optimization

Current implementation uses Pandas and CSV-based processing.

Possible future optimizations:

- Use Parquet format for faster columnar storage
- Use vectorized validation for large-scale datasets
- Use chunk-based processing for datasets larger than available memory
- Introduce distributed processing frameworks for very large workloads

---

# Assumptions

- Supplier data is provided as CSV files.
- Each supplier may have different schemas.
- product_id is considered the unique business key.
- Supplier priority rules are used to resolve duplicate conflicts.
- Synthetic supplier data is used for reproducible testing.
- Input files follow expected supplier formats.
- SQLite is used as the local analytical storage layer.

---

# Known Limitations

- Supports CSV files only.
- Distributed processing is not implemented.
- Real-time streaming ingestion is not implemented.
- Advanced product matching using machine learning is not implemented.
- Output schema currently does not include:
  - currency
  - updated_at
  - source_row

These fields are identified as future improvements for enhanced source traceability and multi-currency support.

- Late-arriving and out-of-order data handling is not implemented because source timestamps are not currently available in the dataset.

---

# Future Improvements

Possible improvements:

- Add API-based supplier ingestion
- Add cloud deployment support
- Add distributed processing using Spark or similar frameworks
- Add real-time streaming ingestion
- Implement advanced product matching algorithms
- Add monitoring dashboards
- Add automated data quality alerting
- Support additional file formats such as JSON and Parquet

---

# AI Assistance

AI tools were used for:

- Requirement analysis
- Architecture discussion
- Documentation refinement
- Identifying validation scenarios
- Improving implementation approaches

All AI-generated suggestions were reviewed, modified where required, implemented, tested, and verified manually.

AI was used only as an assistance tool and not as a replacement for development, debugging, testing, or decision-making.

Detailed information is available in:

AI_USAGE.md

---

# License

This project is developed for technical evaluation and learning purposes.