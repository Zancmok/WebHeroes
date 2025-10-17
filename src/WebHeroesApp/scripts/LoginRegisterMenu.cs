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

		Container testContainer = utilityClass.CreateContainer(this, Control.LayoutPreset.Center);
		CenterContainer testCenterContainer = utilityClass.CreateCenterContainer(testContainer, false, Control.LayoutPreset.Center);
		
		Button buttonLoginPage = utilityClass.CreateButton(testCenterContainer, "MainMenuButtonPlay", new Vector2(10, 10), new Vector2(100,100));
		buttonLoginPage.Pressed += ButtonPressed;

		Button buttonRegisterPage = utilityClass.CreateButton(testCenterContainer, "MainMenuButtonSettings", new Vector2(100, 100), new Vector2(10, 10));
		buttonRegisterPage.Pressed += ButtonPressed;
	}

	private void ButtonPressed()
	{
		GD.Print("ASS");
	}
}
