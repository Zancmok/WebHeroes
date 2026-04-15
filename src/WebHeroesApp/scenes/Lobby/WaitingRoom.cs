using Godot;
using System;
 
public partial class WaitingRoom : Control
{
	private Node socketIOLobby;
	private Label lobbyNameLabel;
	private Label lobbyOwnerLabel;
	private VBoxContainer playerList;
	private Button startButton;
	private Button leaveButton;
	private string _lobbyName;
 
	public override void _Ready()
	{
		socketIOLobby = GetNode<Node>("SocketIOLobby");
 
		lobbyNameLabel 	= GetNode<Label>("VBoxContainer/LobbyName");
		lobbyOwnerLabel = GetNode<Label>("VBoxContainer/Owner");
		playerList 		= GetNode<VBoxContainer>("VBoxContainer/PlayerList");
		startButton 	= GetNode<Button>("VBoxContainer/StartButton");
		leaveButton 	= GetNode<Button>("VBoxContainer/LeaveButton");
 
		startButton.Visible = false;
		leaveButton.Visible = true;

		startButton.Pressed += () => OnStartPressed();
		leaveButton.Pressed += () => OnLeavePressed();
 
		socketIOLobby.Connect("lobby_refresh_received", new Callable(this, nameof(OnLobbyRefresh)));
		socketIOLobby.Connect("get_lobby_received", new Callable(this, nameof(OnGetLobby)));
		socketIOLobby.Connect("game_started", new Callable(this, nameof(OnGameStarted)));
		socketIOLobby.Connect("lobby_closed", new Callable(this, nameof(OnLobbyClosed)));
		socketIOLobby.Connect("join_lobby_confirmed", new Callable(this, nameof(OnJoinLobbyConfirmed)));
 
		var gameState 		= GetNode<Node>("/root/GameState");
		string token 		= gameState.Get("token").AsString();
		_lobbyName			= gameState.Get("lobby_name").AsString();
 
		lobbyNameLabel.Text = _lobbyName;

		socketIOLobby.Connect("socket_ready", new Callable(this, nameof(OnSocketReady)));
		socketIOLobby.Call("connect_to_server", token);
	}
 
	private void OnLobbyRefresh(Variant data)
	{
		return;
	}

	private void OnJoinLobbyConfirmed()
	{
		GD.Print("[WaitingRoom] Join confirmed, requesting lobby data");
		socketIOLobby.Call("get_lobby");
	}
 
	private void OnGetLobby(Variant data)
	{
		GD.Print("[WaitingRoom] OnGetLobby fired, raw: ", data);

		var array = data.AsGodotArray();
		if (array == null || array.Count == 0)
		{
			GD.Print("[WaitingRoom] OnGetLobby: array empty");
			return;
		}
		
		var dict = array[0].AsGodotDictionary();
		if (dict == null)
		{
			GD.Print("[WaitingRoom] OnGetLobby: dict null");
			return;
		}

		if (dict.TryGetValue("owner", out var ownerVar))
		{
			var owner = ownerVar.AsGodotDictionary();
			lobbyOwnerLabel.Text = $"Owner: {owner["member_name"].AsString()}";
			startButton.Visible = true;
			GD.Print("[WaitingRoom] Start button shown for owner: ", owner["member_name"].AsString());
		}
		else
		{
			GD.Print("[WaitingRoom] OnGetLobby: no owner key, keys present: ", dict.Keys);
		}

		if (dict.TryGetValue("members", out var membersVar))
		{
			foreach (var child in playerList.GetChildren())
				child.QueueFree();

			foreach (var member in membersVar.AsGodotArray())
			{
				var m = member.AsGodotDictionary();
				var lbl = new Label();
				lbl.Text = m["member_name"].AsString();
				playerList.AddChild(lbl);
			}
		}

		leaveButton.Visible = true;
	}

	private void OnSocketReady()
	{
		GD.Print("[WaitingRoom] Socket ready, joining: ", _lobbyName);
		socketIOLobby.Call("join_lobby", _lobbyName);
	}
	
	private async void OnGameStarted()
	{
		await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);
		GetTree().ChangeSceneToFile("res://scenes/Game/Game.tscn");
	}
 
	public void OnStartPressed()
	{
		startButton.Disabled = true;
		socketIOLobby.Call("start_game");
	}
 
	public void OnLeavePressed()
	{
		GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
	}
 
	public void OnLobbyClosed()
	{
		GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
	}
}