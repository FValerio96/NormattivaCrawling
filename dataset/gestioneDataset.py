import os
import json

def check_or_create_jsonl_file(nome_file):
    # Percorso del file JSONL nella cartella corrente (che è ora 'dataset')
    file_path = nome_file

    # Verifica se il file JSONL esiste nella cartella corrente
    if os.path.exists(file_path):
        print(f"Il file '{nome_file}' esiste nella cartella.")
    else:
        # Se il file non esiste, crea un nuovo file JSONL con un oggetto JSON vuoto
        with open(file_path, "w") as jsonl_file:
            json.dump("", jsonl_file)
        print(f"Il file '{nome_file}' è stato creato nella cartella.")

    # Restituisci il percorso relativo del file JSONL
    return file_path

def write_comment_to_jsonl(link, jsonl_file_path):
    # Ottenere l'ultima parte del percorso URL
    last_part_of_url = link.split('/')[-1]

    with open(jsonl_file_path, "a") as jsonl_file:
        jsonl_file.write("# " + last_part_of_url + "\n")
