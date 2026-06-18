using Godot;
using System;

public partial class TabsWork : VBoxContainer
{
	public override void _Ready()
	{
		Button loginTab = GetNode<Button>("Tabs/LoginTab");
		Button signUpTab = GetNode<Button>("Tabs/SignUpTab");
		VBoxContainer loginForm = GetNode<VBoxContainer>("FormLogin");
		VBoxContainer signUpForm = GetNode<VBoxContainer>("FormSignUp");
		
		loginTab.Pressed += () => ToggleTabs(loginForm, signUpForm);
		signUpTab.Pressed += () => ToggleTabs(signUpForm, loginForm);
	}
	
	private void ToggleTabs(VBoxContainer toggleOn, VBoxContainer toggleOff)
	{
		toggleOff.Visible = false;
		toggleOn.Visible = true;
	}
}
