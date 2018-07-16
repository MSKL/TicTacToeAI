from Game.Board import Board
from Game.Colors import *
from Game.Player import Player
from Game.Line import Line
import pygame
import numpy as np


class Game:
    def __init__(self, size, win_len, square_size):
        """Initialise board and PyGame"""
        self.size = size
        self.win_len = win_len
        self.square_size = square_size

        # Create a board and lines array
        self.board = Board(size, square_size)
        self.lines = []

        # Setup the PyGame
        pygame.init()
        self.window_size = [(size[0]) * square_size, (size[1]) * square_size]
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(WHITE)
        pygame.display.set_caption("Tic Tac Toe AI")

        # Draw empty board
        self.draw_board()
        self.draw_lines()

        # Initialise players
        self.players = []
        self.players.append(Player(RED, "RED0"))
        self.players.append(Player(BLUE, "BLUE1"))

        # How many tiles were checked
        self.checked_count = 0

        # Red player starts
        self.next_player_index = 0

        # Start the main loop
        self.game_loop()

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
            if self.board.tile_in_bounds(tuple(pos)):
                tile = self.board.tile_at_pos(tuple(pos))
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
            print("Line start ({0}, {1})".format(line.start[0], line.start[1]))
            print("Line end ({0}, {1})".format(line.end[0], line.end[1]))
            self.lines.append(line)
            return player_id
        elif self.checked_count:
            print("The game has ended with draw.")
            return 2

        return None

    def check_draw(self):
        """Checks for draw"""
        board_size = self.size[0] * self.size[1]
        if self.checked_count == board_size:
            print("The game is a draw.")
            return True
        else:
            return False

    def draw_board(self):
        """Draws all rectangles from tiles"""
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                tile = self.board.tiles[x][y]
                pygame.draw.rect(self.screen, tile.tile_color, tile.rect)

    def draw_lines(self):
        """Draws lines stored in the game class"""
        for line in self.lines:
            real_start = (line.start[0] * self.square_size + self.square_size / 2,
                          line.start[1] * self.square_size + self.square_size / 2)
            real_end = (line.end[0] * self.square_size + self.square_size / 2,
                        line.end[1] * self.square_size + self.square_size / 2)

            pygame.draw.line(self.screen, BLACK, real_start, real_end, 10)

    def play(self, position):
        """Tick a square and check, if it is valid"""
        tile = self.board.tile_at_pos(position)
        player = self.players[self.next_player_index]

        # Play the tile
        played = tile.play(self.next_player_index, player)

        if played:
            self.checked_count += 1
            self.check_draw()
            self.check_win(np.array(position), self.next_player_index)
            self.cycle_players()

    def cycle_players(self):
        """Switches to the next player's index"""
        self.next_player_index = (self.next_player_index + 1) % 2

    def loop_tick(self):
        """One tick of the main game loop"""
        # Check the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for x in range(0, self.size[0]):
                    for y in range(0, self.size[1]):
                        tile = self.board.tiles[x][y]
                        if tile.was_hit(mouse_pos):
                            self.play((x, y))

        # Flip the display after possible update
        self.draw_board()
        self.draw_lines()
        pygame.display.flip()
        return False

    def game_loop(self):
        """The main game loop"""
        done = False
        while not done:
            done = self.loop_tick()
