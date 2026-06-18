## SocketIOGame.gd
extends Node

@onready var client: SocketIO = GameState.socket

var players: Array = []
var current_user_index: int = 0
var my_index: int = -1
var recipes: Array = []
var my_resources: Dictionary = {}
var is_ready: bool = false
var _requested_once := false

signal socket_ready()
signal get_game_data_received(data: Dictionary)
signal end_turn_received(data: Dictionary)
signal build_received(data: Dictionary)
signal game_over_received(data: Dictionary)
signal socket_status(message: String)

func _ready() -> void:
	print("[SocketIOGame] _ready")
	if client == null:
		push_error("GameState.socket is null")
		return
	if not client.event_received.is_connected(_on_event_received):
		client.event_received.connect(_on_event_received)
	if not client.socket_connected.is_connected(_on_connected):
		client.socket_connected.connect(_on_connected)

func _exit_tree() -> void:
	if client == null:
		return
	if client.event_received.is_connected(_on_event_received):
		client.event_received.disconnect(_on_event_received)
	if client.socket_connected.is_connected(_on_connected):
		client.socket_connected.disconnect(_on_connected)

func connect_to_server(token: String) -> void:
	emit_signal("socket_status", "Connecting…")
	_requested_once = false
	if client.state == client.State.CONNECTED:
		_on_connected("/")
		return
	client.connect_socket({"token": token})

func _on_connected(_ns: String) -> void:
	print("[SocketIOGame] Connected")
	is_ready = true
	emit_signal("socket_ready")
	_join_lobby_then_request_game_data()

func _join_lobby_then_request_game_data() -> void:
	# Same as web game.js: re-join the remembered lobby, then ask for data.
	var lobby_name := str(GameState.lobby_name).strip_edges()
	if lobby_name != "":
		emit_signal("socket_status", "Joining lobby %s…" % lobby_name)
		client.emit("lobby-management:join-lobby", {"lobby_name": lobby_name})
		await get_tree().create_timer(0.25).timeout
	_request_game_data()

func _request_game_data() -> void:
	if _requested_once:
		# Still allow explicit refreshes, but do not spam on duplicate connected events.
		pass
	_requested_once = true
	emit_signal("socket_status", "Requesting game data…")
	client.emit("game-management:get-game-data")

func refresh_game_data() -> void:
	_requested_once = false
	_join_lobby_then_request_game_data()

func emit_end_turn() -> void:
	# The Flask-SocketIO handler takes no payload. Sending {} can make the
	# Python handler receive an unexpected argument, so match the web client.
	emit_signal("socket_status", "Ending turn…")
	client.emit("game-management:end-turn")

func emit_build(recipe_id: String, location: Array) -> void:
	emit_signal("socket_status", "Sending build…")
	client.emit("game-management:build", {"recipe_id": recipe_id, "location": location})

func _on_event_received(event: String, data: Variant, _ns: String) -> void:
	print("[SocketIOGame] event=", event)
	match event:
		"lobby-management:join-lobby":
			emit_signal("socket_status", "Lobby joined. Waiting for game state…")
		"game-management:get-game-data":
			_handle_get_game_data(_unwrap(data))
		"game-management:end-turn":
			_handle_end_turn(_unwrap(data))
		"game-management:build":
			_handle_build(_unwrap(data))
		"game-management:game-over":
			_handle_game_over(_unwrap(data))

func _handle_get_game_data(data: Dictionary) -> void:
	my_index = int(data.get("my_index", -1))
	current_user_index = int(data.get("current_user_index", 0))
	players = data.get("players", [])

	recipes = []
	for p in data.get("prototypes", []):
		var pd: Dictionary = p if p is Dictionary else {}
		if pd.get("object_type", "") == "recipe-s_prototype":
			recipes.append(pd)

	if my_index >= 0 and my_index < players.size():
		my_resources = (players[my_index] as Dictionary).get("resources", {})
	else:
		my_resources = {}

	emit_signal("socket_status", "")
	emit_signal("get_game_data_received", data)

func _handle_end_turn(data: Dictionary) -> void:
	var old_resources: Array = []
	for p in players:
		old_resources.append((p as Dictionary).get("resources", {}).duplicate())

	current_user_index = int(data.get("next_user_index", current_user_index))
	players = data.get("players", players)

	if my_index >= 0 and my_index < players.size():
		my_resources = (players[my_index] as Dictionary).get("resources", {})

	var gains: Dictionary = {}
	for i in players.size():
		var p: Dictionary = players[i]
		var old: Dictionary = old_resources[i] if i < old_resources.size() else {}
		var player_gains: Dictionary = {}
		for res in p.get("resources", {}):
			var delta := int(p["resources"][res]) - int(old.get(res, 0))
			if delta > 0:
				player_gains[res] = delta
		if not player_gains.is_empty():
			gains[str(i)] = player_gains

	var out := data.duplicate(true)
	out["gains"] = gains
	out["my_resources"] = my_resources
	emit_signal("end_turn_received", out)

func _handle_build(data: Dictionary) -> void:
	var player_data: Dictionary = data.get("player", {})
	var color_name := str(player_data.get("color_type", {}).get("name", ""))
	for i in players.size():
		var p: Dictionary = players[i]
		if str(p.get("color_type", {}).get("name", "")) == color_name:
			players[i] = player_data
			if i == my_index:
				my_resources = player_data.get("resources", my_resources)
			break
	emit_signal("build_received", data)

func _handle_game_over(data: Dictionary) -> void:
	emit_signal("game_over_received", data)

static func _unwrap(data: Variant) -> Dictionary:
	if data is Array and (data as Array).size() > 0:
		var first = (data as Array)[0]
		if first is Dictionary:
			return first as Dictionary
	if data is Dictionary:
		return data as Dictionary
	return {}
