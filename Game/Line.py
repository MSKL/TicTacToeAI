class Line:
    """Represents a line on the tictactoe board"""

    def __init__(self, start, end, score):
        """
        :type start: np.array
        :type end: np.array
        :type score: int
        """
        self.start = start
        self.end = end
        self.score = score

    def __eq__(self, other):
        return self.start == other.start and self.end == other.end and self.score == other.score

    def __gt__(self, other):
        return self.score > other.score
