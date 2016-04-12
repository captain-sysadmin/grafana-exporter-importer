#!/usr/bin/env python

#This is a tool to get grafana dashboards via the HTTP API
#and transplant them to a different grafana instance.

import os
import requests


try:
    sourceKey   = os.environ['SOURCEKEY']
    destKey     = os.environ['DESTKEY']
except Exception, e:
    print "either SOURCEKEY or DESTKEY not set: {0}".format(e)

sourceHost  = 'http://grafana.ft.com'

source = requests.get('{0}/api/search/?query='.format(sourceHost),headers={'Authorization': 'Bearer {0}'.format(sourceKey)})
print source.json()

