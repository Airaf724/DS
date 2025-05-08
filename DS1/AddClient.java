import java.rmi.*;

public class AddClient {
    public static void main(String args[]) {
        try {
            String serverURL = "rmi://" + args[0] + "/AddServer";
            AddServerIntf obj = (AddServerIntf) Naming.lookup(serverURL);

            double a = Double.parseDouble(args[1]);
            double b = Double.parseDouble(args[2]);
            double result = obj.add(a, b);
            System.out.println("Sum: " + result);
        } catch (Exception e) {
            System.out.println("Client failed: " + e);
        }
    }
}
