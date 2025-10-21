using Godot;
using System;
using SilenkLibrary;
using System.Xml.Serialization;

public partial class LoginRegisterMenu : Node2D
{
	private UtilityClass utilityClass;
	
	public override void _Ready()
	{
		GD.Print("MainMenu _ready() called!");
		utilityClass = new UtilityClass();

		HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest"); // add node in editor
		httpRequest.RequestCompleted += OnRequestCompleted;
		httpRequest.Request("https://jsonplaceholder.typicode.com/posts/1");

		CenterContainer testCenterContainer1 = utilityClass.CreateCenterContainer(this);
		
		Button buttonLoginPage = utilityClass.CreateButton(testCenterContainer1, "MainMenuButtonPlay");
		buttonLoginPage.Pressed += ButtonPressed;

		Button buttonRegisterPage = utilityClass.CreateButton(testCenterContainer1, "MainMenuButtonSettings");
		buttonRegisterPage.Pressed += ButtonPressed;
	}

	private void ButtonPressed()
	{
		GD.Print("ASS");
	}

	private void OnRequestCompleted()
	{
		throw new NotImplementedException();
	}
}
