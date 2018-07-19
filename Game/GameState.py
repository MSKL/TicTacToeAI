from Game.Tile import Tile
from Game.Line import Line
import numpy as np


class GameState:
    def __init__(self, size, square_size, win_len):
        """Initialise a tile and create rectangles"""
        self.size = size
        self.win_len = win_len

        # Initialise the tile array
        self.tiles = [size[0] * [None] for i in range(size[1])]

        # Lines contain the winning streaks
        self.lines = []

        # Checked count
        self.checked_count = 0

        # Todo: check the weird indexing
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                self.tiles[x][y] = Tile((x, y), square_size, (0, 0))

        # The tile that was last played is used for checking of the game state
        self.last_played_tile = None

    def tile_at_pos(self, position):
        """Get a tile at given position"""
        return self.tiles[position[0]][position[1]]

    def tile_in_bounds(self, position):
        """Check if the given position if in board bounds"""
        if 0 <= position[0] < self.size[0]:
            if 0 <= position[1] < self.size[1]:
                return True
        return False

    def find_axis_end(self, pos, axis, player_id):
        """Finds one of the ends of the axis. Returns the steps taken
        :type pos: np.array
        :type axis: np.array
        :param player_id: id of the player
        """

        # Copy the mutable array
        pos = pos.copy()

        count = 0
        while True:
            if self.tile_in_bounds(tuple(pos)):
                tile = self.tile_at_pos(tuple(pos))
                if tile.played_by_player(player_id):
                    count += 1
                    pos += axis
                else:
                    break
            else:
                break

        # Subtract the last move which was invalid
        return count, pos - axis

    def check_axis(self, position, axis, player_id):
        """Traverse the axis first to one end, then to the other and keep count
        :type position: np.array
        :type axis: np.array
        :param player_id: id of the player
        :return: Line with score
        """
        score1, line_start = self.find_axis_end(position, axis, player_id)
        axis *= -1  # Reverse axis
        score2, line_end = self.find_axis_end(position, axis, player_id)

        score = score1 + score2 - 1
        return Line(line_start, line_end, score)

    def best_line_after_move(self, position, player_id):
        """Get the score after move"""
        maximum = Line(np.array([0, 0]), np.array([0, 0]), 0)
        # - check
        maximum = max(maximum, self.check_axis(position, np.array([1, 0]), player_id))
        print("horizontal start ({0}, {1})".format(maximum.start[0], maximum.start[1]))
        print("horizontal end ({0}, {1})".format(maximum.end[0], maximum.end[1]))
        # | check
        maximum = max(maximum, self.check_axis(position, np.array([0, 1]), player_id))
        # / check
        maximum = max(maximum, self.check_axis(position, np.array([1, 1]), player_id))
        # \ check
        return max(maximum, self.check_axis(position, np.array([1, -1]), player_id))

    def check_win(self, position, player_id):
        """:returns 0/1 => player0/1 won, 2 => draw, None => anything else"""
        line = self.best_line_after_move(position, player_id)

        if line.score >= self.win_len:
            print("Player ID {0} won!".format(player_id))
            self.lines.append(line)
            return player_id
        elif (self.size[0] * self.size[1]) == self.checked_count:
            print("The game has ended with draw.")
            return 2
        return None

    def play(self, position, player_id):
        """Tick a square and check, if it is valid"""
        tile = self.tile_at_pos(position)

        # Play the tile
        played = tile.play(player_id)

        if played:
            self.checked_count += 1
            self.last_played_tile = tile
            self.check_win(np.array(position), player_id)