using Godot;
using System;

namespace SilenkLibrary
{
	public partial class UtilityClass : Node2D
	{
		public Button CreateButton(Node parent, string buttonText, Vector2 position, Vector2 size)
		{
			Button newButton = new Button();
			newButton.Text = buttonText;
			newButton.Position = position;
			newButton.CustomMinimumSize = size;
			parent.AddChild(newButton);
			return newButton;
		}

		public Container CreateContainer(Node parent, Control.LayoutPreset preset)
		{
			Container newContainer = new Container();
			newContainer.SetAnchorsPreset(preset);
			parent.AddChild(newContainer);
			return newContainer;
		}

		public CenterContainer CreateCenterContainer(Node parent, bool useTopLeft, Control.LayoutPreset preset)
		{

			CenterContainer newCenterContainer = new CenterContainer();
			newCenterContainer.UseTopLeft = useTopLeft;
			newCenterContainer.SetAnchorsPreset(preset);
			parent.AddChild(newCenterContainer);
			return newCenterContainer;
        }
	}
}
