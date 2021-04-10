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

# does the bulk of the processing from our custom csv database to some more useful datafiles

# main program entry
def main(args:list):
    csvs = get_csvs(str(args[0]))
    print(csvs)
    #print(get_openings(str(args[0])))
    iterate_csvs(csvs)

# opens all the files and returns a list of file objects instead of strings
def open_all(out_names:list):
    files = []
    for name in out_names:
        #f = open(name, "w")
        #f.close()
        f = open(name, "a")
        files.append(f)

    return files

def process(csv, data):
    openings_dict = get_openings('D:databases')
    open_fq = init_array(len(openings_dict)+1)
    # data: the data in CSV:
    # | result of the game| opening played | 

    for game in data:
        # analyze it!!!
        analyze_game(open_fq, game[0], game[1])
    save_open_fq(csv, open_fq)
    # in open_fq, assume the index refers to the openings.dat database value.

# result = 0 if draw, result = 1 if white win, result = 2 if black win
def analyze_game(open_fq, result:int, opening:int):
    # funky error checking. This really shouldn't be triggered.
    if opening > len(open_fq)-1:
        return
    # total number of games ++
    open_fq[opening][0] = (open_fq[opening][0])+1
    # white win
    if result == 1:
        open_fq[opening][1] = (open_fq[opening][1])+1
    # black win
    if result == 2:
        open_fq[opening][2] = (open_fq[opening][2])+1

# saves the frequency database into a file
def save_open_fq(csv, open_fq):
    path = "D:databases/"
    csv = strip_csv(csv)
    df = pd.DataFrame(open_fq)
    df.to_csv(csv+"DATA.csv", header=None)
    return

# strips the csv of their GAMES tag.
def strip_csv(csv:str):
    return csv.split("GAMES")[0]

# initializes the numpy array of length size
def init_array(size:int):
    open_fq = np.zeros((size,3), dtype=np.int)
    return open_fq

# get all the relevant csvs from the databases directory
def get_csvs(path:str):
    csvs = []
    for root, directories, files in os.walk(path, topdown=False):
	    for name in files:
		    if ".csv" in name: csvs.append(os.path.join(root, name))
	    for name in directories:
		    if ".csv" in name: csvs.append(os.path.join(root, name))
    return csvs
    
# iterate through all the csvs. calls the processing function.
def iterate_csvs(csvs:list):
    for csv in csvs:
        data = pd.read_csv(csv, header = None)
        data = data.to_numpy(dtype=np.int)
        print("analyzing",csv)
        process(csv, data)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USEAGE: python process.py <path-to-csvs-directory>")
    else:
        main(sys.argv[1:])