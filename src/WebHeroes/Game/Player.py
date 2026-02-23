from Prototype import PlayerColorType


class Player:
    def __init__(self, color_type: PlayerColorType) -> None:
        self.color_type: PlayerColorType = color_type
