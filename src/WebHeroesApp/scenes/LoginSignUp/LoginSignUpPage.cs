using Godot;
using System;
using System.Text;
using SilenkLibrary;
using System.Text.Json;
using System.Collections.Generic;
 
public partial class LoginSignUpPage : Control
{
	private UtilityClass utilityClass;
	private UserManagement userManagement;
	private string realHttps = "https://webheroes.duckdns.org:9027";
	private string testLink = "http://localhost";
	private string testHttpResult;
	private HttpRequest httpRequest;
	private HttpQueue httpQueue;
	public string currentUserToken;
	private Node _socketIOLobby;
	private bool _debugMode = false;
 
	public override void _Ready()
	{
		httpRequest = GetNode<HttpRequest>("CallZancock");
		httpRequest.RequestCompleted += OnRequestCompleted;
		httpQueue = new HttpQueue(httpRequest);
 
		Button signUpSubmit = GetNode<Button>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/Submit");
		signUpSubmit.Pressed += () =>
		{
			SignUp();
		};
 
		Button loginSubmit = GetNode<Button>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormLogin/VBoxContainer/Submit");
		loginSubmit.Pressed += () =>
		{
			Login();
		};


		// --- DEBUG BUTTON ---
		// Grab the SocketIO node that's already in the scene
		_socketIOLobby = GetNode<Node>("SocketIOLobby");  // already in scene as UserManagement

		var debugBtn = new Button();
		debugBtn.Text = "DEBUG: Login + Start Game";
		debugBtn.Position = new Vector2(20, 20);
		debugBtn.AddThemeColorOverride("font_color", new Color(1, 0.3f, 0.3f));
		AddChild(debugBtn);
		debugBtn.Pressed += OnDebugStart;
	}
 
private void OnRequestCompleted(long result, long responseCode, string[] headers, byte[] body)
{
    GD.Print("Response code: ", responseCode);
    string json = Encoding.UTF8.GetString(body);
    GD.Print("Response body: ", json);

    httpQueue.OnCompleted();

    if (string.IsNullOrEmpty(json)) return;

    var doc = JsonDocument.Parse(json).RootElement;

    if (doc.TryGetProperty("token", out var tokenProp))
    {
        currentUserToken = tokenProp.GetString();
        GD.Print("Token saved: ", currentUserToken);

        var gameState = GetNode<Node>("/root/GameState");
        gameState.Set("token", currentUserToken);

        if (_debugMode)
        {
            _debugMode = false;
            // Connect socket and fire debug_create_and_start
            _socketIOLobby.Connect("socket_ready",
                new Callable(this, nameof(OnDebugSocketReady)), (uint)ConnectFlags.OneShot);
            _socketIOLobby.Connect("debug_game_ready",
                new Callable(this, nameof(OnDebugGameReady)), (uint)ConnectFlags.OneShot);
            _socketIOLobby.Call("connect_to_server", currentUserToken);
        }
        else
        {
            GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
        }
    }
    else if (doc.TryGetProperty("object_type", out var typeProp) 
             && typeProp.GetString() == "success-response" 
             && responseCode == 201)
    {
        Login();
    }
}
 
	private void SignUp()
	{
		utilityClass = new UtilityClass();
		LineEdit username = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/UsernameInput/UsernameLine");
		LineEdit password = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/HBoxContainer/VBoxContainer/PasswordInput/PasswordLine");
		LineEdit repeatPassword = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/HBoxContainer/VBoxContainer/RepeatPassword/RepeatPasswordLine");
 
		string usernameData = username.Text;
		string passwordData = password.Text;
		string repeatPasswordData = repeatPassword.Text;
 
		if (passwordData == repeatPasswordData)
		{
			var gameState = GetNode<Node>("/root/GameState");
			gameState.Set("username", usernameData);
 
			var jsonData = new Godot.Collections.Dictionary
			{
				{"username", usernameData},
				{"password", passwordData}
			};
 
			string jsonString = Json.Stringify(jsonData);
			GD.Print(jsonString);
 
			httpQueue.Enqueue($"{realHttps}/user-management/signup", jsonString);
			httpQueue.Enqueue($"{realHttps}/user-management/login", jsonString);
		}
		else
		{
			AcceptDialog alert = utilityClass.CreateAcceptDialog(this, "Warning", "Your password does not match your repeated password!");
		}
	}
 
	private void Login()
	{
		LineEdit username = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormLogin/VBoxContainer/UsernameInput/UsernameLine");
		LineEdit password = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormLogin/VBoxContainer/PasswordInput/PasswordLine");
 
		string usernameData = username.Text;
		string passwordData = password.Text;
 
		var gameState = GetNode<Node>("/root/GameState");
		gameState.Set("username", usernameData);
 
		var jsonData = new Godot.Collections.Dictionary
		{
			{"username", usernameData},
			{"password", passwordData}
		};
 
		string jsonString = Json.Stringify(jsonData);
		GD.Print(jsonString);
 
		httpQueue.Enqueue($"{realHttps}/user-management/login", jsonString);
	}
 
	private void OnDebugStart()
	{
		// Step 1: login with hardcoded creds
		var jsonData = new Godot.Collections.Dictionary
		{
			{ "username", "rapor" },
			{ "password", "123" }
		};
		string jsonString = Json.Stringify(jsonData);
		_debugMode = true;
		httpQueue.Enqueue($"{realHttps}/user-management/login", jsonString);
	}

	private void OnDebugSocketReady()
	{
		var gameState = GetNode<Node>("/root/GameState");
		string lobbyName = "debug-lobby-" + Time.GetTicksMsec();
		gameState.Set("lobby_name", lobbyName);
		_socketIOLobby.Call("debug_create_and_start", lobbyName);
	}

	private void OnDebugGameReady()
	{
		GetTree().ChangeSceneToFile("res://scenes/Game/Game.tscn");
	}

	private void Send()
	{
		userManagement.SendMessage("Hello World!");
	}
 
	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey eventKey)
		{
			if (eventKey.Pressed && eventKey.Keycode == Key.F3)
			{
				GD.Print($"{realHttps}");
				GD.Print($"{testHttpResult}");
				GD.Print(currentUserToken);
			}
		}
	}
}
