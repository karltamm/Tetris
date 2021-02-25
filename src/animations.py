from screen import *
import random
import pygame


class TetrisRain:
    def __init__(self):
        self.droplets = []
        self.last_spawn_time = None

    def spawnDroplets(self):
        # Spawn in intervals
        current_time = pygame.time.get_ticks()
        if self.last_spawn_time is None or current_time - self.last_spawn_time > 1000:
            self.last_spawn_time = current_time

            # Spawn in a row
            for x_pos in range(BOARD_CELL, SCREEN_WIDTH - BOARD_CELL,
                               2 * BOARD_CELL):  # Last param = horizontal spacing
                y_pos = 0 - 2 * BOARD_CELL  # Droplet spawns before screen area
                y_pos += random.randint(1, BOARD_CELL)  # Make vertical spacing random

                if random.randint(0, 9) < 3:  # Spawn randomly
                    self.droplets.append(Droplet(x_pos, y_pos))

    def makeItRain(self):
        self.spawnDroplets()

        # Control droplets
        for i, droplet in enumerate(self.droplets):
            if droplet.y > SCREEN_HEIGHT + BOARD_CELL * 5:  # Delete droplet
                self.droplets.pop(i)
            else:
                droplet.fall()


class Droplet:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.image = random.choice(CELLS_IMAGES)
        self.speed = 1  # px/per cycle (1 cycle = 1/FPS seconds)

    def fall(self):
        self.y += self.speed
        drawObject(self.image, self.x, self.y)
