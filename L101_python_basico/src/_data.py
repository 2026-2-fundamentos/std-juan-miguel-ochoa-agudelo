"""Lectura y conversión de los registros compartidos por las preguntas."""

import csv
import gzip
from pathlib import Path


DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "data.csv.gz"


def read_rows():
    """Lee las filas del archivo tabulado comprimido."""
    with gzip.open(DATA_FILE, "rt", encoding="utf-8", newline="") as file:
        return list(csv.reader(file, delimiter="\t"))


def parse_metrics(field):
    """Convierte `clave:valor,clave:valor` en pares (clave, entero)."""
    return [(key, int(value)) for key, value in (item.split(":") for item in field.split(","))]
