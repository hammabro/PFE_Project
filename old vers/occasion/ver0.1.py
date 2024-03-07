from bs4 import BeautifulSoup
import requests
import urllib.parse
import re

base_url = 'https://www.automobile.tn'
html= requests.get('https://www.automobile.tn/fr/occasion')
soup = BeautifulSoup(html.content, 'lxml')
occasions = soup.find_all('div', class_ = 'occasion-item-v2')
for occasion in occasions:
    link = occasion.find('a', class_='occasion-link-overlay')['href']
    full_link = urllib.parse.urljoin(base_url, link)
    thumb_cap =occasion.find('div', class_= 'thumb-caption')
    name = thumb_cap.find('h2').text

    link_html= requests.get(base_url +link)
    link_soup = BeautifulSoup(link_html.content, 'lxml')
    main_specs=link_soup.find('div', class_ = 'main-specs').ul
    cylindre_li = link_soup.find('span', class_='spec-name', text=re.compile(r'\bCylindrée\b'))
    specifications=link_soup.find('div', class_='col-md-6 mb-3 mb-md-0').find('div', class_='box').find('div', class_='divided-specs').ul
    li_contents = []
    cyl_content=''
    li_specifications=[]

    # Iterate over each li item within the ul
    for spec in main_specs.find_all('li'):
        content = spec.find('span',class_ = 'spec-value').get_text(strip=True)
        li_contents.append(content)

    
    #for the cylindrée attribute 
    if cylindre_li:
        cyl_content = cylindre_li.find_next_sibling('span', class_='spec-value').get_text(strip=True)
    else:
        cyl_content = "N/A"




    couleur_ext="N/A"
    couleur_int="N/A"
    sellerie="N/A"
    nbre_portes="N/A"
    nbre_places="N/A"
    marque="N/A"
    modele="N/A"

    
    for specific in specifications.find_all('li'):
        spec_name = specific.find('span',class_ = 'spec-name').get_text(strip=True)
        spec_value = specific.find('span',class_ = 'spec-value').get_text(strip=True)
        if spec_name=="Couleur extérieure" : couleur_ext=spec_value 
        if spec_name=="Couleur intérieure" : couleur_int=spec_value
        if spec_name=="Sellerie" : sellerie=spec_value
        if spec_name=="Nombre de places" : nbre_places=spec_value
        if spec_name=="Nombre de portes" : nbre_portes=spec_value
        if spec_name=="Modèle" : modele=spec_value
        if spec_name=="Marque" : marque=spec_value


        





    
            

    # Now you have a list 'li_contents' containing the content of each li item
    # You can access each item's content using its index, e.g., li_contents[0], li_contents[1], etc.
    # Or you can iterate over the list to access each item's content


    Kilométrage=li_contents[0]
    Mise_en_circulation=li_contents[1]
    Énergie=li_contents[2]
    Boite_vitesse= li_contents[3]
    Puissance_fiscale=li_contents[4]
    Transmission=li_contents[5]
    Carrosserie=li_contents[6]
    Date_de_l_annonce=li_contents[7]
    cylindrée= cyl_content
    






    print(f"car name : {name.strip()} ")
    
    print(f"kilo : {Kilométrage.strip()} \nmise en circulation : {Mise_en_circulation.strip()} \nenergie : {Énergie.strip()} \nboite vitesse : {Boite_vitesse.strip()} \npuissance fiscale : {Puissance_fiscale.strip()} \ntransmission : {Transmission.strip()} \ncarosseries : {Carrosserie.strip()} \ndate annonce : {Date_de_l_annonce.strip()} \ncylindrée : {cylindrée.strip()}\ncouleur exterieure : {couleur_ext.strip()}\ncouleur interieure : {couleur_int.strip()}\nsellerie : {sellerie.strip()}\nnombres de places : {nbre_places.strip()}\nnombre de portes : {nbre_portes.strip()}\nmarque : {marque.strip()}\nmodele : {modele.strip()}\n")
    print("")
    print("----------------------------------------------------------------")
    print("")
    
    