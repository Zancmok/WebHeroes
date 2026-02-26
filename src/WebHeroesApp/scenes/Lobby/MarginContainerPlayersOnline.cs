using Godot;
using System;


public partial class MarginContainerPlayersOnline : MarginContainer
{
	public override void _Ready()
	{
		int marginValueRight = 150;
		int marginValue = 10;
		AddThemeConstantOverride("margin_top", marginValue);
		AddThemeConstantOverride("margin_left", marginValue);
		AddThemeConstantOverride("margin_bottom", marginValue);
		AddThemeConstantOverride("margin_right", marginValueRight);
	}
}
