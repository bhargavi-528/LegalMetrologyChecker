import re


def clean(value):
    if not value:
        return ""

    value = value.strip()
    value = re.sub(r"\s+", " ", value)

    return value


def search_pattern(patterns, text, flags=re.IGNORECASE):

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags
        )

        if match:
            return clean(match.group(1))

    return ""


def extract_information(text):

    lines = [
        clean(line)
        for line in text.splitlines()
        if clean(line)
    ]

    full_text = "\n".join(lines)

    information = {}

    # MRP
    information["mrp"] = search_pattern(
        [
            r"(?:MRP|M\.R\.P\.?)\s*[:\-]?\s*(?:Rs\.?|₹|INR)?\s*([0-9]+(?:\.[0-9]+)?)",
            r"(?:Rs\.?|₹|INR)\s*([0-9]+(?:\.[0-9]+)?)"
        ],
        full_text
    )

    # Net quantity
    information["net_quantity"] = search_pattern(
        [
            r"(?:Net\s*(?:Qty|Quantity)|Net\s*Wt|Net\s*Weight)\s*[:\-]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:kg|g|gm|ml|l|litre|liter|mg)?)",
            r"\b([0-9]+(?:\.[0-9]+)?)\s*(kg|g|gm|ml|l|litre|liter|mg)\b"
        ],
        full_text
    )

    # Manufacturer
    information["manufacturer"] = search_pattern(
        [
            r"(?:Manufactured\s*by|Manufactured\s*&|Manufacturer)\s*[:\-]?\s*(.+)",
            r"(?:Mfd\.?\s*by|Mfg\.?\s*by)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    # Packer
    information["packer"] = search_pattern(
        [
            r"(?:Packed\s*by|Packer)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    # Importer
    information["importer"] = search_pattern(
        [
            r"(?:Imported\s*by|Importer)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    # Country
    information["country_of_origin"] = search_pattern(
        [
            r"(?:Country\s*of\s*Origin|Made\s*in)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    # Batch
    information["batch_lot"] = search_pattern(
        [
            r"(?:Batch\s*(?:No|Number)?|Lot\s*(?:No|Number)?)\s*[:\-]?\s*([A-Za-z0-9\-/]+)"
        ],
        full_text
    )

    # Date
    date_value = search_pattern(
        [
            r"(?:Mfg|Manufacturing|Manufactured|Packed|Packing)\s*(?:Date|Dt)?\s*[:\-]?\s*([0-9]{1,2}[\/\-][0-9]{1,2}[\/\-][0-9]{2,4})",
            r"(?:Best\s*Before|Use\s*By|Expiry|Expires)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    information["date_information"] = date_value

    # Consumer care
    consumer = search_pattern(
        [
            r"(?:Consumer\s*Care|Customer\s*Care|Helpline|Toll\s*Free)\s*[:\-]?\s*(.+)",
            r"(?:Call|Contact)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    phone = re.search(
        r"\b(?:\+91[\s\-]?)?[6-9][0-9]{9}\b",
        full_text
    )

    if consumer:
        information["consumer_care"] = consumer
    elif phone:
        information["consumer_care"] = phone.group(0)
    else:
        information["consumer_care"] = ""

    # Product name
    product_name = search_pattern(
        [
            r"(?:Product\s*Name|Name\s*of\s*Product)\s*[:\-]?\s*(.+)",
            r"(?:Brand|Brand\s*Name)\s*[:\-]?\s*(.+)"
        ],
        full_text
    )

    # Fallback: first meaningful line
    if not product_name and lines:

        excluded = [
            "ingredients",
            "nutrition",
            "mrp",
            "manufactured",
            "packed",
            "country",
            "consumer",
            "batch"
        ]

        for line in lines:

            lower = line.lower()

            if (
                len(line) > 3
                and not any(word in lower for word in excluded)
            ):
                product_name = line
                break

    information["product_name"] = product_name

    # Confidence/uncertainty handling
    for key in information:
        information[key] = clean(
            information[key]
        )

    return information