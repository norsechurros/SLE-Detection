import pandas as pd

# Load the enriched data and metadata
geo_id = "GSE121239"
enriched_file_name = f"{geo_id}_enriched_expression_data.csv"
metadata_file_name = f"{geo_id}_sample_metadata_with_labels.csv"

enriched_data = pd.read_csv(enriched_file_name)
metadata = pd.read_csv(metadata_file_name)

# Ensure no extra spaces or formatting issues
enriched_data["Sample"] = enriched_data["Sample"].str.strip()
metadata["geo_accession"] = metadata["geo_accession"].str.strip()

# Check for overlap
enriched_samples = set(enriched_data["Sample"])
metadata_samples = set(metadata["geo_accession"])

missing_in_metadata = enriched_samples - metadata_samples
missing_in_enriched = metadata_samples - enriched_samples

print(f"Samples in enriched data but missing in metadata: {missing_in_metadata}")
print(f"Samples in metadata but missing in enriched data: {missing_in_enriched}")
