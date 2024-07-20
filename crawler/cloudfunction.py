from google.cloud import functions_v1, service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudfunctions(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "functii": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/cloudfunctions.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = functions_v1.CloudFunctionsServiceClient(credentials=credentiale)

    try:
        functii = client.list_functions(parent=f"projects/{id_proiect}/locations/-")
        for functie in functii:
            functie_info = {
                "nume_functie": functie.name,
                "punct_intrare": functie.entry_point,
                "runtime": functie.runtime,
                "stare": functie.status
            }
            rezultate["functii"].append(functie_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
