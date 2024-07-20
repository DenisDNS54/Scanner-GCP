import os
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from .scaneaza_proiect import scaneaza_proiect

async def scaneaza_proiecte_in_folder(folder_chei, crawlere_api):
    """Scanează toate proiectele ale căror chei se găsesc în folderul specificat folosind crawlerele furnizate."""
    start_time_global = time.time()
    executor = ThreadPoolExecutor(max_workers=10)
    tasks = []
    for nume_fisier_cheie in os.listdir(folder_chei):
        if nume_fisier_cheie.endswith('.json'):
            tasks.append(scaneaza_proiect(folder_chei, nume_fisier_cheie, crawlere_api, executor))
    
    await asyncio.gather(*tasks)
    executor.shutdown()
    
    end_time_global = time.time()
    print(f"Timp execuție total pentru scanarea tuturor proiectelor: {end_time_global - start_time_global} secunde")
