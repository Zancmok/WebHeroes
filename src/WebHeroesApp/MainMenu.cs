using Godot;
using System;
using SilenkLibrary;
using System.Xml.Serialization;

public partial class MainMenu : Node2D
{
	private Button _button1;
	public override void _Ready()
	{
		_button1 = GetNode<Button>("Button1");
		_button1.Text = "YEES";
		_button1.Pressed += ButtonPressed;



		UtilityClass something = new UtilityClass();
		something.CreateButton("test", (500, 500));
    }


	
	private void ButtonPressed()
	{
		GD.Print("ASS");
	}
}
