#!/usr/bin/python2.7

import requests
import os
from collections import namedtuple
from lxml import html
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
    tree = html.fromstring(page.text)

    lyrics = 0
    for node in tree.xpath('//div[not(@class) and not(@id)]'):
        lyrics = node.xpath('./br | ./i')

    for l in lyrics:
        if l.tail is None:
            # Preserve italics: this part of the text tells the reader
            # that it's the [verse] or [chorus] or [hook], etc
            italicized = "\x1B[3m" + l.text + "\x1B[23m"
            listoflines.append(italicized)
        else:
            listoflines.append(l.tail)

    return listoflines


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
        # Checks to see if it is unicode, if so, format it into something
        # readable.
        if isinstance(l, unicode) is True:
            unicodestring = unicode(l).encode('unicode escape')
            utf = unicodestring.decode('string escape').decode('utf-8')
            # Strips all \n char so the lyrics don't become too long
            parsedLyrics.append((utf).replace('\n', ""))
        else:
            parsedLyrics.append((l.replace('\n', "")))

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
