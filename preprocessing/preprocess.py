import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os

# Geo ID and file names
geo_id = "GSE121239"
enriched_file_name = f"{geo_id}_enriched_expression_data.csv"
metadata_file_name = f"{geo_id}_sample_metadata_with_labels.csv"
merged_file_name = f"{geo_id}_merged_expression_data.csv"

# Step 1: Load the Enriched Expression Data and Metadata
print("Loading enriched expression data...")
enriched_data = pd.read_csv(enriched_file_name)
metadata = pd.read_csv(metadata_file_name)

# Step 2: Clean Metadata Identifiers
print("\nCleaning metadata identifiers...")
metadata["geo_accession"] = metadata["geo_accession"].str.replace(r"[^\w]", "", regex=True)  # Remove special characters
print("Metadata identifiers cleaned.")

# Debugging: Check for Overlap
print("\nChecking for sample overlaps...")
enriched_samples = set(enriched_data["Sample"])
metadata_samples = set(metadata["geo_accession"])

missing_in_metadata = enriched_samples - metadata_samples
missing_in_enriched = metadata_samples - enriched_samples

print(f"Samples in enriched data but missing in metadata: {missing_in_metadata}")
print(f"Samples in metadata but missing in enriched data: {missing_in_enriched}")

# Step 3: Merge Datasets
print("\nMerging datasets...")
merged_data = enriched_data.merge(metadata, left_on="Sample", right_on="geo_accession", how="inner")

if merged_data.empty:
    raise ValueError("No matching samples found after merging. Check your datasets for inconsistencies.")
else:
    merged_data.to_csv(merged_file_name, index=False)
    print(f"Merged data saved to {merged_file_name}. Proceeding with preprocessing.")

# Step 4: Handle Missing Data
print("\nHandling missing data...")
# Drop rows where VALUE or Label is missing
if "VALUE" not in merged_data.columns or "Label" not in merged_data.columns:
    raise ValueError("Missing required columns 'VALUE' or 'Label' in the merged dataset.")
merged_data = merged_data.dropna(subset=["VALUE", "Label"])
print(f"Data after dropping rows with missing values: {merged_data.shape}")

# Step 5: Aggregate Probes for the Same Gene
print("\nAggregating probes for the same gene...")
if "Gene Symbol" not in merged_data.columns:
    raise ValueError("Missing 'Gene Symbol' column in the dataset.")
# Average expression values for the same Gene Symbol
data_grouped = merged_data.groupby("Gene Symbol").agg({
    "VALUE": "mean",                 # Mean expression value
    "Gene Title": "first",           # First non-NA title
    "ENTREZ_GENE_ID": "first",       # First non-NA Entrez ID
    "Label": "first"                 # First label (all labels in a group should be the same)
}).reset_index()
print(f"Data after aggregating by Gene Symbol: {data_grouped.shape}")

# Step 6: Normalize Expression Values
print("\nNormalizing expression values...")
if "VALUE" not in data_grouped.columns:
    raise ValueError("Missing 'VALUE' column after grouping by 'Gene Symbol'.")
scaler = StandardScaler()
data_grouped["Normalized VALUE"] = scaler.fit_transform(data_grouped[["VALUE"]])
print("Normalization complete.")

# Step 7: Prepare Features and Labels
print("\nPreparing features and labels...")
if "Label" not in data_grouped.columns:
    raise ValueError("Missing 'Label' column in the grouped data.")
X = data_grouped[["Normalized VALUE"]]  # Features (normalized expression values)
y = data_grouped["Label"]               # Target labels

# Step 8: Split Data into Training and Test Sets
print("\nSplitting data into training and test sets...")
if len(y.unique()) < 2:
    raise ValueError("Insufficient label diversity for stratified splitting. Check your dataset.")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")

# Step 9: Save Preprocessed Data
print("\nSaving preprocessed data...")
X_train.to_csv(f"{geo_id}_X_train.csv", index=False)
X_test.to_csv(f"{geo_id}_X_test.csv", index=False)
y_train.to_csv(f"{geo_id}_y_train.csv", index=False)
y_test.to_csv(f"{geo_id}_y_test.csv", index=False)
print("Preprocessed data saved successfully!")
