// This file will generate a .json file for all the kills that end each game. 

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

function filterCombos(combos, settings, metadata) {

    return _.filter(combos, (combo) => {

        var wobbles = [];
        let filteredName = true;
        let pummels = 0;
        let chaingrab = false;

        let player = _.find(settings.players, (player) => player.playerIndex === combo.playerIndex);

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

    });




}

function getFinalKills() {
    let files = walk(basePath);

    console.log(`${files.length} replay files found, Extracting Final Kills:`)

    // iterate through the files to process them all.
    _.each(files, (file, i) => {

        console.log(`Processing file ${++numFiles}:`);

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
            const originalCombos = stats.combos;


        } catch (err) {
            // error checking and resolving the error. 


        }



    });

}

getFinalKills();


console.log('Completed Game Ending Kills Generation.');