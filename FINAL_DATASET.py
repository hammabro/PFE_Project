import pandas as pd

# File paths for the two datasets
file_path1 = r"datasets\adjusted\Cars_VF.xlsx"
file_path2 = r"datasets\adjusted\Cars_VF_v2.xlsx"

# Read the datasets
df1 = pd.read_excel(file_path1)
df2 = pd.read_excel(file_path2)

# Combine the datasets
combined_df = pd.concat([df1, df2])



print(combined_df.shape)

# Specify the path for the final combined dataset
output_file_path = r"datasets\final_version\FINAL_DATASET.xlsx"

# Save the final combined dataset to an Excel file
combined_df.to_excel(output_file_path, index=False)

print("Combined dataset saved successfully!")
