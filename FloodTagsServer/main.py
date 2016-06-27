import os

import cherrypy


class App(object):
    first = True

    def __init__(self):
        self.dashboard = Dashboard()

    @cherrypy.expose
    def index(self):
        return open('public/index.html')


class Dashboard(object):
    @cherrypy.expose
    def index(self):
        return open('public/dashboard.html')


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
            'tools.encode.encoding': 'utf-8'
        },
        '/dashboard/get_data': {
            'response.stream': True,
            'tools.encode.encoding': 'utf-8'
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    cherrypy.quickstart(App(), '/', conf)
