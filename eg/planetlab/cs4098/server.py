# 
# Invokes the pre-deployment analysis for the IEEE workflow
#
# Copyright (c) 2013 by Michael Luckeneder
#

import tornado.httpserver, tornado.ioloop, tornado.options, tornado.web, os.path, random, string
from tornado.options import define, options
import Image, ImageFilter, StringIO
import gc
define("port", default=31415, help="run on the given port", type=int)


class UploadHandler(tornado.web.RequestHandler):
    """Example web service"""

    def post(self):
        """Handles post request"""
        
        # fixes PlanetLab memory overflow bug
        gc.enable()

        # retrieve filename
        file1 = self.request.files['file'][0]
        original_fname = file1['filename']


        # fixes PlanetLab memory overflow bug
        gc.collect();

        # write file body to HTTP response
        self.finish(StringIO.StringIO(file1['body']).getvalue())
        
application = tornado.web.Application([
            (r"/process", UploadHandler)
        ])

if __name__ == "__main__":
    application.listen(31415)
    tornado.ioloop.IOLoop.instance().start()