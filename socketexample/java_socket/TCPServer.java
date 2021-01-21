import java.io.*; 
import java.net.*; 

class TCPServer { 

  public static void main(String argv[]) throws Exception 
    { 
      String clientSentence; 
      String capitalizedSentence; 

      ServerSocket welcomeSocket = new ServerSocket(6789); 
  
      while(true) { 
  
           Socket connectionSocket = welcomeSocket.accept(); 
		   System.out.println("...1...!");

           BufferedReader inFromClient = 
              new BufferedReader(new
              InputStreamReader(connectionSocket.getInputStream())); 

           DataOutputStream  outToClient = 
             new DataOutputStream(connectionSocket.getOutputStream()); 

			 		   System.out.println("...2...!");

           clientSentence = inFromClient.readLine(); 
		   		   System.out.println("...3...!");


           capitalizedSentence = clientSentence.toUpperCase(); 

		   System.out.println("Convert:" + clientSentence + " to: " + capitalizedSentence);

           outToClient.writeBytes(capitalizedSentence); 
		   connectionSocket.close();
        } 
    } 
} 