from ._data import parse_metrics, read_rows
from collections import Counter

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    counts = Counter(key for row in read_rows() for key, _ in parse_metrics(row[4]))
    return dict(sorted(counts.items()))
