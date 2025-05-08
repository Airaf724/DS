import java.util.*;

public class BullyAlgorithm {
    static int n; // number of processes
    static boolean[] isActive;
    static int coordinator;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // Initialization
        System.out.print("Enter number of processes: ");
        n = sc.nextInt();
        isActive = new boolean[n + 1];

        // Initially all processes are active
        for (int i = 1; i <= n; i++) {
            isActive[i] = true;
        }

        // Set the highest process as coordinator and fail it
        coordinator = n;
        isActive[coordinator] = false;
        System.out.println("Process " + coordinator + " (initial coordinator) has failed.");

        // Optional: Fail other process
        System.out.print("Enter any other process number to fail (0 for none): ");
        int fail = sc.nextInt();
        if (fail != 0 && fail <= n) {
            isActive[fail] = false;
            System.out.println("Process " + fail + " has also failed.");
        }

        // Start election
        System.out.print("Enter the process number that initiates the election: ");
        int initiator = sc.nextInt();
        if (!isActive[initiator]) {
            System.out.println("Initiator process is not active.");
            return;
        }

        System.out.println("\nElection initiated by process " + initiator + "...\n");
        int newCoordinator = startElection(initiator);

        System.out.println("\nNew Coordinator is Process " + newCoordinator);
        informAllProcesses(newCoordinator);
    }

    // Starts election from a given process
    static int startElection(int initiator) {
        int maxRespondingProcess = initiator;

        for (int i = initiator + 1; i <= n; i++) {
            if (isActive[i]) {
                System.out.println("Process " + initiator + " sends Election message to Process " + i);
                System.out.println("Process " + i + " sends OK to Process " + initiator);

                // Higher process starts its own election
                int candidate = startElection(i);
                if (candidate > maxRespondingProcess) {
                    maxRespondingProcess = candidate;
                }
            }
        }

        return maxRespondingProcess;
    }

    // Inform all active processes about new coordinator
    static void informAllProcesses(int coordinator) {
        for (int i = 1; i <= n; i++) {
            if (i != coordinator && isActive[i]) {
                System.out.println("Process " + coordinator + " informs Process " + i + " as new Coordinator");
            }
        }
    }
}