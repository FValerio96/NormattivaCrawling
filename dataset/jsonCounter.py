import json

def count_jsonl(filename):
    """
    :param filename: name of file
    :return: then number of rows in file
    """
    count = 0
    with open(filename, 'r') as file:
        for line in file:
            try:
                json_object = json.loads(line)
                if isinstance(json_object, dict):  # Verifica se è un oggetto JSON valido
                    count += 1
            except json.JSONDecodeError:
                pass  # Ignora le linee non valide JSON
    return count

#using example:
filename = 'from 1959 to 1964 elenco atti.jsonl'  # replace with the path of your jsonl file
json_count = count_jsonl(filename)
print("Numero totale di oggetti JSON nel file:", json_count)
