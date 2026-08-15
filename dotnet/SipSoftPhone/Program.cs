using System;
using System.Net;
using System.Net.Sockets;
using System.Text;

class Program
{
    static void Main(string[] args)
    {
        const int sipPort = 5060; // SIP varsayılan portu
        Console.WriteLine($"SIP Sunucusu {sipPort} üzerinde başlatılıyor...");

        // UDP Soketi başlat
        using (UdpClient udpServer = new UdpClient(sipPort))
        {
            IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);

            while (true)
            {
                try
                {
                    // Gelen mesajı al
                    byte[] receivedBytes = udpServer.Receive(ref remoteEndPoint);
                    string receivedMessage = Encoding.UTF8.GetString(receivedBytes);
                    Console.WriteLine($"\nGelen Mesaj: {receivedMessage}");
                    Console.WriteLine($"Gönderen: {remoteEndPoint.Address}:{remoteEndPoint.Port}");

                    // Gelen mesajı analiz et ve cevap oluştur
                    string response = HandleSipMessage(receivedMessage);

                    // Cevap gönder
                    if (!string.IsNullOrEmpty(response))
                    {
                        byte[] responseBytes = Encoding.UTF8.GetBytes(response);
                        udpServer.Send(responseBytes, responseBytes.Length, remoteEndPoint);
                        Console.WriteLine($"Cevap Gönderildi: {response}");
                    }
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Hata: {ex.Message}");
                }
            }
        }
    }

    static string HandleSipMessage(string message)
    {
        // Mesajın başlığını kontrol et
        if (message.StartsWith("OPTIONS"))
        {
            // Basit bir 200 OK cevabı
            return "SIP/2.0 200 OK\r\n" +
                   "Via: SIP/2.0/UDP 127.0.0.1;branch=z9hG4bK776asdhds\r\n" +
                   "Content-Length: 0\r\n\r\n";
        }
        else if (message.StartsWith("REGISTER"))
        {
            // Kayıt işlemi için bir yanıt oluşturun
            return "SIP/2.0 200 OK\r\n" +
                   "Via: SIP/2.0/UDP 127.0.0.1;branch=z9hG4bK776asdhds\r\n" +
                   "Content-Length: 0\r\n\r\n";
        }

        // Diğer durumlar için cevap döndürme
        return null;
    }
}
