# Import the necessary modules
import threading
import socket

# Get an alias from the user
alias = input('choose an alias >>> ')

# Create a new client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client socket to a server
client.connect(('127.0.0.1',5678))

# Define a function to receive messages from the server
def client_receive():
    while True:
        try:
            # Receive a message from the server
            message = client.recv(1024).decode('utf-8')
            # If the server requests an alias, send it
            if message == "alias?":
                client.send(alias.encode('utf-8'))
            # Otherwise, print the message
            else:
                print(message)
        # If an error occurs, close the client socket and break the loop
        except:
            print("error!")
            client.close()
            break

# Define a function to send messages to the server
def client_send():
    while True:
        # Get a message from the user and format it with the alias
        message = f'{alias}: {input("")}'
        # Send the message to the server
        client.send(message.encode('utf-8'))

# Create a new thread to receive messages from the server
receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

# Create a new thread to send messages to the server
send_thread = threading.Thread(target=client_send)
send_thread.start()
