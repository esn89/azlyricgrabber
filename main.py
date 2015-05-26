import urlchecker as uc


def test():
    artist = raw_input("Enter artist name: ")
    title = raw_input("Enter song title: ")
    result, url = uc.generateURL(artist, title)


if __name__ == '__main__':
    test()
