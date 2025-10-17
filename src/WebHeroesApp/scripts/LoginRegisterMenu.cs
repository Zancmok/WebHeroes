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
}
