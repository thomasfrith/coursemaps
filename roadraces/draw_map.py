import cv2 as c
import numpy as np

from draw_rules import place_river,place_streets,place_roads,place_bridges,place_park,urban_rural_rivers,place_trees,interpret_grid,place_course_marker
from setup import LENGTH, WIDTH, GRID_LENGTH, GRID_SQUARE_SIZE, BORDER_PADDING
from course_rules import Runner

# set the map seed
map_num = 36
# set the race distance (in metres)
race_distance = 10000

# adjust the race distance to the number of grid squares 
adjusted_race_distance = round(race_distance/GRID_SQUARE_SIZE)
#set the random map seed
np.random.seed(map_num)

#c.destroyAllWindows().


# initiate the image as a white background
img = np.zeros((WIDTH*GRID_LENGTH + BORDER_PADDING,LENGTH*GRID_LENGTH + BORDER_PADDING,3),np.uint8)
img.fill(100)
img[0:round(BORDER_PADDING/2)].fill(255)
img[WIDTH*GRID_LENGTH+round(BORDER_PADDING/2):WIDTH*GRID_LENGTH+round(BORDER_PADDING)].fill(255)
[y[0:round(BORDER_PADDING/2)].fill(255) for y in img]
[y[LENGTH*GRID_LENGTH+round(BORDER_PADDING/2):LENGTH*GRID_LENGTH+round(BORDER_PADDING)].fill(255) for y in img]

# initiate the map grid, the course grid and for course markers
grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
course_grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
course_markers = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
start_finish_markers = [[0 for i in range(WIDTH)] for i in range(LENGTH)]

# make the map
grid = place_river(grid)
grid = place_streets(grid)
grid = place_roads(grid)
grid = place_bridges(grid)
grid = place_park(grid)
grid = urban_rural_rivers(grid)
grid = place_trees(grid)

# get the runner to run the course, starting in the top left, running right
initial_direction = Runner.RIGHT
runner = Runner(initial_direction,0,0)
course_grid, course_markers = runner.run_course(grid, course_grid, course_markers, start_finish_markers, adjusted_race_distance)

# draw the grid and the course onto the map
for i in range(LENGTH):
    for j in range(WIDTH):
        interpret_grid(grid,i,j,img)
        interpret_grid(course_grid,i,j,img)
    
# place the course markers on top of the map    
for i in range(LENGTH):
    for j in range(WIDTH):
        place_course_marker(start_finish_markers,i,j,img)
        place_course_marker(course_markers,i,j,img)

# save the image as a png and the course coordinates (x,y,distance(m)) as a csv
path = "C:/Users/thoma/Anaconda3/coursemaps/roadraces/images"
c.imwrite(path + "/" + "course_map_" + str(race_distance) + "_" + str(LENGTH) + "x" + str(WIDTH) + "_" + str(map_num) + ".png", img)
np.savetxt(path + "/" + "course_coords_"  + str(race_distance) + "_" + str(LENGTH) + "x" + str(WIDTH) + "_" + str(map_num) + ".csv", runner.coords,delimiter =", ", fmt ='% s')

c.imshow("img",img)
c.waitKey(0)


