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
    """Gets the lyrics (raw, no formatting) from www.azlyrics.com

    Args:
        lyricsurl -- the url which contains the actual lyrics
    Returns:
        listoflines -- a list of lines which makes up the entire song

    """

    page = requests.get(lyricsurl)
    tree = html.fromstring(page.text)

    # sel = CSSSelector('div:not([class]):not([id])')
    # listoflines = sel(tree)
    # return listoflines
    # print (listoflines)
    # for l in listoflines:
    #     print l.text_content()

    # this verion works slightl better as it actually gives a list
    lyrics = 0
    for node in tree.xpath('//div[not(@class) and not(@id)]'):
        lyrics = node.xpath('./br | ./i')

    listoflines = []
    for l in lyrics:
        if l.tail is None:
            listoflines.append(l.text)
        else:
            listoflines.append(l.tail)

    return listoflines


def parseLyrics(listoflines):
    i = 0
    for l in listoflines:
        i = i + 1
        print l
    # Need to break entire thing into individual lines...
    # should do it in the next function, righ tnow it is one whole thing
    print i

parseLyrics(getLyrics(lyricsurl))
