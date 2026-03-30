# SocketIOGame.gd
extends Node

@onready var client: SocketIO = $SocketIO
var is_ready: bool = false

signal get_game_data_received(data)
signal end_turn_received(data)
signal build_received(data)
signal socket_ready()

func _ready() -> void:
	print("[SocketIOGame] _ready")
	client.event_received.connect(_on_event_received)
	client.socket_connected.connect(_on_connected)  # fixed

func connect_to_server(token: String) -> void:
	print("[SocketIOGame] connect_to_server, state=", client.state)
	if client.state == client.State.CONNECTED:
		is_ready = true
		_request_game_data()
		return
	client.connect_socket({ "token": token })

func _on_connected(_ns: String) -> void:
	print("[SocketIOGame] Socket connected")
	is_ready = true
	# Rejoin the lobby room first, then ask for game data
	var lobby_name = GameState.lobby_name
	client.emit("lobby-management:join-lobby", { "lobby_name": lobby_name })
	emit_signal("socket_ready")

func _request_game_data() -> void:
	client.emit("game-management:get-game-data")

func emit_end_turn() -> void:
	client.emit("game-management:end-turn")

func emit_build(recipe_id: String, location: Array) -> void:
	client.emit("game-management:build", { "recipe_id": recipe_id, "location": location })

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("[SocketIOGame] Event: ", event, " data: ", data)
	match event:
		"lobby-management:join-lobby":
			_request_game_data()
		"game-management:get-game-data":
			emit_signal("get_game_data_received", data)
		"game-management:end-turn":
			emit_signal("end_turn_received", data)
		"game-management:build":
			emit_signal("build_received", data)
