import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
from string import printable
import re


def convert_to_link(search):

    query = urllib.parse.urlencode({"search_query": search})
    url = "https://www.youtube.com/results?" + query
    response = urllib.request.urlopen(url)
    vids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    link = "https://www.youtube.com/watch?v=" + vids[0]
    return link






