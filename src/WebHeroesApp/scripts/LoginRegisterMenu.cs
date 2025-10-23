using Godot;
using System;
using SilenkLibrary;
using System.Xml.Serialization;
using System.Numerics;

public partial class LoginRegisterMenu : Control
{
	private UtilityClass utilityClass;

	public override void _Ready()
	{
		GD.Print("MainMenu _ready() called!");
		utilityClass = new UtilityClass();

		//HttpRequest httpRequest = GetNode<HttpRequest>("HTTPRequest"); // add node in editor
		//httpRequest.RequestCompleted += OnRequestCompleted;
		//httpRequest.Request("https://jsonplaceholder.typicode.com/posts/1");
		
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
		buttonLoginPage.Pressed += () => ToggleContainerVisibility(registerFormStand);

		Button buttonRegisterPage = utilityClass.CreateButton(loginRegisterButtonStand, "Register", new Godot.Vector2(200, 50));
		buttonRegisterPage.Pressed += () => ButtonPressed("success");
		buttonRegisterPage.Pressed += () => ToggleContainerVisibility(loginFormStand);

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

	public void ToggleContainerVisibility(VBoxContainer myContainer)
	{
		myContainer.Visible = !myContainer.Visible;
	}

	private void DebugSizes(Control control)
	{
		GD.Print($"testControl1 Size: {control.Size}");
		GD.Print($"testControl1 Position: {control.Position}");
		GD.Print($"Viewport Size: {GetViewportRect().Size}");
	}
}
