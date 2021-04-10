import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import re
from openings import get_openings
from openings import store_openings
import sys
import os
import math

# does the bulk of the processing from our custom csv database to some more useful datafiles

class Opening:
    index = win_percent_w = win_percent_b = num_games = 0
    def __init__(self, index, num_games, win_percent_w, win_percent_b):
        self.index = index
        self.win_percent_w = win_percent_w
        self.win_percent_b = win_percent_b
        self.num_games = num_games


# main program entry
def main(args:list):
    csvs = get_csvs(str(args[0]))
    print(csvs)
    iterate_csvs(csvs)

# opens all the files and returns a list of file objects instead of strings
def open_all(out_names:list):
    files = []
    for name in out_names:
        files.append(open(name, "r"))
    return files

# get the DATA csvs only
def get_csvs(path:str):
    csvs = []
    for root, directories, files in os.walk(path, topdown=False):
	    for name in files:
		    if "DATA.csv" in name: csvs.append(os.path.join(root, name))
	    for name in directories:
		    if "DATA.csv" in name: csvs.append(os.path.join(root, name))
    return csvs
    
# do the analysis of the data and return the charts
def analyze(csv, data):
    openings = [] # openings for white
    MAX_GAMES = 1000
    for i in range(data.shape[0]):
        # win percentage for color = # color won / total games played
        total_games = data[i][1]
        # index, num_games, win_percent_w, win_percent_b
        dp = Opening(i,total_games, 0, 0)

        if (total_games > 5000) and (data[i][0] != 165):
            dp.win_percent_w = data[i][2] / data[i][1]
            dp.win_percent_b = data[i][3] / data[i][1]
            openings.append(dp)

    # TESTING
    #for opening in openings:
    #    print(opening.index, opening.num_games, opening.win_percent_w, opening.win_percent_b)
        #print("best for white:")
    #for opening in best_white:
    #    print(opening.index, opening.num_games, opening.win_percent_w, opening.win_percent_b)
    #print("best for black:")
    #for opening in best_black:
    #    print(opening.index, opening.num_games, opening.win_percent_w, opening.win_percent_b)


    # best performing for white and black!
    best_white, best_black = get_best_n_openings(openings, 5)

    # generate, plot, and save the best 5 openings for each color
    generate_chart(csv, best_white, "White")
    generate_chart(csv, best_black, "Black")


# generate and plot the chart
def generate_chart(rating_range:str, best_openings, color:str):
    rating_range = strip_rating(rating_range)
    #print(rating_range)
    plot_chart(rating_range, best_openings, color)


def plot_chart(rating_range, best_openings, color):
    win_w = []
    draw_ = []
    win_b = []
    for opening in best_openings:
        print(opening.index, opening.num_games, opening.win_percent_w, opening.win_percent_b)

    openings_str_list = []
    for opening in best_openings:
        opening_str = get_opening_str(opening.index)
        openings_str_list.append(opening_str)
        # get win% white
        win_w.append(opening.win_percent_w)
        # get win% black
        win_b.append(opening.win_percent_b)
        # get remainder
        draw_.append(1 - (opening.win_percent_w + opening.win_percent_b))

    win_w = np.array(win_w)
    draw_ = np.array(draw_)
    win_b = np.array(win_b)
    #print(win_w)

    #define chart parameters
    N = len(openings_str_list)
    barWidth = .5

    #add labels, title, tick marks, and legend
    plt.xlabel('Openings')
    plt.title('White'+rating_range)

    Pos = range(len(openings_str_list), 0, -1)
    print(Pos)
    plt.barh(Pos, win_w, color='white', edgecolor = '0')
    plt.barh(Pos, draw_, left  = win_w, color='grey', edgecolor = '0')
    plt.barh(Pos, win_b, left  = win_w + draw_, color='black', edgecolor = '0')
    plt.yticks(Pos, openings_str_list)

    plt.show()


# gets the opening name
# returns the openings string
def get_opening_str(index:int):
    openings = get_openings("D:databases")
    for k, v in openings.items():
        if int(k) == index:
            return v
    # if something went wrong
    return -1
    

def strip_rating(filename:str):
    s = filename.split("\\")[1]
    s = s.split("DATA")[0]
    return s

# get the n-best performing openings for white and black in "openings" list of Opening class.
def get_best_n_openings(openings:list, n:int):

    best_openings_w = []
    best_openings_b = []
    for i in range(n):
        best = get_best_opening_w(openings)
        best_openings_w.append(best)
        openings.remove(best)

    for i in range(n):
        best = get_best_opening_b(openings)
        best_openings_b.append(best)
        openings.remove(best)

    return best_openings_w, best_openings_b


def get_best_opening_w(openings:list):
    best_for_white = Opening(0,0,0,0)
    for i in range(len(openings)):
        if openings[i].win_percent_w > best_for_white.win_percent_w:
            best_for_white = openings[i]
    return best_for_white

def get_best_opening_b(openings:list):
    best_for_black = Opening(0,0,0,0)
    for i in range(len(openings)):
        if openings[i].win_percent_b > best_for_black.win_percent_b:
            best_for_black = openings[i]
    return best_for_black

def iterate_csvs(csvs:list):
    for csv in csvs:
        #print(csv)
        data = pd.read_csv(csv, header = None)
        #print(data.head)
        data = data.to_numpy(dtype=np.int)
        print("analyzing",csv)
        analyze(csv, data)
        #print(data.shape)
        break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USEAGE: python process.py <path-to-csvs-directory>")
    else:
        main(sys.argv[1:])