extends Node

@onready var client: SocketIO = GameState.socket
var is_ready: bool = false
var pending_lobby_name: String = ""

signal lobby_refresh_received(data)
signal lobby_created(data)
signal game_started()
signal get_lobby_received(data)
signal lobby_closed()
signal socket_ready()

func _ready() -> void:
	print("SocketIOLobby _ready")
	client.event_received.connect(_on_event_received)
	client.socket_connected.connect(_on_connected)
	client.namespace_connected.connect(_on_namespace_connected)

func _on_namespace_connected(ns: String) -> void:
	print("Namespace connected: ", ns)

func connect_to_server(token: String) -> void:
	print("connect_to_server called, state=", client.state)
	if client.state == client.State.CONNECTED:
		print("Already connected, refreshing directly")
		is_ready = true
		emit_signal("socket_ready")
		#refresh()
		return
	client.connect_socket({ "token": token })

func _on_connected(ns: String) -> void:
	print("Socket connected!", ns)
	is_ready = true

	if pending_lobby_name != "":
		create_lobby(pending_lobby_name)
		pending_lobby_name = ""

	emit_signal("socket_ready")

func refresh() -> void:
	client.emit("lobby-management:refresh")

func create_lobby(lobby_name: String) -> void:
	if not is_ready:
		pending_lobby_name = lobby_name
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

func _exit_tree() -> void:
	client.event_received.disconnect(_on_event_received)
	client.socket_connected.disconnect(_on_connected)
	if client.namespace_connected.is_connected(_on_namespace_connected):
		client.namespace_connected.disconnect(_on_namespace_connected)

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("Event received: ", event, " data: ", data)
	match event:
		"lobby-management:refresh":
			emit_signal("lobby_refresh_received", data)
		"lobby-management:create-lobby":
			emit_signal("lobby_created", data)
		"lobby-management:game-started":
			emit_signal("game_started")
		"lobby-management:get-lobby":
			emit_signal("get_lobby_received", data)
		"lobby-management:lobby-closed":
			emit_signal("lobby_closed")
