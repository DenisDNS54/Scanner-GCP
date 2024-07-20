from google.cloud import pubsub_v1, service_usage_v1
from google.oauth2 import service_account

def serviciu_pubsub(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "subiecte": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/pubsub.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = pubsub_v1.PublisherClient(credentials=credentiale)

    try:
        subiecte = client.list_topics(request={"project": f"projects/{id_proiect}"})
        for subiect in subiecte:
            subiect_info = {
                "nume_subiect": subiect.name
            }
            rezultate["subiecte"].append(subiect_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
