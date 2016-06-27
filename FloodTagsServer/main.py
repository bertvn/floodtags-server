import configparser
import os
import subprocess
import time

import cherrypy
import psutil


class App(object):
    def __init__(self):
        self.dashboard = Dashboard()

    @cherrypy.expose
    def index(self):
        return open('public/index.html')

class Dashboard(object):
    def __init__(self):
        self.pro = None

    @cherrypy.expose
    def index(self):
        return open('public/dashboard.html')

    @cherrypy.expose
    def start_algorithm(self, source, frame, loops):
        config = configparser.ConfigParser()
        config.read(os.path.dirname(__file__) + "/config.ini")
        print(os.path.dirname(__file__) + "/config.ini")
        print(config.sections())
        output = os.path.join(os.path.dirname(__file__) + "/public/result.json")
        location = os.path.join(os.path.dirname(__file__) + "/", config['algorithm']['location'])
        cmd = "python " + location + "main.py -in \"" + source + "\" -tf " + frame + " -l " + loops + " -out \"" + output + "\""
        print(cmd)
        self.pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return "{\"response\" : \"ok\"}"

    @cherrypy.expose
    def stop_algorithm(self):
        if not self.pro:
            return
        process = psutil.Process(self.pro.pid)
        for proc in process.get_children(recursive=True):
            proc.kill()
        process.kill()
        # os.killpg(os.getpgid(self.pro.pid), signal.SIGTERM)  # Send the signal to all the process groups
        self.pro = None
        return "{\"response\" : \"ok\"}"

    @cherrypy.expose
    def get_data(self):
        cherrypy.response.headers["Content-Type"] = "text/event-stream;charset=utf-8"

        def content():
            while True:
                try:
                    with open('public/result.json', 'r', encoding='utf-8') as myfile:
                        results = myfile.read().replace('\n', '')
                    data = 'data: ' + results + '\n\n'
                    yield data
                    os.remove("public/result.json")
                except FileNotFoundError:
                    pass
                time.sleep(60)

        return content()


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

    cherrypy.server.socket_host = '0.0.0.0'
    cherrypy.quickstart(App(), '/', conf)
