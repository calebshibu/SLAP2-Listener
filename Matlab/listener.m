% Define the port number for the server
port = 12345;

% Create a Java ServerSocket object
serverSocket = java.net.ServerSocket(port);

% Wait for a client to connect
disp('Waiting for signal from Python...');
clientSocket = serverSocket.accept();
disp('Client connected.');

% Open a data input stream to receive messages from the client
inputStream = clientSocket.getInputStream();

% Continuously listen for incoming data
while true
    if inputStream.available() > 0
        data = uint8([]);
        while inputStream.available() > 0
            data = [data, inputStream.read()];
        end
        message = char(data');
        if strcmp(message, 'True')
            disp('Received True signal from Python.');
            % Perform your action here
            break; % Exit the loop if desired
        end
    end
    pause(1); % Check every second
end

% Close the streams and socket when done
inputStream.close();
clientSocket.close();
serverSocket.close();