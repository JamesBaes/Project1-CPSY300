"""
Script to upload All_Diets.csv to Azurite Blob Storage
"""
from azure.storage.blob import BlobServiceClient
import os

# Azurite connection string (this is the default - do not change!)
AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

def upload_file_to_azurite(file_path, container_name="diet-data", blob_name=None):
    """
    Upload a file to Azurite Blob Storage.
    
    Args:
        file_path (str): Path to the file to upload
        container_name (str): Name of the container
        blob_name (str): Name for the blob (defaults to filename)
    """
    try:
        # Create blob service client
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURITE_CONNECTION_STRING,
            api_version="2023-11-03"
        )
        
        # Create container if it doesn't exist
        container_client = blob_service_client.get_container_client(container_name)
        try:
            container_client.create_container()
            print(f"✓ Created container: {container_name}")
        except Exception as e:
            if "ContainerAlreadyExists" in str(e):
                print(f"✓ Container already exists: {container_name}")
            else:
                raise
        
        # Upload file
        if blob_name is None:
            blob_name = os.path.basename(file_path)
        
        blob_client = blob_service_client.get_blob_client(
            container=container_name, 
            blob=blob_name
        )
        
        print(f"\n⬆️  Uploading {file_path} to Azurite...")
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        
        print(f"✓ Successfully uploaded to blob: {blob_name}")
        print(f"✓ Container: {container_name}")
        print(f"✓ Blob URL: {blob_client.url}")
        
        return True
        
    except FileNotFoundError:
        print(f"✗ Error: File not found: {file_path}")
        return False
    except Exception as e:
        print(f"✗ Error uploading file: {e}")
        return False


def list_blobs_in_container(container_name="diet-data"):
    """List all blobs in a container."""
    try:
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURITE_CONNECTION_STRING,
            api_version="2023-11-03"
        )
        container_client = blob_service_client.get_container_client(container_name)
        
        print(f"\n📋 Blobs in container '{container_name}':")
        blob_list = container_client.list_blobs()
        for blob in blob_list:
            print(f"  • {blob.name} (Size: {blob.size} bytes)")
        
    except Exception as e:
        print(f"✗ Error listing blobs: {e}")


if __name__ == "__main__":
    # Upload the dataset
    csv_file = "All_Diets.csv"
    
    print("="*70)
    print("UPLOADING DATASET TO AZURITE BLOB STORAGE")
    print("="*70)
    
    if upload_file_to_azurite(csv_file):
        list_blobs_in_container()
    
    print("\n" + "="*70)
    print("✓ UPLOAD COMPLETE!")
    print("="*70)