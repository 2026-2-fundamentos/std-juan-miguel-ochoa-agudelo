"""Resume las horas y millas por conductor y grafica los diez primeros."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def main():
    drivers = pd.read_csv(DATA_DIR / "drivers.csv")
    timesheet = pd.read_csv(DATA_DIR / "timesheet.csv")

    totals = timesheet.groupby("driverId", as_index=False)[
        ["hours-logged", "miles-logged"]
    ].sum()
    summary = (
        totals.merge(drivers[["driverId", "name"]], on="driverId")
        .sort_values("driverId")
        .reset_index(drop=True)
    )

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    summary.to_csv(SUBMISSION_DIR / "summary.csv", index=False)

    top_drivers = summary.nlargest(10, "miles-logged").sort_values("miles-logged")
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.barh(top_drivers["name"], top_drivers["miles-logged"], color="steelblue")
    axis.set_title("Top 10 conductores por millas registradas")
    axis.set_xlabel("Millas registradas")
    axis.set_ylabel("Conductor")
    axis.grid(axis="x", linestyle="--", alpha=0.35)
    figure.tight_layout()
    figure.savefig(SUBMISSION_DIR / "top10_drivers.png", dpi=150)
    plt.close(figure)


if __name__ == "__main__":
    main()
