extends Node

var token: String = ""
var username: String = ""
var lobby_name: String = ""
var socket: SocketIO = null

func _notification(what: int) -> void:
	if what == NOTIFICATION_WM_CLOSE_REQUEST:
		_logout_and_quit()

func _logout_and_quit() -> void:
	if token == "":
		get_tree().quit()
		return

	var http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(func(_r, _c, _h, _b): get_tree().quit())

	var headers = ["Content-Type: application/json"]
	var body = JSON.stringify({ "token": token })
	var err = http.request(
		"https://webheroes.duckdns.org:9027/user-management/logout",
		headers,
		HTTPClient.METHOD_POST,
		body
	)

	if err != OK:
		get_tree().quit()

func _ready() -> void:
	socket = SocketIO.new()
	socket.base_url = "https://webheroes.duckdns.org:9027"
	add_child(socket)
