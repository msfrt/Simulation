clear

%LTS2DARAB creates a delimited text file that can be imported into
%WinDARAB
%d: this is the struct data. Do NOT include any quotes
%......Be sure to upload the LTS output file and this struct
%......Can be done by double clicking on data in bottom left of screen
%f_in: channel names copied from the master channel list that are
%desired for this run. ex. 'channels..0.xlsx'
%f_out: text file name to output ex. 'output.txt'

run_file = 'C:\Users\nic\Desktop\big_long_boy.mat';
f_in = 'E:\Simulation_1920\processing\lts_2_darab\channels2.3.xlsx';
f_out =    'C:\Users\nic\Desktop\big_long_boy.txt';

load(run_file);
d = data;


tic  %time
disp('Uploading desired channels...')
[~,txt,~] = xlsread(f_in);              %import excel
disp('Upload complete')
f = fieldnames(d);                      %collect LTS output channels

raw_data = struct2cell(d);              %grab data
raw_data = raw_data';                   %need to invert

field_cnt = length(txt);                %Pre-define arrays to save time
selected_fields = zeros(0,field_cnt);   
selected_data = zeros(0,field_cnt);
k = 1;
disp('Finding desired data...')
for i = 1:numel(f)
    s1 = f{i};                                  %grab name of channel
    [~,ind]=ismember(s1,strtrim(txt));
    if ind ~= 0 
        unit_name = txt{ind,4};                 %grab units from excel
        if strcmp(unit_name,'<unitless>') || strcmp(unit_name,'') || strcmp(unit_name,'N/A')
            unit_name = 'none';
        end               
        s = strcat(s1,' [',unit_name,']');      %new header       
        selected_fields{k} = s;                 
        selected_data{k} = raw_data{1,i};
        % remember the column of Elapsed_Time
        if s1 == "Elapsed_Time"
            Elapse_Time_column = k;
        end
        k = k + 1;
    end
    
    
    
end
selected_fields{1} = 'xtime [   s]';                %DARAB requirement
selected_data{1} = selected_data{Elapse_Time_column};%Whatever column elapsed time was in
new_data = [selected_fields;selected_data];         %add new header
disp('Desired data collected')
FID_out = fopen(f_out,'w');                         %Output File

[~,col_sz] = size(new_data);                        
row_sz = length(new_data{2,1});
disp('Printing Output file...')
%only a 2x1 cell, the 2nd row contains a cell which is 58916x1 double
for i = 1:col_sz                                    %channel names
    fprintf(FID_out, '%-30s', new_data{1,i});
end    
disp('Channel names written')
fprintf(FID_out, '\r\n');
disp('Writing data...')
%current_row = 0
for j = 1:row_sz                                    %data             
    for k = 1:col_sz
        fprintf(FID_out,'%30d', new_data{2,k}(j,1)); 
    end
    fprintf(FID_out, '\r\n');                       %new row
    %current_row = current_row + 1
    if ~mod(j,5000)
        disp(strcat('.....Printing row:_', int2str(j), '_of_',int2str(row_sz)))
    end
end
fclose(FID_out);  
disp('Output file written')
toc

