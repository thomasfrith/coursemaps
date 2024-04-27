# divide grid into 10 by 10 boxes
# grid size of 100x60

LENGTH = 76
WIDTH = 50
GRID_LENGTH = 10

# pad the edges with a white border of one grid space (therefore need padding of
# 4 grid spaces, 2 for each side)
BORDER_PADDING = 4*GRID_LENGTH

# how big is one grid square (in metres)
GRID_SQUARE_SIZE = 10

# where to put course markers (in metres)
# these need to be multiples of the unit distance or more so it remains an integer
COURSE_MARKERS = 1000
UNIT_DISTANCE = 1000
