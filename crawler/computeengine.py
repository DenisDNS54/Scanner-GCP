from googleapiclient.discovery import build
from google.cloud import service_usage_v1
from google.oauth2 import service_account

def serviciu_computeengine(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "instante": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/compute.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client_compute = build('compute', 'v1', credentials=credentiale)

    try:
        cerere = client_compute.instances().aggregatedList(project=id_proiect)
        raspuns = cerere.execute()
        if 'items' in raspuns:
            for zona, lista_instante_scopate in raspuns['items'].items():
                if 'instances' in lista_instante_scopate:
                    for instanta in lista_instante_scopate['instances']:
                        instanta_info = {
                            "nume_instanta": instanta['name'],
                            "zona": zona,
                            "stare": instanta['status'],
                            "tip_masina": instanta['machineType']
                        }
                        rezultate["instante"].append(instanta_info)
        else:
            rezultate["instante"] = "Nu s-au găsit instanțe Compute Engine."

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
