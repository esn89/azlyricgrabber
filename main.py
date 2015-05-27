import urlchecker as uc
# import lyricsparser as lp


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
        # If it has title but no artist
        elif not artist and title:
            artist = raw_input("Who is the artist of " + title + " ? ")
        # If it has artist but no song title
        elif not title and artist:
            title = raw_input("What would you like to look up from "
                              + artist + " ? ")

    retval, qurl = uc.generateURL(artist, title)
    if retval == 1:
        print "lyrics are found"
    else:
        print "NONE"


if __name__ == '__main__':
    main()
