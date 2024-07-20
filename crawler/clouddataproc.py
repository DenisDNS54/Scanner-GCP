from google.cloud import dataproc_v1, service_usage_v1
from google.oauth2 import service_account

def serviciu_clouddataproc(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "clustere": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/dataproc.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = dataproc_v1.ClusterControllerClient(credentials=credentiale)

    try:
        clustere = client.list_clusters(request={"project_id": id_proiect, "region": "global"})
        for cluster in clustere:
            cluster_info = {
                "nume_cluster": cluster.cluster_name,
                "stare": cluster.status.state
            }
            rezultate["clustere"].append(cluster_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
