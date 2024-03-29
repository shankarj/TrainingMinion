import os
import sys
os.environ["DJANGO_SETTINGS_MODULE"] = "TrainingMinion.settings"

import cherrypy
import django
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from Core.wrappers import config_manager
import Core.core_api as core_api

class DjangoApplication(object):
    HOST = "127.0.0.1"

    def mount_static(self, url, root):
        """
        :param url: Relative url
        :param root: Path to static files root
        """
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def run(self, port):
        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': port,
            'engine.autoreload_on': False,
            'log.screen': True
        })
        self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)

        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()

        cherrypy.engine.block()


if __name__ == "__main__":
    try:
        port = sys.argv[1].split(":")[1]
    except Exception as ex:
        port = 8000

    try:
        core_api.set_engine_id(sys.argv[1])
        config_manager.read_config_file()
        django.setup()
        DjangoApplication().run(int(port))
        print ("Your app is running at http://localhost:" + str(port))
    except Exception as ex:
        pass