# Import the necessary modules
import socket
import threading

# Set the host and port for the server
host_server = '127.0.0.1'
port_server = 5678

# Create a new server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server socket to the host and port
server.bind((host_server, port_server))

# Listen for incoming connections
server.listen()

# Initialize lists to store connected users and their all_user_nicknames
users = []
all_user_nicknames = []

# Function to broadcast a message to all connected users
def broadcast(message):
    for user in users:
        user.send(message)

# Function to handle a single user connection
def handle_user(user):
    while True:
        try:
            # Receive a message from the user
            message = user.recv(1024)
            # Broadcast the message to all users
            broadcast(message)
        except:
            # If an error occurs, remove the user from the list of connected users
            index = users.index(user)
            users.remove(user)
            user.close()
            # Get the user's nick_name and remove it from the list of all_user_nicknames
            nick_name = all_user_nicknames[index]
            all_user_nicknames.remove(nick_name)
            # Broadcast a message indicating that the user has left the chat room
            broadcast(f'{nick_name} has left the chatroom'.encode('utf-8'))
            break

# Main function to handle incoming user connections
def receive():
    while True:
        # Print a message indicating that the server is running and listening for connections
        print('server is running and listening ...')
        # Accept a new user connection
        user, address = server.accept()
        # Print a message indicating that a new connection has been established
        print(f'connection is established with {str(address)}')
        # Ask the user to choose an nick_name
        user.send('nick_name?'.encode('utf-8'))
        # Receive the nick_name from the user
        nick_name = user.recv(1024)
        # Add the user and their nick_name to the appropriate lists
        all_user_nicknames.append(nick_name)
        users.append(user)
        # Print a message indicating the user's nick_name
        print(f'the nick_name of this user is {nick_name}'.encode('utf-8'))
        # Broadcast a message indicating that the user has joined the chat room
        broadcast(f'{nick_name} has connected to the chat room'.encode('utf-8'))
        # Send a welcome message to the user
        user.send('you are now connected!'.encode('utf-8'))
        # Create a new thread to handle the user's messages
        thread = threading.Thread(target=handle_user, args=(user,))
        thread.start()

# Start the main function to listen for incoming user connections
if __name__ == "__main__":
    receive()
