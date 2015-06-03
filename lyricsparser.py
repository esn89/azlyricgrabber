#!/usr/bin/python2.7

import requests
import os
import re
from collections import namedtuple
from lxml import html, etree


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

# lyricsurl = 'http://www.azlyrics.com/lyrics/eminem/withoutme.html'
# lyricsurl = 'http://www.azlyrics.com/lyrics/deathgrips/takyon.html'


def getLyrics(lyricsurl):
    """Gets the lyrics (raw, no formatting) from www.azlyrics.com

    Args:
        lyricsurl -- the url which contains the actual lyrics
    Returns:
        lyrics -- a long string which make up the entire song

    """
    # request the page
    page = requests.get(lyricsurl)
    # specify a parser
    myparser = etree.HTMLParser(encoding="utf-8")
    tree = etree.HTML(page.text, parser=myparser)

    # the node of interest begins with <div> and ends in </div>
    nodestart = tree.xpath('//div[not(@class) and not(@id)]')
    # We want UTF-8 encoding
    nodestart = html.tostring(nodestart[0], encoding='UTF-8')
    uni = unicode(nodestart, "utf-8")
    unicodestring = unicode(uni).encode('unicode escape')

    # Thanks to:
    # https://www.safaribooksonline.com/library/view/python-cookbook-
    # 2nd/0596007973/ch01s22.html
    lyrics = unicodestring.decode('string escape').decode('utf-8')
    lyrics = lyrics.encode("utf-8")

    return lyrics


def parseLyrics(lyrics):
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
    listoflines = []

    # if we have italics, carry it over
    if lyrics.count('<i>') > 0:
         # replace all <i> with: "\x1b[3m"
        lyrics = lyrics.replace('<i>', "\x1b[3m")
        lyrics = lyrics.replace('</i>', "\x1b[23m")
    # Removes the comments if there is any:
    lyrics = re.sub("<!--.*?-->", "", lyrics)
    # # Removes the <div> and </div> tags:
    lyrics = lyrics.replace("<div>", "").replace("</div>", "")

    # At the moment, the entire "lyrics" is just one long string, I need to
    # split them by <br>:
    listoflines = lyrics.split('<br>')

    parsedLyrics = []
    for l in listoflines:
        if l.find('\n\r'):
            l = l.strip('\n\r')
            parsedLyrics.append(l)
        # gotta get rid of unnecessary white space in front of lyrics:
        if l.startswith('\n') and len(l) > 0:
            l = l.lstrip('\n')
            parsedLyrics.append(l)

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
