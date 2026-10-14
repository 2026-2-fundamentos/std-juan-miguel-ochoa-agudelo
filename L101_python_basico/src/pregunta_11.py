from ._data import read_rows

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    totals = {}
    for row in read_rows():
        value = int(row[1])
        for code in set(row[3].split(",")):
            totals[code] = totals.get(code, 0) + value
    return dict(sorted(totals.items()))
