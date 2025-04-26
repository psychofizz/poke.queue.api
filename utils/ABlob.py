import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

load_dotenv()

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_SAK")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
BLOB_NAME = os.getenv("BLOB_NAME")

class ABlob:
    def __init__(self):
        self.blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        self.container_client = self.blob_service_client.get_container_client(BLOB_NAME)

    def generate_sas(self, id: int):
        
        blob_name = f"poke_report_{id}.csv"
        sas_token = generate_blob_sas(
            account_name=self.blob_service_client.account_name,
            container_name=AZURE_STORAGE_CONTAINER,
            blob_name=blob_name,
            account_key=self.blob_service_client.credential.account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=12)
        )
        return sas_token
    
    def delete_csv(self, id):
        blob_name = f"poke_report_{id}.csv"
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            print(f"Attempting to delete the blob: {blob_client.url}")
            blob_client.delete_blob() 
            
            return {"status": "success", "message": "Blob deleted successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}