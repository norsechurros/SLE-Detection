import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import os

geo_id = "GSE121239"
enriched_file_name = f"{geo_id}_enriched_expression_data.csv"
metadata_file_name = f"{geo_id}_sample_metadata_with_labels.csv"
merged_file_name = f"{geo_id}_merged_expression_data.csv"

# Step 1: Load Enriched Expression Data and Metadata with Optimized Data Types
print("Loading enriched expression data...")
enriched_data = pd.read_csv(
    enriched_file_name,
    dtype={"VALUE": "float32", "Sample": "string", "Gene Symbol": "string"},
    usecols=["VALUE", "Sample", "Gene Symbol", "Gene Title", "ENTREZ_GENE_ID"]
)

print("Loading metadata...")
metadata = pd.read_csv(
    metadata_file_name,
    dtype={"geo_accession": "string", "Label": "int8"},
    usecols=["geo_accession", "Label"]
)

# Step 2: Clean Metadata Identifiers
print("\nCleaning metadata identifiers...")
metadata["geo_accession"] = metadata["geo_accession"].str.replace(r"[^\w]", "", regex=True)
print("Metadata identifiers cleaned.")

# Step 3: Merge in Chunks
print("\nMerging datasets...")
chunk_size = 10000  # Number of rows per chunk
merged_chunks = []

for chunk in pd.read_csv(enriched_file_name, chunksize=chunk_size, dtype={"Sample": "string"}):
    chunk = chunk.merge(metadata, left_on="Sample", right_on="geo_accession", how="inner")
    merged_chunks.append(chunk)

merged_data = pd.concat(merged_chunks, ignore_index=True)
print(f"Merged dataset shape: {merged_data.shape}")

if merged_data.empty:
    raise ValueError("No matching samples found after merging. Check your datasets for inconsistencies.")
else:
    merged_data.to_csv(merged_file_name, index=False)
    print(f"Merged data saved to {merged_file_name}. Proceeding with preprocessing.")

# Step 4: Handle Missing Data
print("\nHandling missing data...")
merged_data = merged_data.dropna(subset=["VALUE", "Label"])
print(f"Data after dropping rows with missing values: {merged_data.shape}")

# Step 5: Aggregate Probes for the Same Gene
print("\nAggregating probes for the same gene...")
data_grouped = merged_data.groupby("Gene Symbol").agg({
    "VALUE": "mean",
    "Gene Title": "first",
    "ENTREZ_GENE_ID": "first",
    "Label": "first"
}).reset_index()
print(f"Data after aggregating by Gene Symbol: {data_grouped.shape}")

# Step 6: Normalize Expression Values
print("\nNormalizing expression values...")
scaler = StandardScaler()
data_grouped["Normalized VALUE"] = scaler.fit_transform(data_grouped[["VALUE"]])
print("Normalization complete.")

# Step 7: Prepare Features and Labels
print("\nPreparing features and labels...")
X = data_grouped[["Normalized VALUE"]]
y = data_grouped["Label"]

# Step 8: Split Data into Training and Test Sets
print("\nSplitting data into training and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
print(f"Training set shape: {X_train.shape}, Test set shape: {X_test.shape}")

# Step 9: Save Preprocessed Data
print("\nSaving preprocessed data...")
X_train.to_csv(f"{geo_id}_X_train.csv", index=False)
X_test.to_csv(f"{geo_id}_X_test.csv", index=False)
y_train.to_csv(f"{geo_id}_y_train.csv", index=False)
y_test.to_csv(f"{geo_id}_y_test.csv", index=False)
print("Preprocessed data saved successfully!")
