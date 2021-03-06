% path to the points study excel sheet
f_in_path = 'E:\Simulation_1920\points_study\MIS_points_study_1920.xlsm';

% name of the document to export
f_out = 'curves.txt';

% the tabs to get the data from and the respective table ranges. For the
% table ranges, be sure to include the titles in the range
tabs =         ["Acceleration", "Skidpad", "Autocross", "Endurance"];
table_ranges = ["P3:Q88",       "T2:U87",  "T4:U89",    "I3:J48"];

% polynomial degree to which the regressions should be created
poly_degree = 2;

% open the file for writing
fileID = fopen(f_out, 'w');


% begin the calculation of each regression
for i=1:length(tabs)
    
    % read the table
    table_data = readtable(f_in_path, 'Sheet', tabs(i), ...
        'Range', table_ranges(i));
    
    % turn the table into an array
    data_array = table2array(table_data);
    
    % find the polynomial coefficients that fit the data
    poly_coefficients = polyfit(data_array(:,1), data_array(:,2), ...
        poly_degree);
    
    
    % initialize the string to output
    output_str = tabs(i) + "\r\n";
    
    % append 'y = '
    output_str = strcat(output_str, 'points =', {' '});
    
    
    
    % append the coefficients and x's is appropriate
    for ci=1:length(poly_coefficients)
        
        % append the coefficient
        output_str = strcat(output_str,...
            num2str(poly_coefficients(ci), '%f'));
        
        % append 'x^'
        output_str = strcat(output_str, 't^');
        
        % append the power that we are on
        output_str = strcat(output_str, ...
            num2str(length(poly_coefficients) - ci));
        
        % append a space and a + and then another space
        output_str = strcat(output_str, {' '}, '+', {' '});
        
    end
    
    % clean up the string a bit by removing ^1, t^0, and the last +
    output_str = erase(output_str, '^1');
    output_str = erase(output_str, 't^0 +');
    
    
    % append two line breaks
    output_str = strcat(output_str, '\r\n\r\n');
    fprintf(fileID, output_str);
    
    
end
