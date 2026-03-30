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
 
		var gameState 		= GetNode<Node>("/root/GameState");
		string token 		= gameState.Get("token").AsString();
		string savedName	= gameState.Get("lobby_name").AsString();
 
		lobbyNameLabel.Text = savedName;

		socketIOLobby.Connect("socket_ready", new Callable(this, nameof(OnSocketReady)));
		socketIOLobby.Call("connect_to_server", token);
	}
 
	private void OnLobbyRefresh(Variant data)
	{
		return;
	}
 
	private void OnGetLobby(Variant data)
	{
		// Unwrap array wrapper
		var array = data.AsGodotArray();
		if (array == null || array.Count == 0) return;
		
		var dict = array[0].AsGodotDictionary();
		if (dict == null) return;

		if (dict.TryGetValue("owner", out var ownerVar))
		{
			var owner = ownerVar.AsGodotDictionary();
			GD.Print(owner.ToString());
			lobbyOwnerLabel.Text = $"Owner: {owner["member_name"].AsString()}";
			startButton.Visible = true;
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
		socketIOLobby.Call("get_lobby");
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
		socketIOLobby.Call("disconnect_from_server");
		GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
	}
 
	public void OnLobbyClosed()
	{
		GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
	}
}
