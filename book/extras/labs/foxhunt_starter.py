#!/usr/bin/env python3
"""L19 Lab starter: fix the fox from bearings taken along the firing line.

This file reads the two CSV files and prints the results. The four
functions marked TODO are yours to write in Part 1 of the packet.

Frame: x runs along the firing line (the tape), y runs straight downrange.
Every kit sits on the line (y = 0) with broadside pointed downrange (+y).
theta is Est. Angle with your reference-shot sign applied, so that a
positive angle points toward the +x end of the tape.

Usage:
    python foxhunt_starter.py stations.csv boxes.csv

stations.csv  header row, then one row per station:  x_m,theta_deg,peak_gain_db
boxes.csv     header row, then one row per box:      box,x_m,y_m
Leave peak_gain_db empty for a station whose level you did not record.
"""
import csv
import sys

import numpy as np


def solve(stations):
    """Fix the source from every station's bearing.

    stations: list of (x_m, theta_deg, peak_gain_db or None)
    Returns (fix, residuals): fix is a length-2 array (x, y) in meters;
    residuals has one entry per station, in meters.
    """
    raise NotImplementedError("TODO (Part 1)")


def drop_worst(stations):
    """Find the one station whose bearing disagrees with the rest.

    Returns (index of that station, fix without it).
    """
    raise NotImplementedError("TODO (Part 1)")


def rank_boxes(fix, boxes):
    """Order the boxes from most to least likely to hold the fox.

    boxes: list of (name, x_m, y_m)
    Returns a list of (name, distance_m) in ranked order.
    """
    raise NotImplementedError("TODO (Part 1)")


def amplitude_check(stations, box_xy):
    """Score how well the Peak Array Gain readings fit a source at box_xy.

    Smaller is a better fit. Used only to choose between two boxes that
    sit about equally close to the fix.
    """
    raise NotImplementedError("TODO (Part 1, optional)")


# --- reading and printing: no changes needed below this line --------------

def read_rows(path):
    with open(path, newline="") as f:
        rows = list(csv.reader(f))[1:]
    return [r for r in rows if r and r[0].strip()]


def main(stations_path, boxes_path):
    stations = []
    for r in read_rows(stations_path):
        gain = float(r[2]) if len(r) > 2 and r[2].strip() else None
        stations.append((float(r[0]), float(r[1]), gain))
    boxes = [(r[0], float(r[1]), float(r[2])) for r in read_rows(boxes_path)]

    fix, res = solve(stations)
    print(f"Fix from {len(stations)} bearings: x = {fix[0]:+.2f} m, y = {fix[1]:+.2f} m")
    for (x, th, _), r in zip(stations, res):
        print(f"  station x = {x:+.2f} m, theta {th:+6.1f} deg: residual {r:+.2f} m")
    if len(stations) >= 4:
        k, fix2 = drop_worst(stations)
        print(f"Without station x = {stations[k][0]:+.2f} m: "
              f"fix ({fix2[0]:+.2f}, {fix2[1]:+.2f}) m")
    print("Boxes, most likely first:")
    for name, dist in rank_boxes(fix, boxes):
        print(f"  box {name}: {dist:.2f} m from the fix")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
