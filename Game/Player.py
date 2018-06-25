class Player:
    def __init__(self, color, name="unknown"):
        self.color = color
        self.name = name

    def __str__(self):
        return "\"{0}\" - {1}".format(self.name, self.color)

    def __repr__(self):
        return str(self)