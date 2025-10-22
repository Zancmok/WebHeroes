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

		//HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest"); // add node in editor
		//httpRequest.RequestCompleted += OnRequestCompleted;
		//httpRequest.Request("https://jsonplaceholder.typicode.com/posts/1");



		Control testControl1 = new Control();
		AddChild(testControl1);
		testControl1.SetAnchorsPreset(Control.LayoutPreset.FullRect);
		testControl1.Size = GetViewportRect().Size;
		testControl1.Position = Vector2.Zero;

		CallDeferred(MethodName.DebugSizes, testControl1);
		// dynamic elements
		CenterContainer testCenterContainer1 = utilityClass.CreateCenterContainer(testControl1);

		VBoxContainer vbox = new VBoxContainer();
		vbox.AddThemeConstantOverride("separation", 20);
		testCenterContainer1.AddChild(vbox);

		Button buttonLoginPage = utilityClass.CreateButton(vbox, "MainMenuButtonPlay", new Vector2(200, 50));
		buttonLoginPage.Pressed += () => ButtonPressed("success");

		Button buttonRegisterPage = utilityClass.CreateButton(vbox, "MainMenuButtonSettings", new Vector2(200, 50));
		buttonRegisterPage.Pressed += () => ButtonPressed("success");


		// static elements
		//CenterContainer loginRegisterPageCenterContainer = GetNode<CenterContainer>("LoginRegisterPageCenterContainer");
		//loginRegisterPageCenterContainer.SetAnchorsPreset(Control.LayoutPreset.FullRect);

		//HBoxContainer loginRegisterButtonContainer = GetNode<HBoxContainer>("LoginRegisterPageContainer/LoginRegisterButtonContainer");
		//loginRegisterButtonContainer.SetAnchorsPreset(Control.LayoutPreset.TopWide);

		//Button loginButton = GetNode<Button>("LoginRegisterButtonContainer/LoginButton");
		//loginButton.Text = "Login";
		//loginButton.Pressed += () => ButtonPressed("Login");

		//Button registerButton = GetNode<Button>("LoginRegisterButtonContainer/RegisterButton");
		//registerButton.Text = "Register";
		//registerButton.Pressed += () => ButtonPressed("Register");
	}
	private void ButtonPressed(string response)
	{
		GD.Print($"{response}");
	}

	private void OnRequestCompleted()
	{
		throw new NotImplementedException();
	}

	private void DebugSizes(Control control)
	{
		GD.Print($"testControl1 Size: {control.Size}");
		GD.Print($"testControl1 Position: {control.Position}");
		GD.Print($"Viewport Size: {GetViewportRect().Size}");
	}
}
