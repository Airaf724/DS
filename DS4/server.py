# server.py
from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

# Dictionary to hold client address and their clock data
client_data = {}

# Function to receive clock time from a connected client
def startReceivingClockTime(connector, address):
    while True:
        try:
            # Receive clock time as string
            clock_time_string = connector.recv(1024).decode()
            # Parse the string to datetime object
            clock_time = parser.parse(clock_time_string)
            # Calculate time difference between server and client
            clock_time_diff = datetime.datetime.now() - clock_time

            # Store client data
            client_data[address] = {
                "clock_time": clock_time,
                "time_difference": clock_time_diff,
                "connector": connector
            }

            print(f"Client data updated from {address}\n")
            time.sleep(5)

        except Exception as e:
            print(f"Error receiving data from {address}: {e}")
            break

# Function to accept incoming client connections
def startConnecting(master_server):
    while True:
        # Accept connection from client
        master_slave_connector, addr = master_server.accept()
        slave_address = f"{addr[0]}:{addr[1]}"
        print(f"{slave_address} connected successfully")

        # Create a thread to receive clock from this client
        current_thread = threading.Thread(
            target=startReceivingClockTime,
            args=(master_slave_connector, slave_address)
        )
        current_thread.start()

# Function to calculate average clock difference
def getAverageClockDiff():
    current_client_data = client_data.copy()

    # List of time differences from all clients
    time_difference_list = [
        client['time_difference'] for client in current_client_data.values()
    ]

    # Sum of all differences
    sum_of_clock_difference = sum(time_difference_list, datetime.timedelta())

    # Average time difference
    average_clock_difference = sum_of_clock_difference / len(current_client_data)
    return average_clock_difference

# Function to synchronize all connected clients
def synchronizeAllClocks():
    while True:
        print("New synchronization cycle started.")
        print(f"Number of clients to be synchronized: {len(client_data)}")

        if len(client_data) > 0:
            average_clock_difference = getAverageClockDiff()

            for client_addr, client in client_data.items():
                try:
                    # Adjust current server time with average difference
                    synchronized_time = datetime.datetime.now() + average_clock_difference
                    client['connector'].send(str(synchronized_time).encode())

                except Exception as e:
                    print(f"Error sending synchronized time to {client_addr}: {e}")
        else:
            print("No client data. Synchronization skipped.")
        print("\n")
        time.sleep(5)

# Function to start the clock server
def initiateClockServer(port=8080):
    # Create socket
    master_server = socket.socket()
    master_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created successfully at master node\n")

    # Bind server to the specified port
    master_server.bind(('', port))
    master_server.listen(10)  # Listen for up to 10 connections
    print("Clock server started and listening...\n")

    # Start a thread to handle client connections
    master_thread = threading.Thread(target=startConnecting, args=(master_server,))
    master_thread.start()

    # Start synchronization thread
    sync_thread = threading.Thread(target=synchronizeAllClocks)
    sync_thread.start()

# Main driver
if __name__ == '__main__':
    initiateClockServer(port=8080)
