import shelve
import os

# CONSTANTS
# Score
FAST_DROP_POINTS = 1
SINGLE_ROW_POINTS = 100
MULTIPLE_ROW_POINTS = 200

# INITIALIZE
STATS_DB = shelve.open(os.path.join("data", "stats"))
OPTIONS_DB = shelve.open(os.path.join("data", "options"))


# CLASS
class Score:
    def __init__(self, current_score):
        self.current_score = current_score

    def fullRow(self, stage, full_rows):
        self.current_score += int(
            (SINGLE_ROW_POINTS + (MULTIPLE_ROW_POINTS * (full_rows - 1))) * (1 + (stage - 1) * 0.5))
        return self.current_score

    def drop(self):
        self.current_score += FAST_DROP_POINTS
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

def getHighScore():
    try:
        # If database already has high_score entry
        high_score = STATS_DB["high_score"]
    except:
        high_score = 0

    return high_score


def saveHighScore(current_score, high_score):
    if current_score > high_score:
        STATS_DB["high_score"] = current_score


def closeDB():
    STATS_DB.close()
    OPTIONS_DB.close()
