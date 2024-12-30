import pandas as pd

# Load enriched data and metadata
geo_id = "GSE121239"
enriched_file_name = f"{geo_id}_enriched_expression_data.csv"
metadata_file_name = f"{geo_id}_sample_metadata_with_labels.csv"

enriched_data = pd.read_csv(enriched_file_name)
metadata = pd.read_csv(metadata_file_name)

# Inspect columns and perform trimming to remove extra spaces
enriched_data["Sample"] = enriched_data["Sample"].str.strip()
metadata["geo_accession"] = metadata["geo_accession"].str.strip()

# Check for mismatches
enriched_samples = set(enriched_data["Sample"])
metadata_samples = set(metadata["geo_accession"])

# Samples in enriched data but not in metadata
missing_in_metadata = enriched_samples - metadata_samples
print(f"Samples in enriched data but missing in metadata: {missing_in_metadata}")

# Samples in metadata but not in enriched data
missing_in_enriched = metadata_samples - enriched_samples
print(f"Samples in metadata but missing in enriched data: {missing_in_enriched}")

# Handle mismatches
if missing_in_metadata:
    print("Dropping unmatched samples from enriched data...")
    enriched_data = enriched_data[~enriched_data["Sample"].isin(missing_in_metadata)]

if missing_in_enriched:
    print("Dropping unmatched samples from metadata...")
    metadata = metadata[~metadata["geo_accession"].isin(missing_in_enriched)]

# Merge the datasets
print("Merging datasets...")
merged_data = enriched_data.merge(metadata, left_on="Sample", right_on="geo_accession", how="inner")
print(f"Merged data shape: {merged_data.shape}")

# Save cleaned and merged data
output_file = f"{geo_id}_merged_expression_data.csv"
merged_data.to_csv(output_file, index=False)
print(f"Merged data saved to {output_file}.")
