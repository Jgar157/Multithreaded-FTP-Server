import os
import socket
import sys

MAX_CHUNKS_SIZE = 1000

# Core Functions

# Send command type
def send_command(command, socket):
    socket.sendall(command.encode())


# Select File
def select_file() -> str:
    file_name = input("file name: ")
    return file_name


def file_exists(file_name: str) -> bool:
    return os.path.isfile(file_name)


def send_file_name(file_name, socket):
    socket.sendall(file_name.encode())
    # socket.send("\n".encode())


# Create the client socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = input("Please input the target IP Address: ")
port = int(input("Please input the target port: "))

# Try connecting to the server
try:
    sock.connect((ip_address, port))
except ConnectionRefusedError:  # Exit out if unable to connect
    print(f"Error connecting to {ip_address}")
    sys.exit()

# Core loop
# 1) Upload
# 2) Get
# 3) Exit
while True:
    choice = input("Choose one of the following: \n"
                   "upload\n"
                   "get\n"
                   "exit\n").lower()

    send_command(choice, sock)

    if choice == "upload":
        print("UPLOADING")

        file_name = select_file()
        if file_exists(file_name):

            # Send file name over
            send_file_name(file_name, sock)

            # Send file size over
            file_size = os.path.getsize(file_name)
            sock.send(file_size.to_bytes(4, byteorder="big"))

            # Begin transmitting file over
            with open(file_name, 'rb') as source_file:

                remaining_bytes = file_size
                while remaining_bytes > 0:

                    next_size = min(MAX_CHUNKS_SIZE, remaining_bytes)
                    chunk = source_file.read(next_size)
                    sock.sendall(chunk)

                    remaining_bytes -= next_size

            print("Finished writing all bytes")


        else:

            print("File name does not exist in local directory, please try again.")

    elif choice == "get":
        print("GETTING")

    elif choice == "exit":
        print("~ Exiting gracefully ~")
        sys.exit()

    else:
        print("WRONG COMMAND, EXIT NOW HERETIC")
