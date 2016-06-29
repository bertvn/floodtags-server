"""
server script for displaying the floodtags algorithm found at https://github.com/bertvn/floodtags
"""
import configparser
import os
import subprocess
import time

import cherrypy
import psutil


class App(object):
    """
    main server class
    """
    def __init__(self):
        """
        constructor for the App class
        creates the dashboard webpage
        :return: None
        """
        self.dashboard = Dashboard()

    @cherrypy.expose
    def index(self):
        """
        returns the html page
        :return: html page
        """
        return open('public/index.html')

class Dashboard(object):
    """
    dashboard class
    """
    def __init__(self):
        """
        constructor for the dashboard
        :return: None
        """
        self.pro = None

    @cherrypy.expose
    def index(self):
        """
        returns the html page
        :return: html page
        """
        return open('public/dashboard.html')

    @cherrypy.expose
    def start_algorithm(self, source, frame, loops):
        """
        starts the algorithm
        :param source: datastream to be used
        :param frame: time frame the algorithm uses to filter
        :param loops: amount of times the algorithm is repeated after it's initial run
        :return: Json string
        """
        config = configparser.ConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__)) + "/config.ini")
        output = os.path.join(os.path.dirname(os.path.abspath(__file__)) + r"/public/result.json")
        location = os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/", config['algorithm']['location'].replace("\"",""))
        subprocess.Popen("python --version", stdout=subprocess.PIPE,shell=True)
        cmd = "python " + location + "main.py -in \"" + source + "\" -tf " + frame + " -l " + loops + " -out " + output + ""
        self.pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        return "{\"response\" : \"ok\"}"

    @cherrypy.expose
    def stop_algorithm(self):
        """
        stops the algorithm before it's done
        :return: Json string
        """
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
        """
        when algorithm is completed this function pushes the result to the client
        :return: output from the algorithm
        """
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
