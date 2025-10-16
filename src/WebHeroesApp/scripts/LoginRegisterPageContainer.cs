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

		Container idiotContainer = utilityClass.CreateContainer(this, new Vector2(100, 100));

		Container loginRegisterPageContainer = GetNode<Container>("LoginRegisterPageContainer");
		loginRegisterPageContainer.Position = new Vector2(1000, 1000);
		
		HBoxContainer loginRegisterButtonContainer = GetNode<HBoxContainer>("LoginRegisterPageContainer/LoginRegisterButtonContainer");
		loginRegisterButtonContainer.Position = new Vector2(1000,1000);
		
		Button loginButton = GetNode<Button>("LoginRegisterButtonContainer/LoginButton");
		loginButton.Text = "Login";
		loginButton.Pressed += () => ButtonSuccess("Login");
		
		Button registerButton = GetNode<Button>("LoginRegisterButtonContainer/RegisterButton");
		registerButton.Text = "Register";
		registerButton.Pressed += () => ButtonSuccess("Register");
	}
}
