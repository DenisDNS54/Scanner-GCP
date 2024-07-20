import os
import asyncio
from .scaneaza_proiecte_in_folder import scaneaza_proiecte_in_folder
from crawler.querry import serviciu_querry
from crawler.bigtable import serviciu_bigtable
from crawler.cloudfunction import serviciu_cloudfunctions
from crawler.cloudstorage import serviciu_cloudstorage
from crawler.computeengine import serviciu_computeengine
from crawler.cloudpub import serviciu_pubsub
from crawler.cloudsql import serviciu_cloudsql
from crawler.cloudspanner import serviciu_cloudspanner
from crawler.cloudfirestore import serviciu_cloudfirestore
from crawler.clouddataproc import serviciu_clouddataproc
from crawler.bigquerydatatransfer import serviciu_bigquerydatatransfer
from crawler.cloudrun import serviciu_cloudrun
from crawler.proiect_info import serviciu_proiect_info

def main():
    folder_chei = os.path.expanduser('~/GCPLicenta/keys')
    crawlere_api = {
        "project_info": serviciu_proiect_info,
        "bigquery.googleapis.com": serviciu_querry,
        "bigtableadmin.googleapis.com": serviciu_bigtable,
        "cloudfunctions.googleapis.com": serviciu_cloudfunctions,
        "storage.googleapis.com": serviciu_cloudstorage,
        "compute.googleapis.com": serviciu_computeengine,
        "pubsub.googleapis.com": serviciu_pubsub,
        "sqladmin.googleapis.com": serviciu_cloudsql,
        "spanner.googleapis.com": serviciu_cloudspanner,
        "firestore.googleapis.com": serviciu_cloudfirestore,
        "dataproc.googleapis.com": serviciu_clouddataproc,
        "bigquerydatatransfer.googleapis.com": serviciu_bigquerydatatransfer,
        "run.googleapis.com": serviciu_cloudrun,
    }
    asyncio.run(scaneaza_proiecte_in_folder(folder_chei, crawlere_api))

if __name__ == "__main__":
    main()
