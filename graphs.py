#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db

from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import StringIO

GRAPH_TYPES = {'temperature': u"Temperatur [°C]",
               'airpressure': u"Luftdruck [hPa]"}

GRAPH_INTERVALS = {'last_hour':
                        {'func': db.get_last_hour,
                         'label': "Die letzte Stunde",
                         'sort': 1},
                   'last_6_hours':
                        {'func': db.get_last_6_hours,
                         'label': "Die letzten 6 Stunden",
                         'sort': 2},
                   'last_day':
                        {'func': db.get_last_day,
                         'label': "Der letzte Tag",
                         'sort': 3},
                   'last_3_days':
                        {'func': db.get_last_3_days,
                         'label': "Die letzten 3 Tage",
                         'sort': 4},
                   'last_week':
                        {'func': db.get_last_week,
                         'label': "Die letzte Woche",
                         'sort': 5}}
                   

def graph(graph_type, graph_interval):
    data_getter = GRAPH_INTERVALS[graph_interval]['func']
    snapshots = [sn for sn in data_getter(graph_type)]
    
    values = [snapshot[graph_type] for snapshot in snapshots]
    values.reverse()
    
    timestamps = [snapshot['timestamp'] for snapshot in snapshots]
    timestamps.reverse()
    
    hours = mdates.HourLocator()
    quarter_hours = mdates.MinuteLocator(byminute=1, interval=15)
    hour_format = mdates.DateFormatter("%H:%M")
    
    fig = plt.figure(figsize=(4, 3), dpi=240)
    ax = fig.add_subplot(111)
    ax.plot(timestamps, values)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hour_format)
    
    #needs some tweaking:
    ax.xaxis.set_minor_locator(quarter_hours)
    
    ax.set_ylim(min(values) - 5, max(values) + 5)
    
    ax.grid(True)
    
    fig.autofmt_xdate()
    
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format='png')
    plt.clf()
    plt.cla()
    return imgdata.getvalue()
