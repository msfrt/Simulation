def endurance_points_delta(simulated_time, simulated_baseline):
    actual_time = 1409.969

    time_delta = (simulated_time - simulated_baseline) * 11  # 11 laps
    t = actual_time + time_delta

    ep1 = 0.000281 * (actual_time ** 2) - 1.305057 * actual_time + 1475.89843
    if ep1 > 275:
        ep1 = 275

    ep2 = 0.000281 * (t ** 2) - 1.305057 * t + 1475.89843
    if ep2 > 275:
        ep2 = 275

    return ep2 - ep1


def autocross_points_delta(simulated_time, simulated_baseline):
    actual_time = 54.716

    time_delta = simulated_time - simulated_baseline
    t = actual_time + time_delta

    ax1 = 0.091594 * (actual_time ** 2) - 16.245647 * actual_time + 698.614676
    if ax1 > 125:
        ax1 = 125

    ax2 = 0.091594 * (t ** 2) - 16.245647 * t + 698.614676
    if ax2 > 125:
        ax2 = 125

    return ax2 - ax1


def acceleration_points_delta(simulated_time, simulated_baseline):
    actual_time = 4.307

    time_delta = simulated_time - simulated_baseline
    t = actual_time + time_delta

    ap1 = 9.618854 * (actual_time ** 2) - 144.116392 * actual_time + 529.031468
    if ap1 > 100:
        ap1 = 100

    ap2 = 9.618854 * (t ** 2) - 144.116392 * t + 529.031468
    if ap2 > 100:
        ap2 = 100

    return ap2 - ap1


def skidpad_points_delta(simulated_time, simulated_baseline):
    actual_time = 5.685

    time_delta = simulated_time - simulated_baseline
    t = actual_time + time_delta

    sp1 = 15.856097 * (actual_time ** 2) - 231.676886 * actual_time + 826.334172
    if sp1 > 75:
        sp1 = 75

    sp2 = 15.856097 * (t ** 2) - 231.676886 * t + 826.334172
    if sp2 > 75:
        sp2 = 75

    return sp2 - sp1