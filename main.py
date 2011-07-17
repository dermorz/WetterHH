#!/usr/bin/env python
import db
from parse_data import parse_data
from pymongo.errors import DuplicateKeyError
from tornado import ioloop
import logging

def feed_db():
    data = parse_data()
    for snapshot in data:
        sn = db.connection.Snapshot()
        for key in snapshot:
            sn[key] = snapshot[key]
        try:
            sn.save()
            logging.info('DB feeded')
        except DuplicateKeyError:
            logging.warning('snapshot already in db: %s' % snapshot['timestamp'])


if __name__ == '__main__':
    # initial db-feed before timer starts
    feed_db()
    io_loop = ioloop.IOLoop.instance()
    feed_db_scheduler = ioloop.PeriodicCallback(feed_db, 1000*60*10, io_loop=io_loop)
    feed_db_scheduler.start()
    io_loop.start()