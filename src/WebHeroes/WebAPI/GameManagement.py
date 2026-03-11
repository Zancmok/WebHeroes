from typing import Optional
from os import path
from Game.Field import Field
from flask import Blueprint, Response, send_file
import WebHeroes.config as config
from WebHeroes.LobbyManagement.OwnedLobby import OwnedLobby
from WebHeroes.Responses.DataModels.FieldModel import FieldModel
from WebHeroes.Responses.DataModels.FieldTypeModel import FieldTypeModel
from WebHeroes.Responses.DataModels.MapModel import MapModel
from WebHeroes.Responses.DataModels.ResourceTypeModel import ResourceTypeModel
from WebHeroes.Responses.ResponseTypes.GetGameDataResponse import GetGameDataResponse
from WebHeroes.UserManagement.SessionManager import SessionManager
from WebHeroes.UserManagement.UserSession import UserSession
from ZancmokLib.EHTTPMethod import EHTTPMethod
from ZancmokLib.EHTTPCode import EHTTPCode
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
    @route_blueprint.route("/img/<string:mod_id>/<path:image_id>", methods=[EHTTPMethod.GET])
    def get_img(mod_id: str, image_id: str) -> str | Response:
        file_path: str = path.join(path.dirname(__file__), "..", "BaseMods", mod_id, image_id)

        if not path.isfile(file_path):
            return Response("Image not found", status=EHTTPCode.NOT_FOUND)

        return send_file(file_path)

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
                field_type=FieldTypeModel(
                    name=curr.field_type.name,
                    display_name=curr.field_type.display_name,
                    sprite=curr.field_type.sprite,
                    weight=curr.field_type.weight,
                    minimum_amount=curr.field_type.minimum_amount,
                    resource=ResourceTypeModel(
                        name=curr.field_type.resource.name,
                        display_name=curr.field_type.resource.display_name
                    ) if curr.field_type.resource else None
                ),
                q=curr.q,
                r=curr.r,
                assigned_number=curr.assigned_number
            )

        GameManagement.socket_blueprint.emit("get-game-data", dictify(GetGameDataResponse(
            map=MapModel(
                fields=fields
            )
        )))
