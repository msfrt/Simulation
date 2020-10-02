import pandas as pd
import numpy as np
import plotly.graph_objs as go
import os
from points_deltas import endurance_points_delta
from points_deltas import acceleration_points_delta
from points_deltas import autocross_points_delta
from points_deltas import skidpad_points_delta

TRACK_INT_TO_NAME_DICT = {1: "Acceleration", 2: "Skidpad", 3: "Autocross", 4: "Endurance"}


def save_figure(fig, title):
    """
    Saves the figure object as htmls and pngs
    :param title: a string title
    :param fig: the figure to save
    :return: none
    """

    try:
        fig.write_image("images/png/{}.png".format(title),
                        width=800, height=600)
    except FileNotFoundError:
        os.makedirs("images/png")
        fig.write_image("images/png/{}.png".format(title),
                        width=800, height=600)

    try:
        fig.write_html("images/html/{}.html".format(title))
    except FileNotFoundError:
        os.makedirs("images/html")
        fig.write_html("images/html/{}.html".format(title))


def gridify(df, x_col, y_col, target_col):
    """
    Pull out results into a grid
    :param df: The dataframe of all results masked so that x and y provide a definite target
    :param x_col: The column title for x data
    :param y_col: The column title for y data
    :param target_col: The column to use as the z data
    :return: A 2d array representing x_col x y_col with target_col as the intersection
    """

    # pull out unique values for x and y and create sorted lists for them
    xs = np.array(sorted(df[x_col].unique()))
    ys = np.array(sorted(df[y_col].unique()))

    # map each unique value to it's sorted position (for efficiency purposes)
    x_indecies = {}
    for i in range(len(xs)):
        x_indecies[xs[i]] = i
    y_indecies = {}
    for i in range(len(ys)):
        y_indecies[ys[i]] = i

    # create a grid to place results
    results_grid = np.zeros(shape=(len(ys), len(xs)))

    for x in xs:
        for y in ys:
            mask = (df[x_col] == x) & (df[y_col] == y)

            # find the index that we need to insert into
            x_i = x_indecies[x]
            y_i = len(ys) - 1 - y_indecies[y]  # this is because arrays in the computer are indexed
                                               # from the top left corner downwards

            results_grid[y_i][x_i] = df[mask][target_col]

    return xs, ys, results_grid


df = pd.read_csv("rh_spring_rate_results.csv")

# back-calculate ride height from rh_diff
baseline_ride_height_inches = 1.25
baseline_spring_rate = 250

df["ride_height"] = df["rh_diff"] + baseline_ride_height_inches


# begin to calculate the points delta
baseline_mask = (df["spring_rate"] == baseline_spring_rate) & (df["ride_height"] == baseline_ride_height_inches)
baseline_accel_time = df[(df["track_num"] == 1) & baseline_mask]["!laptime"]
baseline_skidp_time = df[(df["track_num"] == 2) & baseline_mask]["!laptime"]
baseline_autox_time = df[(df["track_num"] == 3) & baseline_mask]["!laptime"]
baseline_endur_time = df[(df["track_num"] == 4) & baseline_mask]["!laptime"]

# insert empty column
df.insert(len(df.columns), "points_delta", np.zeros_like(df.index).astype(float))

# calculate points deltas
for index in df.index:

    # calculations for acceleration
    if df.iloc[index]["track_num"] == 1:
        current_laptime = df.iloc[index]["!laptime"]
        current_pointsd = acceleration_points_delta(float(current_laptime), float(baseline_accel_time))
        df.at[index, "points_delta"] = current_pointsd

    # calculations for skidpad
    elif df.iloc[index]["track_num"] == 2:
        current_laptime = df.iloc[index]["!laptime"]
        current_pointsd = skidpad_points_delta(float(current_laptime), float(baseline_skidp_time))
        df.at[index, "points_delta"] = current_pointsd

    # calculations for autocross
    elif df.iloc[index]["track_num"] == 3:
        current_laptime = df.iloc[index]["!laptime"]
        current_pointsd = autocross_points_delta(float(current_laptime), float(baseline_autox_time))
        df.at[index, "points_delta"] = current_pointsd

    # calculations for endurance
    elif df.iloc[index]["track_num"] == 4:
        current_laptime = df.iloc[index]["!laptime"]
        current_pointsd = endurance_points_delta(float(current_laptime), float(baseline_endur_time))
        df.at[index, "points_delta"] = current_pointsd


# acceleration
track = 1
x_var = "spring_rate"
y_var = "ride_height"
springs_rates, ride_heights, grid = gridify(df[df["track_num"] == track], x_var, y_var, "points_delta")
heatmap = go.Heatmap(z=grid, x=springs_rates, y=ride_heights, hoverongaps=False, colorscale='RdYlGn', zmid=0)
fig = go.Figure(heatmap)
fig.update_layout(
    title="Spring Rate x Ride Height x Points Delta - {}".format(TRACK_INT_TO_NAME_DICT[track]),
    xaxis_title="Spring Rate",
    yaxis_title="Ride Height (inches)")
# fig.show()
save_figure(fig, TRACK_INT_TO_NAME_DICT[track])


# we'll use this 2d array to store all of the points deltas
total_points_deltas = grid


# skidpad
track = 2
x_var = "spring_rate"
y_var = "ride_height"
springs_rates, ride_heights, grid = gridify(df[df["track_num"] == track], x_var, y_var, "points_delta")
heatmap = go.Heatmap(z=grid, x=springs_rates, y=ride_heights, hoverongaps=False, colorscale='RdYlGn', zmid=0)
fig = go.Figure(heatmap)
fig.update_layout(
    title="Spring Rate x Ride Height x Points Delta - {}".format(TRACK_INT_TO_NAME_DICT[track]),
    xaxis_title="Spring Rate",
    yaxis_title="Ride Height (inches)")
# fig.show()
save_figure(fig, TRACK_INT_TO_NAME_DICT[track])

total_points_deltas += grid


# autocross
track = 3
x_var = "spring_rate"
y_var = "ride_height"
springs_rates, ride_heights, grid = gridify(df[df["track_num"] == track], x_var, y_var, "points_delta")
heatmap = go.Heatmap(z=grid, x=springs_rates, y=ride_heights, hoverongaps=False, colorscale='RdYlGn', zmid=0)
fig = go.Figure(heatmap)
fig.update_layout(
    title="Spring Rate x Ride Height x Points Delta - {}".format(TRACK_INT_TO_NAME_DICT[track]),
    xaxis_title="Spring Rate",
    yaxis_title="Ride Height (inches)")
# fig.show()
save_figure(fig, TRACK_INT_TO_NAME_DICT[track])

total_points_deltas += grid

# endurance
track = 4
x_var = "spring_rate"
y_var = "ride_height"
springs_rates, ride_heights, grid = gridify(df[df["track_num"] == track], x_var, y_var, "points_delta")
heatmap = go.Heatmap(z=grid, x=springs_rates, y=ride_heights, hoverongaps=False, colorscale='RdYlGn', zmid=0)
fig = go.Figure(heatmap)
fig.update_layout(
    title="Spring Rate x Ride Height x Points Delta - {}".format(TRACK_INT_TO_NAME_DICT[track]),
    xaxis_title="Spring Rate",
    yaxis_title="Ride Height (inches)")
# fig.show()
save_figure(fig, TRACK_INT_TO_NAME_DICT[track])

total_points_deltas += grid



# all together
track = 4
heatmap = go.Heatmap(z=total_points_deltas, x=springs_rates, y=ride_heights, hoverongaps=False, colorscale='RdYlGn', zmid=0)
fig = go.Figure(heatmap)
fig.update_layout(
    title="Spring Rate x Ride Height x Points Delta - All Tracks",
    xaxis_title="Spring Rate",
    yaxis_title="Ride Height (inches)")
# fig.show()
save_figure(fig, "All_Tracks")


