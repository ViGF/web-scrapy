import requests
from bs4 import BeautifulSoup

arq_csv = open('airbnb.csv', 'w', encoding='utf-8')
baseUrl = 'https://www.airbnb.com.br'
query = '/s/João-Pessoa--State-of-Paraíba--Brazil/homes?adults=1&checkin=2023-02-02&checkout=2023-02-03&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=João%20Pessoa%2C%20State%20of%20Paraíba%2C%20Brazil&place_id=ChIJ16OaATnorAcRNNsmbZxKQW4&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0&price_filter_num_nights=1&search_type=unknown&federated_search_session_id=9a987852-e532-43e2-9636-f8e85bdc9322&pagination_search=true&cursor=eyJzZWN0aW9uX29mZnNldCI6MCwiaXRlbXNfb2Zmc2V0IjowLCJ2ZXJzaW9uIjoxfQ%3D%3D'

def getHTML(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup

def writeInfos(soup):
    titles = soup.find_all('div', {'class': 't1jojoys dir dir-ltr'})
    descriptions = soup.find_all('div', {'class': 'nquyp1l s1cjsi4j dir dir-ltr'})
    prices = soup.find_all('div', {'class': '_tt122m'})
    ratings = soup.find_all('span', {'class': 'r1dxllyb dir dir-ltr'})

    for (title, description, price, rating) in zip(titles, descriptions, prices, ratings):
        accommodation = description.next_sibling.text
        description = description.text
        title = title.text
        neighbourhood = title.split(' em ')[1]
        price = price.text.replace('Total de ', '')
        typeAcomodation = 'Outro'

        if title.__contains__('Apartamento'):
            typeAcomodation = 'Apartamento'
        elif title.__contains__('Quarto inteiro'):
            typeAcomodation = 'Quarto inteiro'
        elif title.__contains__('Quarto compartilhado'):
            typeAcomodation = 'Quarto compartilhado'

        if rating.text != 'Novo':
            ratingString = rating.text.split(' ')
            rating = ratingString[0].replace(',', '.')
            evaluators = ratingString[1].replace('(', '').replace(')', '')
        else:
            rating = 0
            evaluators = 0

        arq_csv.write(
            f"{title};{description};{accommodation};{neighbourhood};{rating};{evaluators};{typeAcomodation};{price}\n"
        )

arq_csv.write("title;description;accommodation;neighbourhood;rating;evaluators;typeAcomodation;price\n")

url = baseUrl + query
soup = getHTML(url)

i = 1

while i:
        try:
            if i == 1:
                writeInfos(soup)
                print(i)
                print(query)

            print(i + 1)
            nextQueryLink = soup.find('button', string=i).next_sibling.get('href')
            print(nextQueryLink)

            url = baseUrl + nextQueryLink
            soup = getHTML(url)

            writeInfos(soup)

            i = i + 1
        except:
            break

arq_csv.close()