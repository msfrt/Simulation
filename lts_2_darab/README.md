# LTS → WinDarab

Using this script is so easy; it's almost like shooting fish in a barrel. You only need to change 2, maybe 3 lines of code.

1. You're going to open `LTS2DARAB_script.m` in MATLAB.
2. Navigate to the folder where you saved your LTS output `.mat` file. Copy the file path in the file browser and replace the string in line 12 of the script with the new file path. Be sure to actually add the file name to the end of the string! A completed line 12 may look like this: `run_file = 'C:\Users\nic\Desktop\big_long_boy.mat';`.
3. Skip line 13 for now. Copy the string from line 12 and paste it into the string for line 14. Then, change the file extension on the string from `.mat` to `.txt`. This tells MATLAB that the output of the script will be a `.txt` file saved in the same location as the original `.mat` file.
4. Okay, this next step might be the most confusing, but you may not need to do it. The channel definitions file is what tells MATLAB what we want to be in the final `.txt` file. LTS has hundreds of channels, and if we converted every single one of them, it would take a long time to run the conversion. If you want to export a channel that's not in the current channels file, you can find the original channels file in the LTS install directory (`E:\PrattMiller\LTS_10.2.0.14104\output data.xls` on the LTS computer). If you choose to edit the channels, be sure to delete the rows that you don't want to export in the `Quasi Static` tab, and then save the `Quasi Static` tab as its own `.xlsx` file somewhere where you can get to it. Then, much like in Step 2 and Step 3, you will copy the file path to the selected channel definitions file in line 13. A completed line 13 may look like: `f_in = 'E:\Simulation_1920\processing\lts_2_darab\channels2.3.xlsx';`.
5. After editing those three lines, verify that they should look somthing like this:
```MATLAB
run_file = 'C:\Users\nic\Desktop\big_long_boy.mat';
f_in = 'E:\Simulation_1920\processing\lts_2_darab\channels2.3.xlsx';
f_out =    'C:\Users\nic\Desktop\big_long_boy.txt';
```
6. Click `Run` in the MATLAB editor toolbar.
