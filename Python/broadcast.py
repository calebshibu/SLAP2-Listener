import socket

# Set up the client to connect to the server on localhost and port 12345
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('127.0.0.1', 12345))
    print("Connected to MATLAB server.")
    
    # Send the 'True' signal to MATLAB
    message = 'True'
    sock.sendall(message.encode())
    print("Sent 'True' signal to MATLAB.")