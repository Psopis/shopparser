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
        self.listhref = list_category
        self.list_object = list_object

    def print(self):
        print(self.title, self.descrpition, self.listhref, self.list_object)


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


fn = 'shop.xlsx'
wb = load_workbook(fn)
ws = wb['data']

url = 'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

urllist = ['http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/']

for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
    urllist.append(a['href'])


def save_ws(title, model, description, creator):
    ws.append([title, creator, model, description])


listurlobj = []
for i in urllist:
    listurlobj = parsing_category_list(i)


# парсит ту хуйню где есть и катергории и объекты по поводо list_object не ебу но там должны быть ссылки
def parsing_category_category(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    description = soup.find('div', class_='category-info').find('ul').text
    list_category = []
    for item in soup.find('div', id='content').find('div', class_='category-list').find_all('li'):
        list_category.append(item.find('a', href=True)['href'])
    list_object = []
    for href in soup.find_all("#content > div.product-list > div:nth-child(1) > div.left"):
        list_object.append(href.find('div', class_='name').find('a', href=True)['href'])

    return CategorySecond(title=title, descrpition=description, list_category=list_category, list_object=list_object)


def parsing_category_category_first(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    description = soup.find('div', class_='category-info').find('ul').text
    list_category = []
    for item in soup.find('div', id='content').find('div', class_='category-list').find_all('li'):
        list_category.append(item.find('a', href=True)['href'])

    return Category(title=title, descrpition=description, listhref=list_category)


def take_href_from_splash(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    list = []
    for item in soup.find('div', id="content").find('div', class_="product-list").find_all('div', class_='name'):
        list.append(item.find('a', href=True).get('href'))
    return list


def parsing_category_obj_in_one_example(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    creator = soup.find('div', class_='right').find('a').text
    model = soup.find('/html/body/div[1]/div[5]/div[2]/div[2]/div[1]/text()[1]')
    description = soup.find('div', id='content').find('div', id='tab-description').text.strip()

    return Category_object(title=title, creator=creator, model=model, descrpition=description)


def add_in_csv_obj(clas):
    save_ws(clas.title, clas.creator, clas.model, clas.descrpition)


def add_in_csv_category(clas):
    list = ""
    for uri in clas.listhref:
        list = f"{uri}, "
    ws.append([clas.title, clas.descrpition, list])


urls = [
        'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/fnc_filtroelem/',
        'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfnm_series/',
        'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfew_series/']

first = parsing_category('http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/')
add_in_csv_category(first)
second = parsing_category_category_first('http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfne_series/')
add_in_csv_category(second)

for i in second.listhref:
    for item in take_href_from_splash(i):
        print(item)
        parsing_category_obj_in_one_example(item).print()
        add_in_csv_obj(parsing_category_obj_in_one_example(item))
    pass

for uri in urls:
    category = parsing_category_category(uri)
    add_in_csv_category(category)
    category.print()
    for item in category.listhref:

        for i in take_href_from_splash(item):
            obj = parsing_category_obj_in_one_example(i)
            parsing_category_obj_in_one_example(i).print()
            add_in_csv_obj(obj)
    for item in category.list_object:
        obj = parsing_category_obj_in_one_example(item)
        add_in_csv_obj(obj)
        obj.print()

wb.save(fn)
wb.close()
