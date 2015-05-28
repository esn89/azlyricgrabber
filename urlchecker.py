#!/usr/bin/python2.7

import requests
import sys
from lxml import html

# this is just an URL for testing, please remove
urlheader = "http://search.azlyrics.com/search.php?q="


def generateURL(artist, title):
    """Generates an URL based on the user's artist and song title

    Args:
        artist -- artist of the song
        title -- title of the song
    Returns:
        0 - if the song and artist cannot be found
        1 - if the song and artist can be found
        url - the url that was generated based on user input

    """
    # Strip the leading and trailing whitespace.  Put "+" in between
    # useful whitespaces.
    artist = artist.lstrip().rstrip().replace(" ", "+")
    title = title.lstrip().rstrip().replace(" ", "+")

    # Generate the full url
    url = urlheader + artist + "+" + title
    return checkURL(url), url


def checkURL(url):
    """Checks the validity of the URL generated from artist and title

    Args:
        url -- the generated URL from generateURL(artist, title)
    Returns:
        0 - if the song and artist does not exist
        1 - if the song and artist exists

    """
    haslyrics = 0

    try:
        page = requests.get(url)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    tree = html.fromstring(page.text)

    listofresults = tree.xpath('//div[@class="panel-heading"]/b')
    # Sometimes when input is vague, www.azlyrics.com returns a lot of possible
    # matches such as "Artist results", "Album results" and "Song results".
    # I only need "Song Results".
    # Do not give user the option to filter by artist/album.  It forces them to
    # enter much stricter input
    for l in listofresults:
        if 'Artist' in l.text or 'Album' in l.text:
            haslyrics = 0
            print "Lyrics cannot be found."
            return haslyrics

    message = tree.xpath('//div[@class="alert alert-warning"]/text()')
    if message:
        # Lyrics can't be found
        response = message[0]
        if "Sorry" in response:
            print "Lyrics cannot be found, please check your spelling"
            haslyrics = 0
    else:
        haslyrics = 1
    return haslyrics
