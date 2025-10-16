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

        public Container CreateContainer(Node parent, Vector2 position)
        {
            Container newContainer = new Container();
            newContainer.RectPosition = position;
            return newContainer;
        }
    }
}