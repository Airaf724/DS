import java.rmi.*;

public class Server {
    public static void main(String args[]) {

        try {
            ServerImpl s = new ServerImpl();
            System.out.println("Server Started......... ");

            Naming.rebind("Server", s);

        } catch (Exception e) {
            System.out.println("Server Error : " + e.getMessage());

        }
    }
}