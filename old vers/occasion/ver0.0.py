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

    link_html= requests.get(full_link)
    link_soup = BeautifulSoup(link_html.content, 'lxml')
    main_specs=link_soup.find('div', class_ = 'main-specs').ul
    cylindre_li = link_soup.find('span', class_='spec-name', text=re.compile(r'\bCylindrée\b'))
    li_contents = []
    cyl_content=''

    # Iterate over each li item within the ul
    for spec in main_specs.find_all('li'):
        content = spec.find('span',class_ = 'spec-value').get_text(strip=True)
        li_contents.append(content)

    if cylindre_li:
        cyl_content = cylindre_li.find_next_sibling('span', class_='spec-value').get_text(strip=True)
    else:
        cyl_content = "N/A"
    
            

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
    
    print(f"kilo : {Kilométrage.strip()} \nmise en circulation : {Mise_en_circulation.strip()} \nenergie : {Énergie.strip()} \nboite vitesse : {Boite_vitesse.strip()} \npuissance fiscale : {Puissance_fiscale.strip()} \ntransmission : {Transmission.strip()} \ncarosseries : {Carrosserie.strip()} \ndate annonce : {Date_de_l_annonce.strip()} \ncylindrée : {cylindrée.strip()}")
    print("")
    print("----------------------------------------------------------------")
    print("")


    