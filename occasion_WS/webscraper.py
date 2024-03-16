from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
import re
import pandas as pd
from selenium.webdriver.common.by import By
import time;
driver = webdriver.Chrome()

base_url = 'https://www.automobile.tn'

driver.get('https://www.automobile.tn/fr/occasion')
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

data = []

elements = driver.find_elements(By.CLASS_NAME, "page-item next disabled")
check = 0
i=0
while check == 0 :
    occasions = soup.find_all('div', class_='occasion-item-v2')

    

    for occasion in occasions:
        link = occasion.find('a', class_='occasion-link-overlay')['href']
        full_link = urllib.parse.urljoin(base_url, link)
        thumb_cap = occasion.find('div', class_='thumb-caption')
        price_div = occasion.find('div', class_='item-foot')
        # name = thumb_cap.find('h2').text
        price = price_div.find('div', class_='price').text

        driver.get(full_link)
        link_html = driver.page_source
        link_soup = BeautifulSoup(link_html, 'lxml')
        main_specs = link_soup.find('div', class_='main-specs').ul
        cylindre_li = link_soup.find('span', class_='spec-name', text=re.compile(r'\bCylindrée\b'))
        specifications = link_soup.find('div', class_='col-md-6 mb-3 mb-md-0').find('div', class_='box').find(
            'div', class_='divided-specs').ul
        li_contents = []
        cyl_content = ''

        # Iterate over each li item within the ul
        for spec in main_specs.find_all('li'):
            content = spec.find('span', class_='spec-value').get_text(strip=True)
            li_contents.append(content)

        # for the cylindrée attribute
        if cylindre_li:
            cyl_content = cylindre_li.find_next_sibling('span', class_='spec-value').get_text(strip=True)
        else:
            cyl_content = "N/A"

        couleur_ext = "N/A"
        couleur_int = "N/A"
        sellerie = "N/A"
        nbre_portes = "N/A"
        nbre_places = "N/A"
        marque = "N/A"
        modele = "N/A"

        for specific in specifications.find_all('li'):
            spec_name = specific.find('span', class_='spec-name').get_text(strip=True)
            spec_value = specific.find('span', class_='spec-value').get_text(strip=True)
            if spec_name == "Couleur extérieure":
                couleur_ext = spec_value
            if spec_name == "Couleur intérieure":
                couleur_int = spec_value
            if spec_name == "Sellerie":
                sellerie = spec_value
            if spec_name == "Nombre de places":
                nbre_places = spec_value
            if spec_name == "Nombre de portes":
                nbre_portes = spec_value
            if spec_name == "Modèle":
                modele = spec_value
            if spec_name == "Marque":
                marque = spec_value

        
        nature ="occasion"
        Kilométrage = li_contents[0]
        Mise_en_circulation = li_contents[1]
        Énergie = li_contents[2]
        Boite_vitesse = li_contents[3]
        Puissance_fiscale = li_contents[4]
        Transmission = li_contents[5]
        Carrosserie = li_contents[6]
        Date_de_l_annonce = li_contents[7]
        cylindrée = cyl_content

        # Append data to list
        data.append([nature , Kilométrage.strip(), Mise_en_circulation.strip(), Énergie.strip(), Boite_vitesse.strip(),
                     Puissance_fiscale.strip(), Transmission.strip(), Carrosserie.strip(), Date_de_l_annonce.strip(),
                     cylindrée.strip(), couleur_ext.strip(), couleur_int.strip(), sellerie.strip(), nbre_places.strip(),
                     nbre_portes.strip(), marque.strip(), modele.strip(), price.strip()])
    print('wfe l traitement')
    pages_div= soup.find('div', class_='pages')
    if pages_div.find('li', class_='page-item next disabled') : 
        print('last page')
        check=1
    else :     
        print('mezelna mouch fel last page ')
        if i==10 :
            check=1
        nextBtn_link = pages_div.find('li', class_='page-item next').find('a')['href']
        next_link = urllib.parse.urljoin(base_url,nextBtn_link)
        driver.get(next_link)
        next_html = driver.page_source
        soup = BeautifulSoup(next_html, 'lxml')
        i+=1



# Close the Selenium WebDriver
driver.quit()

# Create DataFrame from the new data list
df_new = pd.DataFrame(data, columns=['Nature' , 'Kilométrage', 'Mise en circulation', 'Carburant', 'Boite Vitesse', 'Puissance Fiscale',
                                 'Transmission', 'Carrosserie', 'Date annonce', 'Cylindrée', 'Couleur exterieure', 'Couleur interieure', 'Sellerie',
                                 'Nombre de places', 'Nombre de portes', 'Marque', 'Modèle', 'Prix'])

# Load existing data from the Excel file if it exists
try:
    df_old = pd.read_excel('car_data.xlsx',engine='openpyxl')
    # Concatenate old and new data
    df_combined = pd.concat([df_old, df_new], ignore_index=True)
    # Remove duplicates based on the columns you want to consider for uniqueness
    df_combined.drop_duplicates(subset=['Nature','Kilométrage', 'Mise en circulation', 'Carburant', 'Boite Vitesse', 'Puissance Fiscale',
                                 'Transmission', 'Carrosserie', 'Date annonce', 'Cylindrée', 'Couleur exterieure', 'Couleur interieure', 'Sellerie',
                                 'Nombre de places', 'Nombre de portes', 'Marque', 'Modèle', 'Prix'], inplace=True)
    # Save the combined data to the Excel file
    df_combined.to_excel('car_data.xlsx', index=False)
    print("New data added to the existing file.")
except FileNotFoundError:
    # If the file doesn't exist, save the new data directly
    df_new.to_excel('car_data.xlsx', index=False)
    print("New file created with the fetched data.")
