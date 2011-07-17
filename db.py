#!/usr/bin/env python
from mongokit import *
from datetime import datetime

connection = Connection()

@connection.register
class Snapshot(Document):
    __collection__ = 'snapshots'
    __database__ = 'weatherdata'
    structure = {
        'temperature': float,
        'humidity': int,
        'airpressure': float,
        'precipitation': float,
        'irradiance': int,
        'windspeed': float,
        'winddirection': int,
        'timestamp': datetime
    }
    indexes = [
        {
            'fields': 'timestamp',
            'unique': True
        }
    ]


