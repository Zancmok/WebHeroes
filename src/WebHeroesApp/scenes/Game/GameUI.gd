extends CanvasLayer

# Node references
@onready var turn_banner: Label = $Header/HBoxContainer/TurnBanner
@onready var players_list: VBoxContainer = $LeftPanel/VBoxContainer/ScrollContainer/PlayersList
@onready var dice_value: Label = $LeftPanel/VBoxContainer/DiceSection/DiceValue
@onready var resources_grid: GridContainer = $RightPanel/VBoxContainer/ResourceSection/ResourcesGrid
@onready var recipes_list: VBoxContainer = $RightPanel/VBoxContainer/RecipesSection/RecipesList
@onready var end_turn_btn: Button = $RightPanel/VBoxContainer/EndTurnButton

signal end_turn_pressed
signal build_pressed(recipe_name: String, result_type: String)

func update_players(players: Array, current_index: int, _my_index: int) -> void:
	for child in players_list.get_children():
		child.queue_free()

	for i in range(players.size()):
		var player = players[i]
		var color_type = player.get("color_type", {})
		var color = Color(
			color_type.get("r", 255) / 255.0,
			color_type.get("g", 255) / 255.0,
			color_type.get("b", 255) / 255.0
		)

		var row = HBoxContainer.new()

		var swatch = ColorRect.new()
		swatch.custom_minimum_size = Vector2(12, 12)
		swatch.color = color

		var name_label = Label.new()
		name_label.text = color_type.get("display_name", "Player %d" % (i + 1))
		name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL

		row.add_child(swatch)
		row.add_child(name_label)

		if i == current_index:
			var pip = ColorRect.new()
			pip.custom_minimum_size = Vector2(8, 8)
			pip.color = Color.GOLD
			row.add_child(pip)

		if i == current_index:
			row.modulate = Color.WHITE
		else:
			row.modulate = Color(1, 1, 1, 0.5)

		players_list.add_child(row)

func update_resources(resources: Dictionary) -> void:
	for child in resources_grid.get_children():
		child.queue_free()

	for resource_name in resources:
		var name_label = Label.new()
		name_label.text = resource_name
		name_label.size_flags_horizontal = Control.SIZE_EXPAND_FILL

		var amount_label = Label.new()
		amount_label.text = str(resources[resource_name])
		amount_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT

		resources_grid.add_child(name_label)
		resources_grid.add_child(amount_label)

func update_recipes(recipes: Array, my_resources: Dictionary, is_my_turn: bool) -> void:
	for child in recipes_list.get_children():
		child.queue_free()

	for recipe in recipes:
		var result = recipe.get("result", {})
		var object_type = result.get("object_type", "")
		var result_type = ""
		if "road" in object_type:
			result_type = "road"
		elif "settlement" in object_type:
			result_type = "settlement"
		else:
			continue

		var can_afford = is_my_turn
		for ingredient in recipe.get("ingredients", []):
			if my_resources.get(ingredient.get("resource", ""), 0) < ingredient.get("amount", 0):
				can_afford = false
				break

		var btn = Button.new()
		var cost_parts = []
		for ingredient in recipe.get("ingredients", []):
			cost_parts.append("%d %s" % [ingredient.get("amount", 0), ingredient.get("resource", "")])
		var cost_str = ", ".join(cost_parts) if cost_parts.size() > 0 else "free"
		btn.text = "%s\n%s" % [result.get("display_name", recipe.get("display_name", "")), cost_str]
		btn.disabled = not can_afford
		btn.pressed.connect(func(): emit_signal("build_pressed", recipe.get("name", ""), result_type))

		recipes_list.add_child(btn)

func show_dice(number: int) -> void:
	dice_value.text = str(number)
	if number in [6, 8]:
		dice_value.modulate = Color(0.878, 0.361, 0.180)
	else:
		dice_value.modulate = Color.WHITE

func update_turn_banner(players: Array, current_index: int, my_index: int) -> void:
	if players.is_empty():
		turn_banner.text = "Waiting..."
		return
	if current_index == my_index:
		turn_banner.text = "Your Turn"
	else:
		var _name = players[current_index].get("color_type", {}).get("display_name", "Player %d" % (current_index + 1))
		turn_banner.text = "%s's Turn" % _name

func set_end_turn_enabled(enabled: bool) -> void:
	end_turn_btn.disabled = not enabled

func _on_end_turn_pressed() -> void:
	emit_signal("end_turn_pressed")
