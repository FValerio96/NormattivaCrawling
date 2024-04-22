import os

def create_dataset_folder():
    # Verifica se la cartella "dataset" esiste
    if not os.path.exists("dataset"):
        # Se non esiste, crea la cartella
        os.makedirs("dataset")
        print("Cartella 'dataset' creata.")

def check_or_create_jsonl_file():
    create_dataset_folder()

    # Percorso del file JSONL "normattiva1.jsonl" nella cartella "dataset"
    file_path = os.path.join("dataset", "normattiva1.jsonl")

    # Verifica se il file JSONL esiste nella cartella "dataset"
    if os.path.exists(file_path):
        print("Il file 'normattiva1.jsonl' esiste nella cartella 'dataset'.")
    else:
        # Se il file non esiste, lo crea vuoto
        with open(file_path, "w") as jsonl_file:
            pass
        print(f"Il file 'normattiva1.jsonl' è stato creato nella cartella 'dataset'.")

    # Restituisci il percorso relativo del file JSONL
    return file_path
