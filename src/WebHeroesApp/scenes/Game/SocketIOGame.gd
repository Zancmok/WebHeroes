# SocketIOGame.gd
extends Node

@onready var client: SocketIO = GameState.socket
var is_ready: bool = false

signal get_game_data_received(data)
signal end_turn_received(data)
signal build_received(data)
signal socket_ready()

func _ready() -> void:
	print("[SocketIOGame] _ready")
	client.event_received.connect(_on_event_received)
	client.socket_connected.connect(_on_connected)  # fixed

	print("[SocketIOGame] client node: ", client)
	print("[SocketIOGame] event_received connected: ", client.event_received.get_connections())

func connect_to_server(token: String) -> void:
	print("[SocketIOGame] connect_to_server, state=", client.state)
	if client.state == client.State.CONNECTED:
		print("[SocketIOGame] Already connected, requesting game data")
		is_ready = true
		client.emit("lobby-management:join-lobby", { "lobby_name": GameState.lobby_name })
		_request_game_data()
		emit_signal("socket_ready")
		return
	client.connect_socket({ "token": token })

func _on_connected(_ns: String) -> void:
	print("[SocketIOGame] Socket connected")
	is_ready = true
	client.emit("lobby-management:join-lobby", { "lobby_name": GameState.lobby_name })
	_request_game_data()
	emit_signal("socket_ready")

func _request_game_data() -> void:
	print("[SocketIOGame] Requesting game data NOW")
	client.emit("game-management:get-game-data")

func emit_end_turn() -> void:
	client.emit("game-management:end-turn", {})

func emit_build(recipe_id: String, location: Array) -> void:
	client.emit("game-management:build", { "recipe_id": recipe_id, "location": location })

func _exit_tree() -> void:
	client.event_received.disconnect(_on_event_received)
	client.socket_connected.disconnect(_on_connected)

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("[SocketIOGame] Event: ", event, " data: ", data)
	print("[SocketIOGame] RAW event: '", event, "'")
	match event:
		"game-management:get-game-data":
			emit_signal("get_game_data_received", data)
		"game-management:end-turn":
			emit_signal("end_turn_received", data)
		"game-management:build":
			emit_signal("build_received", data)
