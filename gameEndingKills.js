// This file will generate a .json file for all the kills that end each game. 

// NOTE: This file should generate the same number of combos as there are game files in the 'slp' directory. this should add the combo to the .json file even if the last kill combo was just a single move. 


const fs = require('fs');
const _ = require('lodash');
const path = require('path');
const { default: SlippiGame } = require('slp-parser-js'); // the slippi parsing library. 

const basePath = path.join(__dirname, 'slp/');

const dolphin = {
    "mode": "queue",
    "replay": "",
    "isRealTimeMode": false,
    "outputOverlayFiles": true,
    "queue": []
};


const filterByNames = []; // add names as strings to this array. Checks netplay names and nametags. 


// Removal Statistics
var numWobbles = 0;
var numCG = 0;
var numCPU = 0;
var puffMiss = 0;
var badFiles = 0;
var noCombos = 0;
var numFiles = 0;

/*
    this function below will traverse a directory to get all the files in the folder to process. 

*/
function walk(dir) {
    let results = [];
    let list = fs.readdirSync(dir);
    _.each(list, (file) => {
        file = path.join(dir, file);
        let stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            // Recurse into a subdirectory
            results = results.concat(walk(file));
        } else if (path.extname(file) === ".slp") {
            results.push(file);
        }
    });
    return results;
}


/*
    This function will return a list of combos that meets a certain criteria defined within this function. 

*/
function filterCombos(combos, settings, metadata) {

    return _.filter(combos, (combo) => {

        var wobbles = [];
        let filteredName = true;
        let pummels = 0;
        let chaingrab = false;

        let player = _.find(settings.players, (player) => player.playerIndex === combo.playerIndex);

        let opponent = _.find(settings.players, (player) => player.playerIndex !== combo.playerIndex);

        if (filterByNames.length > 0) {
            var matches = [];

            _.each(filterByNames, (filterName) => {


                const netplayName = _.get(metadata, ["players", player.playerIndex, "names", "netplay"], null) || null;
                const playerTag = _.get(player, "nametag") || null;

                const names = [netplayName, playerTag];
                matches.push(_.includes(names, filterName));

            });
            filteredName = _.some(matches, (match) => match);

        }

        if (!filteredName) 
            return filteredName

            // TODO: How to check that the opponent has 0 stocks left after the combo? I only want the combos at the very end of the games. 
        
        return combo.didKill;


    });




}

function getFinalKills() {
    let files = walk(basePath);

    console.log(`${files.length} replay files found, Extracting Final Kills:`)

    // iterate through the files to process them all.
    _.each(files, (file, i) => {

        //console.log(`Processing file ${++numFiles}:`);

        try {

            const game = new SlippiGame(file);

            const curSetting = game.getSettings();
            const curMetadata = game.getMetadata();

            // skip files that are played against CPUs. 
            const cpu = _.some(curSetting.players, (player) => player.type != 0)

            if (cpu) {
                numCPU++;
                return;
            }

            // get the stats for the current game. 
            const curStats = game.getStats();
            const originalCombos = curStats.combos;

            const combos = filterCombos(originalCombos, curSetting, curMetadata);

            _.each(combos, ({startFrame, endFrame, playerIndex}) => {

                let player = _.find(curSetting.players, (player) => player.playerIndex === playerIndex);
                let opponent = _.find(curSetting.players, (player) => player.playerIndex !== playerIndex);

                let x = {

                    path: file,
                    startFrame: startFrame - 240 > -123 ? startFrame - 240 : -123,
                    endFrame: endFrame + 180 < curMetadata.lastFrame ? endFrame + 180 : curMetadata.lastFrame,
                    gameStartAt: _.get(curMetadata, "startAt", ""),
                    gameStation: _.get(curMetadata, "consoleNick", ""),
                    additional: {
                        characterId: player.characterId,
                        opponentCharacterId: opponent.characterId,
                    }


                };

                dolphin.queue.push(x);

            });

            combos.length === 0 ? noCombos++ : console.log(`file ${i + 1} | ${combos.length} combos found in ${path.basename(file)}`);


        } catch (err) {
            // error checking and resolving the error. 

            console.log(`file ${i + 1} | ${file} is bad`);

        }



    });


    console.log(`Total Combos found: ${dolphin.queue.length}`);

    fs.writeFileSync("./endingKills.json", JSON.stringify(dolphin));



}

getFinalKills();


console.log('Completed Game Ending Kills Generation.');