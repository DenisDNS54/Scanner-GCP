from googleapiclient.discovery import build
from google.cloud import service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudsql(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "instante": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/sqladmin.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = build('sqladmin', 'v1beta4', credentials=credentiale)

    try:
        cerere = client.instances().list(project=id_proiect)
        raspuns = cerere.execute()
        if 'items' in raspuns:
            for instanta in raspuns['items']:
                instanta_info = {
                    "nume_instanta": instanta['name'],
                    "versiune_baza_date": instanta['databaseVersion'],
                    "stare": instanta['state']
                }
                rezultate["instante"].append(instanta_info)
        else:
            rezultate["instante"] = "Nu s-au găsit instanțe Cloud SQL."

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
