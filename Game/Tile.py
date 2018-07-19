import random
from pygame import Rect
from Game.Colors import *


class Tile:
    def __init__(self, position, square_size, value, player=None):
        self.value = value
        self.player = player
        self.position = position

        # Calculate rect boundaries
        # Todo: Check the weird behavior. Errors possible
        self.top = self.position[0]*square_size
        self.bot = self.position[0]*square_size + square_size
        self.left = self.position[1]*square_size
        self.right = self.position[1]*square_size + square_size

        # Get the rect's correct color
        shade = random.randint(200, 255)
        if self.player is None:
            self.tile_color = (shade, shade, shade)
        else:
            self.tile_color = player.color

        # Create the rect
        self.rect = Rect(self.top, self.left, self.bot, self.right)

    def was_played(self):
        """Checks if the player has played"""
        return self.value != (0, 0)

    def played_by_player(self, player_index):
        """Check if the tile was played by a player with given id"""
        if player_index == 0:
            return self.value == (1, 0)
        if player_index == 1:
            return self.value == (0, 1)
        return False

    def play(self, player_index):
        """Mark the tile as played. Do nothing if already played."""
        if self.was_played():
            return False

        if player_index == 0:
            self.value = (1, 0)
            self.tile_color = RED
        elif player_index == 1:
            self.value = (0, 1)
            self.tile_color = BLUE

        return True

    def was_hit(self, mouse_position):
        """Check if the tile was hit by mouse"""
        if self.top < mouse_position[0] <= self.bot:
            if self.left < mouse_position[1] <= self.right:
                return True
        return False

    def __str__(self):
        return "Tile value ({0}, {1}) position ({2}, {3})"\
            .format(self.value[0], self.value[1], self.position[0], self.position[1])

    def __repr__(self):
        return str(self)