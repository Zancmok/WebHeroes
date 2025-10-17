using Godot;
using System;
using SilenkLibrary;

public partial class LoginRegisterPageContainer : Container
{
	private UtilityClass utilityClass;


	public void ButtonSuccess(string name)
	{
		GD.Print($"Success {name}");
	}
	
	public override void _Ready()
	{
		utilityClass = new UtilityClass();

		Container loginRegisterPageContainer = GetNode<Container>("LoginRegisterPageContainer");
		loginRegisterPageContainer.SetAnchorsPreset(Control.LayoutPreset.Center);
		
		HBoxContainer loginRegisterButtonContainer = GetNode<HBoxContainer>("LoginRegisterPageContainer/LoginRegisterButtonContainer");
		loginRegisterButtonContainer.SetAnchorsPreset(Control.LayoutPreset.TopWide);
		
		Button loginButton = GetNode<Button>("LoginRegisterButtonContainer/LoginButton");
		loginButton.Text = "Login";
		loginButton.Pressed += () => ButtonSuccess("Login");
		
		Button registerButton = GetNode<Button>("LoginRegisterButtonContainer/RegisterButton");
		registerButton.Text = "Register";
		registerButton.Pressed += () => ButtonSuccess("Register");
	}
}
