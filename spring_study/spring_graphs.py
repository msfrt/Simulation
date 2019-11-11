import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

# file containing the output
data = pd.read_csv("spring_sweep_RESULTS_COMBINED_rev2.csv")

# Event times from competition
acceleration_irl = 4.307
skidpad_irl = 5.685
autocross_irl = 54.716
endurance_irl = 1409.969

# the baseline spring rate
baseline_springrate = 300

# prep the figures
sns.set_style("white")
sns.set_context("notebook")

#figure size in inches and figure dots per inch
figure_size = (5, 5)
figure_dpi = 600


# Create directory to store the images
dirName = 'images'
try:
    os.mkdir(dirName)
except FileExistsError:
    pass



# define the points functions that are from the points study xslm workbook
def acceleration_points(actual_time, baseline_time, time):
    t = (time / baseline_time) * actual_time
    points = 9.618854 * (t**2) - 144.116392 * t + 529.031468
    return points

def skidpad_points(actual_time, baseline_time, time):
    t = (time / baseline_time) * actual_time
    points = 15.856097 * (t**2) - 231.676886 * t + 826.334172
    return points

def autocross_points(actual_time, baseline_time, time):
    t = (time / baseline_time) * actual_time
    points = 0.091594 * (t**2) - 16.245647 * t + 698.614676
    return points

def endurance_points(actual_time, baseline_time, time):
    t = (time / baseline_time) * actual_time
    points = 0.000281 * (t**2) - 1.305057 * t + 1475.89843
    return points


    
def spring_graphs(data, actual_time, track_number, points_function):
    '''
    This function takes in the dataframe, the actual time from comp, the
    baseline sim time, the track number (whatever they are set up as in the
    insight file), and the name of the points function for the event.
    
    Returns nothing, but saves graphs as images in the working directory.
    '''
    
    # self explanitory
    if track_number == 1:
        event_name = "Acceleration"
    elif track_number == 2:
        event_name = "Skidpad"
    elif track_number == 3:
        event_name = "Autocross"
    elif track_number == 4:
        event_name = "Endurance"
        
    # find the baseline laptime from the baseline springrate
    # by using a dual-mask
    masked_df = data[data["spring"] == baseline_springrate]
    baseline_time = masked_df["laptime"][data["track"] == track_number]
    baseline_time = float(baseline_time) # was a df structure, now a flt

    
    # extract the data from the dataframe in preperation for plotting
    springs = data["spring"][data["track"] == track_number]
    times = data["laptime"][data["track"] == track_number]
    frh_max = data["F_Ride_MAX"][data["track"] == track_number]
    frh_avg = data["F_Ride_AVG"][data["track"] == track_number]
    frh_min = data["F_Ride_MIN"][data["track"] == track_number]
    rrh_max = data["R_Ride_MAX"][data["track"] == track_number]
    rrh_avg = data["R_Ride_AVG"][data["track"] == track_number]
    rrh_min = data["R_Ride_MIN"][data["track"] == track_number]
    points = np.array([points_function(actual_time, baseline_time, time) for time in times])

    
    # create a subplot figure for the ride height graph
    fig, ax1 = plt.subplots(figsize=figure_size, dpi=figure_dpi)
    
    # add all of the lines to the plot
    ax1.plot(springs, frh_max, label="Front MAX", color="tab:blue")
    ax1.plot(springs, frh_avg, label="Front AVG", color="blue")
    ax1.plot(springs, frh_min, label="Front MIN", color="darkblue")
    ax1.plot(springs, rrh_max, label="Rear MAX", color="tab:red")
    ax1.plot(springs, rrh_avg, label="Rear AVG", color="red")
    ax1.plot(springs, rrh_min, label="Rear MIN", color="darkred")
    # do all of the labelling and pretty stuff
    ax1.set_xlabel("Spring Rate (lbs/in)")
    ax1.set_ylabel("Ride Height")
    ax1.set_title("Ride Height vs. Spring Rate - {}".format(event_name))
    fig.gca().xaxis.grid(True) # veritical gridlines
    # display a legend for plots with parameter: "label="
    ax1.legend()
    # remove the top and left spines
    sns.despine()
    # fixes the formatting
    fig.tight_layout()
    # saves the figure
    plt.savefig("images/ride-heights_{}.jpg".format(event_name))
    
    
    
    
    
    fig, ax1 = plt.subplots(figsize=figure_size, dpi=figure_dpi)
    fig.gca().xaxis.grid(True) # veritical gridlines
    ax1.plot(springs, times)
    ax1.set_xlabel("Spring Rate (lbs/in)")
    ax1.set_ylabel("Laptimes", color="tab:blue")
    ax1.tick_params(axis='y', labelcolor="tab:blue")
    ax1.set_title("Laptime vs. Spring Rate - {}".format(event_name))
    
    ax2 = ax1.twinx()
    ax2.set_ylabel("Points", color="tab:red")
    ax2.plot(springs, points, color="tab:red")
    ax2.tick_params(axis='y', labelcolor="tab:red")
    baseline_points = points_function(actual_time, baseline_time, baseline_time)
    ax2.hlines(baseline_points, springs.min(), springs.max(), color="grey", linestyle="--", label="baseline points")
    ax2.legend()
    
    fig.tight_layout()
    plt.savefig("images/points_{}.jpg".format(event_name))
    
    
    # return the points, so we can do an analysis of all events together
    return points, baseline_points


# params = dataframe, real-life time, LTS baseline time, track num, points fcn
accel_pts, accel_bsline_pts         = spring_graphs(data, acceleration_irl, 1, acceleration_points)
skidpad_pts, skidpad_bsline_pts     = spring_graphs(data, skidpad_irl,      2, skidpad_points)
autocross_pts, autocross_bsline_pts = spring_graphs(data, autocross_irl,    3, autocross_points)
endurance_pts, endurance_bsline_pts = spring_graphs(data, endurance_irl,    4, endurance_points)

# now plot the total points as a result of spring rate
total_baseline_points = accel_bsline_pts + skidpad_bsline_pts + autocross_bsline_pts + endurance_bsline_pts
total_pts = accel_pts + skidpad_pts + autocross_pts + endurance_pts

# get the list of springs again (this assumes that you have ran every spring
# rate in every event, as this pulls out acceleration spring rates)
springs = data["spring"][data["track"] == 1]

fig, ax1 = plt.subplots(figsize=figure_size, dpi=figure_dpi)
ax1.plot(springs, total_pts, color="darkred")
fig.gca().xaxis.grid(True) # veritical gridlines
ax1.set_xlabel("Spring Rate (lbs/in)")
ax1.set_ylabel("Points")
ax1.set_title("Total Dynamic-Event Points vs. Spring Rate")
ax1.hlines(total_baseline_points, springs.min(), springs.max(), color="grey", linestyle="--", label="baseline")
ax1.legend()
sns.despine()

fig.tight_layout()
plt.savefig("images/overall_points.jpg")






