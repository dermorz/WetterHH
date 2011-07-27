#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""\
snapshot = {'temperature': float,
            'humidity': int,
            'airpressure': float,
            'precipitation': float,
            'irradiance': int,
            'windspeed': float,
            'winddirection': int,
            'timestamp': datetime.datetime}\
"""
import main

import pymongo
from datetime import datetime

connection = pymongo.Connection()
database = connection.weatherdata
collection = database.snapshots
collection.ensure_index('timestamp', unique=True)

def save(snapshot):
    collection.save(snapshot)
    main.log.debug("Snapshot saved: %s" % snapshot['timestamp'])
    connection.end_request()

def get_last_n_snapshots(data_type, n):
    return collection.find({}, {data_type: 1, 'timestamp': 1}).sort('timestamp', -1).limit(n)

# following just for readability
def get_last_hour(data_type):
    return get_last_n_snapshots(data_type, 60)

def get_last_6_hours(data_type):
    return get_last_n_snapshots(data_type, 60*6)

def get_last_day(data_type):
    return get_last_n_snapshots(data_type, 60*24)

def get_last_3_days(data_type):
    return get_last_n_snapshots(data_type, 60*24*3)

def get_last_week(data_type):
    return get_last_n_snapshots(data_type, 60*24*7)