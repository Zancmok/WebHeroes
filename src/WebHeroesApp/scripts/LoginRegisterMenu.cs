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

		Button buttonLoginPage = utilityClass.CreateButton(this, "MainMenuButtonPlay", new Vector2(10, 10), new Vector2(100,100));
		buttonLoginPage.Pressed += ButtonPressed;

		Button buttonRegisterPage = utilityClass.CreateButton(this, "MainMenuButtonSettings", new Vector2(100, 100), new Vector2(10, 10));
		buttonRegisterPage.Pressed += ButtonPressed;
	}

	private void ButtonPressed()
	{
		GD.Print("ASS");
	}
}
