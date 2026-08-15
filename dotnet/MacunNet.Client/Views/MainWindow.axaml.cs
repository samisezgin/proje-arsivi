using Avalonia.Controls;
using Avalonia.Interactivity;
using System.Collections.ObjectModel;

namespace MacunNet.Client.Views
{
    public partial class MainWindow : Window
    {
        private readonly SignalRService _signalRService;
        public ObservableCollection<string> Messages { get; } = new();

        public MainWindow()
        {
            InitializeComponent();
            _signalRService = new SignalRService();
            _signalRService.OnMessageReceived += (user, message) =>
            {
                Messages.Add($"{user}: {message}");
            };
            _signalRService.Connect();
            DataContext = this;

            // **Click eventini burada bağlıyoruz**
            var sendMessageButton = this.FindControl<Button>("SendMessageButton");
            sendMessageButton.Click += OnSendMessageClicked;
        }

        private void OnSendMessageClicked(object? sender, RoutedEventArgs e)
        {
            var user = this.FindControl<TextBox>("UserInput").Text;
            var message = this.FindControl<TextBox>("MessageInput").Text;

            if (!string.IsNullOrEmpty(user) && !string.IsNullOrEmpty(message))
            {
                _signalRService.SendMessage(user, message);
            }
        }
    }
}
