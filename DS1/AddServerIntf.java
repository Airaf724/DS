import java.rmi.*;

public interface AddServerIntf extends Remote {
    double add(double a, double b) throws RemoteException;
}
