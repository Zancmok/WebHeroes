using Godot;
using System;

namespace SilenkLibrary
{
	public partial class UtilityClass
	{
		public Button CreateButton(Node parent, string buttonText, Vector2 size)
		{
			Button newButton = new Button();
			newButton.Text = buttonText;
			newButton.CustomMinimumSize = size;
			parent.AddChild(newButton);
			return newButton;	
		}
		
		public Button CreateButtonExact(Node parent, string buttonText, Vector2 position, Vector2 size)
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

		public CenterContainer CreateCenterContainer(Node parent, bool useTopLeft = false, Control.LayoutPreset preset = Control.LayoutPreset.FullRect)
		{

			CenterContainer newCenterContainer = new CenterContainer();
			newCenterContainer.UseTopLeft = useTopLeft;
			parent.AddChild(newCenterContainer);
			newCenterContainer.SetAnchorsPreset(preset);
			return newCenterContainer;
		}
	}
}
