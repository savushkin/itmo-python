"""
Вход: файл guess.txt содержащий имена для угадывания 

(например из http://www.biographyonline.net/people/famous-100.html можно взять имена)


Написать игру "Угадай по фото"

3 уровня сложности:
1) используются имена только 1-10
2) имена 1-50
3) имена 1-100

- из используемых имен случайно выбрать одно
- запустить поиск картинок в Google по выбранному
- получить ~30-50 первых ссылок на найденные по имени изображения
- выбрать случайно картинку и показать ее пользователю для угадывания
  (можно выбрать из выпадающего списка вариантов имен)
- после выбора сказать Правильно или Нет

п.с. желательно делать серверную часть, т.е. клиент играет в обычном браузере обращаясь к веб-серверу.

п.с. для поиска картинок желательно эмулировать обычный пользовательский запрос к Google
т.е. можно использовать и Google image search API
https://ajax.googleapis.com/ajax/services/search/images? или др. варианты
НО в таком случае нужно предусмотреть существующие ограничения по кол-ву запросов
т.е. кешировать информацию на случай исчерпания кол-ва разрешенных (бесплатных)
запросов или другим образом обходить ограничение.
Т.е. игра не должна прерываться после N запросов (ограничение API)


п.с. желательно "сбалансировать" параметры поиска (например искать только лица, 
использовать только первые 1-30 найденных и т.п.)
для минимизации того что найденная картинка не соответствует имени


"""
import json
import random
import re
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

from bs4 import BeautifulSoup


def get_soup(url, header):
    return BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')


names = []


class GuessWhoHTTPServer(BaseHTTPRequestHandler):
    level = ''
    image_type = 'Action'
    current_name = ''

    # GET
    def do_GET(self):
        if self.path == "/":
            self.path = "/static/index.html"
        try:
            send_reply = False
            if self.path.endswith(".html"):
                mime_type = 'text/html'
                send_reply = True
            if self.path.endswith(".jpg"):
                mime_type = 'image/jpg'
                send_reply = True
            if self.path.endswith(".gif"):
                mime_type = 'image/gif'
                send_reply = True
            if self.path.endswith(".js"):
                mime_type = 'application/javascript'
                send_reply = True
            if self.path.endswith(".css"):
                mime_type = 'text/css'
                send_reply = True

            if send_reply:
                f = open('./' + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mime_type)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            else:
                if self.path.startswith('/set-level'):
                    parsed = urlparse(self.path)
                    self.handle_start_game(parse_qs(parsed.query)['value'])
                if self.path.startswith('/send-result'):
                    parsed = urlparse(self.path)
                    self.handle_result(parse_qs(parsed.query)['value'])
            return
        except IOError:
            self.send_error(404, 'Not Found: %s' % self.path)

    def handle_start_game(self, level):
        global names
        self.level = level
        random.seed()
        self.current_name = self.get_random_name()
        print(self.current_name)

        query = '+'.join(self.current_name.split())
        url = "https://www.google.ru/search?site=&tbm=isch&source=hp&biw=1600&bih=1600&q={0}&oq={0}".format(query)
        header = {'User-Agent': 'Mozilla/5.0'}
        soup = get_soup(url, header)

        images = [a['src'] for a in soup.find_all("img", {"src": re.compile("gstatic.com")})]
        response = {
            'images': [
                {'url': images[random.randint(0, len(images)-1)]},
                {'url': images[random.randint(0, len(images)-1)]},
                {'url': images[random.randint(0, len(images)-1)]}
            ],
            'var': [
                self.get_random_name(),
                self.get_random_name(),
                self.get_random_name(),
                self.get_random_name()
            ],
            'correct_answer': self.current_name
        }

        response['var'][random.randint(0, 3)] = self.current_name

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes(json.dumps(response), encoding='utf-8'))

    def get_random_name(self):
        if self.level == ['low']:
            return names[random.randint(0, 10)]
        if self.level == ['middle']:
            return names[random.randint(0, 50)]
        if self.level == ['hard']:
            return names[random.randint(0, 99)]


def run():
    global names
    print('starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, GuessWhoHTTPServer)
    print('parsing names...')
    args = sys.argv[1:]
    if not args:
        print('use: guess.txt')
        sys.exit(1)
    else:
        file = open(args[0], 'rt')
        file_content = file.read()
        file.close()
        names = file_content.split('\n')

    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
