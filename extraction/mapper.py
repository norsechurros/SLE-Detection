import GEOparse
import pandas as pd
import os

# Replace with your GEO Series ID
geo_id = "GSE121239"
platform_file = "GPL13158-annotation.txt"  # Ensure this file is in the working directory

# Step 1: Load the GEO dataset
print(f"Loading GEO dataset: {geo_id}")
gse = GEOparse.get_GEO(geo=geo_id, destdir="./")

# Step 2: Extract and save expression data
print("\n--- Extracting and Saving Expression Data ---")
data_frames = []
for gsm_name, gsm in gse.gsms.items():
    if not gsm.table.empty:  # Check if the GSM table contains data
        df = gsm.table
        df["Sample"] = gsm_name  # Add sample name as a column
        data_frames.append(df)

# Combine all expression data into a single CSV
if data_frames:
    expression_data = pd.concat(data_frames, ignore_index=True)
    expression_csv = f"{geo_id}_expression_data.csv"
    expression_data.to_csv(expression_csv, index=False)
    print(f"Expression data saved to {expression_csv}")
else:
    print("No expression data found in any GSM samples.")
    exit()

# Step 3: Process the platform annotation file
print(f"\n--- Loading Platform Annotation File: {platform_file} ---")
try:
    # Skip lines starting with `#` and load the annotation data
    platform_data = pd.read_csv(platform_file, sep="\t", comment="#")

    # Keep only relevant columns for mapping
    platform_data = platform_data[["ID", "Gene Symbol", "Gene Title", "ENTREZ_GENE_ID"]]
    print("Platform annotation file loaded successfully.")
    print(platform_data.head())
except Exception as e:
    print(f"Error loading platform file: {e}")
    exit()

# Step 4: Map ID_REF to gene annotations
print("\n--- Mapping ID_REF to Gene Annotations ---")
expression_data = pd.read_csv(expression_csv)  # Load the previously saved expression data
merged_data = pd.merge(expression_data, platform_data, left_on="ID_REF", right_on="ID", how="left")

# Step 5: Save the enriched expression data
enriched_expression_csv = f"{geo_id}_enriched_expression_data.csv"
merged_data.to_csv(enriched_expression_csv, index=False)
print(f"Enriched expression data with gene annotations saved to {enriched_expression_csv}")

# Step 6: Save Platform Metadata (Optional)
platform_metadata_csv = f"{geo_id}_platform_metadata.csv"
platform_metadata = pd.DataFrame.from_dict(
    {gpl_name: gpl.metadata for gpl_name, gpl in gse.gpls.items()},
    orient="index"
)
platform_metadata.to_csv(platform_metadata_csv)
print(f"Platform metadata saved to {platform_metadata_csv}")

print("\n--- Process Complete ---")
