#
# Простой RSS reader
#
# При добавлении ленты (например https://habrahabr.ru/rss/interesting/)
# записи из добавленной ленты сканируются и заносятся в базу (например sqlite)
#
# При нажатии на кнопку обновить - новое сканирование и добавление новых записей (без дублрования существующих)
#
# Отображение ленты начиная с самых свежих записей с пагинацией (несколько записей на странице)
#
# Записи из разных лент хранить и показывать отдельно (по названию ленты).
#
#
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

import feedparser
from bson.json_util import dumps, loads
from bson.objectid import ObjectId
from pymongo import MongoClient


class GuessWhoHTTPServer(BaseHTTPRequestHandler):
    def do_GET(self):
        client = MongoClient('localhost', 27017)
        db = client['rss-scroller']
        tapes = db['tapes']
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

            if self.path.startswith('/get-tapes'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(bytes(dumps(self.get_tapes(tapes)), encoding='utf-8'))

            if self.path.startswith('/get-records'):
                params = parse_qs(urlparse(self.path).query)
                page = int(params['page'][0])
                size = int(params['size'][0])
                tape_id = params['tape'][0]
                tape = tapes.find_one({'_id': ObjectId(tape_id)})
                response = '{{"records":{0}, "pagination":{1}}}'
                if tape is None:
                    print('tape {} not found'.format(tape_id))
                else:
                    records = db['{}_records'.format(tape_id)]
                    all_records = list(records.find())
                    for record in all_records:
                        del record['_id']
                    total = len(all_records)
                    pagination = '{{"page":{0}, "size":{1}, "total":{2}}}'.format(page, size, total)
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    if page * size > total:
                        self.wfile.write(bytes(response.format(dumps(all_records), pagination), encoding='utf-8'))
                    else:
                        self.wfile.write(
                            bytes(response.format(dumps(all_records[(page * size):(page * size + size)]), pagination),
                                  encoding='utf-8'))

            if self.path.startswith('/reload-tape'):
                tape_id = parse_qs(urlparse(self.path).query)['tape'][0]
                tape = tapes.find_one({'_id': ObjectId(tape_id)})
                if tape is None:
                    print('tape {} not found'.format(tape_id))
                else:
                    records = db['{}_records'.format(tape_id)]
                    new_records = self.update_records(tape)['entries']
                    for record in new_records:
                        if 'id' not in record:
                            record['id'] = record['link']
                        if records.find_one({'id': record['id']}) is None:
                            records.insert_one(
                                {"id": record['id'], "link": record['link'], "published": record['published'],
                                 "summary": record['summary']})
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()

            return
        except IOError:
            self.send_error(404, 'Not Found: %s' % self.path)

    def do_POST(self):
        client = MongoClient('localhost', 27017)
        db = client['rss-scroller']
        tapes = db['tapes']
        if self.path.startswith('/add-tape'):
            self.add_tape(tapes, loads(self.rfile.read(int(self.headers['Content-Length'])).decode("utf-8")))
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(dumps(self.get_tapes(tapes)), encoding='utf-8'))

    def get_tapes(self, _tapes):
        return _tapes.find()

    def add_tape(self, _tapes, tape):
        if _tapes.find_one({'url': tape['url']}) is None:
            _tapes.insert_one(tape)
            return True
        return False

    def update_records(self, tape):
        return feedparser.parse(tape['url'])


def run():
    print('starting server...')
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, GuessWhoHTTPServer)
    print('running server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
