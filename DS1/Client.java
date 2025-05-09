import java.rmi.*;
import java.util.*;

public class Client {
    public static void main(String args[]) {
        Scanner sc = new Scanner(System.in);

        try {
            String serverURL = "rmi://localhost/Server";
            ServerIntf serverIntf = (ServerIntf) Naming.lookup(serverURL);
            double num1, num2;
            System.out.print("Enter num1.");
            num1 = sc.nextDouble();

            System.out.print("Enter num2.");
            num2 = sc.nextDouble();

            System.out.println("--------------------------Results--------------------------.");
            System.out.println("Addition is : " + serverIntf.addition(num1, num2));
            System.out.println("Subtraction is : " + serverIntf.subtraction(num1, num2));
            System.out.println("Multiplication is : " + serverIntf.multiplication(num1, num2));
            System.out.println("Division is : " + serverIntf.division(num1, num2));

        } catch (Exception e) {
            System.out.println("Exception occurred at client: " + e);
            e.printStackTrace();

        }
    }
}