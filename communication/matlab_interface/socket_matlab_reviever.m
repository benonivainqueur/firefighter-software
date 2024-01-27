% Create a socket connection
server = tcpip('localhost', 12345, 'NetworkRole', 'server');
fopen(server);

% Receive and deserialize data
data_received = fread(server, server.BytesAvailable);
events = pickle.loads(data_received);

% Process timestamped events (use in your SLAM algorithm)
for i = 1:length(events)
    timestamp = events(i).timestamp;
    eventdata = events(i).data;
    % Your SLAM processing code here
end

% Close the connection
fclose(server);
