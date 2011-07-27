#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db

from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import StringIO

YLABELS = {'temperature': u"Temperatur [°C]",
           'airpressure': u"Luftdruck [hPa]"}

def graph(graph_type):
    snapshots = [sn for sn in db.get_last_6_hours(graph_type)]
    
    values = [snapshot[graph_type] for snapshot in snapshots]
    values.reverse()
    
    timestamps = [snapshot['timestamp'] for snapshot in snapshots]
    timestamps.reverse()
    
    hours = mdates.HourLocator()
    quarter_hours = mdates.MinuteLocator(interval=15)
    hour_format = mdates.DateFormatter("%H:%M")
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(timestamps, values)
    ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_formatter(hour_format)
    ax.xaxis.set_minor_locator(quarter_hours)
    
    ax.set_ylim(min(values)-5, max(values)+5)
    
    fig.autofmt_xdate()
    
    #axis = plt.axis()
    #plt.axis([axis[0], axis[1], axis[2]-5, axis[3]+5])
    #plt.ylabel(YLABELS[graph_type])
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format='png')
    plt.clf()
    plt.cla()
    return imgdata.getvalue()