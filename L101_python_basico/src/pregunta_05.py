from ._data import read_rows

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    ranges = {}
    for row in read_rows():
        letter, value = row[0], int(row[1])
        if letter not in ranges:
            ranges[letter] = [value, value]
        else:
            ranges[letter][0] = max(ranges[letter][0], value)
            ranges[letter][1] = min(ranges[letter][1], value)
    return [(letter, high, low) for letter, (high, low) in sorted(ranges.items())]
