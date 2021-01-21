import java.io.*; 
import java.net.*; 
  
class UDPClient { 
    public static void main(String args[]) throws Exception 
    { 
  
      BufferedReader inFromUser = 
        new BufferedReader(new InputStreamReader(System.in)); 
  
      DatagramSocket clientSocket = new DatagramSocket(); 
  
  ///////////
 //       System.out.println("Please input server IP address: ");
 //       String IPAddressStr = inFromUser.readLine(); 
 //       System.out.println("IPAddr:" + IPAddressStr); 
 //		InetAddress IPAddress = InetAddress.getByName(IPAddressStr);

      InetAddress IPAddress = InetAddress.getByName("localhost"); 
  
      byte[] sendData = new byte[20]; 
      byte[] receiveData = new byte[20]; 
  
      System.out.println("Please input: ");

      String sentence = inFromUser.readLine(); 
      sendData = sentence.getBytes();
      
      DatagramPacket sendPacket = 
        new DatagramPacket(sendData, sendData.length, IPAddress, 9876); 
		
      clientSocket.send(sendPacket); 
  
      DatagramPacket receivePacket = 
          new DatagramPacket(receiveData, receiveData.length); 
  
      clientSocket.receive(receivePacket); 
  
      String modifiedSentence = 
          new String(receivePacket.getData()); 
  
      System.out.println("FROM SERVER:" + modifiedSentence); 
      clientSocket.close(); 
      } 
} 