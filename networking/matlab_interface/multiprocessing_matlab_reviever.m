% Connect to shared memory
shared_memory = memmapfile('shared_memory.dat', 'Format', {'double', [3, 3], 'Timestamps'; 'double', [3, 3], 'EventData'});

while true
    % Read timestamped events from shared memory
    timestamps = shared_memory.Data.Timestamps;
    event_data = shared_memory.Data.EventData;
    
    % Process timestamped events (use in your SLAM algorithm)
    for i = 1:size(timestamps, 1)
        timestamp = timestamps(i, :);
        eventdata = reshape(event_data(i, :), 3, 3);
        % Your SLAM processing code here
        disp(['Timestamp: ' num2str(timestamp) ', Event Data:']);
        disp(eventdata);
    end
    
    pause(1);  % Simulate processing every second
end
