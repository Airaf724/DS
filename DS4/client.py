# client.py
from dateutil import parser
import threading
import datetime
import socket
import time

# Function to continuously send client's local time to the server
def startSendingTime(slave_client):
    while True:
        try:
            # Send current time to server
            slave_client.send(str(datetime.datetime.now()).encode())
            print("Local time sent to server.\n")
            time.sleep(5)
        except Exception as e:
            print(f"Error sending time: {e}")
            break

# Function to receive synchronized time from the server
def startReceivingTime(slave_client):
    while True:
        try:
            # Receive time from server
            synchronized_time = parser.parse(slave_client.recv(1024).decode())
            print(f"Synchronized time received from server: {synchronized_time}\n")
        except Exception as e:
            print(f"Error receiving time: {e}")
            break

# Function to initialize and connect client to server
def initiateSlaveClient(port=8080):
    slave_client = socket.socket()

    try:
        # Connect to the server on localhost
        slave_client.connect(('127.0.0.1', port))
        print("Connected to clock server.\n")

        # Thread to send local time
        send_time_thread = threading.Thread(target=startSendingTime, args=(slave_client,))
        send_time_thread.start()

        # Thread to receive synchronized time
        receive_time_thread = threading.Thread(target=startReceivingTime, args=(slave_client,))
        receive_time_thread.start()

    except Exception as e:
        print(f"Could not connect to server: {e}")

# Main driver
if __name__ == '__main__':
    initiateSlaveClient(port=8080)
