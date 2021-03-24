from assets import *
from database import *

# CONSTANTS
THEMES = ("Classic", "Yin-Yang", "XP")


# CLASSES
class Theme:
    def __init__(self, theme_index):
        if theme_index == 0:
            self.name = "Classic"

            self.T_cell = CLASSIC_RED_CELL
            self.S_cell = CLASSIC_BLUE_CELL
            self.I_cell = CLASSIC_GREEN_CELL
            self.Z_cell = CLASSIC_YELLOW_CELL
            self.J_cell = CLASSIC_PINK_CELL
            self.L_cell = CLASSIC_PURPLE_CELL
            self.O_cell = CLASSIC_BRONZE_CELL
            self.empty_cell = CLASSIC_EMPTY_CELL
            self.shadow_cell = CLASSIC_SHADOW_CELL

            self.bg = None
            self.block_images = CLASSIC_BLOCK_IMAGES
            self.block_images_hl = CLASSIC_BLOCK_IMAGES_HL
        elif theme_index == 1:
            self.name = "Yin-Yang"

            self.T_cell = YIN_YANG_BLACK_CELL
            self.S_cell = YIN_YANG_BLACK_CELL
            self.I_cell = YIN_YANG_BLACK_CELL
            self.Z_cell = YIN_YANG_BLACK_CELL
            self.J_cell = YIN_YANG_BLACK_CELL
            self.L_cell = YIN_YANG_BLACK_CELL
            self.O_cell = YIN_YANG_BLACK_CELL
            self.empty_cell = TRANSPARENT_CELL
            self.shadow_cell = YIN_YANG_SHADOW_CELL

            self.bg = YIN_YANG_BG
            self.block_images = YIN_YANG_BLOCK_IMAGES
            self.block_images_hl = YIN_YANG_BLOCK_IMAGES_HL
        elif theme_index == 2:
            self.name = "XP"

            self.T_cell = XP_BLUE_CELL
            self.S_cell = XP_BLUE_CELL
            self.I_cell = XP_BLUE_CELL
            self.Z_cell = XP_BLUE_CELL
            self.J_cell = XP_BLUE_CELL
            self.L_cell = XP_BLUE_CELL
            self.O_cell = XP_BLUE_CELL
            self.empty_cell = TRANSPARENT_CELL
            self.shadow_cell = XP_SHADOW_CELL

            self.bg = XP_BG
            self.block_images = XP_BLOCK_IMAGES
            self.block_images_hl = XP_BLOCK_IMAGES_HL


# FUNCTIONS
def getThemesInfo():
    themes_info = {}
    active_theme_index = optionsValues("theme")
    num_of_unlocked_trophies = getStat("trophies")

    for i, name in enumerate(THEMES):
        trophies_needed = 0
        is_unlocked = False

        if i == 0:
            is_unlocked = True
        elif i == 1:
            if num_of_unlocked_trophies > 4:
                is_unlocked = True
            else:
                trophies_needed = 5 - num_of_unlocked_trophies
        elif i == 2:
            if num_of_unlocked_trophies > 14:
                is_unlocked = True
            else:
                trophies_needed = 15 - num_of_unlocked_trophies

        if i == active_theme_index:
            is_active = True
        else:
            is_active = False

        themes_info[i] = {
            "name": name,
            "unlocked": is_unlocked,
            "trophies_needed": trophies_needed,
            "active": is_active
        }

    return themes_info
