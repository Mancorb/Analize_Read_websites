from selenium import webdriver
from selenium.webdriver.edge.options import Options
from bs4 import BeautifulSoup
import time

reuters = "https://www.reuters.com/world/middle-east/trump-meet-syrian-president-saudi-before-heading-qatar-2025-05-14/"
APnws = "https://apnews.com/article/trump-syria-saudi-arabia-sharaa-assad-sanctions-bb208f25cfedecd6446fd1626012c0fb"
wiki = "https://en.wikipedia.org/wiki/International_System_of_Units"

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

driver = webdriver.Edge(options=options)
driver.get(APnws)

time.sleep(6)

html = driver.page_source
driver.quit()
soup = BeautifulSoup(html, 'html.parser')


possible_containers = [
    {'id': 'mw-content-text'},
    {'id': 'storytext'},
    {'class': 'entry__content'},    
    {'class': 'article-body__content__17Yit'},
    {'class': 'Page-content'},
    {'class': 'storytext'},    
    {'class': 'post-body-content'},
    {'tag':'article','attrs': {'data-testid': 'Article'}},
    {'tag': 'div', 'attrs': {'class': ['RichTextStoryBody', 'RichTextBody']}},
    {'tag':'article'}
]

#"headline" : "Trump meets with Syria's interim president, a first between the nations’ leaders in 25 years",
#  "authors" : [ "ZEKE MILLER", "JON GAMBRELL", "AAMER MADHANI" ],

with open("sample.txt","w", encoding="utf-8") as f:
    f.write(soup.prettify())




article_body = None

#finding its container

for selector in possible_containers:
    if 'id' in selector:
        article_body = soup.find('div',id=selector['id'])

    elif 'class'in selector:
        article_body = soup.find('tag',id=selector['class'])

    elif 'tag' in selector and selector['tag'] == 'article':
        article_body = soup.find('article')
    
    if article_body:
        break

#extract info

if article_body:
    paragraphs = article_body.find_all('p')
    article_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)

    with open("article.txt", 'w', encoding='utf-8') as f:
        f.write(article_text)
    
    print("[+] Article saved")

else:
    print("[!] Error article could not be saved...")
