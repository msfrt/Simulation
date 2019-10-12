###############################################################################
#
#   Michigan State University Formula Racing Team
#   
#   DL1 GPS CSV converter for NX TXT point-set files
#   Dave Yonkers
#   
#   Be sure so change the file names (and loctions if necessary) below
#
###############################################################################

import csv
import time

# here, if the script is in the same directory as the txt file, you can simply
# put "file_name.txt" -- if the script is not in the same directory, you must
# put the entire directory here as well as the file name
txt_file_location = 'temp.txt'

# where you want to DL1 file saved. Include name and file extension!
output_file_location = 'Finished_CSVs/MIS_AutoX_4.csv'

# was the point-set drawn in the wrong direction? Reverse the track here!
# default is False
reverse_track_bool = False




# set the program start time
start_time = time.time()

# open the txt file
print('opening file...')
txt_fp = open(txt_file_location, 'r')

# skip the first four header lines in the file
for i in range(4):
    txt_fp.readline()


# initialize a list to store all of the points
points_list = []

# gather the data in each line and put it into a list
print('gathering data...')
for line in txt_fp:    
    xyz_list = line.strip().split(' ') # clean it up and split it up!  
    points_list.append(xyz_list) # append to the points list
    
    
# tell the user that we're writing data
print('writing data...')

# open/write a new csv file and prep for writing data
with open(output_file_location, 'w', newline='') as csvfile:
    track_gps = csv.writer(csvfile, delimiter=',') # assign the writing pointer
    
    track_gps.writerow(['Longitude']) # write the first header
    track_gps.writerow(['x', 'y', 'z']) # write the second header
    
    
    # determine which direction the track needs to be
    if reverse_track_bool == False:
        # write the xyz data to the csv file in regular order
        track_gps.writerows(points_list)
    else:
        # write the track data reversed
        track_gps.writerows(reversed(points_list))
            
# we're done here
elapsed_time = time.time() - start_time
print('\nfinished in {:5f} seconds'.format(elapsed_time))
        