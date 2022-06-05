import json

from collections import namedtuple
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

from utils.config import get_config



def get_geocode_coords(input_address, geocode_key):

    params = {'key': geocode_key, 'address': input_address}

    Geocoords = namedtuple('Geocoords', 'lat lng')

    encoded_query = urlencode(params)

    geo_query = "https://maps.googleapis.com/maps/api/geocode/json?" + encoded_query

    print(geo_query)

    http_response = urlopen(geo_query)

    geo_response = http_response.read()

    json_data = json.loads(geo_response)

    status = json_data['status']
    # print(status)
    
    try:
        lat = json_data['results'][0]['geometry']['location']['lat']

        lng = json_data['results'][0]['geometry']['location']['lng']
    except IndexError:
        lat = ''
        lng = ''

    return lat, lng, status


def geocode_addr_df(addr_df, geocode_key=None):
    """takes a pandas df w/addresses, returns lat/long/call status"""
    out_df = addr_df.copy()

    if not geocode_key:
        geocode_key = get_config()['api_key']

    out_df['lat'], out_df['lng'], out_df['status'] = zip(
        *out_df['addr'].apply(
            lambda addr: get_geocode_coords(input_address=addr, geocode_key=geocode_key)
            )
        )
    
    print(f"status counts: {out_df['status'].value_counts()}")

    return out_df
