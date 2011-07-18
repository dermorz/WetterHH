#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO, Image

ylabels = {'temperature': u"Temperatur [°C]",
           'airpressure': u"Luftdruck [hPa]"}

#todo: pretty axis-scales
def graph(graph_type):
    snapshots = db.connection.Snapshot.find().sort('timestamp', -1).limit(60*2)
    values = []
    for sn in snapshots:
        values.append(sn[graph_type])
    values.reverse()
    plt.plot(values)
    plt.ylabel(ylabels[graph_type])
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format='png')
    plt.clf()
    plt.cla()
    return imgdata.getvalue()