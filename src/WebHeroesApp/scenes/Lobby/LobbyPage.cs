using Godot;
using System;

public partial class LobbyPage : Control
{
	private Node socketIOLobby;

	public override void _Ready()
	{
		socketIOLobby = GetNode<Node>("SocketIOLobby");

		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonCreateGame").Pressed += OnCreateNewGame;
		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonBack").Pressed += OnBack;

		socketIOLobby.Connect("lobby_refresh_received", new Callable(this, nameof(OnLobbyRefresh)));
		socketIOLobby.Connect("game_started", new Callable(this, nameof(OnGameStarted)));
		socketIOLobby.Connect("lobby_created", new Callable(this, nameof(OnLobbyCreated)));

		var gameState = GetNode<Node>("/root/GameState");
		string token = gameState.Get("token").AsString();
		socketIOLobby.Call("connect_to_server", token);
	}

	private void OnLobbyCreated(Variant data)
	{
		var array = data.AsGodotArray();
		if (array == null || array.Count == 0) return;

		var dict = array[0].AsGodotDictionary();
		if (dict == null) return;

		if (dict.TryGetValue("object_type", out var type) && type.AsString() == "success-response")
		{
			GetTree().ChangeSceneToFile("res://scenes/Lobby/waiting_room.tscn");
		}
		else if (dict.TryGetValue("reason", out var reason))
		{
			GD.Print("Failed to create lobby: ", reason.AsString());
		}
	}

	private void OnCreateNewGame()
	{
		var gameState = GetNode<Node>("/root/GameState");
		string username = gameState.Get("username").AsString();
		string lobbyName = $"{username}'s Lobby";
		gameState.Set("lobby_name", lobbyName);
		socketIOLobby.Call("create_lobby", lobbyName);
	}

	private void OnBack()
	{
		socketIOLobby.Call("disconnect_from_server");
		GetTree().ChangeSceneToFile("res://scenes/LoginSignUp/LoginRegisterMenu.tscn");
	}

	private void OnLobbyRefresh(Variant data)
	{
		var array = data.AsGodotArray();
		if (array == null || array.Count == 0) return;

		var dict = array[0].AsGodotDictionary();
		if (dict == null) return;

		var lobbyList = GetNode<VBoxContainer>("MarginContainer/VBoxContainer/LobbyList");

		foreach (var child in lobbyList.GetChildren())
			child.QueueFree();

		if (!dict.TryGetValue("lobbies", out var lobbiesVar)) return;

		foreach (var lobbyVar in lobbiesVar.AsGodotArray())
		{
			var lobby = lobbyVar.AsGodotDictionary();
			string name = lobby["lobby_name"].AsString();
			int players = lobby["members"].AsGodotArray().Count;

			var row = new HBoxContainer();
			row.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;

			var nameLabel = new Label();
			nameLabel.Text = name;
			nameLabel.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;
			nameLabel.SizeFlagsStretchRatio = 3.0f;
			nameLabel.ClipText = true;

			var joinBtn = new Button();
			joinBtn.Text = "join";
			joinBtn.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;
			joinBtn.SizeFlagsStretchRatio = 1.0f;

			var descLabel = new Label();
			descLabel.Text = "";
			descLabel.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;
			descLabel.SizeFlagsStretchRatio = 3.0f;

			var playersLabel = new Label();
			playersLabel.Text = players.ToString();
			playersLabel.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;
			playersLabel.SizeFlagsStretchRatio = 1.0f;

			string capturedName = name;
			joinBtn.Pressed += () =>
			{
				var gameState = GetNode<Node>("/root/GameState");
				gameState.Set("lobby_name", capturedName);
				socketIOLobby.Call("join_lobby", capturedName);
				GetTree().ChangeSceneToFile("res://scenes/Lobby/waiting_room.tscn");
			};

			row.AddChild(nameLabel);
			row.AddChild(joinBtn);
			row.AddChild(descLabel);
			row.AddChild(playersLabel);
			lobbyList.AddChild(row);
		}
	}

	private void OnGameStarted()
	{
		GD.Print("Game started! Switching scenes...");
	}
}
