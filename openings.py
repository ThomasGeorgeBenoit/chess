# manages the opening.dat file. Used by preprocess and im sure process in the future.

# where we save our dictionary of openings at the end. Shouldnt be horribly long.
# maps ints to openings for later analysis. For now we just care about the int values!
openings_dict = {}

# loads in the opening file into a dictionary and returns it (a dictionary).
def get_openings(path):
    openings = open(path+"/openings.dat", "r")
    #if len(openings.readlines()) == 0:
    #    return {}
    for opening in openings:
        opening_split = opening.strip().split(",")
        openings_dict[opening_split[1]] = opening_split[0]
    return openings_dict

# stores an openings dictionary into the openings.dat file after use.
# the opposite of get_openings
def store_openings(path, openings_dict):
    out = open(path+"/openings.dat", "w")
    for k,v in openings_dict.items():
        out.write(str(k)+","+str(v)+"\n")