#!/usr/bin/python2.7
import lyricsparser as lp
import colorizefont as cf
import os


def selector(qurl):
    """Returns the url to the actual lyrics based on user selection

    Args:
        qurl -- the url to the search result of artist + song
    Returns:
        lurl -- the url to the page contain the lyrics

    """

    listofmatches = lp.getLyricList(qurl)
    number = 1

    # Clear the previous input screen:
    os.system('clear')

    print "Matches:\n"
    for match in listofmatches:
        # Each listofmatches is a tuple with 3 elements:
        # [0] = artist
        # [1] = title of the song
        # [2] = url of the lyrics
        artist = cf.returnColourFormat(match[0], "RED", "BOLD")
        print str(number) + ". " + match[1] + " - " + artist
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
                return listofmatches[songno][0], listofmatches[songno][1], \
                    listofmatches[songno][2]
        except ValueError:
            print "Not a valid number\n"


def displayLyrics(lurl):
    """Displays lyrics on the user's terminal

    Args:
        lurl -- the URL to the page containing the lyrics
    Returns:
        1 -- if successfully displayed
        0 -- if not successfully displayed
    """

    listoflines = lp.getLyrics(lurl)
    parsed = lp.parseLyrics(listoflines)
    height, width = lp.getTerminalDimensions()

    try:
        for line in parsed:
            print line.center(int(width))
    except:
        return 0
    return 1
