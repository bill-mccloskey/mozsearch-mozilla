import thclient
import requests
import re
import sys

client = thclient.TreeherderClient()
pushes = client.get_pushes('mozilla-central', count=10)
for push in pushes:
    rev = push['revision']

    jobs = client.get_jobs('mozilla-central',
                           push_id=push['id'],
                           job_group_symbol='Searchfox',
                           count=250)
    urls = []
    for job in jobs:
        if job['result'] != 'success':
            continue

        url = ('https://treeherder.mozilla.org:443/api/jobdetail/?job_guid='
               + job['job_guid'] + '&repository=mozilla-central')
        res = client.session.get(url)
        j = res.json()

        for detail in j['results']:
            if detail['title'] != 'artifact uploaded':
                continue

            if detail['value'] != 'target.mozsearch-index.zip':
                continue

            urls.append(detail['url'])


    if urls:
        print rev
        for url in urls:
            print url
        sys.exit(0)

sys.exit(1)
