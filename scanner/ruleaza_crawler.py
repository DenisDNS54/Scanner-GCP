import asyncio
import time

async def ruleaza_crawler(queue, executor, crawler, id_proiect, credentiale, nume_api):
    """Rulează un crawler și înregistrează rezultatele."""
    try:
        start_time = time.time()
        rezultat = await asyncio.get_event_loop().run_in_executor(executor, crawler, id_proiect, credentiale)
        end_time = time.time()
        await queue.put((nume_api, rezultat, end_time - start_time))
    except Exception as e:
        await queue.put((nume_api, {"eroare": str(e)}, 0))
