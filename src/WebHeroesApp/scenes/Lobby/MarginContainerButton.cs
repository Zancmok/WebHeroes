using Godot;
using System;

public partial class MarginContainerButton : MarginContainer
{
	public override void _Ready()
	{
		int marginValue = 10;
		int marginValueLeft = 157;
		AddThemeConstantOverride("margin_top", marginValue);
		AddThemeConstantOverride("margin_left", marginValueLeft);
		AddThemeConstantOverride("margin_bottom", marginValue);
		AddThemeConstantOverride("margin_right", marginValue);
		
	}
}
