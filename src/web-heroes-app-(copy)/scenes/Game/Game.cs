using Godot;
using Godot.Collections;
using System.Linq;

public partial class Game : Node2D
{
	private Node _socketIOGame;
	private Label _debugLabel;
	private Node _gameUI;
	private Array _players = new Array();
	private int _myIndex = -1;
	private int _currentIndex = 0;
	private Array _recipes = new Array();
	private Dictionary _myResources = new Dictionary();
	private string _pendingRecipeName = "";

	public override void _Ready()
	{
		_socketIOGame = GetNode<Node>("SocketIOGame");
		_debugLabel   = GetNode<Label>("DebugLabel");

		_socketIOGame.Connect("socket_ready",           new Callable(this, nameof(OnSocketReady)));
		_socketIOGame.Connect("get_game_data_received", new Callable(this, nameof(OnGameDataReceived)));
		_socketIOGame.Connect("end_turn_received",      new Callable(this, nameof(OnEndTurnReceived)));
		_socketIOGame.Connect("build_received",         new Callable(this, nameof(OnBuildReceived)));
		_socketIOGame.Connect("game_over_received", new Callable(this, nameof(OnGameOverReceived)));
		_socketIOGame.Connect("socket_status", new Callable(this, nameof(OnSocketStatus)));
		GetNode<Node2D>("HexBoard").Connect("placement_selected", new Callable(this, nameof(OnPlacementSelected)));

		_gameUI = GetNode<Node>("GameUI");
		_gameUI.Connect("end_turn_pressed", new Callable(this, nameof(OnEndTurnPressed)));
		_gameUI.Connect("build_pressed",    new Callable(this, nameof(OnBuildPressed)));
		_gameUI.Connect("toggle_numbers",  new Callable(this, nameof(OnToggleNumbers)));
		_gameUI.Connect("toggle_outer",    new Callable(this, nameof(OnToggleOuter)));

		var gameState = GetNode<Node>("/root/GameState");
		string token = gameState.Get("token").AsString();
		_socketIOGame.Call("connect_to_server", token);
	}

	private void OnSocketReady()
	{
		GD.Print("[Game] Socket ready");
		_debugLabel.Text = "Socket connected, waiting for game data...";
	}

	private void OnSocketStatus(string message)
	{
		if (_debugLabel != null)
			_debugLabel.Text = message;
	}

	private void OnGameDataReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		var hexBoard = GetNode<Node2D>("HexBoard");
		hexBoard.Call("load_game_data", data);

		var bounds = hexBoard.Call("get_board_bounds").AsGodotArray();
		var camera = GetNode<Camera2D>("GameCamera");
		camera.Call("set_map_bounds", bounds[0].AsVector2(), bounds[1].AsVector2());
		camera.Position = (bounds[0].AsVector2() + bounds[1].AsVector2()) / 2f;

		_myIndex     = data.TryGetValue("my_index",           out var mi) ? mi.AsInt32() : -1;
		_currentIndex = data.TryGetValue("current_user_index", out var ci) ? ci.AsInt32() : 0;
		_players     = data.TryGetValue("players",            out var pl) ? pl.AsGodotArray() : new Array();

		if (data.TryGetValue("prototypes", out var pr))
		{
			_recipes = new Array();
			foreach (var p in pr.AsGodotArray())
			{
				if (p.AsGodotDictionary().TryGetValue("object_type", out var ot) &&
					ot.AsString() == "recipe-s_prototype")
					_recipes.Add(p);
			}
		}

		if (_myIndex >= 0 && _myIndex < _players.Count)
			_myResources = _players[_myIndex].AsGodotDictionary()
				.TryGetValue("resources", out var res) ? res.AsGodotDictionary() : new Dictionary();

		var isMyTurn = _currentIndex == _myIndex;
		_gameUI.Call("update_players",    _players, _currentIndex, _myIndex);
		_gameUI.Call("update_resources",  _myResources);
		_gameUI.Call("update_recipes",    _recipes, _myResources, isMyTurn);
		_gameUI.Call("update_turn_banner", _players, _currentIndex, _myIndex);
		_gameUI.Call("set_end_turn_enabled", isMyTurn);
		_gameUI.Call("show_status", isMyTurn ? "Choose a build action or end your turn." : "Waiting for another player...");

		_debugLabel.Text = "";
	}

	private void OnEndTurnReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		_currentIndex = data.TryGetValue("next_user_index", out var ni) ? ni.AsInt32() : 0;
		_players      = data.TryGetValue("players",         out var pl) ? pl.AsGodotArray() : _players;

		if (_myIndex >= 0 && _myIndex < _players.Count)
			_myResources = _players[_myIndex].AsGodotDictionary()
				.TryGetValue("resources", out var res) ? res.AsGodotDictionary() : new Dictionary();

		int rolled = data.TryGetValue("rolled_number", out var r) ? r.AsInt32() : 0;

		var isMyTurn = _currentIndex == _myIndex;
		GetNode<Node2D>("HexBoard").Call("flash_matching_tiles", rolled);
		_gameUI.Call("show_dice",         rolled);
		_gameUI.Call("update_players",    _players, _currentIndex, _myIndex);
		_gameUI.Call("update_resources",  _myResources);
		_gameUI.Call("update_recipes",    _recipes, _myResources, isMyTurn);
		_gameUI.Call("update_turn_banner", _players, _currentIndex, _myIndex);
		_gameUI.Call("set_end_turn_enabled", isMyTurn);
		_gameUI.Call("render_gain_log", data.TryGetValue("gains", out var gainsVar) ? gainsVar.AsGodotDictionary() : new Dictionary(), _players, _myIndex);
		_gameUI.Call("show_status", isMyTurn ? "Choose a build action or end your turn." : "Waiting for another player...");
	}

	private void OnBuildReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		GD.Print("[Game] Build received: ", data);

		if (!data.TryGetValue("location", out var locVar))   return;
		if (!data.TryGetValue("building", out var buildVar)) return;
		if (!data.TryGetValue("player",   out var playerVar)) return;

		var location = locVar.AsGodotArray();
		var building = buildVar.AsGodotDictionary();
		var player   = playerVar.AsGodotDictionary();

		// Update the board visually
		var hexBoard = GetNode<Node2D>("HexBoard");
		hexBoard.Call("add_building_from_build", location, building, player);
		_gameUI.Call("on_build_placed");
		_gameUI.Call("show_status", "Build placed.");

		// Update the player entry and resources if the builder is us
		if (!player.TryGetValue("color_type", out var ctVar)) return;
		var colorType = ctVar.AsGodotDictionary();
		if (!colorType.TryGetValue("name", out var colorNameVar)) return;
		string colorName = colorNameVar.AsString();

		for (int i = 0; i < _players.Count; i++)
		{
			var p = _players[i].AsGodotDictionary();
			if (!p.TryGetValue("color_type", out var pctVar)) continue;
			if (!pctVar.AsGodotDictionary().TryGetValue("name", out var pnVar)) continue;
			if (pnVar.AsString() != colorName) continue;

			_players[i] = player;

			if (i == _myIndex && player.TryGetValue("resources", out var resVar))
			{
				_myResources = resVar.AsGodotDictionary();
				var isMyTurn = _currentIndex == _myIndex;
				_gameUI.Call("update_resources", _myResources);
				_gameUI.Call("update_recipes",   _recipes, _myResources, isMyTurn);
				_gameUI.Call("update_players",   _players, _currentIndex, _myIndex);
			}
			break;
		}
	}

	private async void OnEndTurnPressed()
	{
		GD.Print("[Game] End turn pressed");
		_gameUI.Call("set_end_turn_enabled", false);
		_gameUI.Call("show_status", "Ending turn...");
		_socketIOGame.Call("emit_end_turn");

		// Safety refresh: if the broadcast is missed, pull server state shortly after.
		await ToSignal(GetTree().CreateTimer(0.8), SceneTreeTimer.SignalName.Timeout);
		_socketIOGame.Call("refresh_game_data");
	}

	private void OnToggleNumbers(bool showNumbers)
	{
		GetNode<Node2D>("HexBoard").Call("set_show_numbers", showNumbers);
	}

	private void OnToggleOuter(bool showOuter)
	{
		GetNode<Node2D>("HexBoard").Call("set_show_outer", showOuter);
	}

	private void OnBuildPressed(string recipeName, string resultType)
	{
		if (string.IsNullOrEmpty(recipeName))
		{
			_pendingRecipeName = "";
			GetNode<Node2D>("HexBoard").Call("exit_placement_mode");
			_gameUI.Call("show_status", "Build cancelled.");
			return;
		}

		Dictionary resultData = new Dictionary();
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

		Dictionary currentPlayer = new Dictionary();
		if (_myIndex >= 0 && _myIndex < _players.Count)
			currentPlayer = _players[_myIndex].AsGodotDictionary();

		_pendingRecipeName = recipeName;
		GetNode<Node2D>("HexBoard").Call("enter_placement_mode", recipeName, resultType, resultData, currentPlayer);
		_gameUI.Call("show_status", resultType == "road" ? "Click a highlighted edge to build a road. Esc cancels." : "Click a highlighted corner/settlement. Esc cancels.");
	}

	private async void OnPlacementSelected(string recipeId, Array location)
	{
		GD.Print("[Game] Placement selected: ", recipeId, " at ", location);
		_socketIOGame.Call("emit_build", recipeId, location);
		_pendingRecipeName = "";
		GetNode<Node2D>("HexBoard").Call("exit_placement_mode");
		_gameUI.Call("show_status", "Build sent. Waiting for server...");

		// Safety refresh: keeps resources/board synced even if the build broadcast
		// is delayed or the local event update misses a field.
		await ToSignal(GetTree().CreateTimer(0.8), SceneTreeTimer.SignalName.Timeout);
		_socketIOGame.Call("refresh_game_data");
	}


	private void OnGameOverReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		GD.Print("[Game] Game over: ", data);
		_gameUI.Call("set_end_turn_enabled", false);
		_gameUI.Call("show_game_over", data, _players, _myIndex);
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey key && key.Pressed && key.Keycode == Key.Escape)
		{
			if (!string.IsNullOrEmpty(_pendingRecipeName))
			{
				_pendingRecipeName = "";
				GetNode<Node2D>("HexBoard").Call("exit_placement_mode");
				_gameUI.Call("show_status", "Build cancelled.");
			}
		}
	}
}
