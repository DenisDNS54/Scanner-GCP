import json

def obtine_id_proiect_din_fisierul_cheie(cale_fisier_cheie):
    """Extrage ID-ul proiectului dintr-un fișier de cheie de cont de serviciu."""
    with open(cale_fisier_cheie, 'r') as f:
        date_fisier_cheie = json.load(f)
    return date_fisier_cheie.get('project_id')
