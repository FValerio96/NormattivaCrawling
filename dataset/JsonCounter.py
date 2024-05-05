import json

def count_jsonl(filename):
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

# Esempio di utilizzo:
filename = 'from 2014 to 2012 elenco atti.jsonl'  # Sostituisci con il percorso del tuo file JSONL
json_count = count_jsonl(filename)
print("Numero totale di oggetti JSON nel file:", json_count)
