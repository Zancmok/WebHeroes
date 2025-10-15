using Godot;
using System;
using SilenkLibrary;
using System.Xml.Serialization;

public partial class MainMenu : Node2D
{
	private Button _button1;
	private UtilityClass util;
	public override void _Ready()
	{
		_button1 = GetNode<Button>("Button1");
		_button1.Text = "YEES";
		_button1.Pressed += ButtonPressed;

		util = new UtilityClass();
		Button myButton = util.CreateButton("MainMenuButtonPlay", new Vector2(500, 500));
		myButton.Pressed += ButtonPressed;
		AddChild(myButton);
		Button myButton2 = util.CreateButton("MainMenuButtonSettings", new Vector2(1000, 1000));
		AddChild(myButton2);
    }


	
	private void ButtonPressed()
	{
		GD.Print("ASS");
	}
}
