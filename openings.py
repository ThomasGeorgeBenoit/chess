import pandas as pd
import numpy as np


openings_dict = {}

def get_openings():
    openings = open("databases/openings.dat", "r")
    for opening in openings:
        opening_split = opening.strip().split(",")
        openings_dict[opening_split[1]] = opening_split[0]
    return openings_dict

def load_openings():
    pass

def store_openings(openings_dict):
    out = open("databases/openings.dat", "w")
    for k,v in openings_dict.items():
        out.write(str(k)+","+str(v)+"\n")