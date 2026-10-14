from ._data import read_rows

def pregunta_03():
    """
    Sume los valores de la segunda columna (`value`) para cada letra de la
    primera columna (`letter`). Retorne una lista de tuplas `(letra, suma)`
    ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 53), ("B", 36), ("C", 27), ...]
    """

    totals = {}
    for row in read_rows():
        letter, value = row[0], int(row[1])
        totals[letter] = totals.get(letter, 0) + value
    return sorted(totals.items())
