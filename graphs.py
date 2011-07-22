#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db

from datetime import datetime, timedelta
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import StringIO

YLABELS = {'temperature': u"Temperatur [°C]",
           'airpressure': u"Luftdruck [hPa]"}

#todo: pretty axis-scales
def graph(graph_type): 
    values = [s[graph_type] for s in db.get_last_hour(graph_type)]
    values.reverse()
    plt.plot(values)
    plt.ylabel(YLABELS[graph_type])
    imgdata = StringIO.StringIO()
    plt.savefig(imgdata, format='png')
    plt.clf()
    plt.cla()
    return imgdata.getvalue()