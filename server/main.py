from collections import defaultdict

import json
from urllib.request import urlopen
from urllib.parse import urlencode

class Box(object):
  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng
  def around(lat, lng, radius):
  return Box((lat-radius, lat+radius), (lng-radius, lng+radius))

google = around(-33.865055, 151.196064, 0.013)
perth = around (-27.509311, 153.075261, 0.1)
sydney = around(-33.865055, 151.196064, 0.4)

def species_list_url(**kwargs):
  url = "https://data.bionet.nsw.gov.au/biosvcapp/odata/SpeciesSightings_CoreData?"
  filters = []
  if 'lat' in kwargs:
    filters.append(f'(decimalLatitude ge {kwargs["lat"][0]}) and (decimalLatitude le {kwargs["lat"][1]})')
  if 'long' in kwargs:
    filters.append(f'(decimalLongitude ge {kwargs["long"][0]}) and (decimalLongitude le {kwargs["long"][1]})')
  if 'name' in kwargs:
    filters.append(f'contains(toupper(vernacularName),\'{kwargs["name"].upper()}\')' )
  return url + urlencode({'$filter': '(' + (') and ('.join(filters)) + ')'})
  
  def get_url(url):
  return json.loads(urlopen(url).read())
  
  bandicoots = get_url(species_list_url(lat=(-33.846195, -33.841498), long=(151.236511,151.245218), name='whale'))['value']
list(map(lambda x: {
    'lat': x['decimalLatitude'],
    'long': x['decimalLongitude'],
    'date': x['eventDate'],
    'name': x['vernacularName']}, bandicoots))
    
whales = get_url(species_list_url(lat=(-34.229726, -33.814293), long=(150.785827,151.313784), name='koala'))['value']
    
print('\n'.join(list(map(lambda x: f'{x["decimalLatitude"]},{x["decimalLongitude"]}', whales))[:100]))
kangaroo_data = get_url(species_list_url(lat=sydney.lat, long=sydney.lng, name='kangaroo'))['value']

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [10, 10]
from sklearn.cluster import MeanShift

kangaroo_spots = list(set(map(lambda x: (x["decimalLatitude"], x["decimalLongitude"]), kangaroo_data)))
kangaroo_x = list(map(lambda k: k[1], kangaroo_spots))
kangaroo_y = list(map(lambda k: k[0], kangaroo_spots))
kangaroo_clu = MeanShift(bandwidth=0.1, cluster_all=False).fit(np.array(kangaroo_spots))
kangaroo_labels = kangaroo_clu.labels_
kangaroo_centers = kangaroo_clu.cluster_centers_
plt.scatter(kangaroo_x, kangaroo_y, c=kangaroo_labels, s=list(map(lambda x:196, kangaroo_spots)), alpha=0.1)

c_x = list(map(lambda k: k[1], kangaroo_centers))
c_y = list(map(lambda k: k[0], kangaroo_centers))

plt.scatter(c_x, c_y, s=list(map(lambda x:75**2, kangaroo_centers)), alpha=0.2)

plt.scatter(
    kangaroo_x + c_x,
    kangaroo_y + c_y,
    c=list(kangaroo_labels)+list(map(lambda x:-1, kangaroo_centers)),
    s=list(map(lambda x:10**2, kangaroo_spots))+list(map(lambda x:75**2, kangaroo_centers)),
    alpha=0.2)
    
from lxml import etree
from pyquery import PyQuery as pq

def wikisearch(animal):
  url = 'https://en.wikipedia.org/w/index.php?' + urlencode({'title':'Special:Search', 'search': animal})
  response = urlopen(wikisearch('red kangaroo'))
  if response.getcode() != 200: return None
  body = response.read()
  infobox = pq(etree.fromstring(body))('.infobox.biota')
  if ('[href="/wiki/Least_Concern"]').text():
    return 
  return 
