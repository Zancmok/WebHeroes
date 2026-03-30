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

var fields: Dictionary = {}   # "q,r" -> field data
var settlements: Dictionary = {}
var roads: Dictionary = {}

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
