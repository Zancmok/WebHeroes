from Game.Player import Player
from Prototype import RoadPrototype


class Road:
    def __init__(self, road_type: RoadPrototype, owner: Player) -> None:
        self.road_type: RoadPrototype = road_type
        self.owner: Player = owner
