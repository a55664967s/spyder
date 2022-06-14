from flask import Flask, request, jsonify
import sqlite3
from flask import Blueprint
from http import HTTPStatus
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import os
import random
import time
comic_blueprints = Blueprint('comic', __name__, template_folder='templates')


@comic_blueprints.route('/comic/download', methods=['POST'])
def download_comic():
    """
    ---
    tags:
      - download_comic API
    parameters:
      - name: body
        in: body
        schema:
            required:
                - comic_path

            properties:
                comic_path:
                    type: string
    responses:
        400:
            description: Error!
        200:
            description: success!
    """
    insertValues = request.get_json()
    comic_path = insertValues['comic_path']
    # target_url = "https://www.baozimh.com/comic/yaoshenji-taxuedongman"
    target_url = comic_path
    r = requests.get(url=target_url)
    bs = BeautifulSoup(r.text, 'lxml')
    list_con_li = bs.find_all('a', class_='comics-chapters__item')
    chapter_names = []
    chapter_urls = []
    # print(comic_list)
    for comic in list_con_li:
        comic_href = comic.get('href') #取得每一話的網址
        comic_name = comic.text #取得每一話的名稱
        chapter_names.insert(0, comic_name)
        chapter_urls.insert(0,  'https://baozimh.com'+comic_href)#拼街完整路徑
        # print('https://baozimh.com'+comic_href)
    for i in range(2):
        delay_choices = [8, 5, 10, 6, 20, 11]  # 延遲的秒數
        delay = random.choice(delay_choices)  # 隨機選取秒數
        time.sleep(delay)  # 延遲
        # print(i)
        os.mkdir('comic/'+chapter_names[i])
        getphoto(chapter_urls[i], chapter_names[i])
    return('success')


def getphoto(comic_path, comic_name):
    # 網路圖片url
    target_url = comic_path
    r = requests.get(url=target_url)
    bs = BeautifulSoup(r.text, 'lxml')
    list_con_li = bs.find_all('amp-img', class_='comic-contain__item')
    for comic in list_con_li:
        comic_href = comic.get('src')
        print(comic_href)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}
        img_url = comic_href
        req = requests.get(url=img_url, headers=headers)
        name = comic_href.split('/')[-1]
        open(f'comic/'+comic_name+'/'+name, 'wb').write(req.content)


@comic_blueprints.route('/comic/getnumber', methods=['POST'])
def getnumber():
    """
    ---
    tags:
      - getnumber_comic API
    parameters:
      - name: body
        in: body
        schema:
            required:
                - comic_path

            properties:
                comic_path:
                    type: string
    responses:
        400:
            description: Error!
        200:
            description: success!
    """
    insertValues = request.get_json()
    comic_path = insertValues['comic_path']
    # target_url = "https://www.baozimh.com/comic/yaoshenji-taxuedongman"
    target_url = comic_path
    r = requests.get(url=target_url)
    bs = BeautifulSoup(r.text, 'lxml')
    list_con_li = bs.find_all('a', class_='comics-chapters__item')
    chapter_names = []
    # print(comic_list)
    for comic in list_con_li:
        comic_name = comic.text
        head = comic_name.find('第')
        tail = comic_name.find('話')
        number = comic_name[head+1:tail]
        # print(number)
        if number.isdigit():
            chapter_names.insert(0, int(number))
    return jsonify(max(chapter_names)), HTTPStatus.OK


@comic_blueprints.route('/comic/add', methods=['POST'])
def add_comic():
    insertValues = request.get_json()
    comic_name = insertValues['comic_name']
    comic_path = insertValues['comic_path']
    conn = sqlite3.connect('spyder.db')
    c = conn.cursor()
    c.execute("INSERT INTO comic (name,path) VALUES ('%s','%s')" %
              (comic_name, comic_path))
    conn.commit()
    conn.close()
@comic_blueprints.route('/comic/list', methods=['GET'])
def comiclist():
    conn = sqlite3.connect('spyder.db')
    c = conn.cursor()
    cursor=c.execute("select * from comic ")
    result=[]
    for row in cursor:
        result.append(row)
    return jsonify(result)