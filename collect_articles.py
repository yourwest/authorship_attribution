__author__ = 'angelinaprisyazhnaya'

import re
import requests
import os
import urllib
import urllib.request as urlr

urls = ['https://slon.ru/authors/100021', 'https://slon.ru/authors/100053', 'https://slon.ru/authors/39477',
        'https://slon.ru/authors/37648', 'https://slon.ru/authors/39194', 'https://slon.ru/authors/817']

MAIN_URL = 'https://slon.ru'

# Собирает адреса статей со страницы автора.
def collect_urls(url):
    article_urls = []
    url_part = re.search('/authors/\d+', url)
    page_content = requests.get(url).content.decode('utf8')
    article_url = re.findall(r'/posts/\d+', page_content, flags=re.DOTALL)
    for i in set(article_url):
        article_urls.append(MAIN_URL + i)
    next_page = re.search(r'"(\?page=\d+)"\sclass="next-button"', page_content, flags=re.DOTALL)
    if next_page is not None:
        next_page_url = MAIN_URL + url_part.group(0) + next_page.group(1)
        for item in collect_urls(next_page_url):
            article_urls.append(item)
    return article_urls

# Находит название и содержание статьи.
def parse_html(page):
    article_name = re.findall('data-title="(.*?)"', page, flags=re.DOTALL)
    if not article_name != []:
        article_name = re.findall('<title>(.*?)</title>', page, flags=re.DOTALL)
    article_authors = re.findall('data-dimension2="(.*?)"', page, flags=re.DOTALL)
    article_content = re.findall('<div class="post-content with-marker">(.*?)<script type="text/javascript">', page, flags=re.DOTALL)
    if not article_content != []:
        article_content = re.findall('<div id="content" >(.*?)<div class="b-fb-group-join">', page, flags=re.DOTALL)
    if not article_content != []:
        article_content = re.findall('<div class="post-content ">(.*?)<script type="text/javascript">', page, flags=re.DOTALL)
    if not article_content == []:
        name = ''.join(article_name[0].replace('\n', '').replace('/', '-').strip(' '))
        #content = re.sub('[1-9a-zA-Z]|0|#|,|\.|\{|:|\(|\)|\}|\]|\[|;|=|&|\||!|\?|"|\'|/|_|»|«|–|-|—|\*|<|>|@|\+|%', '', article_content[0])
        content = re.sub('<.*?>', '', article_content[0])
        content = re.sub('\s{2,}', ' ', content)
        #content = re.sub('^\s+|\n|\r|\s+$', '', content)
        return [name, content, article_authors]

# Для каждого url (для каждого автора) ищутся ссылки на его статьи, затем на странице
# статьи ищется название и текст. Текст сохраняется в текстовый файл (название файла - название 
# статьи), все текстовые файлы одного автора сохраняются в одну папку (название папки - ID автора).
for url in urls:
    author_number = re.search('/([0-9]+)\\b', url)
    author = author_number.group(1)
    try:
        os.mkdir(author)
    except:
        continue

    article_urls = collect_urls(url)
    for article_url in article_urls:
        try:
            article_page = urlr.urlopen(article_url)
            page_content = article_page.read().decode('utf-8')
            info = parse_html(page_content)
            if info is not None:
                if info[0].endswith('»'):
                    continue
                if len(info[1].split()) < 100 or len(info[1].split()) > 1000:
                    continue
                else:
                    article = open('./' + author + '/' + info[0] + '.txt', 'w', encoding='utf-8')
                    article.write(info[1])
                    article.close()
        except urllib.error.HTTPError:
            continue


