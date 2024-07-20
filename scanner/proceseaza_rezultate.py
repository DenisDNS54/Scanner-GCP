import os
import json
import asyncio

async def proceseaza_rezultate(queue, id_proiect):
    """Procesează rezultatele în ordine și le scrie în fișier."""
    rezultate_proiect = {}
    output_dir = os.path.expanduser('~/GCPLicenta/output')
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.join(output_dir, f'rezultate_{id_proiect}.json')

    while True:
        nume_api, rezultat, durata = await queue.get()
        if nume_api is None:
            break
        rezultate_proiect[nume_api] = rezultat
        print(f"Timp execuție pentru crawler-ul {nume_api}: {durata} secunde")

    with open(file_name, 'w') as f:
        json_output = json.dumps(rezultate_proiect, indent=4)
        json_output = json_output.replace("\\n", "\n").replace("\\\"", "\"")
        f.write(json_output)
    print(f"Rezultatele au fost salvate în {file_name}")
