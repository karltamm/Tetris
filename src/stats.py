import shelve
import os

# CONSTANTS
# Score
FAST_DROP_POINTS = 1
FULL_ROW_POINTS = 200

# INITIALIZE
database = shelve.open(os.path.join("data", "stats"))


# FUNCTIONS
# Score
def increaseScore(current_score, reward, full_rows=0):
    if full_rows:
        return current_score + reward * full_rows
    else:
        return current_score + reward


def getHighScore():
    try:
        # If database already has high_score entry
        high_score = database["high_score"]
    except:
        high_score = 0

    return high_score


def saveHighScore(current_score, high_score):
    if current_score > high_score:
        database["high_score"] = current_score


def closeDatabase():
    database.close()
