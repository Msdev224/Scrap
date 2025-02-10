#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from requests import get
from bs4 import BeautifulSoup as bs


# In[2]:


url = 'https://www.expat-dakar.com/voitures'
res = get(url)
soup = bs(res.text, 'html.parser')
containers = soup.find_all('div', class_ = 'listings-cards__list-item')


# In[3]:


data = []

for container in containers:
    try:
        # Récupération de l'URL
        url_container = container.find('a', class_='listing-card__inner')['href']
        res_c = get(url_container)
        soup_c = bs(res_c.text, 'html.parser')

        # Récupération des éléments dd
        dd_elements = soup_c.find_all('dd', class_="listing-item__properties__description")
        if len(dd_elements) < 5:
            print("Éléments manquants dans le conteneur")
            continue

        marque = dd_elements[0].text.strip()
        modele = dd_elements[1].text.strip()
        etat = dd_elements[2].text.strip()
        transmission = dd_elements[3].text.strip()
        annee = dd_elements[4].text.strip()

        #
        price = soup_c.find('span', class_="listing-card__price__value").text.strip().replace('F Cfa', '')

        
        address = soup_c.find('span', class_="listing-item__address-location").text.strip()

        # Récupération du lien de l'image
        image_link = soup_c.find('img', class_="gallery__image__resource vh-img").get('src', '')

        dic = {
            'Etat': etat,
            'Marque': marque,
            'Annee': annee,
            'Boite_vitesse': transmission,
            'Prix': price,
            'Adresse': address,
            'Image_link': image_link
        }
        data.append(dic)

    except Exception as e:
        # print(f"Erreur lors du traitement d'un conteneur : {e}")
        pass


# In[4]:


df = pd.DataFrame(data)
df.shape


# In[5]:


df = pd.DataFrame()

for page in range(1, 15):  
    url = url = f'https://www.expat-dakar.com/voitures?page={page}'
    res = get(url)
    soup = bs(res.text, 'html.parser')
    containers = soup.find_all('div', class_='listings-cards__list-item') 

    data = []
    for container in containers:
        try:
            url_container = container.find('a', class_='listing-card__inner')['href']
            res_c = get(url_container)
            soup_c = bs(res_c.text, 'html.parser')
         
            dd_elements = soup_c.find_all('dd', class_="listing-item__properties__description")
            
            marque = dd_elements[0].text.strip()
            modele = dd_elements[1].text.strip()
            etat = dd_elements[2].text.strip()
            transmission = dd_elements[3].text.strip()
            annee = dd_elements[4].text.strip()

            price = soup_c.find('span', class_="listing-card__price__value").text.strip().replace('F Cfa', '')
            address = soup_c.find('span', class_="listing-item__address-location").text.strip()
            image_link = soup_c.find('img', class_="gallery__image__resource vh-img").get('src', '')
           
            dic = {
                'Etat': etat,
                'Marque': marque,
                'Modele': modele,
                'Annee': annee,
                'Boite_vitesse': transmission,
                'Prix': price,
                'Adresse': address,
                'Image_link': image_link
            }
            data.append(dic)
        except Exception as e:
            pass
            # print(f"Erreur lors du traitement d'un conteneur : {e}")
    DF = pd.DataFrame(data)
    df = pd.concat([df,DF], axis=0).reset_index(drop=True)


# In[6]:


df.to_csv('not_data_cleaning_vehicule.csv')


# In[7]:


df


# In[10]:


df['Marque'].unique()

