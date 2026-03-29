extends Node

@onready var client: SocketIO = $SocketIO
var is_ready: bool = false

signal get_game_data_received(data)
signal socket_ready()
signal 


func _ready() -> void:
    print("SocketIOGame _ready")
    client.event_received.connect(_on_event_received)
    client.event_received.connect(_on_connected)

func connect_to_server(token: String) -> void:
    print("connect_to_server callde, state = ", client.state)
    if client.state == client.State.CONNECTED:
        print("Already connected, refreshing directly")
        is_ready = true
        return
    client.connect_socket({ "token": token })

func _on_connected(_ns: String) -> void:
    print("Socket connected!", _ns)
    is_ready = true
    emit_signal("socket_ready")



func _on_event_received(event: String, data: Variant, _ns: String) -> void:
    print("Event received: ", event, "data: ", data)
    if event == "game-management:get-game-data":
        emit_signal("get_game_data_received", data)