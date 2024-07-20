from googleapiclient.discovery import build
from google.oauth2 import service_account

def serviciu_proiect_info(id_proiect, credentiale):
    serviciu = build('cloudresourcemanager', 'v1', credentials=credentiale)
    cerere = serviciu.projects().get(projectId=id_proiect)
    try:
        proiect = cerere.execute()
        return {
            "numarProiect": proiect.get("projectNumber"),
            "idProiect": proiect.get("projectId"),
            "stareCicluDeViata": proiect.get("lifecycleState"),
            "nume": proiect.get("name"),
            "timpCreare": proiect.get("createTime")
        }
    except Exception as e:
        return {"eroare": str(e)}
