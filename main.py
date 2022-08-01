from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook


class Category:
    def __init__(self, title, descrpition, listhref):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.listhref = listhref# возраст человека

    def info(self):
        print(self.title, self.descrpition, self.listhref)

def parsing_category(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find("div", id='content').find('h1')
    descrpition = soup.find('div', class_='category-info').find('ul').text
    listhref = []
    for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
        listhref.append(a['href'])

    return Category(title.text, descrpition, listhref)
def parsing_category_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    listhref = []
    for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
        listhref.append(a['href'])

    return listhref


def parsing_object(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find("div", id='content').find('h1').text
    admin_product = soup.find('div', class_='left').find('a').text
    model = title.split(" ")[0]
    description = soup.find('div', id='tab-description').find('ul').text.strip()
    return title, admin_product, model, description
fn = 'shop.xlsx'
wb = load_workbook(fn)
ws = wb['data']

url = 'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

urllist = ['http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/']

for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
    urllist.append(a['href'])


for i in urllist:
    parse = parsing_category(i)
    list = ""
    for i in parse.listhref:
        list = f"{i}, "
    ws.append([parse.title, parse.descrpition, list])

    # parse.info()
    # pd.DataFrame({
    #     "title": parse.title,
    #     "description": parse.descrpition,
    #     "list": parse.listhref
    # }).to_excel('C:/Users/konev/Desktop/Python/teams.xlsx')
listurlobj = []
for i in urllist:
    listurlobj = parsing_category_list(i)


wb.save(fn)
wb.close()