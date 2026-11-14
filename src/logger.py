import json
import os
from datetime import datetime
import uuid


def create_run_metrics(
    status,
    input_records,
    output_records,
    rejected_records,
    execution_time_seconds=None,
    error=None,
    start_time=None
):

    if start_time is None:
        start_time = datetime.now().isoformat()


    end_time = datetime.now().isoformat()


    metrics = {

        "run_id": str(uuid.uuid4()),

        "start_time": start_time,

        "end_time": end_time,

        "status": status,

        "input_records": input_records,

        "output_records": output_records,

        "rejected_records": rejected_records,

        "execution_time_seconds": execution_time_seconds,

        "error": error
    }


    os.makedirs(
        "data/output",
        exist_ok=True
    )


    with open(
        "data/output/run_metrics.json",
        "w"
    ) as file:

        json.dump(
            metrics,
            file,
            indent=4
        )


    return metrics



def create_reconciliation_report(
    input_records,
    output_records,
    rejected_records,
    duplicate_records=0
):

    difference = (
        input_records
        -
        (
            output_records
            + rejected_records
            + duplicate_records
        )
    )


    report = {

        "status": "PASS"
        if difference == 0
        else "FAIL",

        "input_records": input_records,

        "output_records": output_records,

        "rejected_records": rejected_records,

        "duplicate_records_removed": duplicate_records,

        "difference": difference
    }


    os.makedirs(
        "data/output",
        exist_ok=True
    )


    with open(
        "data/output/reconciliation_report.json",
        "w"
    ) as file:

        json.dump(
            report,
            file,
            indent=4
        )


    return report