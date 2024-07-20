from google.cloud import bigquery_datatransfer_v1 as bigquerydatatransfer, service_usage_v1
from google.oauth2 import service_account

def serviciu_bigquerydatatransfer(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "configuratii_transfer": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/bigquerydatatransfer.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client = bigquerydatatransfer.DataTransferServiceClient(credentials=credentiale)

    try:
        parent = client.common_project_path(id_proiect)
        configuratii_transfer = client.list_transfer_configs(parent=parent)
        for configuratie in configuratii_transfer:
            config_info = {
                "id_configuratie": configuratie.name,
                "nume_afisare": configuratie.display_name,
                "id_sursa_date": configuratie.data_source_id,
                "program": configuratie.schedule,
                "stare": configuratie.state
            }
            rezultate["configuratii_transfer"].append(config_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
