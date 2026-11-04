"""Limpia y estandariza los registros de ventas con Pandas."""

import re
import unicodedata
from datetime import datetime
from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"
OUTPUT_COLUMNS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
]


def _normalize_header(header):
    header = header.replace("\ufeff", "").strip().lower()
    return re.sub(r"\s+", "_", header)


def _clean_text(value):
    if pd.isna(value):
        return pd.NA
    return re.sub(r"\s+", " ", str(value)).strip()


def _clean_city(value):
    cleaned = _clean_text(value)
    if pd.isna(cleaned):
        return pd.NA
    normalized = unicodedata.normalize("NFKD", cleaned.casefold())
    unaccented = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    canonical = {
        "bogota": "Bogotá",
        "medellin": "Medellín",
        "sopo": "Sopó",
        "tenjo": "Tenjo",
    }
    return canonical.get(unaccented, cleaned)


def _parse_date(value):
    if pd.isna(value) or not str(value).strip():
        return pd.NA

    value = str(value).strip()
    formats = (
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%y",
        "%d.%m.%Y",
    )
    for date_format in formats:
        try:
            return datetime.strptime(value, date_format).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return pd.NA


def _parse_number(value):
    if pd.isna(value):
        return float("nan")

    text = str(value).strip().upper()
    if not text or text in {"N/A", "NA", "NAN", "NONE"}:
        return float("nan")

    multiplier = 1
    if text.endswith("K"):
        multiplier = 1000
        text = text[:-1]

    number = re.sub(r"[^0-9,.-]", "", text)
    if not number:
        return float("nan")

    separator = max(number.rfind("."), number.rfind(","))
    decimals = len(number) - separator - 1
    if separator >= 0 and decimals in (1, 2):
        integer_part = re.sub(r"[.,]", "", number[:separator])
        decimal_part = number[separator + 1 :]
        number = f"{integer_part}.{decimal_part}"
    else:
        number = re.sub(r"[.,]", "", number)

    try:
        return float(number) * multiplier
    except ValueError:
        return float("nan")


def _parse_discount(value):
    if pd.isna(value):
        return float("nan")
    text = str(value).strip()
    if not text or text.upper() in {"N/A", "NA", "NAN", "NONE"}:
        return float("nan")

    is_percentage = text.endswith("%")
    if is_percentage:
        text = text[:-1].strip()
    try:
        discount = float(text.replace(",", "."))
    except ValueError:
        return float("nan")
    if is_percentage or discount > 1:
        discount /= 100
    return discount


def _parse_weight(value):
    if pd.isna(value):
        return float("nan")
    text = str(value).strip().lower()
    if not text or text in {"n/a", "na", "nan", "none"}:
        return float("nan")

    match = re.search(r"[-+]?\d+(?:[.,]\d+)?", text)
    if not match:
        return float("nan")
    weight = float(match.group().replace(",", "."))
    if "ton" in text or re.search(r"\bt\b", text):
        weight *= 1000
    elif re.search(r"\bg\b", text):
        weight /= 1000
    return weight


def main():
    sales = pd.read_csv(INPUT_FILE, encoding="utf-8-sig", dtype="string")
    sales.columns = [_normalize_header(column) for column in sales.columns]

    sales["supplier_id"] = sales["supplier_id"].map(_clean_text)
    sales["supplier"] = sales["supplier"].map(_clean_text)

    country = sales["country"].str.strip().str.upper()
    sales["country"] = country.replace(
        {"COLOMBIA": "COL", "CO": "COL", "COL": "COL"}
    )
    sales = sales.loc[sales["country"].eq("COL")].copy()

    sales["city"] = sales["city"].map(_clean_city)
    sales["purchase_date"] = sales["purchase_date"].map(_parse_date)
    sales["amount"] = sales["amount"].map(_parse_number)
    sales["discount"] = sales["discount"].map(_parse_discount)
    sales["weight"] = sales["weight"].map(_parse_weight)
    sales["units"] = sales["units"].map(_parse_number)
    sales["unit_price"] = sales["unit_price"].map(_parse_number)

    email = sales["contact_email"].map(_clean_text).str.lower()
    sales["contact_email"] = email.mask(email.isin(["sin correo", "n/a", "na", ""]))

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    sales[OUTPUT_COLUMNS].to_csv(OUTPUT_FILE, index=False)


if __name__ == "__main__":
    main()
