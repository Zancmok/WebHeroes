using Godot;
using System;
using System.Text;
using SilenkLibrary;

public partial class LoginSignUpPage : Control
{
	private UtilityClass utilityClass;
	private string testHttp = "http://127.0.0.1:5000/";
	private string testHttpResult;
	
	public override void _Ready()
	{
		HttpRequest CallZancock = GetNode<HttpRequest>("CallZancock");
		CallZancock.RequestCompleted += OnRequestCompleted;
		CallZancock.Request(testHttp);
	}
	
	private void OnRequestCompleted(long result, long responseCode, string[] headers, byte[] body)
	{
		Godot.Collections.Dictionary json = Json.ParseString(Encoding.UTF8.GetString(body)).AsGodotDictionary();
		GD.Print(json);
		testHttpResult = json.ToString();
	}
	
	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey eventKey)
		{
			if (eventKey.Pressed && eventKey.Keycode == Key.F3)
			{
				GD.Print($"{testHttp}");
				GD.Print($"{testHttpResult}");
			}
		}
	}
}
