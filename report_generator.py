import json
import os
from datetime import datetime


def create_report(result):

    os.makedirs(
        "reports",
        exist_ok=True
    )

    filename = (
        "reports/report_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
        + ".json"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            result,
            file,
            indent=4,
            ensure_ascii=False
        )

    return filename