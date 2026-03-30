extends Camera2D

const ZOOM_MIN = Vector2(0.3, 0.3)
const ZOOM_MAX = Vector2(2.0, 2.0)
const ZOOM_STEP = 0.1
const PAN_SPEED = 800.0

var _dragging: bool = false
var _drag_start: Vector2 = Vector2.ZERO
var _cam_start: Vector2 = Vector2.ZERO

var map_min: Vector2 = Vector2.ZERO
var map_max: Vector2 = Vector2.ZERO

func set_map_bounds(min_pos: Vector2, max_pos: Vector2) -> void:
	map_min = min_pos
	map_max = max_pos
	_clamp_position()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton:
		if event.button_index == MOUSE_BUTTON_WHEEL_UP:
			zoom = (zoom + Vector2(ZOOM_STEP, ZOOM_STEP)).clamp(ZOOM_MIN, ZOOM_MAX)
			_clamp_position()
		elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
			zoom = (zoom - Vector2(ZOOM_STEP, ZOOM_STEP)).clamp(ZOOM_MIN, ZOOM_MAX)
			_clamp_position()
		elif event.button_index == MOUSE_BUTTON_MIDDLE:
			_dragging = event.pressed
			if _dragging:
				_drag_start = event.position
				_cam_start = position

	elif event is InputEventMouseMotion and _dragging:
		position = _cam_start - (event.position - _drag_start) / zoom
		_clamp_position()

func _clamp_position() -> void:
	if map_min == map_max:
		return
	var viewport_half = get_viewport_rect().size / 2.0 / zoom
	var min_cam = map_min + viewport_half
	var max_cam = map_max - viewport_half
	# If map is smaller than viewport, just center it
	if min_cam.x > max_cam.x:
		position.x = (map_min.x + map_max.x) / 2.0
	else:
		position.x = clamp(position.x, min_cam.x, max_cam.x)
	if min_cam.y > max_cam.y:
		position.y = (map_min.y + map_max.y) / 2.0
	else:
		position.y = clamp(position.y, min_cam.y, max_cam.y)
