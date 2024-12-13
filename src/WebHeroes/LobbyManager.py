from flask import jsonify, session, Response
from WebHeroes.RouteManager import RouteManager


class LobbyManager:
    @staticmethod
    @RouteManager.route("/get-basic-user-data/", methods=['GET'])
    def get_basic_user_data() -> Response:
        if not session['access_token']:
            return jsonify({})

        return jsonify(
            {
                'username': session['username'],
                'avatar_url': session['avatar_url']
            }
        )
