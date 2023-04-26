# Import the necessary modules
import threading
import socket

# Get an nick_name from the user
nick_name = input('choose an nick_name >>> ')

# Create a new user socket
user = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the user socket to a server
user.connect(('127.0.0.1',5678))

# Define a function to receive messages from the server
def user_receive():
    while True:
        try:
            # Receive a message from the server
            message = user.recv(1024).decode('utf-8')
            # If the server requests an nick_name, send it
            if message == "nick_name?":
                user.send(nick_name.encode('utf-8'))
            # Otherwise, print the message
            else:
                print(message)
        # If an error occurs, close the user socket and break the loop
        except:
            print("error!")
            user.close()
            break

# Define a function to send messages to the server
def user_send():
    while True:
        # Get a message from the user and format it with the nick_name
        message = f'{nick_name}: {input("")}'
        # Send the message to the server
        user.send(message.encode('utf-8'))

# Create a new thread to receive messages from the server
receive_thread = threading.Thread(target=user_receive)
receive_thread.start()

# Create a new thread to send messages to the server
send_thread = threading.Thread(target=user_send)
send_thread.start()
