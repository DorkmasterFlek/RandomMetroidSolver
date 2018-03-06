#!/usr/bin/python

# https://itemrando.supermetroid.run/randomize

import sys, math, os, json, logging, argparse

# the difficulties for each technics
from parameters import Conf, Knows, Settings, isKnows, isConf, isSettings
from parameters import easy, medium, hard, harder, hardcore, mania, diff2text

# the helper functions
from helpers import Pickup, Bosses, wand, wor, enoughStuffTourian, SMBool

from rom import RomReader, RomType, RomLoader

class Solver:
    # given a rom and parameters returns the estimated difficulty
    
    def __init__(self, type='console', rom=None, params=None, debug=False):
        if debug is True:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger('Solver')

        if params is not None:
            for paramsFileName in params:
                self.loadParams(paramsFileName)

        # can be called from command line (console) or from web site (web)
        self.type = type

        import tournament_locations
        self.locations = tournament_locations.locations

        self.romLoaded = False
        if rom is not None:
            self.loadRom(rom)
        
        self.pickup = Pickup(Conf.majorsPickup, Conf.minorsPickup)

        Bosses.reset()

    def loadRom(self, rom):
        RomLoader.factory(rom).assignItems(self.locations)
        if Conf.guessRomType is True and self.type == 'console':
            guessed = RomType.guess(rom)
            if guessed is not None:
                Conf.romType = guessed
        self.log.info("ROM Type : " + Conf.romType)
        self.fullRando = RomType.apply(Conf.romType)
        
        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("Display items at locations:")
            for location in self.locations:
                self.log.debug('{:>50}: {:>16}'.format(location["Name"], location['itemName']))

        self.romLoaded = True

    def loadParams(self, params):
        ParamsLoader.factory(params).load()

        if self.log.getEffectiveLevel() == logging.DEBUG:
            self.log.debug("loaded knows: ")
            for knows in Knows.__dict__:
                if isKnows(knows):
                    self.log.debug("{}: {}".format(knows, Knows.__dict__[knows]))
            self.log.debug("loaded settings:")
            for setting in Settings.__dict__:
                if isSettings(setting):
                    self.log.debug("{}: {}".format(setting, Settings.__dict__[setting]))
            self.log.debug("loaded conf:")
            for conf in Conf.__dict__:
                if isConf(conf):
                    self.log.debug("{}: {}".format(conf, Conf.__dict__[conf]))

    def solveRom(self):
        if self.romLoaded is False:
            self.log.error("rom not loaded")
            return

        difficulty = self.computeDifficulty()

        if self.type == 'console':
            # print generated path
            if Conf.displayGeneratedPath is True:
                self.printPath("Generated path:", self.visitedLocations)
                # if we've aborted, display remaining majors
                if difficulty == -1:
                    self.printPath("Remaining major locations:", self.majorLocations)
                    self.printPath("Remaining minor locations:", self.minorLocations)

            # display difficulty scale
            self.displayDifficulty(difficulty)

        return difficulty

    def displayDifficulty(self, difficulty):
        if difficulty >= 0:
            text = DifficultyDisplayer(difficulty).scale()
            print("Estimated difficulty: {}".format(text))
        else:
            print("Aborted run, can't finish the game with the given prerequisites")

    def getDiffThreshold(self):
        target = Conf.difficultyTarget
        threshold = target
        epsilon = 0.001
        if target <= easy:
            threshold = medium - epsilon
        elif target <= medium:
            threshold = hard - epsilon
        elif target <= hard:
            threshold = harder - epsilon
        elif target <= harder:
            threshold = hardcore - epsilon
        elif target <= hardcore:
            threshold = mania - epsilon

        return threshold

    def computeDifficulty(self):
        # loop on the available locations depending on the collected items.
        # before getting a new item, loop on all of them and get their difficulty,
        # the next collected item is the one with the smallest difficulty,
        # if equality between major and minor, take major first.

        if not self.fullRando:
            self.majorLocations = [loc for loc in self.locations if loc["Class"] == "Major"]
            self.minorLocations = [loc for loc in self.locations if loc["Class"] == "Minor"]
        else:
            self.majorLocations = self.locations[:] # copy
            self.minorLocations = self.majorLocations

        self.visitedLocations = []
        self.collectedItems = []

        # with the knowsXXX conditions some roms can be unbeatable, so we have to detect it
        previous = -1
        current = 0

        self.log.debug("{}/{}: available major: {}, available minor: {}, visited: {}".format(Conf.majorsPickup, str(Conf.minorsPickup), len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        isEndPossible = False
        endDifficulty = mania
        area = 'Crateria'
        diffThreshold = self.getDiffThreshold()
        while True:
            # actual while condition
            hasEnoughMinors = self.pickup.enoughMinors(self.collectedItems, self.minorLocations)
            hasEnoughMajors = self.pickup.enoughMajors(self.collectedItems, self.majorLocations)
            hasEnoughItems = hasEnoughMajors and hasEnoughMinors
            canEndGame = self.canEndGame()
            (isEndPossible, endDifficulty) = (canEndGame.bool, canEndGame.difficulty)
            if isEndPossible and hasEnoughItems and endDifficulty <= diffThreshold:
                self.log.debug("END")
                break

            #self.log.debug(str(self.collectedItems))
            self.log.debug("Current Area : " + area)

            # check if we have collected an item in the last loop
            current = len(self.collectedItems)
            if current == previous:
                if not isEndPossible:
                    self.log.debug("STUCK ALL")
                else:
                    self.log.debug("HARD END")
                break
            previous = current

            # compute the difficulty of all the locations
            self.computeLocationsDifficulty(self.majorLocations)
            self.computeLocationsDifficulty(self.minorLocations)

            # keep only the available locations
            majorAvailable = [loc for loc in self.majorLocations if loc["difficulty"].bool == True]
            minorAvailable = [loc for loc in self.minorLocations if loc["difficulty"].bool == True]

            # check if we're stuck
            if len(majorAvailable) == 0 and len(minorAvailable) == 0:
                if not isEndPossible:
                    self.log.debug("STUCK MAJORS and MINORS")
                else:
                    self.log.debug("HARD END")
                break

            # sort them on difficulty and proximity
            majorAvailable = self.getAvailableItemsList(majorAvailable, area, diffThreshold, hasEnoughMajors)
            minorAvailable = self.getAvailableItemsList(minorAvailable, area, diffThreshold, hasEnoughMinors)

            # first take major items of acceptable difficulty in the current area
            if (len(majorAvailable) > 0
                   and majorAvailable[0]['Area'] == area
                   and majorAvailable[0]['difficulty'].difficulty <= diffThreshold):
                self.collectMajor(majorAvailable.pop(0))
                continue
            # next item decision
            if len(minorAvailable) == 0 and len(majorAvailable) > 0:
                self.log.debug('MAJOR')
                area = self.collectMajor(majorAvailable.pop(0))
            elif len(majorAvailable) == 0 and len(minorAvailable) > 0:
                # we don't check for hasEnoughMinors here, because we would be stuck, so pickup
                # what we can and hope it gets better
                self.log.debug('MINOR')
                area = self.collectMinor(minorAvailable.pop(0))
            elif len(majorAvailable) > 0 and len(minorAvailable) > 0:
                self.log.debug('BOTH|M=' + majorAvailable[0]['Name'] + ', m=' + minorAvailable[0]['Name'])
                # if both are available, decide based on area and difficulty
                nextMajDifficulty = majorAvailable[0]['difficulty'].difficulty
                nextMinArea = minorAvailable[0]['Area']
                nextMinDifficulty = minorAvailable[0]['difficulty'].difficulty
                if nextMinArea == area and nextMinDifficulty <= diffThreshold and not hasEnoughMinors:
                    area = self.collectMinor(minorAvailable.pop(0))
                # difficulty over area (this is a difficulty estimator,
                # not a speedrunning simulator)
                elif nextMinDifficulty < nextMajDifficulty and not hasEnoughMinors:
                    area = self.collectMinor(minorAvailable.pop(0))
                else:
                    area = self.collectMajor(majorAvailable.pop(0))
        # main loop end
        if isEndPossible:
            self.visitedLocations.append({
                'item' : 'The End',
                'itemName' : 'The End',
                'Name' : 'The End',
                'Area' : 'The End',
                'Room': 'Mother Brain Room',
                'difficulty' : SMBool(True, endDifficulty)
            })

        # compute difficulty value
        difficulty = self.computeDifficultyValue()

        self.log.debug("difficulty={}".format(difficulty))
        self.log.debug("{}/{}: remaining major: {}, remaining minor: {}, visited: {}".format(Conf.majorsPickup, Conf.minorsPickup, len(self.majorLocations), len(self.minorLocations), len(self.visitedLocations)))

        self.log.debug("remaining majors:")
        for loc in self.majorLocations:
            self.log.debug("{} ({})".format(loc['Name'], loc['itemName']))

        self.log.debug("bosses: {}".format(Bosses.golden4Dead))

        return difficulty

    def computeLocationsDifficulty(self, locations):
        for loc in locations:
            if 'PostAvailable' in loc:
                loc['difficulty'] = wand(loc['Available'](self.collectedItems),
                                         loc['PostAvailable'](self.collectedItems + [loc['itemName']]))
            else:
                loc['difficulty'] = loc['Available'](self.collectedItems)

    def computeDifficultyValue(self):
        if not self.canEndGame().bool:
            # we have aborted
            difficulty = -1
        else:
            # sum difficulty for all visited locations
            difficulty_max = 0
            for loc in self.visitedLocations:
                difficulty_max = max(difficulty_max, loc['difficulty'].difficulty)
            difficulty = difficulty_max

        return difficulty

    def getPath(self, locations):
        out = []
        for location in locations:
            out.append([(location['Name'], location['Room']), location['Area'], location['itemName'],
                        '{0:.2f}'.format(location['difficulty'].difficulty),
                        ', '.join(sorted(location['difficulty'].knows)),
                        ', '.join(sorted(list(set(location['difficulty'].items))))])

        return out

    def getKnowsUsed(self):
        knows = []
        for loc in self.visitedLocations:
            knows += loc['difficulty'].knows

        # get unique knows
        knows = list(set(knows))

        return knows

    def printPath(self, message, locations):
        print(message)
        print('{:>50} {:>13} {:>16} {:>14} {} {}'.format("Location Name", "Area", "Item", "Difficulty", "Knows used", "Items used"))
        print('-'*106)
        for location in locations:
            print('{:>50}: {:>12} {:>16} {:>14} {} {}'.format(location['Name'],
                                                              location['Area'],
                                                              location['itemName'],
                                                              location['difficulty'].difficulty,
                                                              sorted(location['difficulty'].knows),
                                                              list(set(location['difficulty'].items))))

    def collectMajor(self, loc):
        self.majorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectMinor(self, loc):
        self.minorLocations.remove(loc)
        self.visitedLocations.append(loc)
        area = self.collectItem(loc)
        return area

    def collectItem(self, loc):
        item = loc["itemName"]
        if item not in Conf.itemsForbidden:
            self.collectedItems.append(item)
        else:
            # update the name of the item
            item = "-{}-".format(item)
            loc["itemName"] = item
            self.collectedItems.append(item)
            # we still need the boss difficulty
            if 'Pickup' not in loc:
                loc["difficulty"] = SMBool(False)
        if 'Pickup' in loc:
            loc['Pickup']()

        self.log.debug("collectItem: {} at {}".format(item, loc['Name']))

        return loc['Area']

    def canEndGame(self):
        # to finish the game you must :
        # - beat golden 4 : we force pickup of the 4 items
        #   behind the bosses to ensure that
        # - defeat metroids
        # - destroy/skip the zebetites
        # - beat Mother Brain
        return wand(Bosses.allBossesDead(), enoughStuffTourian(self.collectedItems))            
    
    def getAvailableItemsList(self, locations, area, threshold, enough):
        around = [loc for loc in locations if loc['Area'] == area and loc['difficulty'].difficulty <= threshold and not Bosses.areaBossDead(area)]
        # usually pickup action means beating a boss, so do that first if possible
        around.sort(key=lambda loc: (0 if 'Pickup' in loc else 1, loc['difficulty'].difficulty))

        outside = [loc for loc in locations if not loc in around]
        self.log.debug("around1 = " + str([loc['Name'] for loc in around]))
        self.log.debug("outside1 = " + str([loc['Name'] for loc in outside]))        
        # we want to sort the outside locations by putting the ones is the same
        # area first if we don't have enough items,
        # then we sort the remaining areas starting whith boss dead status
        outside.sort(key=lambda loc: (0 if loc['Area'] == area and not enough and loc['difficulty'].difficulty <= threshold
                                      else 1,
                                      loc['difficulty'].difficulty if not Bosses.areaBossDead(loc['Area'])
                                                                      and loc['difficulty'].difficulty <= threshold
                                                                      and 'Pickup' in loc
                                      else 100000,
                                      loc['difficulty'].difficulty if not Bosses.areaBossDead(loc['Area'])
                                                                      and loc['difficulty'].difficulty <= threshold
                                      else 100000,                                      
                                      loc['difficulty'].difficulty))
        self.log.debug("around2 = " + str([loc['Name'] for loc in around]))
        self.log.debug("outside2 = " + str([loc['Name'] for loc in outside]))
        
        return around + outside


class ParamsLoader(object):
    @staticmethod
    def factory(params):
        # can be a json, a python file or a dict with the parameters
        if type(params) is str:
            ext = os.path.splitext(params)
            if ext[1].lower() == '.json':
                return ParamsLoaderJson(params)
            else:
                print("wrong parameters file type: {}".format(ext[1]))
                sys.exit(-1)
        elif type(params) is dict:
            return ParamsLoaderDict(params)

    def __init__(self):
        if 'Knows' not in self.params:
            self.params['Knows'] = {}
        if 'Conf' not in self.params:
            self.params['Conf'] = {}
        if 'Settings' not in self.params:
            self.params['Settings'] = {}

        if 'hellRuns' not in self.params['Settings']:
            self.params['Settings']['hellRuns'] = {}
        if 'bossesDifficulty' not in self.params['Settings']:
            self.params['Settings']['bossesDifficulty'] = {}

    def load(self):
        # update the parameters in the parameters classes: Conf, Knows, Settings
        # Conf
        for param in self.params['Conf']:
            if isConf(param):
                setattr(Conf, param, self.params['Conf'][param])

        # Knows
        for param in self.params['Knows']:
            if isKnows(param):
                setattr(Knows, param, SMBool(self.params['Knows'][param][0],
                                             self.params['Knows'][param][1],
                                             ['{}'.format(param)]))

        # Settings
        for param in self.params['Settings']:
            if isSettings(param) and len(self.params['Settings'][param]) > 0:
                setattr(Settings, param, self.params['Settings'][param])

    def dump(self, fileName):
        with open(fileName, 'w') as jsonFile:
            json.dump(self.params, jsonFile)

    def printToScreen(self):
        print("self.params: {}".format(self.params))

        print("loaded knows: ")
        for knows in Knows.__dict__:
            if isKnows(knows):
                print("{}: {}".format(knows, Knows.__dict__[knows]))
        print("loaded settings:")
        for setting in Settings.__dict__:
            if isSettings(setting):
                print("{}: {}".format(setting, Settings.__dict__[setting]))
        print("loaded conf:")
        for conf in Conf.__dict__:
            if isConf(conf):
                print("{}: {}".format(conf, Conf.__dict__[conf]))


class ParamsLoaderJson(ParamsLoader):
    # when called from the test suite
    def __init__(self, jsonFileName):
        with open(jsonFileName) as jsonFile:
            self.params = json.load(jsonFile)
        super(ParamsLoaderJson, self).__init__()

class ParamsLoaderDict(ParamsLoader):
    # when called from the website
    def __init__(self, params):
        self.params = params
        super(ParamsLoaderDict, self).__init__()

class DifficultyDisplayer:
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def text(self):
        if self.difficulty >= easy and self.difficulty < medium:
            difficultyText = diff2text[easy]
        elif self.difficulty >= medium and self.difficulty < hard:
            difficultyText = diff2text[medium]
        elif self.difficulty >= hard and self.difficulty < harder:
            difficultyText = diff2text[hard]
        elif self.difficulty >= harder and self.difficulty < hardcore:
            difficultyText = diff2text[harder]
        elif self.difficulty >= hardcore and self.difficulty < mania:
            difficultyText = diff2text[hardcore]
        else:
            difficultyText = diff2text[mania]

        return difficultyText

    def scale(self):
        previous = 0
        for d in sorted(diff2text):
            if self.difficulty >= d:
                previous = d
            else:
                displayString = diff2text[previous]
                displayString += ' '
                scale = d - previous
                pos = int(self.difficulty - previous)
                displayString += '-' * pos
                displayString += '^'
                displayString += '-' * (scale - pos)
                displayString += ' '
                displayString += diff2text[d]
                break

        return displayString

    def normalize(self):
        if self.difficulty == -1:
            return (None, None)

        previous = 0
        for d in sorted(diff2text):
            if self.difficulty >= d:
                previous = d
            else:
                baseDiff = diff2text[previous]
                normalized = int(5*float(self.difficulty - previous)/float(d - previous))
                break

        return (baseDiff, normalized)

    def percent(self):
        # return the difficulty as a percent
        if self.difficulty == -1:
            return -1
        elif self.difficulty in [0, easy]:
            return 0

        difficultiesPercent = {
            easy: 0,
            medium: 20,
            hard: 40,
            harder: 60,
            hardcore: 80,
            mania: 100,
            mania*2: 100,
            mania*4: 100
        }

        difficulty = self.difficulty if self.difficulty < mania else mania

        lower = 0
        percent = 100
        for upper in sorted(diff2text):
            if self.difficulty >= upper:
                lower = upper
            else:
                lowerPercent = difficultiesPercent[lower]
                upperPercent = difficultiesPercent[upper]

                a = (upperPercent-lowerPercent)/float(upper-lower)
                b = lowerPercent - a * lower

                percent = int(difficulty * a + b)
                break

        return percent

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random Metroid Solver")
    parser.add_argument('romFileName', help="the input rom")
    parser.add_argument('--param', '-p', help="the input parameters", nargs='+', default=None, dest='paramsFileName')

    parser.add_argument('--debug', '-d', help="activate debug logging", dest='debug', action='store_true')
    parser.add_argument('--difficultyTarget', '-t', help="the difficulty target that the solver will aim for", dest='difficultyTarget', nargs='?', default=None, type=int)
    parser.add_argument('--displayGeneratedPath', '-g', help="display the generated path (spoilers!)", dest='displayGeneratedPath', action='store_true')

    args = parser.parse_args()

    solver = Solver(rom=args.romFileName, params=args.paramsFileName, debug=args.debug)

    if args.difficultyTarget is not None:
        Conf.difficultyTarget = args.difficultyTarget

    Conf.displayGeneratedPath = args.displayGeneratedPath

    #solver.solveRom()
    diff = solver.solveRom()
    knowsUsed = solver.getKnowsUsed()
    print("{} : diff : {}".format(diff, args.romFileName))
    print("{} : knows Used : {}".format(len(knowsUsed), args.romFileName))
