#!/usr/bin/env python
import db
import graphs
from parse_data import parse_data
from pymongo.errors import DuplicateKeyError
from tornado import ioloop, web, httpserver 
import logging

def feed_db():
    data = parse_data()
    for snapshot in data:
        sn = db.connection.Snapshot()
        for key in snapshot:
            sn[key] = snapshot[key]
        try:
            sn.save()
            logging.info('DB fed')
        except DuplicateKeyError:
            logging.warning('snapshot already in db: [%s]' % snapshot['timestamp'])


class IndexRequestHandler(web.RequestHandler):
    def get(self):
        self.write("<a href='/gtemperature'>temperature</a><br/>\
                    <a href='/gairpressure'>airpressure</a>")

class GraphRequestHandler(web.RequestHandler):
    def get(self, graph_type):
        if graph_type not in ['temperature', 'airpressure']:
            raise web.HTTPError(404)
        self.set_header("Content-Type", "image/png")
        self.write(graphs.graph(graph_type))

if __name__ == '__main__':
    # initial db-feed before timer starts
    #feed_db()
    application = web.Application([
        (r"/", IndexRequestHandler),
        (r"/g(.*)", GraphRequestHandler),
    ])
    http_server = httpserver.HTTPServer(application)
    http_server.listen(8080)
    io_loop = ioloop.IOLoop.instance()
    feed_db_scheduler = ioloop.PeriodicCallback(feed_db, 1000 * 60 * 5, io_loop=io_loop)
    feed_db_scheduler.start()
    io_loop.start()
