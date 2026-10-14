from ._data import parse_metrics, read_rows

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    totals = {}
    for row in read_rows():
        letter = row[0]
        totals[letter] = totals.get(letter, 0) + sum(
            value for _, value in parse_metrics(row[4])
        )
    return dict(sorted(totals.items()))
