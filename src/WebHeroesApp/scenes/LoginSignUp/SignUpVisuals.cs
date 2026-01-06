using Godot;
using System;
using SilenkLibrary;

public partial class SignUpVisuals : HBoxContainer
{
	
	public override void _Ready()
	{
		Button showPassword = GetNode<Button>("ShowPassword");
		LineEdit passwordLine = GetNode<LineEdit>("VBoxContainer/PasswordInput/PasswordLine");
		LineEdit repeatPasswordLine = GetNode<LineEdit>("VBoxContainer/RepeatPassword/RepeatPasswordLine");
		passwordLine.Secret = true;
		repeatPasswordLine.Secret = true;
		
		showPassword.Pressed += () =>
		{
			passwordLine.Secret = !passwordLine.Secret;
			repeatPasswordLine.Secret = !repeatPasswordLine.Secret;
		};
	}
}
