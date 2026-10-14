from ._data import read_rows
from collections import defaultdict

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    letters_by_value = defaultdict(set)
    for row in read_rows():
        letters_by_value[int(row[1])].add(row[0])
    return [(value, sorted(letters)) for value, letters in sorted(letters_by_value.items())]
