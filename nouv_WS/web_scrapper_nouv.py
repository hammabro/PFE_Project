from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
import re
import pandas as pd
import os.path

driver = webdriver.Chrome()

base_url = 'https://www.automobile.tn'
driver.get('https://www.automobile.tn/fr/neuf')
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')
brands = soup.find('div', class_='brands-list').find_all('a')

data = []

for brand in brands:
    link = brand.get('href')
    full_link = urllib.parse.urljoin(base_url, link)

    driver.get(full_link)
    link_html = driver.page_source
    link_soup = BeautifulSoup(link_html, 'lxml')
    cars = link_soup.find('div',class_='articles').find_all('span', recursive=False)
    for car in cars:
        car_link = car.find('a')['href']
        name = car.find('h2').text
        price = car.find('div', class_='price').find('span').text
        car_full_link = urllib.parse.urljoin(base_url, car_link)
   
        driver.get(car_full_link)
        car_html = driver.page_source
        car_soup = BeautifulSoup(car_html, 'lxml')
        breadcrumbs = [breadcrumb for breadcrumb in car_soup.find('div', class_='breadcrumbs-wrapper').find_all('li', class_='active')]

       
        marque = breadcrumbs[0].find('a').text
        if len(breadcrumbs) >= 3:
            if breadcrumbs[2].find('a'):
                modele = breadcrumbs[1].find('a').text + " " + breadcrumbs[2].find('a').text
            else:
                modele = breadcrumbs[1].find('a').text

        if car_soup.find('div', class_='technical-details') :
            tables =car_soup.find('div', class_='technical-details').find_all('table')
            caracteristiques_tab = tables[0].find('tbody').find_all('tr')
            motorisations_tab = tables[1].find('tbody').find_all('tr')
            Transmission_tab = tables[2].find('tbody').find_all('tr')
            equipment_tab = tables[len(tables)-2].find('tbody').find_all('tr')
            nature = 'neuve'
            for tr in caracteristiques_tab :
                if tr.find('th').text=='Disponibilité' : Carrosserie = tr.find('td').text.strip()
                if tr.find('th').text=='Nombre de places' : nbre_places = tr.find('td').text.strip()
                if tr.find('th').text=='Nombre de portes' : nbre_portes = tr.find('td').text.strip()

            
            for tr in motorisations_tab : 
                if tr.find('th').text=='Energie ' : energie = tr.find('td').text.strip()
                if tr.find('th').text=='Puissance fiscale' : Puissance_fiscale = tr.find('td').text.strip()
                if tr.find('th').text=='Cylindrée' : cylindree = tr.find('td').text.strip()

            for tr in Transmission_tab : 
                if tr.find('th').text=='Transmission' : transmission = tr.find('td').text.strip()
                if tr.find('th').text=='Boîte' : boite_vitesse = tr.find('td').text.strip()

            for tr in equipment_tab : 
                if tr.find('th').text=='Sellerie' : sellerie = tr.find('td').text.strip()
                if tr.find('th').text=='Finition intérieure' : finition_interieure = tr.find('td').text.strip()

            # Append data to list
            data.append([name, nature, energie, boite_vitesse, Puissance_fiscale,
                        transmission, Carrosserie, cylindree, sellerie, nbre_places,
                        nbre_portes, marque, modele, price])
        else:
            Carrosserie = "N/A"
            nbre_places = "N/A"
            nbre_portes= "N/A"
            energie= "N/A"
            Puissance_fiscale= "N/A"
            cylindree= "N/A"
            transmission= "N/A"
            boite_vitesse= "N/A"
            sellerie= "N/A"
            finition_interieure= "N/A"

# Close the Selenium WebDriver after all iterations
driver.quit()

# Create DataFrame from the new data list
df_new = pd.DataFrame(data, columns=['Nom de la voiture', 'nature', 'Énergie', 'Boite vitesse', 'Puissance fiscale',
                                    'Transmission', 'Carrosseries', 'Cylindrée', 'Sellerie',
                                    'Nombre de places', 'Nombre de portes', 'Marque', 'Modèle', 'Prix (à partir de)'])

# Load existing data from the Excel file if it exists
try:
    # Check if the file exists
    # Check if the file exists
    if os.path.isfile('new_car_data.xlsx'):
        # Load existing data from the Excel file
        df_old = pd.read_excel('new_car_data.xlsx', engine='openpyxl')
    else:
        # If the file doesn't exist, create an empty DataFrame
        df_old = pd.DataFrame()

    # Combine old and new data
    df_combined = pd.concat([df_old, df_new], ignore_index=True)

    # Remove duplicates based on the columns you want to consider for uniqueness
    df_combined.drop_duplicates(subset=['Nom de la voiture', 'Énergie', 'Boite vitesse', 'Puissance fiscale',
                                        'Transmission', 'Carrosseries', 'Cylindrée', 'Sellerie',
                                        'Nombre de places', 'Nombre de portes', 'Marque', 'Modèle', 'Prix (à partir de)'],
                                inplace=True)

    # Save the combined data to the Excel file
    df_combined.to_excel('new_car_data.xlsx', index=False)
    print("New data added to the existing file.")
except FileNotFoundError:
    # If the file doesn't exist, save the new data directly
    df_new.to_excel('new_car_data.xlsx', index=False)
    print("New file created with the fetched data.")
