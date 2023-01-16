import requests
from bs4 import BeautifulSoup

arq_csv = open('airbnb.csv', 'w', encoding='utf-8')
url = 'https://www.airbnb.com.br/s/Jo%C3%A3o-Pessoa--State-of-Para%C3%ADba--Brazil/homes?adults=1&checkin=2023-02-02&checkout=2023-02-03'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

titles = soup.find_all('div', {'class': 't1jojoys dir dir-ltr'})
descriptions = soup.find_all('div', {'class': 'nquyp1l s1cjsi4j dir dir-ltr'})
prices = soup.find_all('div', {'class': '_tt122m'})
ratings = soup.find_all('span', {'class': 'r1dxllyb dir dir-ltr'})

arq_csv.write("title;description;accommodation;rating;evaluators;price\n")

for (title, description, price, rating) in zip(titles, descriptions, prices, ratings):
    accommodation = description.next_sibling.contents[0].text
    description = description.text
    title = title.text
    price = price.text.replace('Total de ', '')
    ratingString = rating.text.split(' ')
    rating = ratingString[0]
    evaluators = ratingString[1].replace('(', '').replace(')', '')

    arq_csv.write(f"{title};{description};{accommodation};{rating};{evaluators};{price}\n")

arq_csv.close()