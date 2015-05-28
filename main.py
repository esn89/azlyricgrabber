import urlchecker as uc
import userdisplay as ud


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

    # Checks to see if artist and song combination is valid:
    retval, qurl = uc.generateURL(artist, title)

    # Yay we have lyrics:
    if retval == 1:
        info, lurl = ud.selector(qurl)
        ud.displayLyrics(info, lurl)
    else:
        print "No results found."


if __name__ == '__main__':
    main()
