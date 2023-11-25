from django.core.management.base import BaseCommand, CommandError
from urllib.request import urlopen
from bs4 import BeautifulSoup
from operator import itemgetter

from hardware_store.models import Product, ProductCategory

URL: str = 'https://hagalo.mx/2812-herramientas-y-automotriz'
NAME: str = 'Herramientas'
DESCRIPTION:str = '''Herramientas automotrices'''
CATEGORY = ProductCategory( name = NAME, description = DESCRIPTION)
CATEGORY.save()

def get_soup(url: str) -> BeautifulSoup:
    """Gets the page source code and returns an BeautifulSoup object"""
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode('utf-8')
    return BeautifulSoup(html, 'html.parser')


def get_page_numbers(soup: BeautifulSoup) -> int:
    """Gets the page numbers, and returns the number"""
    print("Getting number of pages...")
    text = soup.find_all('a', ['class', 'js-search-link'])
    *frst, num, last = text
    return int(num.string)


def extract_articles(page: str) -> list[dict]:
    """Extracts the articles of the store and returns a list with the articles"""
    soup = get_soup(page)
    articles = soup.find_all('article', class_='style_product_default')
    article_list = list()
    for article in articles:
        article_name = article.find('a', class_='product_name').string
        article_price = float(
            (article.find('span', class_='price').string).replace('$', '').replace(',', ''))
        artile_image = article.find('img', class_='first-image').get('src')
        article_stock = article.find(
            'div', class_='availability-list').find('span').string
        if article_stock == 'Out of stock':
            article_stock = 0
        else:
            article_stock = int(article_stock.split()[0])
        # Fills the article dictionary
        article_dict: dict = {
            'name': article_name,
            'price': article_price,
            'image': artile_image,
            'stock': article_stock,
            'category': CATEGORY
        }
        article_list.append(article_dict)
    return article_list


def get_articles():
    # Gets the page quantity
    main_page = get_soup(URL)
    page_numbers = get_page_numbers(main_page)
    all_articles = list()
    # Extracts articles from every page
    for page in range(1, page_numbers):
        url = URL+'?page={page}'
        print(f'Getting page {page} of {page_numbers}')
        article_list = extract_articles(
            url.format(page=page))
        for article in article_list:
            all_articles.append(article)
    return all_articles


class Command(BaseCommand):
    def handle(self, *args, **options):
        articles = get_articles()
        for article in articles:
            name, price, image, stock, category = itemgetter('name', 'price', 'image', 'stock', 'category')(article)
            product = Product(name = name, price = price, image = image, stock = stock, category_id = category)
            product.save()
        
        print('Products saved correctly.')