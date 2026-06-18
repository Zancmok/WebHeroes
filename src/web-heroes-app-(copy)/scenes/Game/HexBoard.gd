extends Node2D

# ── Constants ────────────────────────────────────────────────────────────────
const HEX_SIZE := 48.0

const HOT_NUMBERS: Array = [6, 8]

# Colours only — avoids the Variant-indexing problem with a nested Dictionary const
const FIELD_FILL: Dictionary = {
	"forest":      Color(0.176, 0.353, 0.106),
	"hill":        Color(0.545, 0.227, 0.059),
	"pasture":     Color(0.494, 0.784, 0.314),
	"field":       Color(0.831, 0.722, 0.290),
	"mountain":    Color(0.420, 0.420, 0.420),
	"desert":      Color(0.788, 0.690, 0.478),
	"outer-bound": Color(0.102, 0.227, 0.361),
	"outer_bound": Color(0.102, 0.227, 0.361),
}

# ── State ────────────────────────────────────────────────────────────────────
var _fields: Dictionary = {}
var _placed_buildings: Array = []

var _placement_mode: String = ""
var _placement_recipe_id: String = ""
var _placement_result: Dictionary = {}
var _current_player: Dictionary = {}
var _placement_targets: Array = []

var _show_numbers: bool = true
var _show_outer:   bool = true

signal placement_selected(recipe_id: String, location: Array)

# ── Hex math ──────────────────────────────────────────────────────────────────
static func hex_to_pixel(q: int, r: int) -> Vector2:
	return Vector2(
		HEX_SIZE * (sqrt(3.0) * q + sqrt(3.0) / 2.0 * r),
		HEX_SIZE * (3.0 / 2.0 * r)
	)

static func hex_corner_points(center: Vector2, size: float) -> PackedVector2Array:
	var pts := PackedVector2Array()
	for i in 6:
		var angle := deg_to_rad(60.0 * i + 30.0)
		pts.append(center + Vector2(cos(angle), sin(angle)) * size)
	return pts

static func shared_edge_corners(q1: int, r1: int, q2: int, r2: int) -> Array:
	var ca := hex_corner_points(hex_to_pixel(q1, r1), HEX_SIZE)
	var cb := hex_corner_points(hex_to_pixel(q2, r2), HEX_SIZE)
	var result: Array[Vector2] = []
	const EPS := 0.5
	for pa: Vector2 in ca:
		for pb: Vector2 in cb:
			if pa.distance_to(pb) < EPS:
				result.append((pa + pb) / 2.0)
	return result

static func intersection_point(q1: int, r1: int, q2: int, r2: int, q3: int, r3: int) -> Vector2:
	return (hex_to_pixel(q1, r1) + hex_to_pixel(q2, r2) + hex_to_pixel(q3, r3)) / 3.0

static func player_color(player: Dictionary) -> Color:
	var c: Dictionary = player.get("color_type", {})
	if c.is_empty():
		return Color.WHITE
	return Color(float(c.get("r", 255)) / 255.0,
				 float(c.get("g", 255)) / 255.0,
				 float(c.get("b", 255)) / 255.0)

static func sorted_edge_key(q1: int, r1: int, q2: int, r2: int) -> String:
	if q1 < q2 or (q1 == q2 and r1 < r2):
		return "%d,%d-%d,%d" % [q1, r1, q2, r2]
	return "%d,%d-%d,%d" % [q2, r2, q1, r1]

static func field_fill_color(type_name: String) -> Color:
	if FIELD_FILL.has(type_name):
		return FIELD_FILL[type_name] as Color
	return Color.GRAY

static func canonical_edge_key_from_array(loc: Array) -> String:
	return sorted_edge_key(int(loc[0]), int(loc[1]), int(loc[2]), int(loc[3]))

static func canonical_intersection_key_from_array(loc: Array) -> String:
	var coords: Array[Array] = [
		[int(loc[0]), int(loc[1])],
		[int(loc[2]), int(loc[3])],
		[int(loc[4]), int(loc[5])]
	]
	coords.sort()
	return "%d,%d|%d,%d|%d,%d" % [coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0], coords[2][1]]

static func same_owner(a: Dictionary, b: Dictionary) -> bool:
	var an := str(a.get("color_type", {}).get("name", ""))
	var bn := str(b.get("color_type", {}).get("name", ""))
	return an != "" and an == bn


# ── Public API ────────────────────────────────────────────────────────────────
func load_game_data(data: Dictionary) -> void:
	_fields.clear()
	_placed_buildings.clear()

	for key: String in data.get("fields", {}):
		var parts := key.split("\u0000")
		if parts.size() != 2:
			continue
		var q := int(parts[0])
		var r := int(parts[1])
		_fields["%d,%d" % [q, r]] = data["fields"][key]

	for key: String in data.get("settlements", {}):
		var parts := key.split("\u0000")
		if parts.size() != 6:
			continue
		var loc: Array[int] = [int(parts[0]), int(parts[1]), int(parts[2]),
								int(parts[3]), int(parts[4]), int(parts[5])]
		var s: Dictionary = data["settlements"][key]
		_placed_buildings.append({
			"type": "settlement",
			"location": loc,
			"building": s.get("settlement_type", {}),
			"player":   s.get("owner", {})
		})

	for key: String in data.get("roads", {}):
		var parts := key.split("\u0000")
		if parts.size() != 4:
			continue
		var loc: Array[int] = [int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])]
		var rd: Dictionary = data["roads"][key]
		_placed_buildings.append({
			"type": "road",
			"location": loc,
			"building": rd.get("road_type", {}),
			"player":   rd.get("owner", {})
		})

	_exit_placement_mode()
	queue_redraw()

func add_building_from_build(location: Array, building_data: Dictionary, owner_data: Dictionary) -> void:
	var result_type := "road" if location.size() == 4 else "settlement"
	var new_entry := {
		"type":     result_type,
		"location": location,
		"building": building_data,
		"player":   owner_data
	}

	# Roads cannot be upgraded; settlements can become cities. Replace matching
	# locations so drawing/validation always uses the latest server state.
	for i in _placed_buildings.size():
		var b: Dictionary = _placed_buildings[i]
		if b.get("type", "") != result_type:
			continue
		if result_type == "road" and canonical_edge_key_from_array(b.get("location", [])) == canonical_edge_key_from_array(location):
			_placed_buildings[i] = new_entry
			queue_redraw()
			return
		if result_type == "settlement" and canonical_intersection_key_from_array(b.get("location", [])) == canonical_intersection_key_from_array(location):
			_placed_buildings[i] = new_entry
			queue_redraw()
			return

	_placed_buildings.append(new_entry)
	queue_redraw()

func enter_placement_mode(recipe_id: String, result_type: String, result_data: Dictionary = {}, current_player: Dictionary = {}) -> void:
	_placement_recipe_id = recipe_id
	_placement_mode      = result_type
	_placement_result    = result_data
	_current_player      = current_player
	_build_placement_targets()
	queue_redraw()

func exit_placement_mode() -> void:
	_exit_placement_mode()
	queue_redraw()

func set_show_numbers(v: bool) -> void:
	_show_numbers = v
	queue_redraw()

func set_show_outer(v: bool) -> void:
	_show_outer = v
	queue_redraw()

func get_board_bounds() -> Array:
	if _fields.is_empty():
		return [Vector2.ZERO, Vector2.ZERO]
	var min_x := INF; var min_y := INF
	var max_x := -INF; var max_y := -INF
	for key: String in _fields:
		var parts := key.split(",")
		var pos := hex_to_pixel(int(parts[0]), int(parts[1]))
		min_x = min(min_x, pos.x - HEX_SIZE)
		min_y = min(min_y, pos.y - HEX_SIZE)
		max_x = max(max_x, pos.x + HEX_SIZE)
		max_y = max(max_y, pos.y + HEX_SIZE)
	return [Vector2(min_x, min_y), Vector2(max_x, max_y)]

func flash_matching_tiles(rolled_number: int) -> void:
	for key: String in _fields:
		var field: Dictionary = _fields[key]
		if field.get("assigned_number", null) != rolled_number:
			continue
		var parts := key.split(",")
		var center := hex_to_pixel(int(parts[0]), int(parts[1]))
		var flash := _FlashPolygon.new(hex_corner_points(center, HEX_SIZE - 1.5))
		add_child(flash)

# ── Internal ──────────────────────────────────────────────────────────────────
func _exit_placement_mode() -> void:
	_placement_mode      = ""
	_placement_recipe_id = ""
	_placement_result.clear()
	_current_player.clear()
	_placement_targets.clear()


func _road_occupied(location: Array) -> bool:
	var key := canonical_edge_key_from_array(location)
	for b: Dictionary in _placed_buildings:
		if b.get("type", "") == "road" and canonical_edge_key_from_array(b.get("location", [])) == key:
			return true
	return false

func _intersection_building(location: Array) -> Dictionary:
	var key := canonical_intersection_key_from_array(location)
	for b: Dictionary in _placed_buildings:
		if b.get("type", "") == "settlement" and canonical_intersection_key_from_array(b.get("location", [])) == key:
			return b
	return {}

func _has_adjacent_settlement(location: Array) -> bool:
	for b: Dictionary in _placed_buildings:
		if b.get("type", "") != "settlement":
			continue
		var other: Array = b.get("location", [])
		if other.size() != 6:
			continue
		var shared := 0
		for i in range(0, 6, 2):
			for j in range(0, 6, 2):
				if int(location[i]) == int(other[j]) and int(location[i + 1]) == int(other[j + 1]):
					shared += 1
		if shared >= 2:
			return true
	return false

func _player_has_settlement() -> bool:
	for b: Dictionary in _placed_buildings:
		if b.get("type", "") == "settlement" and same_owner(b.get("player", {}), _current_player):
			return true
	return false

func _player_has_road_touching_intersection(location: Array) -> bool:
	for b: Dictionary in _placed_buildings:
		if b.get("type", "") != "road" or not same_owner(b.get("player", {}), _current_player):
			continue
		var road: Array = b.get("location", [])
		if road.size() != 4:
			continue
		var matches := 0
		for i in range(0, 4, 2):
			for j in range(0, 6, 2):
				if int(road[i]) == int(location[j]) and int(road[i + 1]) == int(location[j + 1]):
					matches += 1
		if matches >= 2:
			return true
	return false

func _player_can_place_road(location: Array) -> bool:
	if _road_occupied(location):
		return false
	# Must touch one of my settlements or one of my other roads, matching server Map.build_road.
	for b: Dictionary in _placed_buildings:
		if not same_owner(b.get("player", {}), _current_player):
			continue
		var other: Array = b.get("location", [])
		if b.get("type", "") == "settlement":
			var shared_s := 0
			for i in range(0, 4, 2):
				for j in range(0, 6, 2):
					if int(location[i]) == int(other[j]) and int(location[i + 1]) == int(other[j + 1]):
						shared_s += 1
			if shared_s >= 2:
				return true
		elif b.get("type", "") == "road":
			var shared_r := 0
			for i in range(0, 4, 2):
				for j in range(0, 4, 2):
					if int(location[i]) == int(other[j]) and int(location[i + 1]) == int(other[j + 1]):
						shared_r += 1
			if shared_r >= 1:
				return true
	return false

func _player_can_place_settlement(location: Array) -> bool:
	var existing := _intersection_building(location)
	var prerequisite := str(_placement_result.get("prerequisite_building", ""))
	if prerequisite != "":
		# City upgrade: only my own existing prerequisite building is clickable.
		return not existing.is_empty() \
			and same_owner(existing.get("player", {}), _current_player) \
			and str(existing.get("building", {}).get("name", "")) == prerequisite

	if not existing.is_empty():
		return false
	if _has_adjacent_settlement(location):
		return false
	# First settlement can be anywhere legal. Later settlements must touch my road.
	if _player_has_settlement() and not _player_has_road_touching_intersection(location):
		return false
	return true

# Direction vectors as typed so indexing returns int
const DIRECTIONS: Array[Array] = [
	[1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1], [0, 1]
]

func _build_placement_targets() -> void:
	_placement_targets.clear()

	var inner_keys: Array[String] = []
	for key: String in _fields:
		var type_name: String = _fields[key].get("field_type", {}).get("name", "")
		if not ("outer" in type_name):
			inner_keys.append(key)

	if _placement_mode == "road":
		var drawn: Dictionary = {}
		for key: String in inner_keys:
			var parts := key.split(",")
			var q := int(parts[0])
			var r := int(parts[1])
			for dir: Array in DIRECTIONS:
				var nq: int = q + (dir[0] as int)
				var nr: int = r + (dir[1] as int)
				var nkey := "%d,%d" % [nq, nr]
				if not _fields.has(nkey):
					continue
				var n_type: String = _fields[nkey].get("field_type", {}).get("name", "")
				if "outer" in n_type:
					continue
				var ekey := sorted_edge_key(q, r, nq, nr)
				if drawn.has(ekey):
					continue
				drawn[ekey] = true
				var corners := shared_edge_corners(q, r, nq, nr)
				if corners.size() < 2:
					continue
				var p0 := corners[0] as Vector2
				var p1 := corners[1] as Vector2
				var loc := [q, r, nq, nr]
				# Match the web client: display every unoccupied edge and let the server
				# make the final legality decision. The previous local filter was too
				# strict and could hide valid roads next to newly built villages.
				if _road_occupied(loc):
					continue
				_placement_targets.append({
					"location": loc,
					"mid": (p0 + p1) / 2.0,
					"p0":  p0,
					"p1":  p1
				})

	elif _placement_mode == "settlement":
		var drawn: Dictionary = {}
		for key: String in inner_keys:
			var parts := key.split(",")
			var q := int(parts[0])
			var r := int(parts[1])
			for i in 6:
				var d1: Array = DIRECTIONS[i]
				var d2: Array = DIRECTIONS[(i + 1) % 6]
				var n1q: int = q + (d1[0] as int)
				var n1r: int = r + (d1[1] as int)
				var n2q: int = q + (d2[0] as int)
				var n2r: int = r + (d2[1] as int)
				if not _fields.has("%d,%d" % [n1q, n1r]) or \
				   not _fields.has("%d,%d" % [n2q, n2r]):
					continue
				# Sort coords so the key is canonical
				var coords: Array[Array] = [[q, r], [n1q, n1r], [n2q, n2r]]
				coords.sort()
				var c0: Array = coords[0]
				var c1: Array = coords[1]
				var c2: Array = coords[2]
				var ikey := "%d,%d|%d,%d|%d,%d" % [
					c0[0], c0[1], c1[0], c1[1], c2[0], c2[1]
				]
				if drawn.has(ikey):
					continue
				drawn[ikey] = true
				var center := intersection_point(
					c0[0] as int, c0[1] as int,
					c1[0] as int, c1[1] as int,
					c2[0] as int, c2[1] as int
				)
				var loc := [
					c0[0] as int, c0[1] as int,
					c1[0] as int, c1[1] as int,
					c2[0] as int, c2[1] as int
				]
				if not _player_can_place_settlement(loc):
					continue
				_placement_targets.append({
					"location": loc,
					"center": center
				})

# ── Drawing ───────────────────────────────────────────────────────────────────
func _draw() -> void:
	if _fields.is_empty():
		return

	# Outer tiles first, inner tiles on top
	var sorted_keys: Array = _fields.keys()
	sorted_keys.sort_custom(func(a: String, b: String) -> bool:
		var at: String = _fields[a].get("field_type", {}).get("name", "")
		var bt: String = _fields[b].get("field_type", {}).get("name", "")
		return ("outer" in at) and not ("outer" in bt)
	)

	for key: String in sorted_keys:
		var sp := key.split(",")
		var q := int(sp[0]); var r := int(sp[1])
		var field: Dictionary = _fields[key]
		var type_name: String = field.get("field_type", {}).get("name", "")
		var is_outer := "outer" in type_name
		if is_outer and not _show_outer:
			continue

		var center := hex_to_pixel(q, r)
		var pts    := hex_corner_points(center, HEX_SIZE - 1.5)
		var fill   := field_fill_color(type_name)

		draw_polygon(pts, PackedColorArray([fill]))

		var stroke_color := Color(0, 0, 0, 0.06) if is_outer else Color(0, 0, 0, 0.45)
		var stroke_width := 1.0 if is_outer else 1.5
		draw_polyline(pts + PackedVector2Array([pts[0]]), stroke_color, stroke_width)

		if not is_outer:
			var inner_pts := hex_corner_points(center, HEX_SIZE * 0.78)
			draw_polyline(inner_pts + PackedVector2Array([inner_pts[0]]),
						  Color(1, 1, 1, 0.12), 1.0)

			var assigned: Variant = field.get("assigned_number", null)
			if _show_numbers and assigned != null:
				var num: int = int(assigned)
				var num_color := Color(0.878, 0.361, 0.180) if num in HOT_NUMBERS else Color.BLACK
				draw_circle(center, 16.0, Color(0.961, 0.918, 0.816, 0.93))
				draw_arc(center, 16.0, 0, TAU, 24, Color(0, 0, 0, 0.35), 1.5)
				draw_string(
					ThemeDB.fallback_font, center - Vector2(6, -6),
					str(num), HORIZONTAL_ALIGNMENT_CENTER, -1, 14, num_color
				)

	for b: Dictionary in _placed_buildings:
		_draw_building(b)

	if _placement_mode == "road":
		for t: Dictionary in _placement_targets:
			draw_line(t["p0"], t["p1"], Color(1, 1, 0.4, 0.35), 8.0, true)
			draw_line(t["p0"], t["p1"], Color(1, 1, 0.4, 0.85), 4.0, true)
	elif _placement_mode == "settlement":
		for t: Dictionary in _placement_targets:
			var tc: Vector2 = t["center"]
			draw_circle(tc, 11.0, Color(1, 1, 0.4, 0.35))
			draw_arc(tc, 11.0, 0, TAU, 24, Color(1, 1, 0.4, 0.85), 1.5)

func _draw_building(b: Dictionary) -> void:
	var color  := player_color(b.get("player", {}))
	var loc: Array    = b["location"]
	var building: Dictionary = b.get("building", {})

	if b["type"] == "road":
		var q1: int = loc[0]; var r1: int = loc[1]
		var q2: int = loc[2]; var r2: int = loc[3]
		var corners := shared_edge_corners(q1, r1, q2, r2)
		if corners.size() < 2:
			return
		var c0 := corners[0] as Vector2
		var c1 := corners[1] as Vector2
		draw_line(c0, c1, Color(0, 0, 0, 0.55), 7.0, true)
		draw_line(c0, c1, color, 5.0, true)

	elif b["type"] == "settlement":
		var q1: int = loc[0]; var r1: int = loc[1]
		var q2: int = loc[2]; var r2: int = loc[3]
		var q3: int = loc[4]; var r3: int = loc[5]
		var center  := intersection_point(q1, r1, q2, r2, q3, r3)
		var point_value: int = building.get("point_value", 1)
		var radius := 8.0 if point_value > 1 else 5.0
		draw_circle(center + Vector2(0, 2), radius + 1.0, Color(0, 0, 0, 0.45))
		draw_circle(center, radius, color)
		draw_arc(center, radius, 0, TAU, 16, Color(0, 0, 0, 0.7), 1.5)
		draw_string(
			ThemeDB.fallback_font, center - Vector2(4, -4),
			"C" if point_value > 1 else "S",
			HORIZONTAL_ALIGNMENT_CENTER, -1, int(radius) + 2,
			Color(0, 0, 0, 0.75)
		)

# ── Input ─────────────────────────────────────────────────────────────────────
func _unhandled_input(event: InputEvent) -> void:
	if _placement_mode.is_empty() or _placement_targets.is_empty():
		return
	if not (event is InputEventMouseButton and
			(event as InputEventMouseButton).pressed and
			(event as InputEventMouseButton).button_index == MOUSE_BUTTON_LEFT):
		return

	var local_pos := to_local(get_global_mouse_position())

	if _placement_mode == "road":
		var best_dist := INF
		var best: Dictionary = {}
		for t: Dictionary in _placement_targets:
			var d := local_pos.distance_to(t["mid"] as Vector2)
			if d < best_dist:
				best_dist = d
				best = t
		if best_dist < 20.0 and not best.is_empty():
			get_viewport().set_input_as_handled()
			placement_selected.emit(_placement_recipe_id, best["location"])

	elif _placement_mode == "settlement":
		var best_dist := INF
		var best: Dictionary = {}
		for t: Dictionary in _placement_targets:
			var d := local_pos.distance_to(t["center"] as Vector2)
			if d < best_dist:
				best_dist = d
				best = t
		if best_dist < 18.0 and not best.is_empty():
			get_viewport().set_input_as_handled()
			placement_selected.emit(_placement_recipe_id, best["location"])

# ── Flash tile helper ─────────────────────────────────────────────────────────
class _FlashPolygon extends Polygon2D:
	var _elapsed := 0.0
	const DURATION := 1.1

	func _init(pts: PackedVector2Array) -> void:
		polygon  = pts
		color    = Color(1.0, 0.902, 0.314, 0.55)
		z_index  = 10

	func _process(delta: float) -> void:
		_elapsed += delta
		color.a   = lerpf(0.55, 0.0, _elapsed / DURATION)
		if _elapsed >= DURATION:
			queue_free()