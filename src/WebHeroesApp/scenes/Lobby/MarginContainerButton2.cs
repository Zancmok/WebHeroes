using Godot;
using System;

public partial class MarginContainerButton2 : MarginContainer
{
	public override void _Ready()
	{
		int marginValue = 10;
		int marginValueRight = 150;
		AddThemeConstantOverride("margin_top", marginValue);
		AddThemeConstantOverride("margin_left", marginValue);
		AddThemeConstantOverride("margin_bottom", marginValue);
		AddThemeConstantOverride("margin_right", marginValueRight);
		
	}
}
