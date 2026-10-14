from ._data import parse_metrics, read_rows

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    ranges = {}
    for row in read_rows():
        for key, value in parse_metrics(row[4]):
            if key not in ranges:
                ranges[key] = [value, value]
            else:
                ranges[key][0] = min(ranges[key][0], value)
                ranges[key][1] = max(ranges[key][1], value)
    return [(key, low, high) for key, (low, high) in sorted(ranges.items())]
