using Godot;
using System;
using SilenkLibrary;

public partial class SignUpVisuals : HBoxContainer
{
	private UtilityClass utilityClass;
	
	public override void _Ready()
	{
		Button showPassword = GetNode<Button>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/HBoxContainer/ShowPassword");
		LineEdit passwordLine = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/HBoxContainer/VBoxContainer/PasswordInput/PasswordLine");
		LineEdit repeatPasswordLine = GetNode<LineEdit>("CenterContainer_BasePlate/BoxContainer/VBoxContainer/FormSignUp/VBoxContainer/HBoxContainer/VBoxContainer/RepeatPassword/RepeatPasswordLine");
		passwordLine.Secret = true;
		repeatPasswordLine.Secret = true;
		
		showPassword.Pressed += () =>
		{
			passwordLine.Secret = !passwordLine.Secret;
			repeatPasswordLine.Secret = !repeatPasswordLine.Secret;
		};
	}
}
