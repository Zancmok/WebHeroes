using Godot;
using Godot.Collections;

public partial class Game : Node2D
{
	private Node       _socketIOGame;
	private Label      _debugLabel;
	private Node       _gameUI;
	private Node2D     _hexBoard;   // cached once in _Ready
	private Camera2D   _camera;     // cached once in _Ready

	private Array      _players     = new Array();
	private int        _myIndex     = -1;
	private int        _currentIndex = 0;
	private Array      _recipes     = new Array();
	private Dictionary _myResources = new Dictionary();
	private string     _pendingRecipeName  = "";
	private string     _lastSentRecipeName = "";
	private bool       _optimisticCostApplied = false;

	public override void _Ready()
	{
		_socketIOGame = GetNode<Node>("SocketIOGame");
		_debugLabel   = GetNode<Label>("DebugLabel");
		_gameUI       = GetNode<Node>("GameUI");
		_hexBoard     = GetNode<Node2D>("HexBoard");
		_camera       = GetNode<Camera2D>("GameCamera");

		_socketIOGame.Connect("socket_ready",           new Callable(this, nameof(OnSocketReady)));
		_socketIOGame.Connect("get_game_data_received", new Callable(this, nameof(OnGameDataReceived)));
		_socketIOGame.Connect("end_turn_received",      new Callable(this, nameof(OnEndTurnReceived)));
		_socketIOGame.Connect("build_received",         new Callable(this, nameof(OnBuildReceived)));
		_socketIOGame.Connect("game_over_received",     new Callable(this, nameof(OnGameOverReceived)));
		_socketIOGame.Connect("socket_status",          new Callable(this, nameof(OnSocketStatus)));

		_hexBoard.Connect("placement_selected", new Callable(this, nameof(OnPlacementSelected)));

		_gameUI.Connect("end_turn_pressed", new Callable(this, nameof(OnEndTurnPressed)));
		_gameUI.Connect("build_pressed",    new Callable(this, nameof(OnBuildPressed)));
		_gameUI.Connect("toggle_numbers",   new Callable(this, nameof(OnToggleNumbers)));
		_gameUI.Connect("toggle_outer",     new Callable(this, nameof(OnToggleOuter)));

		var gameState = GetNode<Node>("/root/GameState");
		string token  = gameState.Get("token").AsString();
		_socketIOGame.Call("connect_to_server", token);
	}

	// ── Helpers ────────────────────────────────────────────────────────────────

	private static Dictionary UnpackData(Variant raw)
	{
		if (raw.VariantType == Variant.Type.Array)
		{
			var arr = raw.AsGodotArray();
			if (arr.Count > 0 && arr[0].VariantType == Variant.Type.Dictionary)
				return arr[0].AsGodotDictionary();
		}
		if (raw.VariantType == Variant.Type.Dictionary)
			return raw.AsGodotDictionary();
		return new Dictionary();
	}

	private void RefreshUI(bool isMyTurn)
	{
		_gameUI.Call("update_players",       _players, _currentIndex, _myIndex);
		_gameUI.Call("update_resources",     _myResources);
		_gameUI.Call("update_recipes",       _recipes, _myResources, isMyTurn);
		_gameUI.Call("update_turn_banner",   _players, _currentIndex, _myIndex);
		_gameUI.Call("set_end_turn_enabled", isMyTurn);
		_gameUI.Call("show_status", isMyTurn
			? "Choose a build action or end your turn."
			: "Waiting for another player...");
	}

	// ── Socket handlers ────────────────────────────────────────────────────────

	private void OnSocketReady()
	{
		_debugLabel.Text = "Socket connected, waiting for game data...";
	}

	private void OnSocketStatus(string message)
	{
		_debugLabel.Text = message;
	}

	private void OnGameDataReceived(Variant raw)
	{
		var data = UnpackData(raw);

		if (!data.TryGetValue("players", out var playersGuard) ||
			playersGuard.AsGodotArray().Count == 0)
			return;

		_hexBoard.Call("load_game_data", data);

		var bounds = _hexBoard.Call("get_board_bounds").AsGodotArray();
		_camera.Call("set_map_bounds", bounds[0].AsVector2(), bounds[1].AsVector2());
		_camera.Position = (bounds[0].AsVector2() + bounds[1].AsVector2()) / 2f;

		_myIndex      = data.TryGetValue("my_index",           out var mi) ? mi.AsInt32() : -1;
		_currentIndex = data.TryGetValue("current_user_index", out var ci) ? ci.AsInt32() : 0;
		_players      = data.TryGetValue("players",            out var pl) ? pl.AsGodotArray() : new Array();

		if (data.TryGetValue("prototypes", out var pr))
		{
			var nextRecipes = new Array();
			foreach (var p in pr.AsGodotArray())
			{
				var proto = p.AsGodotDictionary();
				if (proto.TryGetValue("object_type", out var ot) && ot.AsString() == "recipe-s_prototype")
					nextRecipes.Add(p);
			}
			if (nextRecipes.Count > 0)
				_recipes = nextRecipes;
		}

		if (_myIndex >= 0 && _myIndex < _players.Count)
		{
			var me = _players[_myIndex].AsGodotDictionary();
			if (me.TryGetValue("resources", out var res))
				_myResources = res.AsGodotDictionary();
		}

		RefreshUI(_currentIndex == _myIndex);
		_debugLabel.Text = "";
	}

	private void OnEndTurnReceived(Variant raw)
	{
		var data = UnpackData(raw);

		_currentIndex = data.TryGetValue("next_user_index", out var ni) ? ni.AsInt32() : 0;
		if (data.TryGetValue("players", out var pl))
			_players = pl.AsGodotArray();

		if (data.TryGetValue("my_resources", out var myResVar))
		{
			_myResources = myResVar.AsGodotDictionary();
		}
		else if (_myIndex >= 0 && _myIndex < _players.Count)
		{
			var me = _players[_myIndex].AsGodotDictionary();
			if (me.TryGetValue("resources", out var res))
				_myResources = res.AsGodotDictionary();
		}

		int rolled = data.TryGetValue("rolled_number", out var r) ? r.AsInt32() : 0;
		_optimisticCostApplied = false;
		_lastSentRecipeName    = "";

		var gains = data.TryGetValue("gains", out var gainsVar)
			? gainsVar.AsGodotDictionary()
			: new Dictionary();

		var isMyTurn = _currentIndex == _myIndex;
		// _hexBoard.Call("flash_matching_tiles", rolled);
		// _gameUI.Call("show_dice", rolled);
		// _gameUI.Call("render_gain_log", gains, _players, _myIndex);
		RefreshUI(isMyTurn);
	}

	private void OnBuildReceived(Variant raw)
	{
		var data = UnpackData(raw);

		if (!data.TryGetValue("location", out var locVar))    return;
		if (!data.TryGetValue("building", out var buildVar))  return;
		if (!data.TryGetValue("player",   out var playerVar)) return;

		var location = locVar.AsGodotArray();
		var building = buildVar.AsGodotDictionary();
		var player   = playerVar.AsGodotDictionary();

		_hexBoard.Call("add_building_from_build", location, building, player);
		_gameUI.Call("on_build_placed");
		_gameUI.Call("show_status", "Build placed.");

		if (!player.TryGetValue("color_type", out var ctVar)) return;
		if (!ctVar.AsGodotDictionary().TryGetValue("name", out var colorNameVar)) return;
		string colorName = colorNameVar.AsString();

		for (int i = 0; i < _players.Count; i++)
		{
			var p = _players[i].AsGodotDictionary();
			if (!p.TryGetValue("color_type",  out var pctVar)) continue;
			if (!pctVar.AsGodotDictionary().TryGetValue("name", out var pnVar)) continue;
			if (pnVar.AsString() != colorName) continue;

			_players[i] = player;

			if (i == _myIndex)
			{
				if (player.TryGetValue("resources", out var resVar))
					_myResources = resVar.AsGodotDictionary();

				_optimisticCostApplied = false;
				_lastSentRecipeName    = "";
				_gameUI.Call("update_resources", _myResources);
				_gameUI.Call("update_recipes",   _recipes, _myResources, _currentIndex == _myIndex);
				_gameUI.Call("update_players",   _players, _currentIndex, _myIndex);
			}
			break;
		}
	}

	private void OnGameOverReceived(Variant raw)
	{
		var data = UnpackData(raw);
		_gameUI.Call("set_end_turn_enabled", false);
		_gameUI.Call("show_game_over", data, _players, _myIndex);
	}

	// ── UI handlers ────────────────────────────────────────────────────────────

	private void OnEndTurnPressed()
	{
		_gameUI.Call("set_end_turn_enabled", false);
		_gameUI.Call("show_status", "Ending turn...");
		_socketIOGame.Call("emit_end_turn");
	}

	private void OnToggleNumbers(bool showNumbers) => _hexBoard.Call("set_show_numbers", showNumbers);
	private void OnToggleOuter(bool showOuter)     => _hexBoard.Call("set_show_outer",   showOuter);

	private void OnBuildPressed(string recipeName, string resultType)
	{
		if (string.IsNullOrEmpty(recipeName))
		{
			_pendingRecipeName = "";
			_hexBoard.Call("exit_placement_mode");
			_gameUI.Call("show_status", "Build cancelled.");
			return;
		}

		Dictionary resultData     = new Dictionary();
		Dictionary currentPlayer  = new Dictionary();

		foreach (var recipeVar in _recipes)
		{
			var recipe = recipeVar.AsGodotDictionary();
			if (recipe.TryGetValue("name", out var n) && n.AsString() == recipeName)
			{
				if (recipe.TryGetValue("result", out var rv))
					resultData = rv.AsGodotDictionary();
				break;
			}
		}

		if (_myIndex >= 0 && _myIndex < _players.Count)
			currentPlayer = _players[_myIndex].AsGodotDictionary();

		_pendingRecipeName = recipeName;
		_hexBoard.Call("enter_placement_mode", recipeName, resultType, resultData, currentPlayer);
		_gameUI.Call("show_status", resultType == "road"
			? "Click a highlighted edge to build a road. Esc cancels."
			: "Click a highlighted corner/settlement. Esc cancels.");
	}

	private void OnPlacementSelected(string recipeId, Array location)
	{
		_lastSentRecipeName    = recipeId;
		_optimisticCostApplied = ApplyLocalRecipeCost(recipeId);

		if (_optimisticCostApplied)
		{
			_gameUI.Call("update_resources", _myResources);
			_gameUI.Call("update_recipes",   _recipes, _myResources, _currentIndex == _myIndex);
		}

		_socketIOGame.Call("emit_build", recipeId, location);
		_pendingRecipeName = "";
		_hexBoard.Call("exit_placement_mode");
		_gameUI.Call("show_status", "Build sent. Waiting for server...");
	}

	// ── Helpers ────────────────────────────────────────────────────────────────

	private bool ApplyLocalRecipeCost(string recipeName)
	{
		if (string.IsNullOrEmpty(recipeName)) return false;

		foreach (var recipeVar in _recipes)
		{
			var recipe = recipeVar.AsGodotDictionary();
			if (!recipe.TryGetValue("name", out var nameVar) || nameVar.AsString() != recipeName)
				continue;

			if (!recipe.TryGetValue("ingredients", out var ingredientsVar))
				return false;

			foreach (var ingVar in ingredientsVar.AsGodotArray())
			{
				var ing = ingVar.AsGodotDictionary();
				if (!ing.TryGetValue("resource", out var resVar))  continue;
				if (!ing.TryGetValue("amount",   out var amtVar))  continue;

				var key     = resVar.AsString();
				var amount  = amtVar.AsInt32();
				var current = _myResources.TryGetValue(key, out var curVar) ? curVar.AsInt32() : 0;
				_myResources[key] = Mathf.Max(0, current - amount);
			}
			return true;
		}
		return false;
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey { Pressed: true, Keycode: Key.Escape }
			&& !string.IsNullOrEmpty(_pendingRecipeName))
		{
			_pendingRecipeName = "";
			_hexBoard.Call("exit_placement_mode");
			_gameUI.Call("show_status", "Build cancelled.");
		}
	}
}
