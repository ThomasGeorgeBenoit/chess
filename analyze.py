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

#big_data = int

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

def get_csvs(path:str):
    csvs = []
    for root, directories, files in os.walk(path, topdown=False):
	    for name in files:
		    if "DATA.csv" in name: csvs.append(os.path.join(root, name))
	    for name in directories:
		    if "DATA.csv" in name: csvs.append(os.path.join(root, name))
    return csvs
    
def analyze(data):
    #print(data)
    best_win_w = [0,0,0] # [opening index, win % for color, number of games]
    best_win_b = [0,0,0] # [opening index, win % for color, number of games]
    for i in range(data.shape[0]):
        #print(i)
        # win percentage for color = # color won / total games played
        #print(data[i][1])

        #print(data[i][2] / data[i][1])
        total_games = data[i][1]
        if total_games > 100:
            win_p_w = data[i][2] / data[i][1]
            win_p_b = data[i][3] / data[i][1]

            #print(win_p_w, win_p_b)

            if win_p_w > best_win_w[1]:
                print("A")
                best_win_w[1] = win_p_w
                best_win_w[0] = i
                best_win_w[2] = total_games

            if win_p_b > best_win_b[1]:
                best_win_b[1] = win_p_b
                best_win_b[0] = i
                best_win_b[2] = total_games

    print(best_win_w)
    print(best_win_b)
    # best performing for black

    # best performing for white
        

def iterate_csvs(csvs:list):
    for csv in csvs:
        #print(csv)
        data = pd.read_csv(csv, header = None)
        #print(data.head)
        data = data.to_numpy(dtype=np.int)
        print("analyzing",csv)
        analyze(data)
        #print(data.shape)
        break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USEAGE: python process.py <path-to-csvs-directory>")
    else:
        main(sys.argv[1:])