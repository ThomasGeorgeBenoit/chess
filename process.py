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

#big_data = int

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
    #print(len(openings_dict)+1)
    open_fq = init_array(len(openings_dict)+1)
    print(open_fq.shape)
    #print(data.shape)

    # data: the data in CSV:
    # | result of the game| opening played | 

    #result = data.bincount(axis=0)[0]
    #u, indices = np.unique(data, return_inverse=True)
    #most_popular_opening = u[np.argmax(np.apply_along_axis(np.bincount, 0,
    #    indices.reshape(data.shape), None, np.max(indices) + 1), axis=0)][1]

    #for k,v in openings_dict.items():
    #    if most_popular_opening == int(k):
    #        print("the most popular opening:", v)

    # for each opening, get the total number of games played
    for game in data:
        #print(game[0], game[1])
        analyze_game(open_fq, game[0], game[1])
    #print(open_fq)
    save_open_fq(csv, open_fq)
    # in open_fq, assume index refers to the openings.dat database value.
    #print(open_fq)

# result = 0 if draw, result = 1 if white win, result = 2 if black win
def analyze_game(open_fq, result:int, opening:int):
    #print(open_fq.shape)
    # total number of games ++
    #print(opening)
    if opening > len(open_fq)-1:
        return
    open_fq[opening][0] = (open_fq[opening][0])+1
    # white win
    if result == 1:
        open_fq[opening][1] = (open_fq[opening][1])+1
    # black win
    if result == 2:
        open_fq[opening][2] = (open_fq[opening][2])+1

def save_open_fq(csv, open_fq):
    path = "D:databases/"
    #print(open_fq.dtype)
    #save = open("D:databases/FQ.csv", "w")
    csv = strip_csv(csv)
    df = pd.DataFrame(open_fq)
    df.to_csv(csv+"DATA.csv", header=None)
    #np.savetxt(save, open_fq.astype(int))
    return

def strip_csv(csv:str):
    return csv.split("GAMES")[0]

# initializes the numpy array of length size
def init_array(size:int):
    #print(size)
    open_fq = np.zeros((size,3), dtype=np.int)
    return open_fq

def get_csvs(path:str):
    csvs = []
    for root, directories, files in os.walk(path, topdown=False):
	    for name in files:
		    if ".csv" in name: csvs.append(os.path.join(root, name))
	    for name in directories:
		    if ".csv" in name: csvs.append(os.path.join(root, name))
    return csvs
    
def iterate_csvs(csvs:list):
    for csv in csvs:
        #print(csv)
        data = pd.read_csv(csv, header = None)
        #print(data.head)
        data = data.to_numpy(dtype=np.int)
        print("analyzing",csv)
        process(csv, data)
        #print(data.shape)
        #break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USEAGE: python process.py <path-to-csvs-directory>")
    else:
        main(sys.argv[1:])