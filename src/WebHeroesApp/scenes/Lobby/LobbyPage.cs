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
	}

	private void OnCreateNewGame()
	{
		// add popup later for naming of the lobby
		lobbyManager.CreateLobby("MyLobby");
	}

	private void OnBack()
	{
		GetTree().ChangeSceneToFile("res://scenes/LoginSignUp/LoginRegisterMenu.tscn");
	}

	private void OnLobbyRefresh(Variant data)
	{
		GD.Print("Lobby list updated: ", data);
		// TODO: populate lobby list UI from the "data"	
	}

	private void OnGameStarted()
	{
		GD.Print("Game started! Switching scenes...");
		// add: GetTree().ChangeSceneToFile("");
	}
}
