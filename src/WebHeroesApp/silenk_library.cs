using Godot;
using System;

namespace silenk_library
{
    public partial class Utility_class : Node2D
    {
        public Button createButton(string buttonText, Vector2 position)
        {
            Button newButton = new Button();
            newButton.Text = buttonText;
            newButton.Position = position;
            AddChild(newButton);
            GD.Print("ass");
            return newButton;
        }
    }
}