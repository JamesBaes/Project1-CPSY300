"""
Simplified Serverless Function for Task 3
Reads CSV from Azurite, processes data, saves to JSON
"""
import pandas as pd
from azure.storage.blob import BlobServiceClient
import json
from datetime import datetime
import os

# Azurite connection string (default - do not change!)
AZURITE_CONNECTION_STRING = (
    "DefaultEndpointsProtocol=http;"
    "AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    "BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;"
)

def lambda_handler():
    """
    Main serverless function - does 3 things:
    1. Download CSV from Azurite
    2. Process the data
    3. Save results to JSON
    """
    print("\n" + "="*70)
    print("SERVERLESS FUNCTION STARTED")
    print("="*70)
    
    # STEP 1: Download CSV from Azurite Blob Storage
    print("\nSTEP 1: Downloading from Azurite...")
    
    try:
        # Connect to Azurite
        blob_service_client = BlobServiceClient.from_connection_string(
            AZURITE_CONNECTION_STRING,
            api_version="2023-11-03"
        )
        
        # Get the blob (file)
        blob_client = blob_service_client.get_blob_client(
            container="diet-data",
            blob="All_Diets.csv"
        )
        
        # Download and load into DataFrame
        download_stream = blob_client.download_blob()
        blob_data = download_stream.readall()
        
        from io import StringIO
        df = pd.read_csv(StringIO(blob_data.decode('utf-8')))
        
        print(f"✓ Downloaded {len(df)} records from Azurite")
        
    except Exception as e:
        print(f"✗ Error downloading from Azurite: {e}")
        return
    
    # STEP 2: Process the data
    print("\nSTEP 2: Processing nutritional data...")
    
    try:
        # Clean data - remove rows with missing values
        df_clean = df.dropna(subset=['Protein(g)', 'Carbs(g)', 'Fat(g)'])
        
        # Calculate average macronutrients by diet type
        avg_macros = df_clean.groupby('Diet_type')[['Protein(g)', 'Carbs(g)', 'Fat(g)']].mean()
        
        # Find top 5 protein recipes per diet
        top_protein = df_clean.sort_values('Protein(g)', ascending=False).groupby('Diet_type').head(5)
        
        print(f"✓ Processed {len(df_clean)} records")
        print(f"✓ Analyzed {len(avg_macros)} diet types")
        
    except Exception as e:
        print(f"✗ Error processing data: {e}")
        return
    
    # STEP 3: Save results to JSON (NoSQL simulation)
    print("\nSTEP 3: Saving results to NoSQL database...")
    
    try:
        # Create outputs directory
        os.makedirs('outputs', exist_ok=True)
        
        # Prepare results
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_records': len(df_clean),
            'diet_types': len(avg_macros),
            'average_macronutrients': avg_macros.to_dict('index'),
            'top_protein_recipes': top_protein[['Diet_type', 'Recipe_name', 'Protein(g)']].to_dict('records')
        }
        
        # Save to JSON file
        output_file = 'outputs/nosql_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✓ Results saved to {output_file}")
        
    except Exception as e:
        print(f"✗ Error saving results: {e}")
        return
    
    print("\n" + "="*70)
    print("✅ SERVERLESS FUNCTION COMPLETED SUCCESSFULLY")
    print("="*70)
    print(f"Processed: {results['total_records']} records")
    print(f"Diet types: {results['diet_types']}")
    print(f"Output: {output_file}")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Run the function
    lambda_handler()