from ._data import read_rows
from collections import defaultdict

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    letters_by_value = defaultdict(list)
    for row in read_rows():
        letters_by_value[int(row[1])].append(row[0])
    return sorted(letters_by_value.items())
