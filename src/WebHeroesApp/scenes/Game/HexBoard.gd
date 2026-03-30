extends Node2D

const HEX_SIZE = 48.0

const FIELD_COLORS = {
	"forest":      Color(0.176, 0.353, 0.106),
	"hill":        Color(0.545, 0.227, 0.059),
	"pasture":     Color(0.494, 0.784, 0.314),
	"field":       Color(0.831, 0.722, 0.290),
	"mountain":    Color(0.420, 0.420, 0.420),
	"desert":      Color(0.788, 0.690, 0.478),
	"outer-bound": Color(0.102, 0.227, 0.361),
	"outer_bound": Color(0.102, 0.227, 0.361),
}

const HOT_NUMBERS = [6, 8]

var fields: Dictionary = {}
var settlements: Dictionary = {}
var roads: Dictionary = {}

var _placement_type: String = ""  # "road" or "settlement", empty = no placement
var _placement_targets: Array = []  # Array of {location: Array, points: PackedVector2Array}

signal placement_selected(location: Array)

func load_game_data(data: Dictionary) -> void:
	fields.clear()
	settlements.clear()
	roads.clear()

	for key in data.get("fields", {}):
		var parts = key.split("\u0000")
		if parts.size() != 2:
			continue
		var q = int(parts[0])
		var r = int(parts[1])
		fields["%d,%d" % [q, r]] = data["fields"][key]

	for key in data.get("settlements", {}):
		settlements[key] = data["settlements"][key]

	for key in data.get("roads", {}):
		roads[key] = data["roads"][key]

	queue_redraw()

func hex_to_pixel(q: int, r: int) -> Vector2:
	var x = HEX_SIZE * (sqrt(3.0) * q + sqrt(3.0) / 2.0 * r)
	var y = HEX_SIZE * (3.0 / 2.0 * r)
	return Vector2(x, y)

func hex_corner_points(center: Vector2, size: float) -> PackedVector2Array:
	var pts = PackedVector2Array()
	for i in range(6):
		var angle = deg_to_rad(60.0 * i + 30.0)
		pts.append(center + Vector2(cos(angle), sin(angle)) * size)
	return pts

func enter_placement_mode(type: String) -> void:
	_placement_type = type
	_build_placement_targets()
	queue_redraw()

func exit_placement_mode() -> void:
	_placement_type = ""
	_placement_targets.clear()
	queue_redraw()

func _build_placement_targets() -> void:
	_placement_targets.clear()

	var inner_fields: Array = []
	for key in fields:
		var type_name: String = fields[key].get("field_type", {}).get("name", "")
		if not ("outer" in type_name):
			inner_fields.append(key)

	if _placement_type == "road":
		var drawn: Dictionary = {}
		var directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]
		for key in inner_fields:
			var parts = key.split(",")
			var q = int(parts[0])
			var r = int(parts[1])
			for dir in directions:
				var nq = q + dir[0]
				var nr = r + dir[1]
				var nkey = "%d,%d" % [nq, nr]
				if not fields.has(nkey):
					continue
				var n_type: String = fields[nkey].get("field_type", {}).get("name", "")
				if "outer" in n_type:
					continue
				var edge_key = _sorted_edge_key(q, r, nq, nr)
				if drawn.has(edge_key):
					continue
				drawn[edge_key] = true
				var corners = _shared_edge_corners(q, r, nq, nr)
				if corners.size() < 2:
					continue
				_placement_targets.append({
					"location": [q, r, nq, nr],
					"points": PackedVector2Array([corners[0], corners[1]])
				})

	elif _placement_type == "settlement":
		var drawn: Dictionary = {}
		var directions = [[1,0],[1,-1],[0,-1],[-1,0],[-1,1],[0,1]]
		for key in inner_fields:
			var parts = key.split(",")
			var q = int(parts[0])
			var r = int(parts[1])
			for i in range(6):
				var d1 = directions[i]
				var d2 = directions[(i + 1) % 6]
				var n1q = q + d1[0]; var n1r = r + d1[1]
				var n2q = q + d2[0]; var n2r = r + d2[1]
				if not fields.has("%d,%d" % [n1q, n1r]) or not fields.has("%d,%d" % [n2q, n2r]):
					continue
				var coords = [[q, r], [n1q, n1r], [n2q, n2r]]
				coords.sort()
				var ikey = "%d,%d|%d,%d|%d,%d" % [coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0], coords[2][1]]
				if drawn.has(ikey):
					continue
				drawn[ikey] = true
				var center = (hex_to_pixel(coords[0][0], coords[0][1]) +
							  hex_to_pixel(coords[1][0], coords[1][1]) +
							  hex_to_pixel(coords[2][0], coords[2][1])) / 3.0
				_placement_targets.append({
					"location": [coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0], coords[2][1]],
					"center": center
				})

func _sorted_edge_key(q1: int, r1: int, q2: int, r2: int) -> String:
	if q1 < q2 or (q1 == q2 and r1 < r2):
		return "%d,%d-%d,%d" % [q1, r1, q2, r2]
	return "%d,%d-%d,%d" % [q2, r2, q1, r1]

func _shared_edge_corners(q1: int, r1: int, q2: int, r2: int) -> Array:
	var ca = hex_corner_points(hex_to_pixel(q1, r1), HEX_SIZE)
	var cb = hex_corner_points(hex_to_pixel(q2, r2), HEX_SIZE)
	var shared: Array = []
	const EPS = 0.5
	for pa in ca:
		for pb in cb:
			if pa.distance_to(pb) < EPS:
				shared.append((pa + pb) / 2.0)
	return shared

func _draw() -> void:
	if fields.is_empty():
		return

	for key in fields:
		var parts = key.split(",")
		var q = int(parts[0])
		var r = int(parts[1])
		var field = fields[key]
		var type_name: String = field.get("field_type", {}).get("name", "")
		var center = hex_to_pixel(q, r)
		var pts = hex_corner_points(center, HEX_SIZE - 1.5)

		var color = FIELD_COLORS.get(type_name, Color.GRAY)
		draw_polygon(pts, PackedColorArray([color]))
		draw_polyline(pts + PackedVector2Array([pts[0]]), Color(0, 0, 0, 0.45), 1.5)

		var assigned_number = field.get("assigned_number", null)
		if assigned_number != null and type_name != "outer-bound" and type_name != "outer_bound":
			var num_color = Color(0.878, 0.361, 0.180) if assigned_number in HOT_NUMBERS else Color.BLACK
			draw_circle(center, 16, Color(0.961, 0.918, 0.816))
			draw_string(
				ThemeDB.fallback_font,
				center - Vector2(6, -6),
				str(assigned_number),
				HORIZONTAL_ALIGNMENT_CENTER,
				-1,
				14,
				num_color
			)

	# Draw placement targets on top
	if _placement_type == "road":
		for target in _placement_targets:
			var pts: PackedVector2Array = target["points"]
			draw_line(pts[0], pts[1], Color(1, 1, 0.4, 0.4), 8.0, true)
			draw_line(pts[0], pts[1], Color(1, 1, 0.4, 0.85), 4.0, true)

	elif _placement_type == "settlement":
		for target in _placement_targets:
			var c: Vector2 = target["center"]
			draw_circle(c, 10.0, Color(1, 1, 0.4, 0.4))
			draw_arc(c, 10.0, 0, TAU, 24, Color(1, 1, 0.4, 0.85), 1.5)

func _unhandled_input(event: InputEvent) -> void:
	if _placement_type == "" or _placement_targets.is_empty():
		return

	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		var local_pos = to_local(get_global_mouse_position())

		if _placement_type == "road":
			var best_dist = INF
			var best_target = null
			for target in _placement_targets:
				var pts: PackedVector2Array = target["points"]
				var mid = (pts[0] + pts[1]) / 2.0
				var dist = local_pos.distance_to(mid)
				if dist < best_dist:
					best_dist = dist
					best_target = target
			if best_dist < 20.0 and best_target != null:
				get_viewport().set_input_as_handled()
				emit_signal("placement_selected", best_target["location"])

		elif _placement_type == "settlement":
			var best_dist = INF
			var best_target = null
			for target in _placement_targets:
				var dist = local_pos.distance_to(target["center"])
				if dist < best_dist:
					best_dist = dist
					best_target = target
			if best_dist < 18.0 and best_target != null:
				get_viewport().set_input_as_handled()
				emit_signal("placement_selected", best_target["location"])

func get_board_bounds() -> Array:
	if fields.is_empty():
		return [Vector2.ZERO, Vector2.ZERO]

	var min_x = INF; var min_y = INF
	var max_x = -INF; var max_y = -INF

	for key in fields:
		var parts = key.split(",")
		var pos = hex_to_pixel(int(parts[0]), int(parts[1]))
		min_x = min(min_x, pos.x - HEX_SIZE)
		min_y = min(min_y, pos.y - HEX_SIZE)
		max_x = max(max_x, pos.x + HEX_SIZE)
		max_y = max(max_y, pos.y + HEX_SIZE)

	return [Vector2(min_x, min_y), Vector2(max_x, max_y)]