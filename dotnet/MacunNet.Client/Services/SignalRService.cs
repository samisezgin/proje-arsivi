using Microsoft.AspNetCore.SignalR.Client;
using System;
using System.Threading.Tasks;

public class SignalRService
{
    private HubConnection _connection;

    public event Action<string, string> OnMessageReceived;

    public async Task Connect()
    {
        _connection = new HubConnectionBuilder()
            .WithUrl("http://localhost:5186/chatHub") // Backend URL'ni güncelle!
            .Build();

        _connection.On<string, string>("ReceiveMessage", (user, message) =>
        {
            OnMessageReceived?.Invoke(user, message);
        });

        await _connection.StartAsync();
    }

    public async Task SendMessage(string user, string message)
    {
        if (_connection.State == HubConnectionState.Connected)
        {
            await _connection.InvokeAsync("SendMessage", user, message);
        }
    }
}
