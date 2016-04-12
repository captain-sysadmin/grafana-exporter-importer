#!/usr/bin/env python

#This is a tool to get grafana dashboards via the HTTP API
#and transplant them to a different grafana instance.

import os
import json
import requests
import progressbar


#get the API keys for each service.
#source needs viewer, dest needs admin

try:
    sourceKey   = os.environ['SOURCEKEY']
    destKey     = os.environ['DESTKEY']
except Exception, e:
    print "either SOURCEKEY or DESTKEY not set: {0}".format(e)


destructive     = True #delete the destination dashboards before over writing
sourceHost      = 'http://grafana.ft.com'
destHost        = 'http://dev.grafana.ft.com'
auth            = {
    'source':{'Authorization': 'Bearer {0}'.format(sourceKey)},
    'dest': {'Authorization': 'Bearer {0}'.format(destKey),'content-type': 'application/json'}
    }


#lets search the source for all dashboards:
source = requests.get('{0}/api/search/?query='.format(sourceHost),headers=auth['source'])
dashboards =  source.json()

tags                = []
dashboardToUpload   = []

print "Downloading dashboards from source grafana instance"
pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()],maxval=len(dashboards)).start()
i = 0
#now lets go through them all and download the dashboard
for dashboard in dashboards:
    pbar.update(i)
    i = i +1
    getDashboard = requests.get('{0}/api/dashboards/{1}'.format(sourceHost, dashboard['uri']), headers=auth['source'])
    if getDashboard.status_code == requests.codes.ok:#pylint: disable=no-member
        newDashboard = getDashboard.json()
        if destructive:
            newDashboard['overwrite'] = True

        #set the id to null, otherwise we get a 404
        #matching is done on title
        newDashboard['dashboard']['id'] = None
        newDashboard['dashboard']['tags'] = dashboard['tags']
        dashboardToUpload.append(newDashboard)
    else:
        print "failed to download: {0}".format(dashboard['title'])
pbar.finish()

#we now have all the dashboards (we hope)
#lets start pushing them into the destination grafana server
print "Uploading dashboards to destination Grafana instance"
pbar = progressbar.ProgressBar(widgets=[progressbar.Percentage(), progressbar.Bar()],maxval=len(dashboards)).start()
i = 0
for dashboard in dashboardToUpload:
    pbar.update(i)
    i = i +1
    destination = requests.post('{0}/api/dashboards/db'.format(destHost), data=json.dumps(dashboard), headers=auth['dest'])
    if destination.status_code == requests.codes.ok:#pylint: disable=no-member
        #print "uploaded {0}".format(dashboard['dashboard']['title'])
        pass
    else:
        print "failed to upload {0}, with error: {1}".format(dashboard['dashboard']['title'], destination.status_code)
        print destination.text

pbar.finish()
