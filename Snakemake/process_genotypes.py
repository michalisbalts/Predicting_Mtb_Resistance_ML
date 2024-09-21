import pandas as pd
import os
import glob

# Function to process a batch of files
def process_batch(files_batch, data_dict, snp_positions):
    for file_path in files_batch:
        unique_id = os.path.splitext(os.path.basename(file_path))[0]
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip().replace('\r', '')  # Strip newline and remove carriage return
                if not line:
                    continue  # skip empty lines
                parts = line.split()
                snp_position = parts[0]
                genotype = parts[1]
                snp_positions.add(snp_position)
                data_dict.setdefault(unique_id, {}).update({snp_position: genotype})

# Initialize an empty dictionary to hold all data
data_dict = {}

# Define a set to keep track of all unique SNP positions
snp_positions = set()

# Define the path to the directory containing the edited VCF files
edited_vcf_dir = "/mnt/raid0/michalis/edited_vcfs"

# Read all file paths
vcf_files = glob.glob(os.path.join(edited_vcf_dir, "*.txt"))

# Define batch size
batch_size = 1000

# Process files in batches
for i in range(0, len(vcf_files), batch_size):
    batch_files = vcf_files[i:i + batch_size]
    process_batch(batch_files, data_dict, snp_positions)
    print(f"Processed batch {i//batch_size + 1}/{len(vcf_files)//batch_size}")

# Convert the SNP positions to a sorted list
snp_positions = sorted(list(snp_positions), key=int)

# Create a DataFrame from the dictionary
df_final = pd.DataFrame.from_dict(data_dict, orient='index', columns=snp_positions)

# Define the path to save the CSV file
output_dir = "/mnt/raid0/michalis/snakemakeproject"
dataframe_csv_path = os.path.join(output_dir, "genotype_dataframe.csv")

# Save the final DataFrame to the specified CSV file
df_final.to_csv(dataframe_csv_path, sep=',', header=True, index=True, index_label='UNIQUEID')

# Display the head of the dataframe to ensure it looks correct
print(df_final.head())
