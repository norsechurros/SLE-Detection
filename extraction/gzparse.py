import GEOparse
import pandas as pd
import os

# Define dataset ID and file path
geo_id = "GSE239458"
gz_file_path = f"./{geo_id}_family.soft.gz"  # Adjust this path if the file is elsewhere

# Check if file exists
if not os.path.exists(gz_file_path):
    print(f"File {gz_file_path} does not exist. Please download it and place it in the current directory.")
else:
    print(f"Processing file: {gz_file_path}")

    # Parse the .gz file using GEOparse
    gse = GEOparse.get_GEO(filepath=gz_file_path)

    # Save metadata
    print("\n--- Saving Sample Metadata ---")
    metadata = pd.DataFrame.from_dict({gsm_name: gsm.metadata for gsm_name, gsm in gse.gsms.items()}, orient="index")
    metadata.to_csv(f"{geo_id}_sample_metadata.csv")
    print(f"Sample metadata saved to {geo_id}_sample_metadata.csv")

    # Extract and save expression data if available
    print("\n--- Extracting Expression Data ---")
    data_frames = []
    for gsm_name, gsm in gse.gsms.items():
        if not gsm.table.empty:
            df = gsm.table
            df["Sample"] = gsm_name  # Add sample name as a column
            data_frames.append(df)
            print(f"Expression data found for {gsm_name}.")
        else:
            print(f"No expression data for {gsm_name}.")

    # Combine and save all expression data
    if data_frames:
        expression_data = pd.concat(data_frames, ignore_index=True)
        expression_csv = f"./expressions/{geo_id}_expression_data.csv"
        os.makedirs("./expressions", exist_ok=True)
        expression_data.to_csv(expression_csv, index=False)
        print(f"Expression data saved to {expression_csv}")
    else:
        print("No expression data found in any GSM samples.")

    # Save platform metadata
    print("\n--- Saving Platform Metadata ---")
    platform_metadata = pd.DataFrame.from_dict(
        {gpl_name: gpl.metadata for gpl_name, gpl in gse.gpls.items()},
        orient="index"
    )
    platform_metadata.to_csv(f"{geo_id}_platform_metadata.csv")
    print(f"Platform metadata saved to {geo_id}_platform_metadata.csv")
