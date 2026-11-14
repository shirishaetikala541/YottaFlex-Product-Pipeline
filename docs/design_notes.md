# Design Notes

## Design Approach

The pipeline is designed as a modular data processing system.

The solution separates different responsibilities into independent modules:

- Ingestion module for reading supplier files
- Transformation module for schema standardization
- Validation module for data quality checks
- Logging module for execution metrics and monitoring
- Pipeline module for orchestration

This modular design improves maintainability, testing, and future scalability.

---

## Data Processing Flow

1. Supplier CSV files are read from input sources.
2. Each supplier data format is transformed into a common schema.
3. Standardized records are combined into a unified dataset.
4. Data quality validations are performed.
5. Invalid records are moved to quarantine storage.
6. Valid records are published as final output.
7. Reconciliation reports and execution metrics are generated.

---

# Design Decisions

## Modular Architecture

Separate modules were created instead of writing all logic in a single file.

Benefits:

- Better maintainability
- Easier debugging
- Simple testing
- Future scalability

---

## CSV Based Input

CSV files were selected as the input source because:

- Easy to reproduce locally
- Suitable for supplier feed simulation
- Requires no external infrastructure

Trade-off:

- CSV storage has limitations for very large production workloads and high-frequency data processing.

---

## Source Traceability

The field `source_supplier` is maintained in the output dataset.

This helps identify:

- Original supplier source
- Data lineage
- Debugging issues

Source traceability is maintained for all retained output records using source_supplier and source_file fields.

---

## Validation Strategy

Invalid records are identified using business rules:

- Missing mandatory fields
- Invalid prices
- Duplicate product IDs
- Schema consistency checks

Invalid records are stored separately in:

```
data/quarantine/rejected_records.csv
```

This prevents poor quality data from reaching downstream consumers.

---

## Idempotency Design

The pipeline is designed to be idempotent.

For every execution:

- Source files are read again
- Output files are regenerated
- Existing output is replaced instead of appending duplicate records

This ensures rerunning the pipeline with the same input produces the same result.

---

## Conflict Resolution Strategy

When the same product is received from multiple suppliers, duplicate records are resolved using supplier priority rules.

Current priority:

1. supplier_a
2. supplier_b
3. supplier_c

The highest priority supplier record is selected and duplicate product IDs are removed.

This approach:

- Provides deterministic output.
- Prevents duplicate products.
- Maintains source traceability using source_supplier and source_file fields.

Future versions can implement more advanced strategies such as:
- Latest supplier update priority.
- Data quality based ranking.
- Confidence scoring.

---

## Reconciliation Strategy

A reconciliation report is generated after every pipeline execution.

The report validates:

- Total input records
- Total output records
- Rejected records
- Record count differences

Example output:

```
status: PASS
input_records: 300000
output_records: 299797
rejected_records: 3
duplicate_records_removed: 200
difference: 0
```

This provides confidence that the transformation process completed correctly.

---

## Performance Monitoring

The pipeline captures execution time during every run.

Execution metrics include:

- Run ID
- Start time
- Input record count
- Output record count
- Rejected record count
- Execution time

Metrics are stored in:

```
data/output/run_metrics.json
```

Optimization:

Pandas vectorized operations are used for transformation and cleaning instead of row-by-row processing.

---

# Trade-offs

## CSV Storage vs Database

Chosen:

CSV files for input and output exchange

SQLite for storing standardized processed data and analytical querying

Advantages:

- Simple setup
- Easy testing
- No external dependencies

Trade-off:

- Limited scalability for very large production workloads

---

## Local Processing vs Distributed Processing

Chosen:

Local Python processing

Advantages:

- Faster development
- Easy execution
- Suitable for the challenge scope

Trade-off:

- Not optimized for very large datasets

---

## Rule Based Validation vs Machine Learning Validation

Chosen:

Rule based validation

Advantages:

- Deterministic results
- Easy to explain
- Simple maintenance

Trade-off:

- Cannot automatically learn new data patterns

---

# Error Handling Strategy

The pipeline captures:

- Validation failures
- Rejected records
- Execution metrics
- Processing status

Invalid records are isolated without stopping the complete processing flow.

---

# Future Enhancements

Possible improvements:

- PostgreSQL or MySQL integration
- API based supplier ingestion
- Cloud deployment
- Advanced conflict resolution
- Large scale distributed processing
- Support for larger datasets