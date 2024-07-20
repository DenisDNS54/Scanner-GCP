import json
from google.cloud import bigquery, service_usage_v1
from google.oauth2 import service_account

def serviciu_querry(id_proiect, credentiale):
    rezultate = {
        "serviciu": {},
        "seturi_de_date": [],
        "joburi": []
    }

    client_utilizare_serviciu = service_usage_v1.ServiceUsageClient(credentials=credentiale)
    nume = f"projects/{id_proiect}/services/bigquery.googleapis.com"
    cerere = service_usage_v1.GetServiceRequest(name=nume)
    serviciu = client_utilizare_serviciu.get_service(request=cerere)
    rezultate["serviciu"] = {
        "nume": serviciu.name,
        "stare": serviciu.state,
        "configuratie": str(serviciu.config)
    }

    client_bq = bigquery.Client(project=id_proiect, credentials=credentiale)

    try:
        seturi_de_date = list(client_bq.list_datasets())
        for set_de_date in seturi_de_date:
            dataset_info = {
                "id_set_de_date": set_de_date.dataset_id,
                "tabele": []
            }
            referinta_set_de_date = client_bq.dataset(set_de_date.dataset_id)
            tabele = list(client_bq.list_tables(referinta_set_de_date))
            for tabel in tabele:
                tabel_info = {
                    "id_tabel": tabel.table_id,
                    "numar_randuri": tabel.num_rows,
                    "schema": [field.to_api_repr() for field in tabel.schema],
                    "creat": str(tabel.created),
                    "ultima_modificare": str(tabel.modified),
                    "descriere": tabel.description
                }
                dataset_info["tabele"].append(tabel_info)
            rezultate["seturi_de_date"].append(dataset_info)

        joburi = list(client_bq.list_jobs(max_results=10))
        for job in joburi:
            job_info = {
                "id_job": job.job_id,
                "tip": job.job_type,
                "stare": job.state,
                "creat": str(job.created),
                "inceput": str(job.started),
                "terminat": str(job.ended),
                "eroare": job.error_result['message'] if job.error_result else None
            }
            rezultate["joburi"].append(job_info)
        
    except Exception as e:
        rezultate["eroare"] = str(e)

    return rezultate
