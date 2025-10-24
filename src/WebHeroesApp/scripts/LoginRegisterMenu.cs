using Godot;
using System;
using SilenkLibrary;
using System.Xml.Serialization;
using System.Numerics;


public partial class LoginRegisterMenu : Control
{
	private UtilityClass utilityClass;
	const string testLink = "https://bug-free-space-parakeet-x5rgqx99q679h9pp6-5000.app.github.dev/";

	public override void _Ready()
	{
		GD.Print("MainMenu _ready() called!");
		utilityClass = new UtilityClass();

		HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest"); // add node in editor
		httpRequest.Request($"{testLink}/user-management/signup", null, Godot.HttpClient.Method.Post);
		
		this.Size = GetViewportRect().Size;
		this.Position = Godot.Vector2.Zero;
		this.SetAnchorsPreset(Control.LayoutPreset.FullRect);

		// dynamic elements
		CenterContainer lRPageAtlas = utilityClass.CreateCenterContainer(this);
		
		VBoxContainer lRPage = utilityClass.CreateVBoxContainer(lRPageAtlas, "separation", 10);
		HBoxContainer loginRegisterButtonStand = utilityClass.CreateHBoxContainer(lRPage, "separation", 10);
		VBoxContainer loginFormStand = utilityClass.CreateVBoxContainer(lRPage, "separation", 10);
		VBoxContainer registerFormStand = utilityClass.CreateVBoxContainer(lRPage, "separation", 10);
		
		// loginRegisterButtonStand buttons
		Button buttonLoginPage = utilityClass.CreateButton(loginRegisterButtonStand, "Login", new Godot.Vector2(200, 50));
		buttonLoginPage.Pressed += () => ButtonPressed("success");
		buttonLoginPage.Pressed += () => ToggleContainerVisibility(registerFormStand, loginFormStand);

		Button buttonRegisterPage = utilityClass.CreateButton(loginRegisterButtonStand, "Register", new Godot.Vector2(200, 50));
		buttonRegisterPage.Pressed += () => ButtonPressed("success");
		buttonRegisterPage.Pressed += () => ToggleContainerVisibility(loginFormStand, registerFormStand);

		// loginFormStand form
		//text that says Username
		Label userNameInputLabel = new Label();
		userNameInputLabel.Text = "Username";
		loginFormStand.AddChild(userNameInputLabel);
		
		//input bar for Username
		LineEdit userNameInput = new LineEdit();
		userNameInput.CustomMinimumSize = new Godot.Vector2(0,50);
		loginFormStand.AddChild(userNameInput);

		//text that says Password
		Label passWordInputLabel = new Label();
		passWordInputLabel.Text = "Password";
		loginFormStand.AddChild(passWordInputLabel);
		
		// password bit container
		HBoxContainer passWordRow = utilityClass.CreateHBoxContainer(loginFormStand, "separation", 10);
		//input bar for Password
		LineEdit passWordInput = new LineEdit();
		passWordInput.CustomMinimumSize = new Godot.Vector2(0, 50);
		passWordInput.SizeFlagsHorizontal = Control.SizeFlags.ExpandFill;
		passWordInput.Secret = true;
		passWordInput.SecretCharacter = "*";
		passWordRow.AddChild(passWordInput);
		//hide Password button
		Button showPassWord = utilityClass.CreateButton(passWordRow, "Show", new Godot.Vector2(50, 50));
		showPassWord.Pressed += () =>
		{
			passWordInput.Secret = !passWordInput.Secret;
		};

		// login button
		utilityClass.CreateButton(loginFormStand, "Login", new Godot.Vector2(0, 50));

		// register button
		utilityClass.CreateButton(registerFormStand, "Register", new Godot.Vector2(0, 50));
		
		
		

		// registerFormStand form
		Label userNameInputLabel1 = new Label();
		
		CallDeferred(MethodName.DebugSizes, this);
	}
	
	private void ButtonPressed(string response)
	{
		GD.Print($"{response}");
	}

	private void OnRequestCompleted()
	{
		throw new NotImplementedException();
	}

	public void ToggleContainerVisibility(VBoxContainer myContainerInvisible, VBoxContainer myContainerVisible)
	{
		myContainerInvisible.Visible = false;
		myContainerVisible.Visible = true;
	}

	private void DebugSizes(Control control)
	{
		GD.Print($"testControl1 Size: {control.Size}");
		GD.Print($"testControl1 Position: {control.Position}");
		GD.Print($"Viewport Size: {GetViewportRect().Size}");
	}
}
