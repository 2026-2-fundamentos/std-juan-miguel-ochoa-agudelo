from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def pregunta_01():
    """
    Las frases de este laboratorio no están en una tabla, sino en miles de
    archivos de texto organizados en carpetas. Dentro de `data/` hay dos
    carpetas, `train/` y `test/`, y cada una contiene las carpetas
    `negative/`, `neutral/` y `positive/`. Cada archivo `.txt` contiene una
    frase, y la carpeta donde se encuentra indica su sentimiento.

    Su tarea es construir un dataset para cada división y guardarlo en:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Cada archivo debe tener dos columnas: `phrase`, con el texto de la frase,
    y `target`, con el nombre de la carpeta de sentimiento (`negative`,
    `neutral` o `positive`). Recorra las carpetas y los archivos en orden
    alfabético, de modo que el resultado sea siempre el mismo. No guarde el
    índice de Pandas en el CSV.

    Ejemplo del formato de cada archivo:

        phrase,target
        "The real estate company posted a net loss ...",negative
        ...
        "Cardona slowed her vehicle , turned around ...",neutral
        ...
    """

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    for split in ("train", "test"):
        records = []
        split_dir = DATA_DIR / split
        for sentiment_dir in sorted(path for path in split_dir.iterdir() if path.is_dir()):
            for text_file in sorted(sentiment_dir.glob("*.txt")):
                phrase = text_file.read_text(encoding="utf-8").strip()
                records.append({"phrase": phrase, "target": sentiment_dir.name})

        dataset = pd.DataFrame(records, columns=["phrase", "target"])
        dataset.to_csv(SUBMISSION_DIR / f"{split}_dataset.csv", index=False)
