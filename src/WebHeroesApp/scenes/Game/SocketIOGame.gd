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
	client.socket_connected.connect(_on_connected)
	client.namespace_connected.connect(_on_namespace_connected)

	print("[SocketIOGame] client node: ", client)
	print("[SocketIOGame] event_received connected: ", client.event_received.get_connections())

func _on_namespace_connected(ns: String) -> void:
	print("[SocketIOGame] Namespace connected: ", ns)

func connect_to_server(token: String) -> void:
	print("[SocketIOGame] connect_to_server, state=", client.state)
	if client.state == client.State.CONNECTED:
		print("[SocketIOGame] Connected - forcing fresh reconnect for game session")
		is_ready = true
		client.disconnect_socket()
		await get_tree().create_timer(0.2).timeout
		client.connect_socket({ "token": token })
		return
	print("[SocketIOGame] Not connected — connecting fresh")
	client.connect_socket({ "token": token })

func _on_connected(_ns: String) -> void:
	print("[SocketIOGame] Socket connected", _ns)
	is_ready = true
	_request_game_data()
	emit_signal("socket_ready")

func _request_game_data() -> void:
	print("[SocketIOGame] Requesting game data")
	client.emit("game-management:get-game-data")

func emit_end_turn() -> void:
	client.emit("game-management:end-turn", {})

func emit_build(recipe_id: String, location: Array) -> void:
	client.emit("game-management:build", { "recipe_id": recipe_id, "location": location })

func _exit_tree() -> void:
	if client.event_received.is_connected(_on_event_received):
		client.event_received.disconnect(_on_event_received)
	if client.socket_connected.is_connected(_on_connected):
		client.socket_connected.disconnect(_on_connected)

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("[SocketIOGame] Event received: ", event, " data: ", data)
	match event:
		"game-management:get-game-data":
			print("[SocketIOGame] game data received")
			emit_signal("get_game_data_received", data)
		"game-management:end-turn":
			emit_signal("end_turn_received", data)
		"game-management:build":
			emit_signal("build_received", data)
