from google.cloud import spanner_admin_instance_v1 as spanner_admin_instance, service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudspanner(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "instante": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/spanner.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = spanner_admin_instance.InstanceAdminClient(credentials=credentiale)

    try:
        instante = client.list_instances(parent=f"projects/{id_proiect}")
        for instanta in instante:
            instanta_info = {
                "id_instanta": instanta.name,
                "configuratie": instanta.config,
                "nume_afisat": instanta.display_name,
                "numar_noduri": instanta.node_count,
                "stare": instanta.state
            }
            rezultate["instante"].append(instanta_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
