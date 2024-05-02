import json

def remove_duplicate_text(jsonl_file):
    texts_set = set()
    output_lines = []
    removed_count_duplicate = 0
    removed_count_invalid = 0

    with open(jsonl_file, 'r') as f:
        for line in f:
            json_obj = json.loads(line)
            text = json_obj.get('text', '')
            if text not in texts_set and text != "NON ANCORA ESISTENTE O VIGENTE":
                texts_set.add(text)
                output_lines.append(json_obj)
            else:
                if text == "NON ANCORA ESISTENTE O VIGENTE":
                    removed_count_invalid += 1
                else:
                    removed_count_duplicate += 1

    # Scrivi il nuovo file JSONL senza duplicati
    with open(jsonl_file, 'w') as f:
        for json_obj in output_lines:
            f.write(json.dumps(json_obj) + '\n')

    print(f"Numero di JSON rimossi per duplicati: {removed_count_duplicate}")
    print(f"Numero di JSON rimossi per testo non valido: {removed_count_invalid}")


# Esempio di utilizzo:
jsonl_file_path = 'dataset/from 2014 to 2004 elenco atti.jsonl'
remove_duplicate_text(jsonl_file_path)
