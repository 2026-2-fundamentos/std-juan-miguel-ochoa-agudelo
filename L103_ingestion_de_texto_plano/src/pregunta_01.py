import re
from pathlib import Path

import pandas as pd


REPORT_FILE = Path(__file__).resolve().parents[1] / "data" / "clusters_report.txt"
ROW_START = re.compile(r"^\s*(\d+)\s+(\d+)\s+(\d+,\d+)\s*%\s*(.*)$")


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    records = []
    current_record = None

    def save_current_record():
        if current_record is None:
            return
        keywords = re.sub(r"\s+", " ", " ".join(current_record[3])).strip()
        keywords = keywords.removesuffix(".")
        records.append(
            {
                "cluster": current_record[0],
                "cantidad_de_palabras_clave": current_record[1],
                "porcentaje_de_palabras_clave": current_record[2],
                "principales_palabras_clave": keywords,
            }
        )

    with REPORT_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            match = ROW_START.match(line)
            if match:
                save_current_record()
                current_record = [
                    int(match.group(1)),
                    int(match.group(2)),
                    float(match.group(3).replace(",", ".")),
                    [match.group(4).strip()],
                ]
            elif current_record is not None and line.strip() and not set(line.strip()) <= {"-"}:
                current_record[3].append(line.strip())

    save_current_record()
    return pd.DataFrame(
        records,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )
