using Godot;
using System;

public partial class LobbyPage : Control
{
	private UserManagementLobby lobbyManager;

	public override void _Ready()
	{
		lobbyManager = GetNode<UserManagementLobby>("UserManagementLobby");

		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonCreateGame").Pressed += OnCreateNewGame;
		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonBack").Pressed += OnBack;


		GetNode<Node>("SocketIOLobby").Connect("lobby_refresh_received", new Callable(this, nameof(OnLobbyRefresh)));

		GetNode<Node>("SocketIOLobby").Connect("game_started", new Callable(this, nameof(OnGameStarted)));

		GetNode<Node>("SocketIOLobby").Connect("lobby_created", new Callable(this, nameof(OnLobbyCreated)));
	}

	private void OnLobbyCreated(Variant data)
	{
		var array = data.AsGodotArray();
		if (array == null ||array.Count == 0) return;
		
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
		GD.Print(gameState.Get("username"));
		GD.Print(gameState.Get("lobby_name"));
		lobbyManager.CreateLobby(lobbyName);
	}

	private void OnBack()
	{
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
		descLabel.Text = "";  // placeholder — add game description field when server sends it
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
			lobbyManager.JoinLobby(capturedName);
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
		// add: GetTree().ChangeSceneToFile("");
	}
}
