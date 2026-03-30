using Godot;
using System;
using System.Collections.Generic;
 
public partial class LobbyPage : Control
{
	private Node socketIOLobby;
	private HttpRequest httpRequest;
	private HttpQueue httpQueue;
	private bool _loggingOut = false;
	private const string BaseUrl = "https://webheroes.duckdns.org:9027";
	
	public override void _Ready()
	{
		httpRequest = GetNode<HttpRequest>("CallZancmok");
		httpRequest.RequestCompleted += OnRequestCompleted;
		httpQueue = new HttpQueue(httpRequest);
 
		socketIOLobby = GetNode<Node>("SocketIOLobby");
 
		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonCreateGame").Pressed += OnCreateNewGame;
		GetNode<Button>("MarginContainer/VBoxContainer/HBoxContainer/ButtonBack").Pressed += OnBack;
 
		socketIOLobby.Connect("lobby_refresh_received", new Callable(this, nameof(OnLobbyRefresh)));
		socketIOLobby.Connect("game_started", new Callable(this, nameof(OnGameStarted)));
		socketIOLobby.Connect("lobby_created", new Callable(this, nameof(OnLobbyCreated)));
		
 
		var gameState = GetNode<Node>("/root/GameState");
		string token = gameState.Get("token").AsString();
		socketIOLobby.Connect("socket_ready", new Callable(this, nameof(OnSocketReady)));
		socketIOLobby.Call("connect_to_server", token);



	}
 
	private void OnRequestCompleted(long result, long responseCode, string[] headers, byte[] body)
	{
		GD.Print("[LobbyPage] HTTP response: ", responseCode);
		httpQueue.OnCompleted();

		if (_loggingOut)
		{
			_loggingOut = false;
			GetTree().ChangeSceneToFile("res://scenes/LoginSignUp/LoginRegisterMenu.tscn");	
		}
	}
 
	private void LogOut()
	{
		_loggingOut = true;
		socketIOLobby.Call("disconnect_from_server");

		var gameState = GetNode<Node>("/root/GameState");
		string token = gameState.Get("token").AsString();
		string body = string.IsNullOrEmpty(token)
			? "{}"
			: $"{{\"token\":\"{token}\"}}";
 
		httpQueue.Enqueue($"{BaseUrl}/user-management/logout", body);

		GD.Print(
			gameState.Get("token").AsString() + "; " +
			gameState.Get("username").AsString() + "; " +
			gameState.Get("lobby_name").AsString()
			);
 
		gameState.Set("token", "");
		gameState.Set("username", "");
		gameState.Set("lobby_name", "");
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
	}
 
	private void OnCreateNewGame()
	{
		ShowLobbyNameDialog();
	}
 
	private void ShowLobbyNameDialog()
	{
		var lobbyNameDialog = new ConfirmationDialog();
		lobbyNameDialog.Title = "Creating lobby...";
		lobbyNameDialog.OkButtonText = "Create";

		var LineEdit = new LineEdit();
		LineEdit.PlaceholderText = "Enter lobby name...";
		lobbyNameDialog.AddChild(LineEdit);

		AddChild(lobbyNameDialog);
		lobbyNameDialog.PopupCentered();

		lobbyNameDialog.Confirmed += () =>
		{
			string lobbyName = LineEdit.Text.Trim();
			if (!string.IsNullOrEmpty(lobbyName))
			{
				var gameState = GetNode<Node>("/root/GameState");
				gameState.Set("lobby_name", lobbyName);
				socketIOLobby.Call("create_lobby", lobbyName);
			}
			lobbyNameDialog.QueueFree();
		};

		lobbyNameDialog.Canceled += () => lobbyNameDialog.QueueFree();
	} 

	private void OnBack()
	{
		LogOut();
	}
 
	private void OnLobbyRefresh(Variant data)
	{
		GD.Print("[LobbyPage] OnLobbyRefresh called, data: ", data);
		var array = data.AsGodotArray();
		GD.Print("[LobbyPage] array count: ", array?.Count); 
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
			string name    = lobby["lobby_name"].AsString();
			int players    = lobby["members"].AsGodotArray().Count;
 
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

	private void OnSocketReady()
	{
		socketIOLobby.Call("refresh");
	}
 
	private void OnGameStarted()
	{
		GD.Print("[LobbyPage] Game started!");
	}
}
