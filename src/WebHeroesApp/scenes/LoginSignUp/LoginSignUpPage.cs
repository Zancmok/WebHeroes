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
	private string testLink = "https://localhost";
	private string testHttpResult;
	private HttpRequest httpRequest;
	private HttpQueue httpQueue;
	public string currentUserToken;
 
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
 
			GetTree().ChangeSceneToFile("res://scenes/Lobby/Lobby.tscn");
		}
		else if (doc.TryGetProperty("object-type", out var typeProp) && typeProp.GetString() == "success-response" && responseCode == 201)
		{
			// if signing up is successful, login automatically
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
 
			httpQueue.Enqueue($"{testLink}/user-management/signup", jsonString);
			httpQueue.Enqueue($"{testLink}/user-management/login", jsonString);
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
 
		httpQueue.Enqueue($"{testLink}/user-management/login", jsonString);
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
				GD.Print($"{testLink}");
				GD.Print($"{testHttpResult}");
				GD.Print(currentUserToken);
			}
		}
	}
}
