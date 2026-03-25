using Godot;
using System.Collections.Generic;
 
public class HttpQueue
{
    public record RequestData(string Url, string Body, string[] Headers);
 
    private readonly Queue<RequestData> _queue = new();
    private bool _inProgress = false;
    private readonly HttpRequest _node;
 
    public HttpQueue(HttpRequest node)
    {
        _node = node;
    }
 
    public void Enqueue(string url, string body = "{}", string[] headers = null)
    {
        headers ??= ["Content-Type: application/json"];
        _queue.Enqueue(new RequestData(url, body, headers));
        Process();
    }
 
    public void OnCompleted()
    {
        _inProgress = false;
        Process();
    }
 
    private void Process()
    {
        if (_inProgress || _queue.Count == 0) return;
        var next = _queue.Dequeue();
        _inProgress = true;
        _node.Request(next.Url, next.Headers, HttpClient.Method.Post, next.Body);
    }
}
 