'''
    Slippi File Renaming Script: Rename Slippi Files based on the characters and in-game tags used
    Filename Specification:
        CharacterName(TAG)-Vs-CharacterName(TAG)<year-month-day-hour-minute-second>.slp

            ex) CaptainFalcon(DOOM)-Vs-Jigglypuff<20191010191914>.slp

        Written by Kyle "1ncredibr0" Swygert
        Using py-slippi v1.3.1
'''

from slippi import *
from os import walk, listdir, rename

# iterate over the files in a directory
for filename in listdir('./slp'):

    # open the game file, get the characters, and get the tags if they exist.

    dst = ''
    src = ''

    tempGame = Game("slp/" + filename)


    if tempGame.start.is_teams == True:
        # TODO: Implement renaming of Teams games
        print("{} is a Teams game, cannot rename.".format(filename))
        # Team Naming Guide Idea: TeamGreen(Falco+(H E L P))-Vs-TeamBlue(CaptainFalcon+(S E L F))<datetime>.slp

    else:

        # Count number of players in current game
        currentPlayers = 0
        for player in tempGame.start.players:
            if player != None:
                currentPlayers += 1

        if currentPlayers != 2:
            # TODO: implement renaming free-for-all matches with just character names, not tags.
            print("{} is an FFA or Teams with more than 2 players, cannot rename.".format(
                filename))

        else:
            # there are only 2 players in the game, rename the files. 

            # list used to build the new Filename
            newFileNameParts = []

            firstChar = False

            # iterate over players in the game
            for player in tempGame.start.players:

                # append the formatted character name from the character object to the list
                [newFileNameParts.append(item.lower().capitalize()) for item in str(
                    player.character).split('.')[-1].split('_')] if player != None else None

                # append the player tag to the list if they were using one
                newFileNameParts.append(
                    '(' + player.tag + ')') if player != None and player.tag != '' else None

                # append '-Vs-' string to list if this is the first player being added to the list
                if newFileNameParts != [] and firstChar == False:
                    firstChar = True
                    newFileNameParts.append('-Vs-')


            # Build the new Filename
            for item in newFileNameParts:
                dst += item

            # appending the date and time that the game was played to reduce chance of overwriting files
            dst += '<' + str(tempGame.metadata.date).split('+')[0].replace(
                ' ', '').replace('-', '').replace(':', '') + '>'

            dst += '.slp'

            src = 'slp/' + filename
            dst = 'slp/' + dst

            rename(src, dst)

            newFileNameParts.clear()

print("All files in the /slp/ directory have been renamed.")