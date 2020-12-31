#!/usr/bin/env python

import requests
import sys

import osmose_config

main_url = 'http://polygons.openstreetmap.fr/'
relation_generation_url = main_url + 'index.py'
polygon_union_url = main_url + 'get_poly.py'

fails = []
for c in osmose_config.config.values():
    if not hasattr(c, 'polygon_id'):
        continue
    if not c.polygon_id:
        continue

    print('  ', c.country, c.polygon_id)

    # generate relation boundary
    x = '0.020000'
    y = '0.005000'
    z = '0.005000'
    r = requests.post(relation_generation_url, params={'id': c.polygon_id}, data={'x': x, 'y': y, 'z': z})
    if r.status_code == 500:
        fails.append([c.country, c.polygon_id, 'Geom Error'])
    elif r.status_code != 200:
        fails.append([c.country, c.polygon_id, 'Error'])
    else:
        r = requests.get(polygon_union_url, params={'id': c.polygon_id, 'params': '{}-{}-{}'.format(x,y,z)})
        if r.status_code != 200:
            fails.append([c.country, c.polygon_id, 'Bad geom'])

if len(fails) > 0:
    print(fails)
    sys.exit(1)
