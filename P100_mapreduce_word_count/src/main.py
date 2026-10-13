import time
import shutil
import string
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
INPUT_DIR = ACTIVITY_DIR / "temp" / "input"
OUTPUT_DIR = ACTIVITY_DIR / "temp" / "output"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def main():
    # Deja vacías las carpetas de trabajo, conservando sus marcadores de Git.
    for directory in (INPUT_DIR, OUTPUT_DIR, SUBMISSION_DIR):
        directory.mkdir(parents=True, exist_ok=True)
        for item in directory.iterdir():
            if item.name == ".gitkeep":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

    # Simula un conjunto grande de datos creando 1.000 copias de cada texto.
    copies_per_file = 1000
    for source_file in sorted(DATA_DIR.glob("*.txt")):
        text = source_file.read_text(encoding="utf-8")
        for copy_number in range(1, copies_per_file + 1):
            copy_name = f"{source_file.stem}_{copy_number:05d}.txt"
            (INPUT_DIR / copy_name).write_text(text, encoding="utf-8")

    start_time = time.time()

    # Lee todas las líneas de entrada como pares (archivo, línea).
    sequence = []
    for input_file in sorted(INPUT_DIR.glob("*.txt")):
        with input_file.open("r", encoding="utf-8") as file:
            sequence.extend((input_file, line) for line in file)

    # Mapper: normaliza cada línea y emite (palabra, 1).
    punctuation_table = str.maketrans("", "", string.punctuation)
    pairs_sequence = []
    for _, line in sequence:
        normalized_line = line.lower().translate(punctuation_table)
        pairs_sequence.extend((word, 1) for word in normalized_line.split())

    # Shuffle and sort: agrupa las mismas palabras una al lado de la otra.
    pairs_sequence.sort()

    # Reducer: suma los valores asociados a cada palabra.
    result = []
    for word, count in pairs_sequence:
        if result and result[-1][0] == word:
            result[-1] = (word, result[-1][1] + count)
        else:
            result.append((word, count))

    # Escribe la salida simulada y el marcador de finalización.
    part_file = OUTPUT_DIR / "part-00000"
    with part_file.open("w", encoding="utf-8") as file:
        for word, count in result:
            file.write(f"{word}\t{count}\n")

    (OUTPUT_DIR / "_SUCCESS").write_text("", encoding="utf-8")

    # Copia los archivos de salida a la carpeta que se entrega.
    for output_file in OUTPUT_DIR.iterdir():
        if output_file.is_file() and output_file.name != ".gitkeep":
            shutil.copy2(output_file, SUBMISSION_DIR / output_file.name)

    print(f"Tiempo de ejecución: {time.time() - start_time:.2f} segundos")


if __name__ == "__main__":
    main()
