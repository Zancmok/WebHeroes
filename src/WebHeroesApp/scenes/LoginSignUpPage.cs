using Godot;
using System;
using SilenkLibrary;

public partial class LoginSignUpPage : Control
{
	private UtilityClass utilityClass;
	
	public override void _Ready()
	{
		Button showPassword = GetNode<Button>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormLogin/VBoxContainer/PasswordInput/ShowPassword");
		LineEdit passwordLine = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormLogin/VBoxContainer/PasswordInput/PasswordLine");
		passwordLine.Secret = true;
		
		showPassword.Pressed += () =>
		{
			passwordLine.Secret = !passwordLine.Secret;
		};
		
		
	}
}
