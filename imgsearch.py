"""
Group 3
Searches for images
@author Shams Ansari
# add your name here if you are in this project
"""

from bs4 import BeautifulSoup
import json
import urllib.request, urllib.error, urllib.parse
import re

class ImageSearch():
    def __init__(self):
        pass

    def get_soup(self, url, header):
        """
        Returns the html source code the website
        :param url: url of website to get html code
        :param header: info for browsers
        :return: a Soup object with html data
        """
        return BeautifulSoup(
            urllib.request.urlopen(urllib.request.Request(url,
                                                          headers=header)),
            'html.parser')

    def bing_image_search(self, query):
        """
        Returns the urls of the first query search
        :param query: A string of words
        :return: a tuple. (the image name, the murl, the turl)
        """
        query = query.split()
        query = '+'.join(query)
        url = "http://www.bing.com/images/search?q=" + query + "&FORM=HDRSC2"

        header = {
            'User-Agent':
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
        soup = self.get_soup(url, header)
        image_result_raw = soup.find("a", {"class": "iusc"})

        m = json.loads(image_result_raw["m"])
        murl, turl = m["murl"], m["turl"]

        image_name = urllib.parse.urlsplit(murl).path.split("/")[-1]
        #murl is the mobile image
        #turl is the desktop image
        return (image_name, murl, turl)


def clean_query(query):
    '''
      Cleans the query, remove any troublesome characters
    '''
    query = query.encode("ascii", "ignore").decode()
    query = re.sub(r'\W+', '', query).strip()
    return query
