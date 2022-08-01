from bs4 import BeautifulSoup
import requests
from openpyxl import load_workbook


class Category_object:
    def __init__(self, title, descrpition, creator, model):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.creator = creator
        self.model = model

    def print(self):
        print(self.title, self.descrpition, self.model, self.creator)


class CategorySecond:
    def __init__(self, title, descrpition, list_category, list_object):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.list_category = list_category
        self.list_object = list_object

    def print(self):
        print(self.title, self.descrpition, self.list_category, self.list_object)


class Category:
    def __init__(self, title, descrpition, listhref):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.listhref = listhref  # возраст человека

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


def parsing_splash(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find("div", id='content').find('h1').text
    descrpition = soup.find('div', class_='category-info').find('ul').text
    list = []
    for a in soup.find('div', class_='category-list').findAll('a', href=True):
        list.append(a['href'])
    return list


def parsing_splashsecond(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    href = ""
    for i in \
            soup.find('div', class_="content").find('div', class_="product-list").find('div', class_="left").find('div',
                                                                                                                  class_="name").find(
                'a', href=True)['href']:
        href = f"{i}"
    parsing_object(i)


fn = 'shop.xlsx'
wb = load_workbook(fn)
ws = wb['data']

url = 'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

urllist = ['http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/']

for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
    urllist.append(a['href'])

#     list = ""
#     for i in parse.listhref:
#         list = f"{i}, "
#     ws.append([parse.title, parse.descrpition, list])

listurlobj = []
for i in urllist:
    listurlobj = parsing_category_list(i)


# парсит ту хуйню где есть и катергории и объекты по поводо list_object не ебу но там должны быть ссылки
def parsing_category_category(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    description = soup.find('div', class_='category-info').find('ul').text
    list_category = soup.find('div', id='content').find('div', class_='category-list').findAll('a', href=True)
    list_object = soup.find('#content > div.product-list > div:nth-child(1) > div.left > div.image > a')
    return CategorySecond(title=title, descrpition=description, list_category=list_category, list_object=list_object)


def parsing_category_obj(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    creator = soup.find('#content > div.product-info > div.right > div.description > a').text
    model = title.split(" ")[0]
    description = soup.find("#tab-description > ul").text
    return Category_object(title=title, creator=creator, model=model, description=description)


# parsing_category_category('http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/fnc_filtroelem/').print()
# for i in parsing_category_category('http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/fnc_filtroelem/'):
#     print(i)
# wb.save(fn)
# wb.close()
