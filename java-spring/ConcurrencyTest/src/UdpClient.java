import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UdpClient {
    public static void main(String[] args) {
        String message = "INVITE sip:alice@example.com SIP/2.0\r\nCall-ID: 1234567890abcdef\r\n\r\n";
        String serverHost = "localhost"; // veya sunucu IP'si
        int serverPort = 5060; // Sunucu tarafında açtığın port

        try (DatagramSocket socket = new DatagramSocket()) {
            byte[] buffer = message.getBytes();

            InetAddress address = InetAddress.getByName(serverHost);
            DatagramPacket packet = new DatagramPacket(buffer, buffer.length, address, serverPort);

            socket.send(packet);
            System.out.println("Mesaj gönderildi: " + message);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
