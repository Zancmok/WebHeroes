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

	public override void _Ready()
	{
		_socketIOGame = GetNode<Node>("SocketIOGame");
		_debugLabel   = GetNode<Label>("DebugLabel");

		_socketIOGame.Connect("socket_ready",           new Callable(this, nameof(OnSocketReady)));
		_socketIOGame.Connect("get_game_data_received", new Callable(this, nameof(OnGameDataReceived)));
		_socketIOGame.Connect("end_turn_received",      new Callable(this, nameof(OnEndTurnReceived)));
		_socketIOGame.Connect("build_received",         new Callable(this, nameof(OnBuildReceived)));
		
		var gameState = GetNode<Node>("/root/GameState");
		// TEMP: fake game state for testing
		gameState.Set("token", "SlJioOHc-_lZtcBEQ9V_yLPHKZoXNj9-4BiJ4nxLLIQ");
		gameState.Set("lobby_name", "nigger2");
		
		string token  = gameState.Get("token").AsString();
		_socketIOGame.Call("connect_to_server", token);

		_gameUI = GetNode<Node>("GameUI");
		_gameUI.Connect("end_turn_pressed", new Callable(this, nameof(OnEndTurnPressed)));
		_gameUI.Connect("build_pressed", new Callable(this, nameof(OnBuildPressed)));
	}

	private void OnSocketReady()
	{
		GD.Print("[GamePage] Socket ready");
		_debugLabel.Text = "Socket connected, waiting for game data...";
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

	_myIndex = data.TryGetValue("my_index", out var mi) ? mi.AsInt32() : -1;
	_currentIndex = data.TryGetValue("current_user_index", out var ci) ? ci.AsInt32() : 0;
	_players = data.TryGetValue("players", out var pl) ? pl.AsGodotArray() : new Array();
	_recipes = data.TryGetValue("prototypes", out var pr) 
		? pr.AsGodotArray().Where(p => p.AsGodotDictionary().TryGetValue("object_type", out var ot) 
			&& ot.AsString() == "recipe-s_prototype").ToGodotArray()
		: new Array();

	if (_myIndex >= 0 && _myIndex < _players.Count)
		_myResources = _players[_myIndex].AsGodotDictionary()
			.TryGetValue("resources", out var res) ? res.AsGodotDictionary() : new Dictionary();

	var isMyTurn = _currentIndex == _myIndex;
	_gameUI.Call("update_players", _players, _currentIndex, _myIndex);
	_gameUI.Call("update_resources", _myResources);
	_gameUI.Call("update_recipes", _recipes, _myResources, isMyTurn);
	_gameUI.Call("update_turn_banner", _players, _currentIndex, _myIndex);
	_gameUI.Call("set_end_turn_enabled", isMyTurn);
}

	private void OnEndTurnReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		_currentIndex = data.TryGetValue("next_user_index", out var ni) ? ni.AsInt32() : 0;
		_players = data.TryGetValue("players", out var pl) ? pl.AsGodotArray() : _players;

		if (_myIndex >= 0 && _myIndex < _players.Count)
			_myResources = _players[_myIndex].AsGodotDictionary()
				.TryGetValue("resources", out var res) ? res.AsGodotDictionary() : new Dictionary();

		int rolled = data.TryGetValue("rolled_number", out var r) ? r.AsInt32() : 0;

		var isMyTurn = _currentIndex == _myIndex;
		_gameUI.Call("show_dice", rolled);
		_gameUI.Call("update_players", _players, _currentIndex, _myIndex);
		_gameUI.Call("update_resources", _myResources);
		_gameUI.Call("update_recipes", _recipes, _myResources, isMyTurn);
		_gameUI.Call("update_turn_banner", _players, _currentIndex, _myIndex);
		_gameUI.Call("set_end_turn_enabled", isMyTurn);
	}

	private void OnBuildReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		GD.Print("[GamePage] Build placed: ", data);
	}

	private void OnEndTurnPressed()
	{
		var socketIOGame = GetNode<Node>("SocketIOGame");
		socketIOGame.Call("emit_end_turn");
	}

	private void OnBuildPressed(string recipeName, string resultType)
	{
		GD.Print("[Game] Build pressed: ", recipeName, " ", resultType);
		// placement mode coming next
	}

	
}
