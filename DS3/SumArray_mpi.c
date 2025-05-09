#include <mpi.h>
#include <stdio.h>

int main(int argc, char *argv[])
{
    int np, pid;
    MPI_Status status;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &pid);
    MPI_Comm_size(MPI_COMM_WORLD, &np);

    int n = 8;
    int a[8] = {1, 2, 3, 4, 5, 6, 7, 8}; // example array
    int elements_per_process = n / np;
    int partial_sum = 0;

    if (pid == 0)
    {
        // Server process
        int index = 0;

        for (int i = 1; i < np; i++)
        {
            index = i * elements_per_process;
            int elements_to_send = (i == np - 1) ? (n - index) : elements_per_process;

            // Send number of elements and elements to client
            MPI_Send(&elements_to_send, 1, MPI_INT, i, 0, MPI_COMM_WORLD);
            MPI_Send(&a[index], elements_to_send, MPI_INT, i, 0, MPI_COMM_WORLD);

            printf("Server sent %d elements to process %d: ", elements_to_send, i);
            for (int j = 0; j < elements_to_send; j++)
            {
                printf("%d ", a[index + j]);
            }
            printf("\n");
        }

        // Partial sum by server (first chunk)
        for (int i = 0; i < elements_per_process; i++)
        {
            partial_sum += a[i];
        }
        printf("Server computed partial sum: %d from elements: ", partial_sum);
        for (int i = 0; i < elements_per_process; i++)
        {
            printf("%d ", a[i]);
        }
        printf("\n");

        // Receive partial sums from clients
        int tmp = 0;
        for (int i = 1; i < np; i++)
        {
            MPI_Recv(&tmp, 1, MPI_INT, MPI_ANY_SOURCE, 0, MPI_COMM_WORLD, &status);
            printf("Server received partial sum %d from process %d\n", tmp, status.MPI_SOURCE);
            partial_sum += tmp;
        }

        printf("\n✅ Total sum of array: %d\n", partial_sum);
    }
    else
    {
        // Client processes
        int n_elements_received = 0;
        MPI_Recv(&n_elements_received, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);
        int received_data[n_elements_received];
        MPI_Recv(&received_data, n_elements_received, MPI_INT, 0, 0, MPI_COMM_WORLD, &status);

        printf("Client %d received %d elements: ", pid, n_elements_received);
        for (int i = 0; i < n_elements_received; i++)
        {
            printf("%d ", received_data[i]);
        }
        printf("\n");

        for (int i = 0; i < n_elements_received; i++)
        {
            partial_sum += received_data[i];
        }

        printf("Client %d computed partial sum: %d\n", pid, partial_sum);

        MPI_Send(&partial_sum, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}