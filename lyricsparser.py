#!/usr/bin/python2.7

import requests
from collections import namedtuple
from lxml import html
from lxml.cssselect import CSSSelector

queryurl = "http://search.azlyrics.com/search.php?q=\
        joey+bada%24%24+don%27t+front"


def getLyricList(queryurl):
    """Gets a list of possible matches based on the user's artist and title

    Args:
        url -- the result of the search query made by the user which contains
        a list of possible matches.
    Returns:
        a list of possible matches in the format of:
        (title-artist, lyricsurl)

    """
    listofLyrics = []

    # Defining the named tuple
    Lyrics = namedtuple('Lyrics', ['title', 'url'])

    page = requests.get(queryurl)
    tree = html.fromstring(page.text)

    # Gets a list of songs that are returned in HTML format and their
    # associated URL for the actual lyrics
    for node in tree.xpath('//td[@class="text-left visitedlyr"]'):
        lyricsurl = node.xpath('.//a/@href')[0]
        song = node.xpath('./a/b')[0].text
        artist = node.xpath('./b')[0].text
        title = song + " - " + artist
        # Creates a new Lyrics tuple
        l = Lyrics(title, lyricsurl)
        listofLyrics.append(l)

    return listofLyrics

lyricsurl = 'http://www.azlyrics.com/lyrics/eminem/withoutme.html'


def getLyrics(lyricsurl):
    listoflines = []

    page = requests.get(lyricsurl)
    tree = html.fromstring(page.text)

    sel = CSSSelector('div:not([class]):not([id])')
    results = sel(tree)
    for r in results:
        print r.text_content()
    # match = results[2]
    # print html.tostring(match)

    # match = results[44]
    # for match in results:
    #    print html.tostring(match)

    # this works
    # for br in tree.xpath("*//br"):
    #     if br.tail is not None:
    #         print br.tail.strip()
    #         listoflines.append(br.tail)


def parseLyrics():
    pass

getLyrics(lyricsurl)

