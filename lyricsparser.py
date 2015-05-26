#!/usr/bin/python2.7
import requests
from lxml import html

url = "http://search.azlyrics.com/search.php?q=joey+bada%24%24+don%27t+front"


def getLyrics(url):

    page = requests.get(url)
    tree = html.fromstring(page.text)

    # listofresults = tree.xpath('//td[@class="text-left visitedlyr"]/a/b')
    # print len(listofresults)

    # for title in listofresults:
    #     print title.text
    for node in tree.xpath('//td[@class="text-left visitedlyr"]'):
        song = node.xpath('./a/b')[0].text
        artist = node.xpath('./b')[0].text
        print song + " " + artist


getLyrics(url)
