extends Node

@onready var client: SocketIO = $SocketIO

signal lobby_refresh_received(data)
signal lobby_created(data)
signal game_started()

func _ready() -> void:
	client.event_received.connect(_on_event_received)
	client.socket_connected.connect(_on_connected)

func connect_to_server(token: String) -> void:
	client.connect_socket({ "token": token })

func _on_connected() -> void:
	print("Socket connected!")
	refresh()

func refresh() -> void:
	client.emit("lobby-management:refresh")

func create_lobby(lobby_name: String) -> void:
	client.emit("lobby-management:create-lobby", { "lobby_name": lobby_name })

func join_lobby(lobby_name: String) -> void:
	client.emit("lobby-management:join-lobby", { "lobby_name": lobby_name })

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("Event received: ", event, " data: ", data)
	if event == "lobby-management:refresh":
		emit_signal("lobby_refresh_received", data)
	elif event == "lobby-management:create-lobby":
		emit_signal("lobby_created", data)
	elif event == "lobby-management:game-started":
		emit_signal("game_started")
