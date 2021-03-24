import shelve
import os

# CONSTANTS
# Score
SINGLE_ROW_POINTS = 100

# Trophies
TROPHIES = [[["Novice(classic)", "Reach 10,000 points in classic mode", "high_score", 10000],
             ["Advanced(classic)", "Reach 50,000 points in classic mode", "high_score", 50000],
             ["Master(classic)", "Reach 100,000 point in classic mode", "high_score", 100000],
             ["Legend(classic)", "Reach 250,000 points in classic mode", "high_score", 250000]],

            [["Novice(power-ups)", "Reach 10,000 points with power-ups", "high_score_powers", 20000],
             ["Advanced(power-ups)", "Reach 65,000 points with power-ups", "high_score_powers", 65000],
             ["Master(power-ups)", "Reach 125,000 point with power-ups", "high_score_powers", 125000],
             ["Legend(power-ups)", "Reach 300,000 points with power-ups", "high_score_powers", 300000]],

            [["Double", "Do 50 double row clears", "rows_2", 50],
             ["Triple", "Do 25 triple row clears", "rows_3", 25],
             ["Tetris", "Do 10 quadruple row clears", "rows_4", 10],
             ["Clean board", "Make a quadruple-line perfect clear", "perfect_clears_4", 1]],

            [["Clear", "Clear 100 rows", "rows", 100],
             ["Clearer", "Clear 250 rows", "rows", 250],
             ["Clearest", "Clear 500 rows", "rows", 500],
             ["Clear game", "Clear 100 rows in one game", "single_game_rows", 100]],

            [["Long game", "Spend 10 minutes in one game", "single_game_time_ingame", 600],
             ["No-life", "Spend 2 hours in-game", "time_ingame", 7200],
             ["Try hard", "Get all trophies", "trophies", 16],
             ["Gamer", "Play 100 games", "games_played", 100]]]

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
def optionsValues(option, invert=False, new_value=None):
    try:
        value = OPTIONS_DB[option]
    except:  # No such option saved in database, so create new value
        if option == "sound" or option == "music":
            value = 1
        elif option == "theme":
            value = 0
        else:
            value = True

    if invert:
        value = not value
        OPTIONS_DB[option] = value
    elif new_value is not None:
        value = new_value
        OPTIONS_DB[option] = value
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
