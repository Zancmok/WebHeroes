from typing import Optional
from Game.Field import Field
from flask import Blueprint
import WebHeroes.config as config
from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby
from WebHeroes.Responses.DataModels.FieldModel import FieldModel
from WebHeroes.Responses.DataModels.MapModel import MapModel
from WebHeroes.Responses.ResponseTypes.GetGameDataResponse import GetGameDataResponse
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.UserManagement.UserSession import UserSession
from ZancmokLib.StaticClass import StaticClass
from ZancmokLib.SocketBlueprint import SocketBlueprint
from WebHeroes.Responses import dictify


class GameManagement(StaticClass):
    route_blueprint: Blueprint = Blueprint(
        name="WebAPI:GameManagement",
        import_name=__name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH,
        url_prefix="/game-management"
    )

    socket_blueprint: SocketBlueprint = SocketBlueprint(name="game-management")

    @staticmethod
    @socket_blueprint.on("get-game-data")
    def get_game_data() -> None:
        user_session: Optional[UserSession] = SessionManager.get_user_session()
        if not user_session:
            return
        user_session: UserSession

        # TODO: Write this thingy bettah
        lobby: OwnedLobby = user_session.get_lobby()

        fields: dict[str, FieldModel] = {}
        for cords in lobby.game.game_map.fields:
            curr: Field = lobby.game.game_map.fields[cords]

            fields[f"{cords[0]}\0{cords[1]}"] = FieldModel(
                field_type=curr.field_type.name,
                sprite=curr.field_type.sprite,
                resource=curr.field_type.resource.name if curr.field_type.resource else None,
                assigned_number=curr.assigned_number
            )

        GameManagement.socket_blueprint.emit("get-game-data", dictify(GetGameDataResponse(
            map=MapModel(
                fields=fields
            )
        )))
