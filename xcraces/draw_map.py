import cv2 as c
import numpy as np

from draw_rules import place_river,place_streets,place_roads,place_bridges,place_park,urban_rural_rivers,place_lake,place_mud,\
place_puddles, place_trees, place_one_road, rural_bridges, place_hills,clean_up_course,\
max_hill_height
from draw_features import interpret_grid, interpret_course, place_course_marker, place_course_title
from models import Course_Type, Grid_Type
from setup import LENGTH, WIDTH, GRID_LENGTH, GRID_SQUARE_SIZE, BORDER_PADDING, UNIT_DISTANCE
from course_rules import Runner

# set the map seed
map_num = 200
# set the race distance (in metres)
race_distance = 10000

# adjust the race distance to the number of grid squares 
adjusted_race_distance = round(race_distance/GRID_SQUARE_SIZE)
#set the random map seed
np.random.seed(map_num)

#c.destroyAllWindows().


# initiate the image as a green background with a white border
img = np.zeros((WIDTH*GRID_LENGTH + BORDER_PADDING,LENGTH*GRID_LENGTH + BORDER_PADDING,3),np.uint8)
img[:] = (44,160,44)

img[0:round(BORDER_PADDING/2)].fill(255)
img[WIDTH*GRID_LENGTH + round(BORDER_PADDING/2):WIDTH*GRID_LENGTH + BORDER_PADDING].fill(255)

for img_row in img:
    img_row[0:round(BORDER_PADDING/2)].fill(255)
    img_row[LENGTH*GRID_LENGTH + round(BORDER_PADDING/2):LENGTH*GRID_LENGTH + BORDER_PADDING].fill(255)


# initiate the map grid, the course grid and for course markers
grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
course_grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
course_markers = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
start_finish_markers = [[0 for i in range(WIDTH)] for i in range(LENGTH)]

# make the map
grid = place_river(grid)
grid = place_one_road(grid)
grid = place_bridges(grid)
grid = place_park(grid)
grid = place_lake(grid)
grid = urban_rural_rivers(grid)
grid = rural_bridges(grid)
grid = place_mud(grid)
grid = place_puddles(grid)
hill_grid = place_hills(grid)
grid, hill_grid = place_trees(grid,hill_grid)

# get the runner to run the course, starting in the top left, running right with the first turn downwards
initial_direction = Runner.RIGHT
initial_turn = Runner.DOWN
runner = Runner(initial_direction,initial_turn,4,4)
course = [Course_Type.SMALL_LAP,Course_Type.SMALL_LAP,Course_Type.SMALL_LAP]
course_grid, course_markers = runner.run_course(grid, hill_grid, course_grid, course_markers, start_finish_markers, adjusted_race_distance,course)

course_grid, course_grid_alt = clean_up_course(grid, hill_grid, course_grid)

# draw the grid and the course onto the map
for i in range(LENGTH):
    for j in range(WIDTH):
        interpret_grid(grid,i,j,-1,img)
        for n in range(max_hill_height):
            interpret_grid(hill_grid,i,j,n,img)

# put mud on the hills and the course on the mud        
for i in range(LENGTH):
    for j in range(WIDTH):         
            
        interpret_course(grid,course_grid,i,j,-1,img)
        
        for n in range(max_hill_height):
            interpret_course(grid,course_grid_alt,i,j,n,img)

# place the course markers on top of the map    
for i in range(LENGTH):
    for j in range(WIDTH):
        place_course_marker(start_finish_markers,i,j,img)
        #place_course_marker(course_markers,i,j,img)
        
place_course_title(course,runner.laps,race_distance/UNIT_DISTANCE,0,0,img)

# save the image as a png and the course coordinates (x,y,distance(m)) as a csv
path = "C:/Users/thoma/Anaconda3/coursemaps/xcraces/images"
c.imwrite(path + "/" + "xc_course_map_" + str(race_distance) + "_" + str(LENGTH) + "x" + str(WIDTH) + "_" + str(map_num) + ".png", img)
np.savetxt(path + "/" + "xc_course_coords_"  + str(race_distance) + "_" + str(LENGTH) + "x" + str(WIDTH) + "_" + str(map_num) + ".csv", runner.coords,delimiter =", ", fmt ='% s')

c.imshow("img",img)
c.waitKey(0)


