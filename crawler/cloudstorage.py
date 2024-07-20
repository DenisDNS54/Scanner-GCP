import json
import os
from google.cloud import storage, service_usage_v1
from google.oauth2 import service_account

def serviciu_cloudstorage(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "bucketuri": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/storage.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    configuratie = str(serviciu.config)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": configuratie
    }

    client = storage.Client(project=id_proiect, credentials=credentiale)

    try:
        bucketuri = client.list_buckets()
        for bucket in bucketuri:
            bucket_info = {
                "nume_bucket": bucket.name,
                "locatie": bucket.location,
                "clasa_stocare": bucket.storage_class
            }
            rezultate["bucketuri"].append(bucket_info)

    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
