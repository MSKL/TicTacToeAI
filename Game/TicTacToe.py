from Game.GameState import GameState
from Game.Colors import *
import pygame


class Game:
    def __init__(self, size, win_len, square_size):
        """Initialise board and PyGame"""
        self.size = size
        self.square_size = square_size

        # Create a board and lines array
        self.board = GameState(size, square_size, win_len)

        # Setup the PyGame
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe AI")
        self.window_size = [(size[0]) * square_size, (size[1]) * square_size]
        self.screen = pygame.display.set_mode(self.window_size)
        self.screen.fill(WHITE)

        # Setup the text
        pygame.font.init()
        self.information_text = "Scio me nihil scire."
        self.my_font = pygame.font.SysFont("helvetica", 16)

        # Index of the next player that will play
        self.next_player_index = 0

        # If the game has ended with win or draw
        self.ended = False

        # Start the main loop
        self.game_loop()

    def draw_board(self):
        """Draws all rectangles from tiles"""
        for x in range(0, self.size[0]):
            for y in range(0, self.size[1]):
                tile = self.board.tiles[x][y]
                pygame.draw.rect(self.screen, tile.tile_color, tile.rect)

    def draw_lines(self):
        """Draws lines stored in the game class"""
        for line in self.board.lines:
            real_start = (line.start[0] * self.square_size + self.square_size / 2,
                          line.start[1] * self.square_size + self.square_size / 2)
            real_end = (line.end[0] * self.square_size + self.square_size / 2,
                        line.end[1] * self.square_size + self.square_size / 2)

            pygame.draw.line(self.screen, BLACK, real_start, real_end, 10)

    def draw_text(self):
        """Draws the text information to the screen"""
        textsurface = self.my_font.render(self.information_text, True, (0, 0, 0))
        self.screen.blit(textsurface, (10, 10))

    def cycle_players(self):
        """Switches to the next player's index"""
        self.next_player_index = (self.next_player_index + 1) % 2

    def game_loop(self):
        """The main game loop"""
        done = False

        # One tick of the main game loop
        while not done:
            for event in pygame.event.get():
                # On the application closed
                if event.type == pygame.QUIT:
                    done = True

                # On user clicked the screen
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    for x in range(0, self.size[0]):
                        for y in range(0, self.size[1]):

                            # If user clicked a tile
                            tile = self.board.tiles[x][y]
                            if tile.was_hit(mouse_pos):

                                # Played returns a number if the game has ended
                                played = self.board.play(position=(x, y), player_id=self.next_player_index)
                                if played is not None:
                                    if played == 0 or played == 1:
                                        self.information_text = "Player ID {0} won!".format(played)
                                    elif played == 2:
                                        self.information_text = "The game has ended with draw."
                                self.cycle_players()

            self.draw_board()
            self.draw_lines()
            self.draw_text()
            pygame.display.flip()
