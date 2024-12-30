import pandas as pd

# Function to clean metadata and assign labels
def process_metadata(geo_id):
    # Construct the metadata file name
    sample_metadata_file = f"{geo_id}_sample_metadata.csv"
    
    try:
        # Load the metadata file
        print(f"Loading metadata file: {sample_metadata_file}...")
        sample_metadata = pd.read_csv(sample_metadata_file)
        
        # Clean the `title` column and assign labels
        if "title" in sample_metadata.columns:
            print("Processing 'title' column to extract disease state...")
            # Remove brackets and single quotes, then extract disease state
            sample_metadata["Cleaned Title"] = sample_metadata["title"].str.strip("[]").str.replace("'", "")
            sample_metadata["Label"] = sample_metadata["Cleaned Title"].apply(
                lambda x: 0 if "Healthy" in x else 1
            )
        else:
            raise KeyError("The 'title' column is missing. Please check the metadata file.")

        # Save the updated metadata file
        output_file = f"{geo_id}_sample_metadata_with_labels.csv"
        sample_metadata.to_csv(output_file, index=False)
        print(f"Updated metadata saved as '{output_file}'.")
    except FileNotFoundError:
        print(f"Error: File '{sample_metadata_file}' not found. Ensure the file exists in the directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Specify the GEO ID
    geo_id = "GSE121239"  # Change this to process other datasets
    process_metadata(geo_id)
