from bs4 import BeautifulSoup
import requests
from openpyxl import Workbook

fn = 'shop.xlsx'
wb = Workbook()
ws = wb.active
ws.append(['Название', 'Артикул', 'Описание (html)', 'Производитель', 'Модель', 'Категория'])
ws2 = wb.create_sheet(title="categories")
ws2.append(['Название', 'Фотография', 'Описание (html)', 'Родительская категория'])


class Category_object:
    def __init__(self, title, article, descrpition, creator, model, category):
        self.title = title
        self.article = article
        self.descrpition = descrpition
        self.creator = creator
        self.model = model
        self.category = category
        self.index = 1


class CategorySecond:
    def __init__(self, src, title, descrpition, list_category, list_object, category):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.listhref = list_category
        self.list_object = list_object
        self.index = 1
        self.src = src
        self.category = category


class Category:
    def __init__(self, src, category, title, descrpition, listhref):
        self.title = title  # имя человека
        self.descrpition = descrpition
        self.listhref = listhref  # возраст человека
        self.index = 1
        self.src = src
        self.category = category


def parsing_category(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find("div", id='content').find('h1')
    descrpition = soup.find('div', class_='category-info').find('ul').text

    photo = soup.find('div', id='content').find('div', class_='category-info').find('div', class_='image').find(
        'img').get('src')
    p = requests.get(photo)
    out = open(f"photos/Фильтроэлементы.png", "wb")
    out.write(p.content)
    out.close()
    listhref = []
    for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
        listhref.append(a['href'])
    return Category(title.text, descrpition, str(listhref), "", photo)


def parsing_category_list(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    listhref = []
    for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
        listhref.append(a['href'])

    return listhref


url = 'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

urllist = ['http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/']

for a in soup.find('div', class_='category-list').find('ul').findAll('a', href=True):
    urllist.append(a['href'])


def save_ws(title, model, description, creator):
    print(1 + '1')
    ws2.append([title, creator, model, description])


listurlobj = []
for i in urllist:
    listurlobj = parsing_category_list(i)


# парсит ту хуйню где есть и катергории и объекты по поводо list_object не ебу но там должны быть ссылки
def parsing_category_category(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    category = soup.find('div', id='content').find('div', class_='breadcrumb').find_all('a')[-2].text
    photo = soup.find('div', id='content').find('div', class_='category-info').find('div', class_='image').find(
        'img').get('src')
    title = soup.find('div', id='content').find('h1').text
    p = requests.get(photo)
    out = open(f"photos/f{title}.png", "wb")
    out.write(p.content)
    out.close()
    description = soup.find('div', class_='category-info').find('ul').text
    list_category = []
    for item in soup.find('div', id='content').find('div', class_='category-list').find_all('li'):
        list_category.append(item.find('a', href=True)['href'])
    list_object = []
    for href in soup.find_all("#content > div.product-list > div:nth-child(1) > div.left"):
        list_object.append(href.find('div', class_='name').find('a', href=True)['href'])

    print(photo, title, list_category, list_object, category)

    parent_category = soup.select('#content > div.breadcrumb > a:nth-child(5)')[0].text

    parent_category = '' if parent_category == title else parent_category

    ws2.append([title, photo, description, parent_category])
    return CategorySecond(src=photo, title=title, descrpition=description, list_category=list_category,
                          list_object=list_object, category=category)


def parsing_category_category_first(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    photo = soup.find('div', id='content').find('div', class_='category-info').find('div', class_='image').find(
        'img').get('src')
    title = soup.find('div', id='content').find('h1').text
    p = requests.get(photo)
    out = open(f"photos/f{title}.png", "wb")
    out.write(p.content)
    out.close()
    category = soup.find('div', id='content').find('div', class_='breadcrumb').find_all('a')[-2].text
    description = soup.find('div', class_='category-info').find('ul').text
    list_category = []
    for item in soup.find('div', id='content').find('div', class_='category-list').find_all('li'):
        list_category.append(item.find('a', href=True)['href'])

    return Category(title=title, descrpition=description, listhref=list_category, category=category, src=photo)


def take_href_from_splash(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    list = []
    for item in soup.find('div', id="content").find('div', class_="product-list").find_all('div', class_='name'):
        list.append(item.find('a', href=True).get('href'))
    return list


def take_href_from_splash_with_add(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    list = []
    for item in soup.find('div', id="content").find('div', class_="product-list").find_all('div', class_='name'):
        list.append(item.find('a', href=True).get('href'))
    title = soup.select('#content > h1')[0].text
    photo = soup.select('#content > div.category-info > div > img')[0].get('src')
    p = requests.get(photo)
    out = open(f"photos/f{title}.png", "wb")
    out.write(p.content)
    out.close()
    description = soup.select('#content > div.category-info')[0].get_text()
    parent_category = soup.select('#content > div.breadcrumb > a:nth-child(5)')[0].text
    parent_category = '' if parent_category == title else parent_category
    ws2.append([title, photo, description, parent_category])
    return list


def parsing_category_obj_in_one_example(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', id='content').find('h1').text
    creator = soup.find('div', class_='right').find('a').text
    model = soup.select('#content > div.product-info > div.right > div.description')[0].get_text()
    model = model.split('\n')[2].split(': ')[1]
    description = soup.find('div', id='content').find('div', id='tab-description').text.strip()
    category = soup.select('#content > div.breadcrumb > a:nth-child(6)')[0].text

    return Category_object(title=title, creator=creator, model=model, descrpition=description, article=model,
                           category=category)


def add_in_csv_obj(clas):
    save_ws(clas.title, clas.creator, clas.model, clas.descrpition)


def save_product(clas):
    ws.append([clas.title, clas.article, clas.descrpition, clas.creator, clas.model, clas.category])


def add_in_csv_category(clas):
    list = ""
    for uri in clas.listhref:
        list = f"{uri}, "
    ws2.append([
        clas.title, clas.src, clas.descrpition, list
    ])


urls = [
    'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfne_series/',
    'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/fnc_filtroelem/',
    'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfnm_series/',
    'http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfew_series/']

second = parsing_category_category_first('http://www.shopprom.ru/aspiration/wamflo/wamflo_filtroelement/kfne_series/')

for i in second.listhref:  # Там где нет подкатегорий
    # print(i)
    for item in take_href_from_splash(i):
        obj = parsing_category_obj_in_one_example(item)
        save_product(obj)
size = 0
for uri in urls:  # категория
    category = parsing_category_category(uri)
    for item in category.listhref:
        try:
            for i in take_href_from_splash_with_add(item):
                # print(item, i, 'lol')
                size += 1
                if size == 139:
                    break

                obj = parsing_category_obj_in_one_example(i)
                save_product(obj)
                # add_in_csv_obj(obj)
        except Exception as e:
            print(e)

    for item in category.list_object:
        # print(item)
        obj = parsing_category_obj_in_one_example(item)
        add_in_csv_obj(obj)

wb.save(fn)
