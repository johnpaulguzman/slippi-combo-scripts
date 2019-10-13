from slippi import *
from os import walk, listdir, rename


for filename in listdir('./slp'):

    # default: CharacterVsCharacter.slp
    # tags: Character(TAG)VsCharacter(TAG).slp

    # open the game file, get the characters, and get the tags if they exist. 
    # slippi.players.tag

    dst = ''
    src = ''

    tempGame = Game("slp/" + filename)

    if tempGame.start.is_teams == True:
        print("{} is a teams match, cannot rename.".format(filename))
        break

    newFileNameParts = []

    firstChar = False


    # Note: how to add the Vs into the list? When to do that? 
    for player in tempGame.start.players:

        newFileNameParts.append(str(player.character).split('.')[-1]) if player != None else None

        newFileNameParts.append('(' + player.tag + ')') if player != None and player.tag != '' else None

        if newFileNameParts != [] and firstChar ==  False:
            firstChar = True
            newFileNameParts.append('Vs')




    for item in newFileNameParts:
        dst += item


    # add the time the game was played to the file name so that games with the same characters in it are not overwritten. 

    dst += str(tempGame.metadata.date).split(' ')[-1].split('+')[0]

    dst += '.slp'

    #print("{} is the new filename".format(dst))

    src = "slp/" + filename
    dst = 'slp/' + dst

    rename(src, dst)

    newFileNameParts.clear()
    