"""Convierte el CSV de conductores al JSON solicitado por la actividad."""

import csv
import json
from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "drivers.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "drivers.json"
OUTPUT_COLUMNS = ("driverId", "name", "certified", "wage-plan")


def main():
    with INPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        records = [
            {column: row[column] for column in OUTPUT_COLUMNS}
            for row in reader
        ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
