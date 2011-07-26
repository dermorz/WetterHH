#!/usr/bin/env python
# -*- coding: utf-8 -*-

import graphs
import parser

from tornado import ioloop, web, httpserver 
import logging

logging.basicConfig()
log = logging.getLogger("WetterHH")
log.setLevel(logging.DEBUG)

class IndexRequestHandler(web.RequestHandler):
    def get(self):
        self.render("templates/base.html", title="WetterHH", graphs=graphs.YLABELS)

class GraphRequestHandler(web.RequestHandler):
    def get(self, graph_type):
        if graph_type not in ['temperature', 'airpressure']:
            raise web.HTTPError(404)
        self.set_header("Content-Type", "image/png")
        self.write(graphs.graph(graph_type))

if __name__ == '__main__':
    application = web.Application([
        (r"/", IndexRequestHandler),
        (r"/g(.*)", GraphRequestHandler),
    ])
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    io_loop = ioloop.IOLoop.instance()
    feed_db_scheduler = ioloop.PeriodicCallback(parser.parse_data, 1000 * 60 * 5, io_loop=io_loop)
    feed_db_scheduler.start()
    io_loop.start()
    log.debug("Server started.")
