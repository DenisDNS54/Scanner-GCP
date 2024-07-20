import os
import time
import asyncio
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from .obtine_id_proiect import obtine_id_proiect_din_fisierul_cheie
from .este_api_activat import este_api_activat
from .ruleaza_crawler import ruleaza_crawler
from .proceseaza_rezultate import proceseaza_rezultate

async def scaneaza_proiect(folder_chei, nume_fisier_cheie, crawlere_api, executor):
    """Scanează un proiect."""
    start_time_proiect = time.time()
    cale_fisier_cheie = os.path.join(folder_chei, nume_fisier_cheie)
    id_proiect = obtine_id_proiect_din_fisierul_cheie(cale_fisier_cheie)
    if id_proiect:
        print(f"\nScanare proiect {id_proiect} folosind cheia {nume_fisier_cheie}")
        credentiale = service_account.Credentials.from_service_account_file(
            cale_fisier_cheie,
            scopes=[
                'https://www.googleapis.com/auth/cloud-platform',
                'https://www.googleapis.com/auth/bigquery'
            ]
        )
        credentiale.refresh(Request())

        queue = asyncio.Queue()
        procesare_task = asyncio.create_task(proceseaza_rezultate(queue, id_proiect))

        for nume_api, crawler in crawlere_api.items():
            if nume_api == "project_info":
                await ruleaza_crawler(queue, executor, crawler, id_proiect, credentiale, nume_api)
            else:
                if await este_api_activat(credentiale, id_proiect, nume_api, executor):
                    await ruleaza_crawler(queue, executor, crawler, id_proiect, credentiale, nume_api)
                else:
                    await queue.put((nume_api, {"eroare": f"API-ul {nume_api} nu este activat pentru proiectul {id_proiect}"}, 0))

        await queue.put((None, None, 0))
        await procesare_task

        end_time_proiect = time.time()
        print(f"Timp execuție pentru scanarea proiectului {id_proiect}: {end_time_proiect - start_time_proiect} secunde")
    else:
        print(f"Nu am putut găsi ID-ul proiectului în fișierul cheie {nume_fisier_cheie}")
