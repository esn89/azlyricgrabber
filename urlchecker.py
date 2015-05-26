#!/usr/bin/python2.7

import requests
import sys
from lxml import html

urlheader = "http://search.azlyrics.com/search.php?q="


def generateURL(artist, title):
    # Strip the leading and trailing whitespace.  Put "+" in between
    # useful whitespaces.
    artist = artist.lstrip().rstrip().replace(" ", "+")
    title = title.lstrip().rstrip().replace(" ", "+")
    url = urlheader + artist + "+" + title
    return checkURL(url), url


def checkURL(url):
    haslyrics = 0
    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    tree = html.fromstring(page.text)
    message = tree.xpath('//div[@class="alert alert-warning"]/text()')
    if message:
        # Lyrics can't be found
        response = message[0]
        if "Sorry" in response:
            print "Lyrics cannot be found, please check your spelling"
            haslyrics = 0
    else:
        haslyrics = 1
        print message
    return haslyrics
