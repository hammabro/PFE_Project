import pandas as pd

# Step 1: Read the dataset
file_path = r"datasets\unified\unified_car_data_v2.xlsx"
df = pd.read_excel(file_path)

# Step 2: Modify the dataset (drop columns)
columns_to_drop = ['État', 'Description', 'Nature','Cylindrée','Transmission','Date annonce','Couleur exterieure','Couleur interieure','Sellerie','Nombre de places','Nombre de portes']  # Specify columns you want to drop
df_modified = df.drop(columns=columns_to_drop)

# Step 3: Close the file after reading
del df

# Step 4: Save the modified dataset to a different location
output_path = "Cars_VF_v2.xlsx"  # Specify the output path
df_modified.to_excel(output_path, index=False)  # Save the modified dataset to Excel

# Output confirmation
print("Changes saved to:", output_path)