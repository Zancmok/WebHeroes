using Godot;
using System;
using System.Text.Json;

public partial class UserManagementLobby : Node
{
    private Node socketIOLobby;
    public string Token { get; set; }

    public override void _Ready()
    {
        socketIOLobby = GetNode<Node>("../SocketIOLobby");

        // Connect signals from GDScript to C# methods
        socketIOLobby.Connect("lobby_refresh_received", 
            new Callable(this, nameof(OnLobbyRefresh)));
        socketIOLobby.Connect("lobby_created", 
            new Callable(this, nameof(OnLobbyCreated)));
    }

    public void ConnectToServer(string token)
    {
        Token = token;
        socketIOLobby.Call("connect_to_server", token);
    }

    public void Refresh()
    {
        socketIOLobby.Call("refresh");
    }

    public void CreateLobby(string lobbyName)
    {
        socketIOLobby.Call("create_lobby", lobbyName);
    }

    public void JoinLobby(string lobbyName)
    {
        socketIOLobby.Call("join_lobby", lobbyName);
    }

    private void OnLobbyRefresh(Variant data)
    {
        GD.Print("Lobby refresh received: ", data);
        // TODO: parse data and update UI
        // data will be a Godot Dictionary with "members" and "lobbies" arrays
    }

    private void OnLobbyCreated(Variant data)
    {
        GD.Print("Lobby created response: ", data);
    }
}