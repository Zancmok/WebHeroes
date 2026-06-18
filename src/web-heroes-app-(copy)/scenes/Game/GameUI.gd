## GameUI.gd
extends CanvasLayer

@onready var turn_banner: Label = $Header/HBoxContainer/TurnBanner
@onready var status_label: Label = $Header/HBoxContainer/StatusLabel
@onready var players_list: VBoxContainer = $LeftPanel/VBoxContainer/PlayersScroll/PlayersList
@onready var dice_value: Label = $LeftPanel/VBoxContainer/DiceSection/DiceValue
@onready var gain_log: VBoxContainer = $LeftPanel/VBoxContainer/GainSection/GainScroll/GainLog
@onready var resources_grid: GridContainer = $RightPanel/VBoxContainer/ResourceSection/ResourcesGrid
@onready var recipes_list: VBoxContainer = $RightPanel/VBoxContainer/RecipesSection/RecipesList
@onready var end_turn_btn: Button = $RightPanel/VBoxContainer/EndTurnButton
@onready var numbers_btn: Button = $RightPanel/VBoxContainer/BoardOptions/ToggleNumbersButton
@onready var outer_btn: Button = $RightPanel/VBoxContainer/BoardOptions/ToggleOuterButton
@onready var game_over_overlay: Control = $GameOverOverlay
@onready var game_over_title: Label = $GameOverOverlay/Panel/VBoxContainer/Title
@onready var game_over_winner: Label = $GameOverOverlay/Panel/VBoxContainer/Winner
@onready var game_over_sub: Label = $GameOverOverlay/Panel/VBoxContainer/Sub

signal end_turn_pressed()
signal build_pressed(recipe_name: String, result_type: String)
signal toggle_numbers(show_numbers: bool)
signal toggle_outer(show_outer: bool)

var _active_recipe_btn: Button = null
var _show_numbers := true
var _show_outer := true

func _ready() -> void:
	game_over_overlay.visible = false
	show_status("Waiting for game data…")
	# Connect in code as a backup. Scene connections can break when the scene is edited/re-saved.
	if not end_turn_btn.pressed.is_connected(_on_end_turn_pressed):
		end_turn_btn.pressed.connect(_on_end_turn_pressed)
	if not numbers_btn.pressed.is_connected(_on_toggle_numbers_pressed):
		numbers_btn.pressed.connect(_on_toggle_numbers_pressed)
	if not outer_btn.pressed.is_connected(_on_toggle_outer_pressed):
		outer_btn.pressed.connect(_on_toggle_outer_pressed)

func update_players(p_players: Array, current_index: int, p_my_index: int) -> void:
	_clear(players_list)
	for i in p_players.size():
		var player: Dictionary = p_players[i]
		var ct: Dictionary = player.get("color_type", {})
		var color := Color(float(ct.get("r", 255)) / 255.0, float(ct.get("g", 255)) / 255.0, float(ct.get("b", 255)) / 255.0)
		var row := HBoxContainer.new()
		row.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var swatch := ColorRect.new()
		swatch.custom_minimum_size = Vector2(14, 14)
		swatch.color = color
		row.add_child(swatch)
		var name_lbl := Label.new()
		name_lbl.text = "%s%s" % [ct.get("display_name", "Player %d" % (i + 1)), " (You)" if i == p_my_index else ""]
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		row.add_child(name_lbl)
		if i == current_index:
			var pip := Label.new()
			pip.text = "▶"
			row.add_child(pip)
		row.modulate = Color.WHITE if i == current_index else Color(1, 1, 1, 0.58)
		players_list.add_child(row)

func update_resources(resources: Dictionary) -> void:
	_clear(resources_grid)
	if resources.is_empty():
		var placeholder := Label.new()
		placeholder.text = "No resources"
		resources_grid.add_child(placeholder)
		return
	for res_name in resources:
		var name_lbl := Label.new()
		name_lbl.text = _pretty_resource(str(res_name))
		name_lbl.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var amt_lbl := Label.new()
		amt_lbl.text = str(resources[res_name])
		amt_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		resources_grid.add_child(name_lbl)
		resources_grid.add_child(amt_lbl)

func update_recipes(p_recipes: Array, p_my_resources: Dictionary, is_my_turn: bool) -> void:
	_clear(recipes_list)
	_active_recipe_btn = null
	if p_recipes.is_empty():
		var placeholder := Label.new()
		placeholder.text = "No build recipes"
		recipes_list.add_child(placeholder)
		return
	for recipe in p_recipes:
		var result: Dictionary = recipe.get("result", {})
		var obj_type := str(result.get("object_type", ""))
		var result_type := ""
		if "road" in obj_type:
			result_type = "road"
		elif "settlement" in obj_type:
			result_type = "settlement"
		else:
			continue
		var can_afford := is_my_turn
		for ing in recipe.get("ingredients", []):
			if int(p_my_resources.get(ing.get("resource", ""), 0)) < int(ing.get("amount", 0)):
				can_afford = false
				break
		var cost_parts: Array = []
		for ing in recipe.get("ingredients", []):
			cost_parts.append("%d %s" % [int(ing.get("amount", 0)), _pretty_resource(str(ing.get("resource", "")))])
		var btn := Button.new()
		var cost_text := _join_text_parts(cost_parts, ", ") if cost_parts.size() > 0 else "free"
		btn.text = "%s\n%s" % [result.get("display_name", recipe.get("display_name", "Build")), cost_text]
		btn.disabled = not can_afford
		btn.toggle_mode = true
		btn.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var captured_name := str(recipe.get("name", ""))
		var captured_type := result_type
		btn.pressed.connect(func():
			if _active_recipe_btn == btn:
				_active_recipe_btn = null
				btn.button_pressed = false
				emit_signal("build_pressed", "", "")
				return
			if _active_recipe_btn != null:
				_active_recipe_btn.button_pressed = false
			_active_recipe_btn = btn
			btn.button_pressed = true
			emit_signal("build_pressed", captured_name, captured_type)
		)
		recipes_list.add_child(btn)

func show_dice(number: int) -> void:
	dice_value.text = str(number) if number > 0 else "—"
	dice_value.modulate = Color(0.878, 0.361, 0.180) if number in [6, 8] else Color.WHITE

func update_turn_banner(p_players: Array, current_index: int, p_my_index: int) -> void:
	if p_players.is_empty():
		turn_banner.text = "Waiting…"
		return
	if current_index == p_my_index:
		turn_banner.text = "Your Turn"
	elif current_index >= 0 and current_index < p_players.size():
		var active: Dictionary = p_players[current_index]
		var active_color: Dictionary = active.get("color_type", {})
		turn_banner.text = "%s's Turn" % active_color.get("display_name", "Player %d" % (current_index + 1))
	else:
		turn_banner.text = "Waiting…"

func set_end_turn_enabled(enabled: bool) -> void:
	end_turn_btn.disabled = not enabled
	end_turn_btn.tooltip_text = "End your turn" if enabled else "You can only end your own turn"

func show_status(message: String) -> void:
	status_label.text = message

func render_gain_log(gains: Dictionary, p_players: Array, p_my_index: int) -> void:
	if gains.is_empty():
		return
	for player_idx_str in gains:
		var idx := int(player_idx_str)
		var player_gains: Dictionary = gains[player_idx_str]
		var p_player: Dictionary = p_players[idx] if idx >= 0 and idx < p_players.size() else {}
		var p_color: Dictionary = p_player.get("color_type", {})
		var who := "You" if idx == p_my_index else str(p_color.get("display_name", "Player %d" % (idx + 1)))
		var gained_parts: Array = []
		for res in player_gains:
			gained_parts.append("+%d %s" % [int(player_gains[res]), _pretty_resource(str(res))])
		var entry := Label.new()
		entry.text = "%s gained %s" % [who, _join_text_parts(gained_parts, ", ")]
		gain_log.add_child(entry)
		gain_log.move_child(entry, 0)
	while gain_log.get_child_count() > 12:
		gain_log.get_child(gain_log.get_child_count() - 1).queue_free()

func on_build_placed() -> void:
	if _active_recipe_btn != null:
		_active_recipe_btn.button_pressed = false
	_active_recipe_btn = null

func show_game_over(data: Dictionary, p_players: Array, p_my_index: int) -> void:
	var winner: Dictionary = data.get("winner", {})
	var winner_color: Dictionary = winner.get("color_type", {})
	var my_player: Dictionary = p_players[p_my_index] if p_my_index >= 0 and p_my_index < p_players.size() else {}
	var my_color: Dictionary = my_player.get("color_type", {})
	var is_me := str(winner_color.get("name", "")) != "" and str(winner_color.get("name", "")) == str(my_color.get("name", ""))
	game_over_title.text = "Victory!" if is_me else "Game Over"
	game_over_winner.text = "%s won" % winner_color.get("display_name", "A player")
	game_over_sub.text = "You reached the required points." if is_me else "The game has ended."
	game_over_overlay.visible = true
	show_status("Game over.")

func _on_end_turn_pressed() -> void:
	print("[GameUI] End turn pressed")
	emit_signal("end_turn_pressed")

func _on_toggle_numbers_pressed() -> void:
	_show_numbers = not _show_numbers
	numbers_btn.text = "Numbers: %s" % ("On" if _show_numbers else "Off")
	emit_signal("toggle_numbers", _show_numbers)

func _on_toggle_outer_pressed() -> void:
	_show_outer = not _show_outer
	outer_btn.text = "Outer: %s" % ("On" if _show_outer else "Off")
	emit_signal("toggle_outer", _show_outer)

func _clear(node: Node) -> void:
	for child in node.get_children():
		child.queue_free()

func _join_text_parts(parts: Array, separator: String) -> String:
	var text := ""
	for i in range(parts.size()):
		if i > 0:
			text += separator
		text += str(parts[i])
	return text

func _pretty_resource(resource_id: String) -> String:
	var parts := resource_id.split(":")
	var raw := parts[parts.size() - 1] if parts.size() > 0 else resource_id
	return raw.capitalize()
