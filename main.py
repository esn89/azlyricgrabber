#!/usr/bin/python2.7
import sys
import urlchecker as uc
import userdisplay as ud


def run():
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

    # Checks to see if artist and song combination is valid:
    retval, qurl = uc.generateURL(artist, title)

    # Yay we have lyrics:
    if retval == 1:
        art, songname, lurl = ud.selector(qurl)
        ud.displayLyrics(lurl)
        return
    else:
        print "No results found.\n"
        return


def main():
    try:
        run()
        rerun = "Y"
        while rerun == "Y":
            rerun = raw_input("\nSearch another song? [Y/n] ")
            if rerun == "N" or rerun == "n":
                print "\nBye!"
                sys.exit(0)
            elif rerun == "Y" or rerun == "y":
                run()
            else:
                print "\nInvalid Option\n"
                rerun = "Y"
                continue

    except KeyboardInterrupt:
        print "\nShutdown requested, exiting..."
    sys.exit(0)

if __name__ == '__main__':
    main()
