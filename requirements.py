import subprocess
import sys

def generate_requirements():
    # Esegui il comando pip freeze per ottenere tutte le dipendenze del progetto
    result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    # Scrivi l'output in un file requirements.txt
    with open('requirements.txt', 'w') as f:
        f.write(output)

generate_requirements()
