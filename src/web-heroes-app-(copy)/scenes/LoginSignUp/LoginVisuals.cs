using Godot;
using System;
using SilenkLibrary;

public partial class LoginVisuals : VBoxContainer
{
	
	public override void _Ready()
	{
		Button showPassword = GetNode<Button>("PasswordInput/ShowPassword");
		LineEdit passwordLine = GetNode<LineEdit>("PasswordInput/PasswordLine");
		passwordLine.Secret = true;
		
		showPassword.Pressed += () =>
		{
			passwordLine.Secret = !passwordLine.Secret;
		};
	}
}
