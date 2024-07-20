import asyncio
from googleapiclient.discovery import build

async def este_api_activat(credentiale, id_proiect, nume_api, executor):
    """Verifică dacă un API dat este activat pentru proiect."""
    try:
        serviciu = build('serviceusage', 'v1', credentials=credentiale)
        cerere = serviciu.services().get(name=f'projects/{id_proiect}/services/{nume_api}')
        raspuns = await asyncio.get_event_loop().run_in_executor(executor, cerere.execute)
        return raspuns['state'] == 'ENABLED'
    except Exception as e:
        print(f"Eroare la verificarea API-ului {nume_api} pentru proiectul {id_proiect}: {e}")
        return False
