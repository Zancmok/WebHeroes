extends Node

@onready var client: SocketIO = $SocketIO
var is_ready: bool = false
var pending_lobby_name: String = ""
var _pending_debug_start: bool = false  # NEW
var _waiting_to_start: bool = false

signal lobby_refresh_received(data)
signal lobby_created(data)
signal game_started()
signal get_lobby_received(data)
signal lobby_closed()
signal socket_ready()
signal debug_game_ready()  # NEW

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
		refresh()
		return
	client.connect_socket({ "token": token })

func _on_connected(ns: String) -> void:
	print("Socket connected!", ns)
	is_ready = true
	
	var saved_lobby = GameState.lobby_name
	if saved_lobby != "":
		join_lobby(saved_lobby)

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

# NEW: creates lobby then immediately starts the game
func debug_create_and_start(lobby_name: String) -> void:
	_pending_debug_start = true
	create_lobby(lobby_name)

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("Event received: ", event, " data: ", data)
	if event == "lobby-management:refresh":
		emit_signal("lobby_refresh_received", data)
	elif event == "lobby-management:create-lobby":
		emit_signal("lobby_created", data)
		if _pending_debug_start:
			_pending_debug_start = false
			var response = data
			if response is Array and response.size() > 0:
				response = response[0]
			if response is Dictionary and response.get("object_type") == "failed-response":
				# Lobby already exists — join it first, then start on join confirmation
				_waiting_to_start = true
				var lobby_name = GameState.lobby_name
				client.emit("lobby-management:join-lobby", { "lobby_name": lobby_name })
			else:
				# Lobby created fresh — start immediately
				client.emit("lobby-management:start-game")
	elif event == "lobby-management:join-lobby":
		if _waiting_to_start:
			_waiting_to_start = false
			client.emit("lobby-management:start-game")
	elif event == "lobby-management:game-started":
		emit_signal("game_started")
		emit_signal("debug_game_ready")
	elif event == "lobby-management:get-lobby":
		emit_signal("get_lobby_received", data)
	elif event == "lobby-management:lobby-closed":
		emit_signal("lobby_closed")
