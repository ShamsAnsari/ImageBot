"""
Group 3
Searches for images
@author Shams Ansari
# add your name here if you are in this project
"""

import json
import os
import re

import requests


class ImageSearch():
    def __init__(self):
        pass

    def image_search(self, query):
        """
        Gets image corresponding to query
        :param query: a string of words, cleaned for non-ascii and  "troublesome" characters
        :return: a URL to the image
        """
        print(query)
        url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

        querystring = {"q": query, "pageNumber": "1", "pageSize": "1", "autoCorrect": "true", "safeSearch":"true"}

        headers = {
            'x-rapidapi-key': os.environ.get('x-rapidapi-key'),
            'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).text
        j = json.loads(response)
        if len(j['value']) == 0:
            return None
        img_url = j['value'][0]['url']
        print(img_url)
        # try:
        #     urllib.request.urlopen(img_url).getcode()
        # except:
        #     return None

        return img_url


def clean_query(query):
    '''
      Cleans the query, remove any troublesome characters
    '''
    query = query.encode("ascii", "ignore").decode()
    query = re.sub(r'[^a-zA-Z0-9 ]', '', query).strip()
    return query
