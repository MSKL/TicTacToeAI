from Game.Tile import Tile


class Board:
    def __init__(self, size, square_size):
        """Initialise a tile and create rectangles"""
        self.size = size

        # Initialise the tile array
        self.tiles = [size[0] * [None] for i in range(size[1])]

        # Todo: check the weird indexing
        for x in range(0, size[0]):
            for y in range(0, size[1]):
                self.tiles[x][y] = Tile((x, y), square_size, (0, 0))

    def tile_at_pos(self, position):
        """Get a tile at given position"""
        return self.tiles[position[0]][position[1]]

    def tile_in_bounds(self, position):
        """Check if the given position if in board bounds"""
        if 0 <= position[0] < self.size[0]:
            if 0 <= position[1] < self.size[1]:
                return True
        return False
