'''
    Slippi File Renaming Script: Rename Slippi Files based on the characters and in-game tags used
    Filename Specification:
        CharacterName(TAG)-Vs-CharacterName(TAG)<year-month-day-hour-minute-second>.slp

            ex) CaptainFalcon(DOOM)-Vs-Jigglypuff<20191010191914>.slp

        Written by Kyle "1ncredibr0" Swygert
        Using py-slippi v1.3.1
'''

'''

NOTE: there may be a difference when parsing replays captured from a Wii vs a connection to a PC. Make sure that the PC captured replays are parsed the same as the Wii captured files. 

TODO: Rename replays against CPUs using the tag CPU for the character to make sure it is not a human player. 
TODO: create functions generate_singles_game_name() and generate_doubles_game_name()
TODO: detect if the program is being run on linux or windows for changing the / to \ in windows for renaming files properly. 


'''



from slippi import *
from os import walk, listdir, rename, path

def generate_file_name(slippiFile):
    '''
    
    '''
    print('implement the file name function')

    pass

def generate_doubles_game_name(slippiFile):
    '''
    Team Naming Guide Idea: TeamGreen(Falco+(H E L P))-Vs-TeamBlue(CaptainFalcon+(S E L F))_datetime.slp
    TeamColor(char1(TAG)-char2(TAG))-Vs-TeamColor(char3(TAG)-char4(TAG))_datetime.slp
    '''
    print('implement the doubles function')
    pass

def generate_free_for_all_game_name(slippiFile):
    '''
    iterate through all the players in the game
    build a list of strings of the character names and '-Vs-'
    Ex) Fox-Vs-Falco-Vs-Sheik_20191010143456.slp


    '''
    print('implement the free-for-all function')

    pass

def generate_singles_game_name(slippiFile):
    '''
    this function will build a string based on the characters used in the game. 

    TODO: create cases in this function in the future to rename files based on the type of game being played. 
        ex) singles, doubles, free for all. 

    if is teams game:
        generate_doubles_game_name()

    else:

        if 2 players in game:
            generate_singles_game_name()

        elif more than 2 players in game:
            # either a 3 or 4 person free for all match. 
            generate_free_for_all_game_name()


    '''

    newFile = ''

    # list used to build the new Filename
    newFileNameParts = []

    firstChar = False

    #curPlatform = tempGame.metadata.platform

    # iterate over players in the game
    for player in slippiFile.start.players:

        # append the formatted character name from the character object to the list
        [newFileNameParts.append(item.lower().capitalize()) for item in str(player.character).split('.')[-1].split('_')] if player != None else None

        # append the player tag to the list if they were using one
        newFileNameParts.append('(' + player.tag + ')') if player != None and player.tag != '' else None

        # append '-Vs-' string to list if this is the first player being added to the list
        if newFileNameParts != [] and firstChar == False:
            firstChar = True
            newFileNameParts.append('-Vs-')


    # Build the new Filename
    for item in newFileNameParts:
        newFile += item

    # appending the date and time that the game was played to reduce chance of overwriting files
    # TODO: remove the trailing time part that is added when processing files captured from a PC.
        # reorganize the program: have a flag for processing Console Replays and processing PC replays. 

                
    # Could I do list comprehension here to replace the multiple different characters with nothing?
    # NOTE: the previous format of <date>.slp is not allowed on the windows platform, so it is now replaced with _date.slp
    newFile += '_' + str(slippiFile.metadata.date).split('+')[0].replace(' ', '').replace('-', '').replace(':', '').split('.')[0] #  + '_'

    newFile += '.slp'

    #print(newFile)

    return newFile


def rename_files_in_folder(folder):
    '''
    this function accepts the name of a folder as a string and will rename all the .slp files in the directory and sub-directories. 
    '''

    print('folder that contains all the slippi files: {}'.format(folder))

    for root, dirs, files in walk(folder):
        # root represents the current directory that is being processed
        # dirs represents the sub-directories in the currently processing directory
        # files represents the files inside the root directory

        # I want to store the file back into the directory that it came from in the directories, and I believe that I will need the root string to do that. 
        #print(root + " " + str(files))

        for curr in files:
            #print(root + curr)

            '''when using the rename() function:

                dst += .slp

                dst = root + '/' + dst
                src = root + '/' + originalFileName

            '''

            # check if the file ends in .slp
            # check that the game is not a teams or FFA
            # if only a 2 player game, send the SlippiGame file to the generate_file_name() function. 

            #print(curr)

            if curr.split('.')[-1] == 'slp':

                # NOTE: when building the pathname, we can use the os.path.join() function to insert the '/' characters into the path automatically. 

                #currFilePath = root + '/' + curr

                currFilePath = path.join(root, curr)

                #print('can process file {}'.format(currFilePath))


                try:

                    tempGame = Game(currFilePath)

                except:
                    # TODO: look into why the renaming program breaks here. what exception is being thrown? This might be because of the replay being cut off when the connection was cut. see if there is any way to tell if a file is malformed...
                    print('{} broke the execution for some reason, look into why that happened...'.format(currFilePath))
                    pass

                #tempGame = Game(curr)
                

                if tempGame.start.is_teams != True:

                    # Count number of players in current game
                    currentPlayers = 0
                    for player in tempGame.start.players:
                        if player != None:
                            currentPlayers += 1


                    #print('number of players in game: {}'.format(currentPlayers))

                    if currentPlayers != 2:
                        # TODO: implement renaming free-for-all matches with just character names, not tags.
                        print("{} is a FFA with more than 2 players, cannot rename.".format(
                            curr))

                    else: 

                        try:

                            #print('the game only has 2 players')

                            newFileName = ''
                            newFileName = generate_singles_game_name(tempGame)

                            #print('just created a file name: {}'.format(newFileName))

                            #newFileName += '.slp'

                            #print("new file name: {}".format(newFileName))

                            #newFileName = root + '/' + newFileName
                            newFileName = path.join(root, newFileName)

                            print('old file name: {}'.format(currFilePath))
                            print('new file name: {}\n\n'.format(newFileName))

                            rename(currFilePath, newFileName) # note: this line here is causing issues when running on windows... I wonder why this is happening... This might be because of the file path differences between Linux and windows...
                            #print('successfully renamed the file')

                        except:
                            print("could not process file {}".format(curr))
                           
                else:
                    print('{} is a teams game'.format(curr))


            else:
                print('{} was wrong file format'.format(curr))


# NOTE: this is where the program starts executing when run as a command line program. 
# TODO: change the folder input parameter for the function to be based on the command line argument that the user has given rather than being a hard coded directory name. 
#rename_files_in_folder('.\slp') # NOTE: '/' for linux, '\' for windows. 

directory = path.join(path.dirname(path.realpath(__file__)), 'slp')

rename_files_in_folder(directory)

"""
# iterate over the files in a directory
for filename in listdir('./slp'):

    try:

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
                # there are only 2 players in the game, rename the file. 

                #print(generate_file_name(tempGame) + '\n\n')

                '''
                # list used to build the new Filename
                newFileNameParts = []

                firstChar = False

                #curPlatform = tempGame.metadata.platform

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
                # TODO: remove the trailing time part that is added when processing files captured from a PC.
                    # reorganize the program: have a flag for processing Console Replays and processing PC replays. 

                
                # Could I do list comprehension here to replace the multiple different characters with nothing?
                dst += '<' + str(tempGame.metadata.date).split('+')[0].replace(
                    ' ', '').replace('-', '').replace(':', '').split('.')[0] + '>'

                '''

                dst = generate_file_name(tempGame)

                dst += '.slp'

                src = 'slp/' + filename
                dst = 'slp/' + dst

                rename(src, dst)

                newFileNameParts.clear()

    except:
        print("{} cannot be processed, skipping file.".format(filename))

"""

print("All files in the /slp/ directory have been renamed.")
