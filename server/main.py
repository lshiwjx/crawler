# -*- coding: utf-8 -*-
# filename: main.py
import web
from handle import Handle
import os

urls = (
    '/wx', 'Handle',
    # add show files here
    '/test', 'list_file'
)

class list_file:

    def GET(self):
        file_path = './teacher_info/test.txt'
        if os.path.exists(file_path):
            lines = open(file_path, 'r').readlines()
            return_str = ''
            for line in lines:
                return_str = return_str + line.strip() + '\n'
            return return_str
        else:
            raise web.notfound()


if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
