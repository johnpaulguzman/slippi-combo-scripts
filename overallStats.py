'''
    Pieces of data to get from processing all files in a folder. Turn this data into a JSON file that can be read by another program. 

    character occurances
    stage occurances
    win percentage by character
    average stock time (frames)
    average stock percent at time of death

    remove data from CPU players

    longest combo (# of hits)
    longest combo (highest percent)

    ports most often used by players


'''

'''
    Functions to write for future Slippi analysis programs
        Determine winner of game: game file
            returns the string of the character object


    TODO: try to make the program a bit more efficient so that it takes as little time as possible to analyze the data. 


'''



'''


    program output:

    (length of gameFiles list) Files found

    Stats computation complete:
        (numCPU) CPU Files not processed
        Stats written to stats.txt // try to rename the file to the name of the folder that the replay files are stored in



'''


from slippi import *
from os import walk
game = Game("testGame.slp")

gameFiles = []

# populate a list with the names of the game file names.
for (dirpath, dirnames, filenames) in walk("./slp"):
    gameFiles.extend(filenames)
    break


file = open("stats.txt", "w+")

metadata = game.metadata

gameDur = metadata.duration

gameStart = metadata.date

# number of CPU games removed
cpuGames = 0

CPU = 0

# Dict to keep track of number of times character is used
charOccur = {}

# Dict to keep track of number of times a stage is used
stageOccur = {}

# Dict to keep track of wins for a certain character
numCharWins = {}
# TODO: Remove losses after testing is completed. 
numCharLosses = {}


print(str(gameDur) + " Frames")
print(gameStart)

print(metadata.players)

print(game.start.stage)

# print the player characters in the current game.
for player in game.start.players:
    print(player.character) if player != None else None


for singleGame in gameFiles:

    #print("processing new file")

    tempGame = Game("slp/" + singleGame)

    tempMeta = tempGame.metadata

    tempStart = tempGame.start

    # list of strings for the characters that are in the current game that is being processed. 
    charsInCurrGame = []

    if tempStart.is_teams == True:
        print("this game is not singles, not going to process this game. ")
        break

    # increment the stage that was used
    if str(tempStart.stage).split('.')[-1] not in stageOccur.keys():
        # turn the stage object into a string, split it on the '.' char, then put the stage name into the dict. 
        stageOccur[str(tempStart.stage).split('.')[-1]] = 1
    else:
        stageOccur[str(tempStart.stage).split('.')[-1]] += 1

    # increment the characters that were used.
    for player in tempStart.players:

        if player != None:

            
            tempCharacter = str(player.character).split('.')[-1]

            if tempCharacter not in charsInCurrGame:
                charsInCurrGame.append(tempCharacter)


            # NOTE: This player type checking is not working properly... Fix this as soon as possible.
            if player.type is CPU:
                cpuGames += 1
                print('CPU Game found, not processing...')
                break

            if str(player.character).split('.')[-1] not in charOccur.keys():
                # translate the character object to a string, split on the '.' char, then input only the name of the character into the dict.
                charOccur[str(player.character).split('.')[-1]] = 1
            else:
                charOccur[str(player.character).split('.')[-1]] += 1


    # Known: at this point, the charsInCurrGame list contains only the characters in the current game. can use this to determine the other character that won the game. 

    #print("chars in current game: {}".format(charsInCurrGame))

    

    for frame in tempGame.frames:
        # iterate through the frames to see which caracter won each game. 



        for playerPort in frame.ports:

            if playerPort != None:

                if playerPort.leader.post.stocks == 0:
                    # found the character that lost the game, need to find the character that won the game. 
                    
                    
                    # TODO: currently, the number of losses and the number of wins do not add up to the number of times the character was played. Think about the case of a ditto match. Number of losses does not add to number of games played. 


                    #print("{} lost this game.".format(str(playerPort.leader.post.character).split('.')[-1]))


                    # the loser for the current game was found, add the other character, that being the winner, to the numCharWins Dict. 
                    for currChar in charsInCurrGame:
                        if currChar != str(playerPort.leader.post.character).split('.')[-1]:
                            # NOTE: there are only 2 characters in the list, so the other character is the winner. 
                            
                            #print("{} won this game.".format(currChar))

                            # add currChar to numCharWins Dict
                            if currChar not in numCharWins.keys():
                                numCharWins[currChar] = 1
                            else:
                                numCharWins[currChar] += 1




                    # adding the loser to the numCharLosses Dict
                    if str(playerPort.leader.post.character).split('.')[-1] not in numCharLosses.keys():
                        numCharLosses[str(playerPort.leader.post.character).split('.')[-1]] = 1
                    else:
                        numCharLosses[str(playerPort.leader.post.character).split('.')[-1]] += 1



# outputting to the stats.txt file

file.writelines("Num Times Char Used:\n")
file.writelines(str(charOccur) + '\n')
file.writelines("Num Times Stage Used:\n")
file.writelines(str(stageOccur) + '\n')
file.writelines("Num Times Char lost:\n")
file.writelines(str(numCharLosses) + '\n')
file.writelines("Num Times Char Won:\n")
file.writelines(str(numCharWins))
print("stat computation completed")
