'''
    Pieces of data to get from processing all files in a folder

    character occurances
    stage occurances
    win percentage by character
    average stock time (frames)
    average stock percent at time of death

    remove data from CPU players

    longest combo (# of hits)
    longest combo (highest percent)


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

# Dict to keep track of number of times character is used
charOccur = {}

# Dict to keep track of number of times a stage is used
stageOccur = {}


# Dict to keep track of wins for a certain character
nunmCharWins = {}

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

    # increment the stage that was used
    if tempStart.stage not in stageOccur.keys():
        stageOccur[tempStart.stage] = 1
    else:
        stageOccur[tempStart.stage] += 1

    # increment the characters that were used.
    for player in tempStart.players:

        if player != None:

            if player.character not in charOccur.keys():
                charOccur[player.character] = 1
            else:
                charOccur[player.character] += 1

        #charOccur[player.char if player != None else None] += 1


file.writelines(str(charOccur))
file.writelines(str(stageOccur))
print("stat computation completed")