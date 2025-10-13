using Godot;
using System;

public partial class MainMenu : Node2D
{
	public override void _Ready()
	{
		Button button1 = GetNode<Button>("Button1");
		button1.Text = "YEES";
		button1.Pressed += ButtonPressed;
	}
	
	private void ButtonPressed()
	{
		GD.Print("ASS");
	}
}
