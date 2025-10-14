using Godot;
using System;

namespace SilenkLibrary
{
    public partial class UtilityClass : Node2D
    {
        public Button CreateButton(string buttonText, Vector2 position)
        {
            Button newButton = new Button();
            newButton.Text = buttonText;
            newButton.Position = position;
            AddChild(newButton);
            GD.Print("ass");
            return newButton;
        }

        internal void CreateButton(string v, (int, int) value)
        {
            throw new NotImplementedException();
        }
    }
}