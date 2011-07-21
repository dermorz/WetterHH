#!/usr/bin/env python
# -*- coding: utf-8 -*-

import db
import main

from BeautifulSoup import BeautifulSoup
import datetime
from urllib2 import urlopen

def parse_data():
    url = "http://wetter.rzbd.haw-hamburg.de/php/aktuell_old.php3"
    wetter = urlopen(url).read()
    soup = BeautifulSoup(wetter)
    table = soup.find('table')
    rows = table.findAll('tr')
    for n in xrange(1, 11):
        try:
            cols = rows[n].findAll('td')
            dtstring = cols[7].string + cols[8].string
            snapshot = {'temperature': float(cols[0].string),
                        'humidity': int(cols[1].string),
                        'airpressure': float(cols[2].string),
                        'precipitation': float(cols[3].string),
                        'irradiance': int(cols[4].string),
                        'windspeed': float(cols[5].string),
                        'winddirection': int(cols[6].string),
                        'timestamp': datetime.datetime.strptime(
                                                dtstring, "%d.%m.%Y%H:%M")}
            db.save(snapshot)
        except:
            main.log.warning("parsing error")