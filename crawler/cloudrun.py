from googleapiclient.discovery import build
from google.cloud import service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudrun(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "servicii_cloudrun": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/run.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = build('run', 'v1', credentials=credentiale)

    try:
        cerere = client.projects().locations().services().list(parent=f"projects/{id_proiect}/locations/-")
        raspuns = cerere.execute()
        if 'items' in raspuns:
            for serviciu in raspuns['items']:
                serviciu_info = {
                    "nume_serviciu": serviciu['metadata']['name'],
                    "url": serviciu['status']['url'],
                    "timp_creare": serviciu['metadata']['creationTimestamp'],
                    "ultima_modificare": serviciu['metadata']['generation']
                }
                rezultate["servicii_cloudrun"].append(serviciu_info)
        else:
            rezultate["servicii_cloudrun"] = "Nu au fost găsite servicii Cloud Run."

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
