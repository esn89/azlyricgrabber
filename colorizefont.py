#!/usr/bin/python2.7


def returnColourFormat(tobeformatted, textcolor, bgcolor="NONE",
                       textstyle="NOFX"):
    """Returns two strings for surrounding text with format and color

    Text color  Code |   Text style  Code  |   Background color  |  Code
    -----------------|---------------------|---------------------|-------
        Black   30   |   No effect   0     |               Black |   40
        Red     31   |   Bold        1     |               Red   |   41
        Green   32   |   Underline   4     |               Green |   42
        Yellow  33   |   Blink       5     |               Yellow|   43
        Blue    34   |   Inverse     7     |               Blue  |   44
        Purple  35   |   Hidden      8     |               Purple|   45
        Cyan    36   |                     |               Cyan  |   46
        White   37   |                     |               White |   47
    ---------------------------------------------------------------------

    Args:
        textcolor -- an int which is the color of the text
        textstyle -- an int which corresponds to the textstyle
        bgcolor -- an int which is the background colour
    Returns:
        finalstring -- the inputted string surrounded with
            formatting

        For example:
        "\033[5;41;32mGREEN TEXT\033[0m"
        Gives blinking green text on red background

    """
    # First things first, let's makes sure the user input string is not empty:

    tcolor = {"BLACK":  "30",
              "RED":    "31",
              "GREEN":  "32",
              "YELLOW": "33",
              "BLUE":   "34",
              "PURPLE": "35",
              "CYAN":   "36",
              "WHITE":  "37"
              }
    tstyle = {"NOFX":        "0",
              "BOLD":        "1",
              "UNDERLINE":   "4",
              "BLINK":       "5",
              "INVERSE":     "7",
              "HIDDEN":      "8"
              }
    bgvalue = {"BLACK":         "40",
               "RED":           "41",
               "GREEN":         "42",
               "YELLOW":        "43",
               "BLUE":          "44",
               "PURPLE":        "45",
               "CYAN":          "46",
               "WHITE":         "47"
               }

    endstring = "\033[0m"
    startstring = "\033["


    # For text style:

    if textstyle.upper() in tstyle:
        startstring = startstring + tstyle[textstyle.upper()] + ";"
    else:
        startstring = startstring + "0" + ";"

    # For color background:
    # If the background is none, we don't add anything to our format string
    if bgcolor.upper() == "NONE":
        pass
    elif bgcolor.upper() in bgvalue:
        startstring = startstring + bgvalue[bgcolor.upper()] + ";"
    else:
        pass

    # For text color:
    if textcolor.upper() in tcolor:
        startstring = startstring + tcolor[textcolor.upper()] + "m"
    else:
        # If we provide an invalide text color, it defaults to white:
        startstring = startstring + "37" + "m"

    finalstring = startstring + tobeformatted + endstring
    return finalstring
