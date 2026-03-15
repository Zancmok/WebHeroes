from Prototype import PlayerColor


class Player:
    def __init__(self, color_type: PlayerColor) -> None:
        self.color_type: PlayerColor = color_type
