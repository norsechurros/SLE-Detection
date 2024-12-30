import os
import GEOparse
import pandas as pd

# Replace 'GSE121239' with your GEO Series ID
geo_id = "GSE121239"

# Step 1: Load the GEO dataset
print(f"Loading GEO dataset: {geo_id}")
gse = GEOparse.get_GEO(geo=geo_id, destdir="./")

# Step 2: Check if GSM samples contain expression data
print("\n--- Extracting and Saving Expression Data ---")
data_frames = []
for gsm_name, gsm in gse.gsms.items():
    if not gsm.table.empty:  # Check if the GSM table is not empty
        df = gsm.table
        df["Sample"] = gsm_name  # Add sample name as a column
        data_frames.append(df)
    else:
        print(f"Sample {gsm_name} does not contain expression data.")

# Combine and save all expression data into a single CSV
if data_frames:
    expression_data = pd.concat(data_frames, ignore_index=True)
    expression_csv = f"{geo_id}_expression_data.csv"
    expression_data.to_csv(expression_csv, index=False)
    print(f"Expression data saved to {expression_csv}")
else:
    print("No expression data found in any GSM samples.")

# Step 3: Save GSM sample metadata
print("\n--- Saving Sample Metadata ---")
metadata_csv = f"{geo_id}_sample_metadata.csv"
metadata = pd.DataFrame.from_dict({gsm_name: gsm.metadata for gsm_name, gsm in gse.gsms.items()}, orient="index")
metadata.to_csv(metadata_csv)
print(f"Sample metadata saved to {metadata_csv}")

# Step 4: Save Platform metadata
print("\n--- Saving Platform Metadata ---")
platform_metadata_csv = f"{geo_id}_platform_metadata.csv"
platform_metadata = pd.DataFrame.from_dict(
    {gpl_name: gpl.metadata for gpl_name, gpl in gse.gpls.items()},
    orient="index"
)
platform_metadata.to_csv(platform_metadata_csv)
print(f"Platform metadata saved to {platform_metadata_csv}")

print("\n--- Process Complete ---")
