using Godot;
using Godot.Collections;

public partial class GamePage : Node2D
{
	private Node _socketIOGame;
	private Label _debugLabel;

	public override void _Ready()
	{
		_socketIOGame = GetNode<Node>("SocketIOGame");
		_debugLabel   = GetNode<Label>("DebugLabel");

		_socketIOGame.Connect("socket_ready",           new Callable(this, nameof(OnSocketReady)));
		_socketIOGame.Connect("get_game_data_received", new Callable(this, nameof(OnGameDataReceived)));
		_socketIOGame.Connect("end_turn_received",      new Callable(this, nameof(OnEndTurnReceived)));
		_socketIOGame.Connect("build_received",         new Callable(this, nameof(OnBuildReceived)));

		var gameState = GetNode<Node>("/root/GameState");
		string token  = gameState.Get("token").AsString();
		_socketIOGame.Call("connect_to_server", token);
	}

	private void OnSocketReady()
	{
		GD.Print("[GamePage] Socket ready");
		_debugLabel.Text = "Socket connected, waiting for game data...";
	}

	private void OnGameDataReceived(Variant raw)
	{
		// data arrives wrapped in a single-element Array — unwrap it
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		GD.Print("[GamePage] Game data received: ", data);
		_debugLabel.Text = "Game data received! Fields: " + 
			(data.TryGetValue("fields", out var f) ? f.AsGodotDictionary().Count.ToString() : "?");
	}

	private void OnEndTurnReceived(Variant raw)
	{
		Dictionary data;
		if (raw.AsGodotArray() is { Count: > 0 } arr)
			data = arr[0].AsGodotDictionary();
		else
			data = raw.AsGodotDictionary();

		int rolled = data.TryGetValue("rolled_number", out var r) ? r.AsInt32() : 0;
		GD.Print("[GamePage] End turn, rolled: ", rolled);
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
}
