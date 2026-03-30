import random
from typing import Optional
from WebHeroes.UserManagement.UserSession import UserSession
from WebHeroes.UserManagement.SessionManager import SessionManager
from LuaBridge import LuaSandbox, BasePrototype
from Prototype import prototype_definitions, FieldPrototype, SettingsPrototype, Recipe, PlayerColor, ResourcePrototype
from .Map import Map
from .Player import Player
from .Field import Field
from .Settlement import Settlement


class Game:
    def __init__(self, member_ids: set[int]) -> None:
        self.lua_sandbox: LuaSandbox = LuaSandbox(
            mod_paths=["core", "base"],  # "til-mod"
            prototypes=prototype_definitions
        )

        self.running: bool = False
        self.game_map: Optional[Map] = None
        self.member_ids: set[int] = member_ids
        self.users: list[UserSession] = []
        self.players: dict[UserSession, Player] = {}
        self.recipes: list[Recipe] = []
        self.current_user_index: int = 0
        self.prototypes: list[BasePrototype] = []

    def run(self) -> None:
        if self.running:
            raise Exception("Game already running!")

        self.running = True

        self.prototypes = self.lua_sandbox.run()

        settings: Optional[SettingsPrototype] = None

        fields: list[FieldPrototype] = []
        player_colors: list[PlayerColor] = []
        resources: list[ResourcePrototype] = []
        for prototype in self.prototypes:
            if isinstance(prototype, SettingsPrototype):
                settings = prototype

            if isinstance(prototype, FieldPrototype):
                fields.append(prototype)

            if isinstance(prototype, Recipe):
                self.recipes.append(prototype)

            if isinstance(prototype, PlayerColor):
                player_colors.append(prototype)

            if isinstance(prototype, ResourcePrototype):
                resources.append(prototype)

        self.game_map = Map(fields, settings)

        for i, member_id in enumerate(self.member_ids):
            user: UserSession = SessionManager.get_user_session_by_user_id(member_id)

            self.users.append(user)
            self.players[user] = Player(player_colors[i], resources)

    def end_turn(self, rolled_number: int) -> None:
        # Grant standard resources
        for intersection in self.game_map.intersections:
            settlement: Settlement = self.game_map.intersections[intersection].settlement
            if not settlement:
                continue

            for field_cords in intersection:
                field: Field = self.game_map.fields[field_cords]

                if field.assigned_number != rolled_number:
                    continue

                settlement.owner.resources[field.field_type.resource] += settlement.settlement_type.resource_multiplier

        # Special rare case bonus resource give
        if rolled_number in (2, 12):
            for user_session in self.players:
                player: Player = self.players[user_session]

                random_free_resource: str = random.choice(list(player.resources.keys()))

                player.resources[random_free_resource] += 1

        # Pass the turn to the next player
        self.current_user_index += 1
        self.current_user_index %= len(self.users)
