from google.cloud import firestore_v1, service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudfirestore(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "colectii": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/firestore.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = firestore_v1.Client(project=id_proiect, credentials=credentiale)

    try:
        colectii = client.collections()
        for colectie in colectii:
            colectie_info = {
                "id_colectie": colectie.id
            }
            rezultate["colectii"].append(colectie_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
