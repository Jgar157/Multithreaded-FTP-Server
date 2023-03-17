import socket
import sys

COMMAND_BYTES_IN = 1024
MAX_TCP_CHUNK = 1000


def get_command_from_bits(socket):
    command = socket.recv(COMMAND_BYTES_IN).decode()
    return command


# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 8888))
sock.listen(5)

# Get Connection
(client, address) = sock.accept()
print(address)

while True:
    # Read input from the user on what to handle next
    user_command = get_command_from_bits(client)
    print(user_command)

    if user_command == "upload":
        print("Beginning upload from Client")

        # Receive filename from client
        file_name = client.recv(1024)
        file_name = file_name.decode()
        print("Received File name:", file_name)

        # Update filename to make new copy
        file_name = f"new_{file_name}"

        # Receive file size from client
        file_size = client.recv(1024)
        remaining_bytes = int.from_bytes(file_size, byteorder='big', signed=False)
        print("File size:", remaining_bytes)

        # Open new file and begin writing
        # wb: write bytes
        with open(file_name, 'wb') as target_file:

            while remaining_bytes > 0:
                print("Remaining bytes:", remaining_bytes)
                next_size = min(MAX_TCP_CHUNK, remaining_bytes)  # Only read remaining amount
                chunk = client.recv(next_size)
                target_file.write(chunk)  # Write the received bytes to the file

                # Now that we have written bytes, let us reduce the amount left to read
                remaining_bytes -= next_size

        # Hopefully done writing by here
        print("Finish")


    elif user_command == "get":
        print("Preparing file to send to Client")

    elif user_command == "exit":
        print("~ Exiting Gracefully ~")

    else:
        print("Incorrect command from client")
