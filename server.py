# Import the necessary modules
import socket
import threading

# Set the host and port for the server
host = '127.0.0.1'
port = 5678

# Create a new server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the host and port
server.bind((host, port))

# Listen for incoming connections
server.listen()

# Initialize lists to store connected clients and their aliases
clients = []
aliases = []

# Function to broadcast a message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Function to handle a single client connection
def handle_client(client):
    while True:
        try:
            # Receive a message from the client
            message = client.recv(1024)
            # Broadcast the message to all clients
            broadcast(message)
        except:
            # If an error occurs, remove the client from the list of connected clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            # Get the client's alias and remove it from the list of aliases
            alias = aliases[index]
            aliases.remove(alias)
            # Broadcast a message indicating that the client has left the chat room
            broadcast(f'{alias} has left the chatroom'.encode('utf-8'))
            break

# Main function to handle incoming client connections
def receive():
    while True:
        # Print a message indicating that the server is running and listening for connections
        print('server is running and listening ...')
        # Accept a new client connection
        client, address = server.accept()
        # Print a message indicating that a new connection has been established
        print(f'connection is established with {str(address)}')
        # Ask the client to choose an alias
        client.send('alias?'.encode('utf-8'))
        # Receive the alias from the client
        alias = client.recv(1024)
        # Add the client and their alias to the appropriate lists
        aliases.append(alias)
        clients.append(client)
        # Print a message indicating the client's alias
        print(f'the alias of this client is {alias}'.encode('utf-8'))
        # Broadcast a message indicating that the client has joined the chat room
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        # Send a welcome message to the client
        client.send('you are now connected!'.encode('utf-8'))
        # Create a new thread to handle the client's messages
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Start the main function to listen for incoming client connections
if __name__ == "__main__":
    receive()
