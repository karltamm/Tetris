import shelve
import os

# CONSTANTS
# Score
SINGLE_ROW_POINTS = 100

# INITIALIZE
STATS_DB = shelve.open(os.path.join("data", "stats"))
OPTIONS_DB = shelve.open(os.path.join("data", "options"))


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
def optionsValues(name, change=False):
    try:
        value = OPTIONS_DB[name]
    except:
        value = True
        OPTIONS_DB[name] = value
    if change:
        value = not value
        OPTIONS_DB[name] = value
    return value


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


def closeDB():
    STATS_DB.close()
    OPTIONS_DB.close()
