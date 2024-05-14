import pandas as pd

# Load data from the Excel files
try:
    df_tayara = pd.read_excel('Tayara_car_data_v2.xlsx', engine='openpyxl')
    df_automobile = pd.read_excel('automobile_car_data_v2.xlsx', engine='openpyxl')
except FileNotFoundError:
    print("One or both files not found.")
    exit()

# Rename columns for Tayara data
df_tayara.rename(columns={'Marque': 'Marque', 'Modèle': 'Modèle', 'Etat': 'État', 'Kilométrage': 'Kilométrage', 
                          'Carburant': 'Carburant', 'Boite Vitesse': 'Boite Vitesse', 'Puissance Fiscale': 'Puissance Fiscale',
                          'Carrosserie': 'Carrosserie', 'Cylindrée': 'Cylindrée', 'Année': 'Année', 'Prix': 'Prix', 'description': 'Description'},
                 inplace=True)

# Rename columns for Automobile data
df_automobile.rename(columns={'Nature': 'Nature', 'Kilométrage': 'Kilométrage', 'Mise en circulation': 'Mise en circulation',
                              'Carburant': 'Carburant', 'Boite Vitesse': 'Boite Vitesse', 'Puissance Fiscale': 'Puissance Fiscale',
                              'Transmission': 'Transmission', 'Carrosserie': 'Carrosserie', 'Date annonce': 'Date annonce',
                              'Cylindrée': 'Cylindrée', 'Couleur exterieure': 'Couleur exterieure', 'Couleur interieure': 'Couleur interieure',
                              'Sellerie': 'Sellerie', 'Nombre de places': 'Nombre de places', 'Nombre de portes': 'Nombre de portes',
                              'Marque': 'Marque', 'Modèle': 'Modèle', 'Prix': 'Prix'},
                     inplace=True)

# Set unique columns for Tayara data
df_tayara_unique = df_tayara[['Marque', 'Modèle', 'État', 'Kilométrage', 'Carburant', 'Boite Vitesse', 
                               'Puissance Fiscale', 'Carrosserie', 'Cylindrée', 'Année', 'Prix', 'Description']]

# Set unique columns for Automobile data
df_automobile_unique = df_automobile[['Nature', 'Kilométrage', 'Mise en circulation', 'Carburant', 'Boite Vitesse', 
                                       'Puissance Fiscale', 'Transmission', 'Carrosserie', 'Date annonce', 'Cylindrée', 
                                       'Couleur exterieure', 'Couleur interieure', 'Sellerie', 'Nombre de places', 
                                       'Nombre de portes', 'Marque', 'Modèle', 'Prix']]

# Convert 'Puissance Fiscale' column to the same data type in both dataframes
df_tayara_unique['Puissance Fiscale'] = df_tayara_unique['Puissance Fiscale'].astype(str)
df_automobile_unique['Puissance Fiscale'] = df_automobile_unique['Puissance Fiscale'].astype(str)

# Merge the dataframes on common columns
df_unified = pd.concat([df_tayara_unique, df_automobile_unique], ignore_index=True)

# Save the unified dataframe to a new Excel file
df_unified.to_excel('unified_car_data_v2.xlsx', index=False)

print("Unified database created and saved.")
