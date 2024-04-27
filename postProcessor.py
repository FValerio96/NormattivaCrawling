import json

def remove_duplicate_text(jsonl_file):
    texts_set = set()
    output_lines = []
    removed_count = 0

    with open(jsonl_file, 'r') as f:
        for line in f:
            json_obj = json.loads(line)
            text = json_obj.get('text', '')
            if text not in texts_set:
                texts_set.add(text)
                output_lines.append(json_obj)
            else:
                removed_count += 1

    # Scrivi il nuovo file JSONL senza duplicati
    with open(jsonl_file, 'w') as f:
        for json_obj in output_lines:
            f.write(json.dumps(json_obj) + '\n')

    print(f"Numero di JSON rimossi: {removed_count}")

# Esempio di utilizzo:
jsonl_file_path = 'dataset/2015 elenco atti.jsonl'
remove_duplicate_text(jsonl_file_path)
