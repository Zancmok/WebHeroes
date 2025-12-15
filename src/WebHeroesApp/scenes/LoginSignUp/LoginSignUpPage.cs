using Godot;
using System;
using System.Text;
using SilenkLibrary;
using System.Net.Http.Headers;
using System.ComponentModel.DataAnnotations;
using System.Text.Json;
using SocketIOClient;

public partial class LoginSignUpPage : Control
{
	private UtilityClass utilityClass;
	private SocketIO _socket;
	private string testHttp = "http://127.0.0.1:5000/ping";
	private string testHttpResult;
	private HttpRequest httpRequest;
	public string currentUserToken;
		
	public override void _Ready()
	{
		httpRequest = GetNode<HttpRequest>("CallZancock");
		httpRequest.RequestCompleted += OnRequestCompleted;
		
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
		string json = Encoding.UTF8.GetString(body);
		GD.Print(json);
		currentUserToken = JsonDocument.Parse(json).RootElement.GetProperty("token").GetString();
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
			var jsonData = new Godot.Collections.Dictionary
			{
				{"username", usernameData},
				{"password", passwordData}
			};
			
			string jsonString = Json.Stringify(jsonData);
			GD.Print(jsonString);

			MakePostRequest("http://127.0.0.1:5000/user-management/signup", jsonString);
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
		
		var jsonData = new Godot.Collections.Dictionary
		{
			{"username", usernameData},
			{"password", passwordData}
		};
		
		string jsonString = Json.Stringify(jsonData);
		GD.Print(jsonString);

		MakePostRequest("http://127.0.0.1:5000/user-management/login", jsonString);
	}
	
	private void MakePostRequest(string url, string body, string[] headers = null)
	{
		if (headers == null)
		{
			headers = ["Content-Type: application/json"];
		}
		
		httpRequest.Request(url, headers, HttpClient.Method.Post, body);
	}
	
	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey eventKey)
		{
			if (eventKey.Pressed && eventKey.Keycode == Key.F3)
			{
				GD.Print($"{testHttp}");
				GD.Print($"{testHttpResult}");
				GD.Print(currentUserToken);
			}
		}
	}
}
