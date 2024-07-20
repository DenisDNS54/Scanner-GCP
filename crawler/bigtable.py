from google.cloud import bigtable, service_usage_v1
from google.cloud.bigtable import Client
from google.oauth2 import service_account

def serviciu_bigtable(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "instante": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/bigtable.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = Client(project=id_proiect, credentials=credentiale, admin=True)

    try:
        instante = client.list_instances()[0]
        for instanta in instante:
            instanta_info = {
                "id_instanta": instanta.instance_id,
                "tabele": []
            }
            tabele = instanta.list_tables()
            for tabela in tabele:
                tabela_info = {
                    "id_tabela": tabela.table_id,
                    "politica_iam": str(tabela.get_iam_policy())
                }
                instanta_info["tabele"].append(tabela_info)
            rezultate["instante"].append(instanta_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
