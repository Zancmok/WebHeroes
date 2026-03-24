using Godot;
using System;

public partial class LobbyPage : Control
{
	private UserManagementLobby lobbyManager;

	public override void _Ready()
	{
		lobbyManager = GetNode<UserManagementLobby>("UserManagementLobby");

		GetNode<Button>("BoxContainer/VBoxContainer/HBoxContainer/MarginContainerButton/ButtonCreateGame")
			.Pressed += OnCreateNewGame;

		GetNode<Button>("BoxContainer/VBoxContainer/HBoxContainer/MarginContainerButton2/ButtonBack")
			.Pressed += OnBack;

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
		string username = gameState.Get("Username").AsString();
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

		GD.Print("=== LOBBY REFRESH DATA ===");
		GD.Print(data);
		GD.Print("==========================");
		
		var array = data.AsGodotArray();
		if (array == null || array.Count == 0) return;
		
		var dict = array[0].AsGodotDictionary();
		if(dict == null) return;

		var lobbyList = GetNode<VBoxContainer>("BoxContainer/VBoxContainer/HBoxContainer3/VBoxContainer2/LobbyList");

		foreach (var child in lobbyList.GetChildren())
		{
			child.QueueFree();
		}

		if (!dict.TryGetValue("lobbies", out var lobbiesVar)) return;

		foreach(var lobbyVar in lobbiesVar.AsGodotArray())
		{
			var lobby = lobbyVar.AsGodotDictionary();
			string name = lobby["lobby_name"].AsString();
			int players = lobby["members"].AsGodotArray().Count;

			var row = new HBoxContainer();
			var nameLabel = new Label();
			var joinBtn = new Button();
			var playlabel = new Label();

			nameLabel.Text = name;
			nameLabel.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;
			joinBtn.Text = "join";
			playlabel.Text = players.ToString();
			playlabel.SizeFlagsHorizontal = Control.SizeFlags.Expand | Control.SizeFlags.Fill;

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
			row.AddChild(playlabel);
			lobbyList.AddChild(row);
		}
		
		//if (dict.TryGetValue("")){return;}
		// TODO: populate lobby list UI from the "data"	
	}

	private void OnGameStarted()
	{
		GD.Print("Game started! Switching scenes...");
		// add: GetTree().ChangeSceneToFile("");
	}
}
