import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import re
from openings import get_openings
from openings import store_openings



# turns pgn format into a more useful format

# main program entry
def main():
    openings_dict = get_openings()
    print(openings_dict)
    pgns = open("databases/lichess_db_standard_rated_2013-01.pgn", "r")
    out = open("databases/OUT_lichess_db_standard_rated_2013-01.pgn", "w")
    #openings = {}
    start = time.time()
    process(openings_dict, pgns, out)
    end = time.time() - start
    print(end)
    #print(openings_dict)
    store_openings(openings_dict)
    #print(openings)

def process(openings_dict, pgns, out):
    result = avg_elo = white_elo = 0 # 1 if white win, 0 if draw, 2 if black win
    opening = ''
    i = 0
    for line in pgns:
        # testing
        #if i > 127:   
        #    return

        if line.startswith("[R"): #Result 
            i+=1
            quote_val = match_quotes(line)
            result = get_result(quote_val)

        elif line.startswith("[WhiteE"): #WhiteElo
            quote_val = match_quotes(line)
            white_elo = elo_to_int(quote_val)

        elif line.startswith("[BlackE"): #BlackElo
            quote_val = match_quotes(line)
            black_elo = elo_to_int(quote_val)
            # we can assume white's elo is already known because of the PGN format
            avg_elo = get_avg_elo(white_elo, black_elo)
            #print(avg_elo)
            
        elif line.startswith("[Opening"):
            quote_val = match_quotes(line)
            #opening_str = quote_val.split(":")[0]
            opening_str = clean_opening_str(quote_val)
            #print(quote_val,"-->>>", opening_str)
            #opening = opening_to_int(quote_val)
            opening = opening_to_int(openings_dict, opening_str)
            
            #print(opening_str)
            #print(i,"result:",result,"elo",avg_elo,"opening:",opening, opening_str)
            #print(opening, opening_str)s
            out.write(str(result)+","+str(avg_elo)+","+str(opening)+"\n")

def clean_opening_str(opening_str):
    opening_str = opening_str.split(":")[0]
    opening_str = opening_str.split("#")[0].strip()
    #print(opening_str)
    return opening_str

def get_avg_elo(elo1, elo2):
    # check for and ignore bad elo values
    if (elo1 == 0):
        return elo2
    if (elo2 == 0):
        return elo1
    return np.divide(np.add(elo1, elo2), 2)

def elo_to_int(elo):
    elo = strip_questionmark(elo)
    if elo == '':
        #print("found empty elo... ignoring...")
        return 0
    else:
        return int(elo)


def strip_questionmark(quote_val):
    return quote_val.replace("?","") 

def opening_to_int(openings_dict, opening_str):
    opening_int = openings_dict.get(opening_str)
    if not opening_int:
        openings_dict[opening_str] = len(openings_dict)+1
        opening_int = len(openings_dict)+1
    return opening_int



def get_result(quote_val):
    if quote_val.startswith("1/"): #draw
        return 0
    elif quote_val.startswith("1"): #white win
        return 1
    else:
        return 2

def match_quotes(line):
    return re.search("\"(.)*\"", line).group(0)[1:-1]

if __name__ == "__main__":
    main()

