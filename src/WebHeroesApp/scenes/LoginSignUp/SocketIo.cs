using Godot;
using System;

public partial class SocketIo : Node
{
	public override void _Ready()
	{
		Connect("message_received", new Callable(this, nameof(OnMessage)));
		//Connect("connect_socket", new Callable(this, nameof(ConnectSocket)));
	}
	
	private void OnMessage(Variant data)
	{
		GD.Print("Received: ", data.AsString());
	}
	
	public void SendMessage(string message)
	{
		GD.Print("C# SendMessage:", message);
		EmitSignal("refresh");
	}
	
	//private void ConnectSocket()
}
