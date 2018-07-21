from Game.Tile import Tile
from Game.Line import Line
import numpy as np


class GameState:
    def __init__(self, size, square_size, win_len):
        """Initialise a tile and create rectangles"""
        self.size = size
        self.win_len = win_len
        self.checked_count = 0
        self.tiles = [size[0] * [None] for i in range(size[1])]

        # Lines contain the winning streaks
        self.lines = []

        # Initialise all tiles as empty tiles
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                self.tiles[x][y] = Tile((x, y), square_size, (0, 0))

        # The tile that was last played is used for checking of the game state - win,..
        self.last_played_tile = None

    def __get_tile_at_pos(self, position):
        """Get a tile at given position"""
        return self.tiles[position[0]][position[1]]

    def __is_in_bounds(self, position):
        """Check if the given position if in board bounds."""
        if 0 <= position[0] < self.size[0]:
            if 0 <= position[1] < self.size[1]:
                return True
        return False

    def __find_axis_end(self, pos, axis, player_id):
        """Finds one of the ends of the axis. Returns the steps taken.
        :type pos: np.array
        :type axis: np.array
        :param player_id: id of the player
        """

        # Copy the mutable array
        pos = pos.copy()

        # Traverse to the end and count the steps
        count = 0
        while True:
            if self.__is_in_bounds(tuple(pos)):
                tile = self.__get_tile_at_pos(tuple(pos))
                if tile.played_by_player(player_id):
                    count += 1
                    pos += axis
                else:
                    break
            else:
                break

        # Subtract the last move which was invalid
        return count, pos - axis

    def __check_axis(self, position, axis, player_id):
        """Traverse the axis first to one end, then to the other and keep count
        :type position: np.array
        :type axis: np.array
        :param player_id: id of the player
        :return: Line with score
        """

        # Go to the both ends of the axis
        score1, line_start = self.__find_axis_end(position, axis, player_id)
        score2, line_end = self.__find_axis_end(position, axis * -1, player_id)

        # Omit the current square that is calculated twice
        score = score1 + score2 - 1
        return Line(line_start, line_end, score)

    def __best_line_after_move(self, position, player_id):
        """Get the score after move. NP arrays are used as a vector"""
        # Zero length line
        maximum = Line(np.array([0, 0]), np.array([0, 0]), 0)
        # - check
        maximum = max(maximum, self.__check_axis(position, np.array([1, 0]), player_id))
        # | check
        maximum = max(maximum, self.__check_axis(position, np.array([0, 1]), player_id))
        # / check
        maximum = max(maximum, self.__check_axis(position, np.array([1, 1]), player_id))
        # \ check
        maximum = max(maximum, self.__check_axis(position, np.array([1, -1]), player_id))
        # Return the best fit
        return maximum

    def check_win(self, position, player_id):
        """Checks if any of the players won or the game has ended with draw
        None => The game is undecided
        0 => player 0 won
        1 => player 1 won
        2 => draw
        """
        line = self.__best_line_after_move(position, player_id)

        if line.score >= self.win_len:
            print("Player ID {0} won!".format(player_id))
            self.lines.append(line)
            return player_id
        elif (self.size[0] * self.size[1]) == self.checked_count:
            print("The game has ended with draw.")
            return 2
        else:
            return None

    def play(self, position, player_id):
        """Tick a square and check, if it is valid"""
        tile = self.__get_tile_at_pos(position)

        if not tile.was_played():
            self.last_played_tile = tile
            self.last_played_tile.play(player_id)
            self.checked_count += 1
            self.check_win(np.array(position), player_id)
