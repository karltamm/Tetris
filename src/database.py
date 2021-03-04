import shelve
import os

# CONSTANTS
# Score
SINGLE_ROW_POINTS = 100

# Trophies
TROPHIES = [[["Legend", "Reach 500,000 points", "high_score", 500000],
             ["Master", "Reach 100,000 point", "high_score", 100000],
             ["Advanced", "Reach 50,000 points", "high_score", 50000],
             ["Novice", "Reach 10,000 points", "high_score", 10000]],

            [["Tetris", " Do 10 Quadruple row clears", "rows_4", 10],
             ["Clear", "Clear 100 rows", "rows", 100],
             ["Clearer", "Clear 250 rows", "rows", 250],
             ["Clearest", "Clear 500 rows", "rows", 500]],

            [["No-life", "Spend 2 hours in-game", "time_ingame", 7200],
             ["Try hard", "Get all trophies", "trophies", 16],
             ["Clean board", "Make a quadruple-line perfect clears", "perfect_clears_4", 1],
             ["Gamer", "Play 100 games", "games_played", 100]],

            [["Long game", "Spend 10 minutes in one game", "", 600],
             ["", "", "", 2],
             ["", "", "", 2],
             ["", "", "", 2]]]

# INITIALIZE
STATS_DB = shelve.open(os.path.join("../data", "stats"))
OPTIONS_DB = shelve.open(os.path.join("../data", "options"))
SAVED_GAME_DB = shelve.open(os.path.join("../data", "saved_game"))


# CLASS
class Score:
    def __init__(self, current_score):
        self.current_score = current_score

    def fullRow(self, stage, full_rows):
        if (full_rows == 1):
            self.current_score += SINGLE_ROW_POINTS * stage
            saveStat("rows_1", 1)
        elif (full_rows == 2):
            self.current_score += SINGLE_ROW_POINTS * 3 * stage
            saveStat("rows_2", 1)
        elif (full_rows == 3):
            self.current_score += SINGLE_ROW_POINTS * 5 * stage
            saveStat("rows_3", 1)
        else:
            self.current_score += SINGLE_ROW_POINTS * 8 * stage
            saveStat("rows_4", 1)
        return self.current_score

    def perfectClear(self, stage, full_rows):
        saveStat("perfect_clears", 1)
        if (full_rows == 1):
            self.current_score += SINGLE_ROW_POINTS * 8 * stage
            saveStat("perfect_clears_1", 1)
        elif (full_rows == 2):
            self.current_score += SINGLE_ROW_POINTS * 12 * stage
            saveStat("perfect_clears_2", 1)
        elif (full_rows == 3):
            self.current_score += SINGLE_ROW_POINTS * 18 * stage
            saveStat("perfect_clears_3", 1)
        else:
            self.current_score += SINGLE_ROW_POINTS * 20 * stage
            saveStat("perfect_clears_4", 1)
        return self.current_score

    def drop(self, points):
        self.current_score += points
        return self.current_score
    # Can add more functions for adding score (perfect clear, T-spin...)


# FUNCTIONS
# Options
def optionsValues(name, change=False, new_value=None):
    try:
        value = OPTIONS_DB[name]
    except:
        if name == "sound":
            value = 1
        else:
            value = True
    if change:  # inverts boolean value
        value = not value
        OPTIONS_DB[name] = value
    elif new_value is not None:  # Changes int value
        value = new_value
        OPTIONS_DB[name] = value
    else:  # if value wasn't changed, returns it
        return value


# Stats
def getStat(stat):
    try:
        # If database already has high_score entry
        value = STATS_DB[stat]
    except:
        value = 0
    return value


def saveStat(stat, new_value, compare=0):
    if compare:
        # Replace stat with value if new value is higher
        if new_value > getStat(stat):
            STATS_DB[stat] = new_value
    else:
        # Add new value to old stat value
        STATS_DB[stat] = getStat(stat) + new_value


# Saved game
def checkIfGameIsSaved():
    try:
        save_exsists = SAVED_GAME_DB["save_exsists"]
    except:
        save_exsists = False
    return save_exsists


def closeDB():
    STATS_DB.close()
    OPTIONS_DB.close()
    SAVED_GAME_DB.close()
