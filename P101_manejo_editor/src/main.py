"""Cuenta palabras en los textos de data usando un flujo MapReduce local."""

import shutil
import string
import time
from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
INPUT_DIR = ACTIVITY_DIR / "temp" / "input"
OUTPUT_DIR = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
COPIES_PER_FILE = 1000


def clear_directory(directory):
    """Crea una carpeta vacía, conservando el marcador de Git si existe."""
    directory.mkdir(parents=True, exist_ok=True)
    for item in directory.iterdir():
        if item.name == ".gitkeep":
            continue
        if item.is_dir():
            shutil.rmtree(item)
        else:
            item.unlink()


def main():
    for directory in (INPUT_DIR, OUTPUT_DIR, SUBMISSION_DIR):
        clear_directory(directory)

    # Genera 1.000 copias de cada texto para simular un conjunto mayor.
    for source_file in sorted(DATA_DIR.glob("*.txt")):
        text = source_file.read_text(encoding="utf-8")
        for number in range(1, COPIES_PER_FILE + 1):
            copy_name = f"{source_file.stem}_{number:05d}.txt"
            (INPUT_DIR / copy_name).write_text(text, encoding="utf-8")

    start_time = time.time()

    # Mapper: transforma cada palabra normalizada en el par (palabra, 1).
    punctuation_table = str.maketrans("", "", string.punctuation)
    pairs = []
    for input_file in sorted(INPUT_DIR.glob("*.txt")):
        with input_file.open("r", encoding="utf-8") as file:
            for line in file:
                words = line.lower().translate(punctuation_table).split()
                pairs.extend((word, 1) for word in words)

    # Shuffle/sort agrupa palabras iguales; reducer suma sus valores.
    pairs.sort()
    counts = []
    for word, value in pairs:
        if counts and counts[-1][0] == word:
            counts[-1] = (word, counts[-1][1] + value)
        else:
            counts.append((word, value))

    part_file = OUTPUT_DIR / "part-00000"
    with part_file.open("w", encoding="utf-8") as file:
        for word, count in counts:
            file.write(f"{word}\t{count}\n")

    (OUTPUT_DIR / "_SUCCESS").write_text("", encoding="utf-8")

    # Copia los resultados a submission, que es la carpeta evaluada.
    for output_file in OUTPUT_DIR.iterdir():
        if output_file.is_file():
            shutil.copy2(output_file, SUBMISSION_DIR / output_file.name)

    print(f"Tiempo de ejecución: {time.time() - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
