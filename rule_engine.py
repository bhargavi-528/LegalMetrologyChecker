import json


def load_rules():

    with open(
        "rules.json",
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)["rules"]


def check_rules(extracted):

    rules = load_rules()

    results = []

    present = 0
    missing = 0
    verify = 0

    for rule in rules:

        field = rule["field"]

        value = extracted.get(
            field,
            ""
        )

        if value:

            status = "PRESENT"
            present += 1

        else:

            status = "NEEDS VERIFICATION"
            verify += 1

        results.append({
            "id": rule["id"],
            "field": field,
            "label": rule["label"],
            "status": status,
            "value": value,
            "description": rule["description"]
        })

    total = len(results)

    if total:
        score = round(
            (present / total) * 100,
            1
        )
    else:
        score = 0

    if verify == 0:
        overall = "READY FOR REVIEW"
    else:
        overall = "REVIEW REQUIRED"

    return {
        "rules": results,
        "present": present,
        "missing": missing,
        "verify": verify,
        "total": total,
        "score": score,
        "overall": overall
    }