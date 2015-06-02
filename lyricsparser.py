#!/usr/bin/python2.7

import requests
import os
import re
from collections import namedtuple
from lxml import html, etree
queryurl = "http://search.azlyrics.com/search.php?q=\
        joey+bada%24%24+don%27t+front"


def getLyricList(queryurl):
    """Gets a list of possible matches based on the user's artist and title

    Args:
        url -- the result of the search query made by the user which contains
        a list of possible matches.
    Returns:
        listofLyrics -- a list of possible matches in the format of:
        (title-artist, lyricsurl)

    """
    listofLyrics = []

    # Defining the named tuple
    Lyrics = namedtuple('Lyrics', ['artist', 'title', 'url'])

    page = requests.get(queryurl)
    tree = html.fromstring(page.text)

    # Gets a list of songs that are returned in HTML format and their
    # associated URL for the actual lyrics
    for node in tree.xpath('//td[@class="text-left visitedlyr"]'):
        lyricsurl = node.xpath('.//a/@href')[0]
        song = node.xpath('./a/b')[0].text
        artist = node.xpath('./b')[0].text
        # Creates a new Lyrics tuple
        l = Lyrics(artist, song, lyricsurl)
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

    listoflines = []
    page = requests.get(lyricsurl)
    myparser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page.text, parser=myparser)


    es = tree.xpath('//div[not(@class) and not(@id)]')
    es = html.tostring(es[0], encoding='UTF-8')
    u = unicode(es, "utf-8")
    unicodestring = unicode(u).encode('unicode escape')
    utf = unicodestring.decode('string escape').decode('utf-8')
    print utf
    # lyrics = html.tostring(es[0])

    # print lyrics.count('<br>')
    # replace all <i> with: "\x1b[3m"
    # lyrics = lyrics.replace('<i>', "\x1b[3m")
    # lyrics = lyrics.replace('</i>', "\x1b[23m")
    # # Removes the comments if there is any:
    # lyrics = re.sub("<!--.*?-->", "", lyrics)
    # # Removes the <div> and </div> tags:
    # lyrics = lyrics.replace("<div>", "").replace("</div>", "")

    # listoflines = lyrics.split('<br>')
    # return listoflines


def parseLyrics(listoflines):
    """Parses the raw lyrics

    Removing leading '\n' chars, places where there are
    two \n\n (to save space) and unicode chars.

    Args:
        listoflines -- a list of lines which make up the lyrics which may
            contain '\n' and/or unicode chars
    Returns:
        parsedLyrics -- a list of lines with '\n' removed and unicode that
            have been converted to utf-8

    """
    parsedLyrics = []
    for l in listoflines:
        print l
    return parsedLyrics


def getTerminalDimensions():
    """Returns the height and width of user's terminal window

    Args:
        none
    Returns:
        height = height of the terminal
        width = width of the terminal
    """

    height, width = os.popen('stty size', 'r').read().split()
    return height, width

(getLyrics(lyricsurl))
