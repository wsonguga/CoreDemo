import java.io.*; 
import java.net.*; 
  
class UDPServer { 
  public static void main(String args[]) throws Exception 
    { 
  
      DatagramSocket serverSocket = new DatagramSocket(9876); 
  
      byte[] receiveData = new byte[20]; 
      byte[] sendData  = new byte[20]; 
  
      while(true) 
        { 
  
          DatagramPacket receivePacket = 
             new DatagramPacket(receiveData, receiveData.length); 
           serverSocket.receive(receivePacket);
          
          String sentence = new String(receivePacket.getData()); 
  
          InetAddress IPAddress = receivePacket.getAddress(); 
  
          int port = receivePacket.getPort(); 
  
          String capitalizedSentence = sentence.toUpperCase(); 

          sendData = capitalizedSentence.getBytes(); 

		  System.out.println("Convert:" + sentence + " to: " + capitalizedSentence);

  
          DatagramPacket sendPacket = 
             new DatagramPacket(sendData, sendData.length, IPAddress, 
                               port); 
  
          serverSocket.send(sendPacket); 
        } 
    } 
}