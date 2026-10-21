"""Resume los registros de conductores mediante SQLite y crea un gráfico."""

import csv
import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def load_csv(connection, csv_path, table, columns, value_types):
    """Carga un CSV a SQLite usando los nombres y tipos indicados."""
    definitions = ", ".join(
        f'"{column}" {value_type}' for column, value_type in zip(columns, value_types)
    )
    connection.execute(f'CREATE TABLE "{table}" ({definitions})')

    placeholders = ", ".join("?" for _ in columns)
    column_names = ", ".join(f'"{column}"' for column in columns)
    with csv_path.open("r", encoding="utf-8", newline="") as file:
        rows = csv.DictReader(file)
        values = [tuple(row[column] for column in columns) for row in rows]

    connection.executemany(
        f'INSERT INTO "{table}" ({column_names}) VALUES ({placeholders})', values
    )


def main():
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(":memory:") as connection:
        load_csv(
            connection,
            DATA_DIR / "drivers.csv",
            "drivers",
            ["driverId", "name", "ssn", "location", "certified", "wage-plan"],
            ["INTEGER", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT"],
        )
        load_csv(
            connection,
            DATA_DIR / "timesheet.csv",
            "timesheet",
            ["driverId", "week", "hours-logged", "miles-logged"],
            ["INTEGER", "INTEGER", "INTEGER", "INTEGER"],
        )

        query = """
            SELECT
                timesheet.driverId AS driver_id,
                SUM(timesheet."hours-logged") AS hours_logged,
                SUM(timesheet."miles-logged") AS miles_logged,
                drivers.name AS name
            FROM timesheet
            INNER JOIN drivers ON timesheet.driverId = drivers.driverId
            GROUP BY timesheet.driverId, drivers.name
            ORDER BY driver_id
        """
        summary = connection.execute(query).fetchall()

    summary_path = SUBMISSION_DIR / "summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["driver_id", "hours_logged", "miles_logged", "name"])
        writer.writerows(summary)

    top_drivers = sorted(summary, key=lambda row: (-row[2], row[0]))[:10]
    top_drivers.reverse()
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.barh([row[3] for row in top_drivers], [row[2] for row in top_drivers])
    axis.set_title("Top 10 conductores por millas registradas")
    axis.set_xlabel("Millas registradas")
    axis.set_ylabel("Conductor")
    axis.grid(axis="x", linestyle="--", alpha=0.35)
    figure.tight_layout()
    figure.savefig(SUBMISSION_DIR / "top10_drivers.png", dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    main()
