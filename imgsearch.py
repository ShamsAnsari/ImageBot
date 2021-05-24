"""
Group 3
Searches for images
@author Shams Ansari
# add your name here if you are in this project
"""

import json
import re
import requests




class ImageSearch():
    def __init__(self):
        pass



    def image_search(self, query):
        url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"

        querystring = {"q": query, "pageNumber": "1", "pageSize": "1", "autoCorrect": "true"}

        headers = {
            'x-rapidapi-key': "55f51a2243mshbc2295c2780c0bap185cabjsne0fe7d2d67d4",
            'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com"
        }


        response = requests.request("GET", url, headers=headers, params=querystring).text
        j = json.loads(response)
        img_url = j['value'][0]['url']
        return img_url



def clean_query(query):
    '''
      Cleans the query, remove any troublesome characters
    '''
    query = query.encode("ascii", "ignore").decode()
    query = re.sub(r'[^a-zA-Z0-9 ]', '', query).strip()
    return query
