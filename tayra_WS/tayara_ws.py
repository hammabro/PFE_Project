from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
import re
import pandas as pd
import os.path

driver = webdriver.Chrome()

base_url = 'https://www.tayara.tn/'

data = []



for i in range(1, 201):
    url = f'https://www.tayara.tn/ads/c/V%C3%A9hicules/Voitures/?page={i}'
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    annonces = soup.find('div').find_all('article', class_='mx-0')

    for annonce in annonces:
        if annonce.find('data') and len(annonce.find('data').find_all('span'))==3 :  
            prix_span = annonce.find('data').find_all('span')
            price_comp = int(prix_span[0].text + prix_span[1].text)
            if price_comp > 5000:
                price = annonce.find('data').text
                car_link = annonce.find('a').get('href')
                car_full_link = urllib.parse.urljoin(base_url, car_link)

                driver.get(car_full_link)
                car_html = driver.page_source
                car_soup = BeautifulSoup(car_html, 'lxml')
                kilometrage = "http:N/A"
                couleur = "N/A"
                etat = "N/A"
                boite = "N/A"
                marque= "N/A"
                modele = "N/A"
                carburant = "N/A"
                annee = "N/A"
                cylindree = "N/A"
                puiss_fiscale = "N/A"
                carrosserie = "N/A"

                if  car_soup.find('div').find('div',class_="h-[1px] w-full bg-gray-300 mt-7 mb-4 undefined") :  
                    criteres_div = car_soup.find('div').find('div',class_="h-[1px] w-full bg-gray-300 mt-7 mb-4 undefined").parent
                    if criteres_div.find('ul',class_="grid gap-3 grid-cols-12") :
                        criteres=criteres_div.find('ul',class_="grid gap-3 grid-cols-12").find_all('li',class_="col-span-6 lg:col-span-3")
                        for critere in criteres : 
                            titre=critere.find('div').find('span').find('span',class_="text-gray-600/80 text-2xs md:text-xs lg:text-xs font-medium").text
                            valeur=critere.find('div').find('span').find('span',class_="text-gray-700/80 text-xs md:text-sm lg:text-sm font-semibold").text

                            if titre=="Kilométrage" : kilometrage=valeur
                            if titre=="Couleur du véhicule" : couleur=valeur
                            if titre=="Etat du véhicule" : etat=valeur
                            if titre=="Boite" : boite=valeur
                            if titre=="Marque" : marque=valeur
                            if titre=="Modèle" : modele=valeur
                            if titre=="Carburant" : carburant=valeur
                            if titre=="Année" : annee=valeur
                            if titre=="Cylindrée" : cylindree=valeur
                            if titre=="Puissance fiscale" : puiss_fiscale=valeur
                            if titre=="Type de carrosserie" : carrosserie=valeur
                
                
                data.append([marque, modele, etat,kilometrage ,carburant , boite, puiss_fiscale , carrosserie, cylindree, annee, price])
    print(f" page {i} succesfully scraped")
        

# Close the Selenium WebDriver after all iterations
driver.quit()

# Create DataFrame from the new data list
df_new = pd.DataFrame(data, columns=['Marque', 'Modele', 'Etat', 'Kilometrage', 'Carburant',
                                    'Boite Vitesse','Puissance Fiscale', 'Carrosseries', 'Cylindrée', 'Annee','Prix (à partir de)'])

# Load existing data from the Excel file if it exists
try:
    # Check if the file exists
    # Check if the file exists
    if os.path.isfile('Tayara_car_data.xlsx'):
        # Load existing data from the Excel file
        df_old = pd.read_excel('Tayara_car_data.xlsx', engine='openpyxl')
    else:
        # If the file doesn't exist, create an empty DataFrame
        df_old = pd.DataFrame()

    # Combine old and new data
    df_combined = pd.concat([df_old, df_new], ignore_index=True)

    # Remove duplicates based on the columns you want to consider for uniqueness
    df_combined.drop_duplicates(subset=['Marque', 'Modele', 'Etat', 'Kilometrage', 'Carburant',
                                    'Boite Vitesse','Puissance Fiscale', 'Carrosseries', 'Cylindrée', 'Annee','Prix (à partir de)'],
                                inplace=True)

    # Save the combined data to the Excel file
    df_combined.to_excel('Tayara_car_data.xlsx', index=False)
    print("New data added to the existing file.")
except FileNotFoundError:
    # If the file doesn't exist, save the new data directly
    df_new.to_excel('Tayara_car_data.xlsx', index=False)
    print("New file created with the fetched data.")
