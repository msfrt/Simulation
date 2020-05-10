% output aer file path and file name
f_out_path = 'E:\Simulation1718\LTS\parameters\aero\aero_maps/sr19_rev3.05.aer';

% input aero file, xslx format
f_in_path =  'E:\Simulation1718\LTS\parameters\aero\aero_maps/sr19_rev2.xlsx';

% create a new aer file for the output in the desired path
out_file = fopen(f_out_path, 'w');

% the tabs to get the data from and the respective table ranges
tabs =         ["front" ,"rear"  ,"drag"  ];
table_ranges = ["A1:C20","A1:C20","A1:C20"];

% spline names - Lankes says don't touch these, they're probably good
spline_name = ["!Front Downforce Spline,", "!Rear Downforce Spline",...
               "!Dragforce Spline"];
spline      = ["SPLINE/11,", "SPLINE/12,", "SPLINE/13,"];

% parameters for the exported aeromap size
start_rh = 0.2; % in
stop_rh  = 2.8; % in
step_rh  = 0.1; % in

% just define the newline character here because it's a pain to type
nl = "\r\n";

for i=1:length(tabs)
    
    % read the table
    raw_table_data = readtable(f_in_path, 'Sheet', tabs(i), ...
        'Range', table_ranges(i));
    
    % put the table data into a useful form
    data_array = table2array(raw_table_data);
    
    % unpack the data array into columns
    frh = data_array(:,1); % front ride height = first column
    rrh = data_array(:,2); % rear ride height = second column
    lbs = data_array(:,3); % lbs in downforce = third column
    
    % create a 2d grid of ride heights to store the intrapolated
    % and extrapolated data that we're about to calculate
    [frh_q,rrh_q] = meshgrid(start_rh:step_rh:stop_rh,...
                    start_rh:step_rh:stop_rh);
                
    % intrapolate the given data to the resolution of the grid
    lbs_q = griddata(frh, rrh, lbs, frh_q, rrh_q);
    
    surf(interp2(lbs_q))
    % surf(lbs_q)
    
    % print the spline name and the spine to the file
    fprintf(out_file, spline_name(i) + nl);
    fprintf(out_file,      spline(i) + nl);

    
    
    % rewrite the array of frh values into x value string that we can use
    x_str = ",X=";
    
    for val=frh_q(1,:) % iterate through every column. grab the first row
        
        % make the float a string with 3-decimal precision first
        num_str = num2str(val, '%0.3f');
        
        % append the number to the main string
        x_str = strcat(x_str, num_str, ',');
        
    end
    
    % chop off the last comma that we added up there
    x_str = strip(x_str, 'right', ',');
    
    % append a new line char
    x_str = strcat(x_str, nl);
    
    % add the x vals string to the file
    fprintf(out_file, x_str);
    
    
    
    % now for the y vals and the z vals
    for y_index = 1:1:length(rrh_q(:,1)) % every number in the first column
        
        % the y value for this iteration
        y_str = ",Y=";
        num_str = num2str(rrh_q(y_index,1), '%0.3f');
        y_str = strcat(y_str, num_str, ',');
        
        % initialize a z_val string
        z_str = "";
        
        % get the zvals in each column for this row (iteration)
        for zval = lbs_q(y_index,:)
            
            % concatenate the zval to the list of them
            z_num = num2str(zval, '%0.3f');
            z_str = strcat(z_str, z_num, ',');
            
        end
        
        % add the zvals to this y string
        y_str = strcat(y_str, z_str);
        
        % chop off the last comma that we added up there
        y_str = strip(y_str, 'right', ',');
        
        % append a new line char
        y_str = strcat(y_str, nl);
        
        % sauce it into the file
        fprintf(out_file, y_str);
          
        
    end
    
    % print some extrapolation command for lts
    fprintf(out_file, nl);
    fprintf(out_file, ",LINEAR_EXTRAPOLATE");
    
    % sauce a new/blank into the file before starting the next map
    fprintf(out_file, nl);
    fprintf(out_file, nl);

end



% print to the file
% fprintf(output_file_ID, 'this is me testing \r\nnewline hehe');