extends Node

@onready var client: SocketIO = $SocketIO
var is_ready: bool = false

signal lobby_refresh_received(data)
signal lobby_created(data)
signal game_started()
signal get_lobby_received(data)

func _ready() -> void:
	print("SocketIOLobby _ready")
	client.event_received.connect(_on_event_received)
	client.socket_connected.connect(_on_connected)
	client.namespace_connected.connect(_on_namespace_connected)

func _on_namespace_connected(ns: String) -> void:
	print("Namespace connected: ", ns)

func connect_to_server(token: String) -> void:
	print("connect_to_server callded with token: ", token)
	client.connect_socket({ "token": token })

func _on_connected(ns: String) -> void:
	print("Socket connected!", ns)
	is_ready = true
	refresh()

func refresh() -> void:
	client.emit("lobby-management:refresh")

func create_lobby(lobby_name: String) -> void:
	if not is_ready:
		push_error("Socket not ready yet!")
		return
	client.emit("lobby-management:create-lobby", { "lobby_name": lobby_name })

func join_lobby(lobby_name: String) -> void:
	client.emit("lobby-management:join-lobby", { "lobby_name": lobby_name })

func get_lobby() -> void:
	client.emit("lobby-management:get-lobby")

func start_game() -> void:
	client.emit("lobby-management:start-game")

func disconnect_from_server() -> void:
	client.disconnect_socket()
	is_ready = false

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("Event received: ", event, " data: ", data)
	if event == "lobby-management:refresh":
		emit_signal("lobby_refresh_received", data)
	elif event == "lobby-management:create-lobby":
		emit_signal("lobby_created", data)
	elif event == "lobby-management:game-started":
		emit_signal("game_started")
	elif event == "lobby-management:get-lobby":
		emit_signal("get_lobby_received", data)
