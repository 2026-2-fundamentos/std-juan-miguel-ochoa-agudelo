"""Funciones compartidas para cargar las tablas TSV de L102."""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def read_table(name):
    return pd.read_csv(DATA_DIR / name, sep="\t")
