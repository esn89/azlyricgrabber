import urlchecker as uc
import lyricsparser as lp


def selector(qurl):
    listofmatches = lp.getLyricList(qurl)
    number = 1
    if len(listofmatches) > 1:
        print "Results:\n"
        for match in listofmatches:
            print str(number) + ". " + match[0]
            number = number + 1
        while True:
            songno = raw_input("Please select the number from the possible "
                               "matches:\n--> ")
            try:
                songno = int(songno)
                if songno <= 0 or songno > len(listofmatches):
                    print "Not a valid selection\n"
                else:
                    return songno
            except ValueError:
                print "Not a valid number\n"

    else:
        print "Results:\n"
        print str(number) + ".  " + listofmatches[0][0] + "\n"
        while True:
            songno = raw_input("Please select the number from the possible "
                               "match:\n--> ")
            try:
                songno = int(songno)
                print songno
                if songno == 1:
                    return songno
                else:
                    print "Not a valid selection\n"
            except ValueError:
                print "Not a valid number\n"


def main():

    artist = ""
    title = ""
    while True:
        if artist and title:
            break
        # If both artist and title fields are empty
        elif not artist and not title:
            artist = raw_input("Enter artist name: ")
            title = raw_input("Enter song title: ")
            print "\n"
        # If it has title but no artist
        elif not artist and title:
            artist = raw_input("Who is the artist of " + title + "? ")
        # If it has artist but no song title
        elif not title and artist:
            title = raw_input("What would you like to look up from "
                              + artist + "? ")

    retval, qurl = uc.generateURL(artist, title)

    if retval == 1:
        print selector(qurl)
    else:
        print "No results found."


if __name__ == '__main__':
    main()
