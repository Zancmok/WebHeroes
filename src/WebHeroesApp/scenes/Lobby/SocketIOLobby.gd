extends Node

@onready var client: SocketIO = $SocketIO

signal lobby_refresh_received(data)
signal lobby_created(data)

func _ready() -> void:
    client.event_received.connect(_on_event_received)
    client.socket_connected.connect(_on_connected)

func connect_to_server(token: String) -> void:
    client.auth = { "token": token }
    client.connect_socket()

func _on_connected() -> void:
    print("Socket connected!")
    refresh()

func refresh() -> void:
    client.emit("lobby-management:refresh")

func create_lobby(lobby_name: String) -> void:
    client.emit("lobby-management:create-lobby", { "lobby_name": lobby_name })

func join_lobby(lobby_name: String) -> void:
    client.emit("lobby-management:join-lobby", { "lobby_name": lobby_name })

func _on_event_received(event: String, data: Variant, ns: String) -> void:
    print("Event received: ", event, " data: ", data)
    if event == "lobby-management:refresh":
        emit_signal("lobby_refresh_received", data)
    elif event == "lobby-management:create-lobby":
        emit_signal("lobby_created", data)
```

**Step 2** — in your `Lobby.tscn`, add two child nodes under the root: a `Node` with `SocketIOLobby.gd` attached, and under that a `Node` with the SocketIO addon script (`res://addons/godot-socketio/socketio.gd`) with `autoconnect = false` and `base_url = "https://localhost"`.

The scene tree should look like:
```
lobby (Control)
├── ... (your existing UI nodes)
└── SocketIOLobby (Node) ← SocketIOLobby.gd
    └── SocketIO (Node)  ← addons/godot-socketio/socketio.gd