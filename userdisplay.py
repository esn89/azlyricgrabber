#!/usr/bin/python2.7
import lyricsparser as lp


def selector(qurl):
    """Returns the url to the actual lyrics based on user selection

    Args:
        qurl -- the url to the search result of artist + song
    Returns:
        lurl -- the url to the page contain the lyrics

    """

    listofmatches = lp.getLyricList(qurl)
    number = 1
    print "Matches:\n"
    for match in listofmatches:
        print str(number) + ". " + match[0]
        number = number + 1
    while True:
        songno = raw_input("Please select the number from the possible "
                           "matches\n--> ")
        try:
            songno = int(songno)
            if songno <= 0 or songno > len(listofmatches):
                print "Not a valid selection\n"
            else:
                # Re-adjust our selection:
                # Humans read lists starting with 1,
                # Lists starts with 0, so offset of -1:
                songno = songno - 1
                return listofmatches[songno][0], listofmatches[songno][1]
        except ValueError:
            print "Not a valid number\n"


def displayLyrics(songinfo, lurl):
    listoflines = lp.getLyrics(lurl)
    parsed = lp.parseLyrics(listoflines)
    lp.formatLyrics(parsed)
