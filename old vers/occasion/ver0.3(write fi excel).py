from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.parse
import re
import pandas as pd

driver = webdriver.Chrome()

base_url = 'https://www.automobile.tn'
driver.get('https://www.automobile.tn/fr/occasion/2')
html = driver.page_source

soup = BeautifulSoup(html, 'lxml')
occasions = soup.find_all('div', class_='occasion-item-v2')

data = []

for occasion in occasions:
    link = occasion.find('a', class_='occasion-link-overlay')['href']
    full_link = urllib.parse.urljoin(base_url, link)
    thumb_cap = occasion.find('div', class_='thumb-caption')
    price_div = occasion.find('div', class_='item-foot')
    name = thumb_cap.find('h2').text
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
    data.append([name.strip(), Kilométrage.strip(), Mise_en_circulation.strip(), Énergie.strip(), Boite_vitesse.strip(),
                 Puissance_fiscale.strip(), Transmission.strip(), Carrosserie.strip(), Date_de_l_annonce.strip(),
                 cylindrée.strip(), couleur_ext.strip(), couleur_int.strip(), sellerie.strip(), nbre_places.strip(),
                 nbre_portes.strip(), marque.strip(), modele.strip(), price.strip()])

# Close the Selenium WebDriver
driver.quit()

# Create DataFrame from the data list
df = pd.DataFrame(data, columns=['Nom de la voiture', 'Kilométrage', 'Mise en circulation', 'Énergie', 'Boite vitesse', 'Puissance fiscale',
                                 'Transmission', 'Carosseries', 'Date annonce', 'Cylindrée', 'Couleur exterieure', 'Couleur interieure', 'Sellerie',
                                 'Nombre de places', 'Nombre de portes', 'Marque', 'Modèle', 'Prix'])

# Save DataFrame to Excel file
df.to_excel('car_data.xlsx', index=False)
