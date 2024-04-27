import numpy as np
import copy

from models import Grid_Type, Course_Type, Course_Marker
from setup import LENGTH, WIDTH, GRID_LENGTH, BORDER_PADDING

# set parameters for map features

max_street_length = 20
min_street_length = 5

max_block_length = 10
min_block_length = 1

max_fraction_trees = 0.1
min_fraction_trees = 0.01

max_bridges = 6
min_bridges = 3

max_lake_length = 12
min_lake_length = 8

max_mud_length = 5
min_mud_length = 2

max_fraction_mud = 0.1
min_fraction_mud = 0.01

max_fraction_wet = 0.001
min_fraction_wet = 0.0001

max_hill_length = 16
min_hill_length = 8

max_hill_height = 10
min_hill_height = 6

max_fraction_hill = 0.75
min_fraction_hill = 0.5


# auto-generate a town with houses, roads, a river and parks with trees.


# what is the previous left tile 
def get_left_tile(grid,x_grid,y_grid):
    
    if x_grid != 0:
        return grid[x_grid-1][y_grid]
    else:
        return Grid_Type.EMPTY
    
# what is the next right tile 
def get_right_tile(grid,x_grid,y_grid):
    
    if x_grid != LENGTH - 1:
        return grid[x_grid+1][y_grid]
    else:
        return Grid_Type.EMPTY
    
# what is the bottom tile
def get_bottom_tile(grid,x_grid,y_grid):
    
    if y_grid != WIDTH - 1:
        return grid[x_grid][y_grid+1]
    else:
        return Grid_Type.EMPTY
    
# what is the previous tile above
def get_top_tile(grid,x_grid,y_grid):
    
    if y_grid != 0:
        return grid[x_grid][y_grid-1]
    else:
        return Grid_Type.EMPTY

# create a river
def place_river(grid):
    
    #does the river start from the top or the left
    river_source = np.random.choice(["top", "left"])
    if river_source == "top":
        x_river = np.random.randint(LENGTH)
        y_river = 0
        river = Grid_Type.RIVER_V
    if river_source == "left":
        x_river = 0
        y_river = np.random.randint(WIDTH)
        river = Grid_Type.RIVER_H


    # work down and right to place sections of river at random
    while x_river < LENGTH and y_river < WIDTH:
                
        grid[x_river][y_river] = river
               
        if river == Grid_Type.RIVER_H or river == Grid_Type.RIVER_B_RT:
            x_river += 1
            river = np.random.choice([Grid_Type.RIVER_H,Grid_Type.RIVER_B_LD])
        elif river == Grid_Type.RIVER_V or river == Grid_Type.RIVER_B_LD:
            y_river += 1
            river = np.random.choice([Grid_Type.RIVER_V,Grid_Type.RIVER_B_RT])
            
    return grid

# create single housing blocks
def place_block(grid,start_x,start_y):
    
    # how many house in a street
    street_length = np.random.randint(min_street_length,max_street_length)
    # are the streets horizontal or vertical?
    street_layout = np.random.choice(["v","h"])
    
    # how many streets are there in this block?
    block_length = np.random.randint(min_block_length,max_block_length)
    
    # depending on the orientation of the block, place houses in lines
    # in sets of two with a gap inbetween for roads
    # if rivers are encountered, don't build on top of them
    # also return the height and width of the block
    for i in range(street_length):
        for j in range(block_length):
            
            if street_layout == "v":
                
                x_block = start_x+3*j+1
                y_block = start_y+i
                if x_block >= LENGTH - 1 or y_block >= WIDTH - 1:
                        return grid, x_block, y_block
                    
                if any(grid[x_block-1][y_block] == rivers for rivers in Grid_Type.CHOICES_RIVER):
                    pass
                else:
                    grid[x_block-1][y_block] = Grid_Type.HOUSE
                if any(grid[x_block][y_block] == rivers for rivers in Grid_Type.CHOICES_RIVER):
                    pass
                else:
                    grid[x_block][y_block] = Grid_Type.HOUSE
            if street_layout == "h":
                
                x_block = start_x+i
                y_block = start_y+3*j+1
                if x_block >= LENGTH - 1 or y_block >= WIDTH - 1:
                        return grid, x_block, y_block
                    
                if any(grid[x_block][y_block-1] == rivers for rivers in Grid_Type.CHOICES_RIVER):
                    pass
                else:
                    grid[x_block][y_block-1] = Grid_Type.HOUSE
                if any(grid[x_block][y_block] == rivers for rivers in Grid_Type.CHOICES_RIVER):
                    pass
                else:
                    grid[x_block][y_block] = Grid_Type.HOUSE

    return grid, x_block, y_block

# create a collection of blocks
# starting from x = 1, y = 1 to leave room for a road
# work left to right and place blocks, recording the maximum height of 
# each row of blocks
# start the next row of blocks from the maximum height of the previous one
def place_streets(grid):
    
    x_loc = 1
    y_loc = 1
    y_max = y_loc
    while y_loc < WIDTH - 1:
        while x_loc < LENGTH - 1:
            grid, x_block, y_block = place_block(grid,x_loc,y_loc)
            x_loc = x_block + 2
            y_max = max(y_max,y_block)
            
        x_loc = 1
        y_loc = y_max + 2    
        
    return grid

# create roads
def place_road_sections(grid):
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            # put in roads between houses
            if t_g == Grid_Type.HOUSE and b_g == Grid_Type.HOUSE and g == 0:
                grid[i][j] = Grid_Type.ROAD_H
            if r_g == Grid_Type.HOUSE and l_g == Grid_Type.HOUSE and g == 0:
                grid[i][j] = Grid_Type.ROAD_V
            
            # put in roads along houses if the otherside is empty
            if ((t_g == Grid_Type.HOUSE and (b_g == Grid_Type.EMPTY or b_g == 0)) or ((t_g == Grid_Type.EMPTY or t_g == 0) and b_g == Grid_Type.HOUSE)) and g == 0:
                grid[i][j] = Grid_Type.ROAD_H
            if ((r_g == Grid_Type.HOUSE and (l_g == Grid_Type.EMPTY or l_g == 0)) or ((r_g == Grid_Type.EMPTY or r_g == 0) and l_g == Grid_Type.HOUSE)) and g == 0:
                grid[i][j] = Grid_Type.ROAD_V
            
            # put in bends if there are two roads that connect to this square
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP) and g ==0:
                grid[i][j] = Grid_Type.ROAD_B_LT
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM) and g ==0:
                grid[i][j] = Grid_Type.ROAD_B_LD   
            if any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP) and g ==0:
                grid[i][j] = Grid_Type.ROAD_B_RT
            if any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM) and g ==0:
                grid[i][j] = Grid_Type.ROAD_B_RD
                    
            #put in turnings if there are three roads that connect to this square
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP):
                grid[i][j] = Grid_Type.ROAD_T_HT
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM):
                grid[i][j] = Grid_Type.ROAD_T_HD
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP):
                grid[i][j] = Grid_Type.ROAD_T_VL
            if any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP):
                grid[i][j] = Grid_Type.ROAD_T_VR
                
            #put in junctions if there are four roads that connect to this square
            if any(l_g == left for left in Grid_Type.CHOICES_FROM_LEFT) and any(r_g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and any(t_g == top for top in Grid_Type.CHOICES_FROM_TOP) and any(b_g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM):
                grid[i][j] = Grid_Type.ROAD_J

    return grid

# interate the road placement until the grid doesn't change
def place_roads(grid):
    
    #what was the old grid
    old_grid = copy.deepcopy(grid)
    #create new grid 
    new_grid = place_road_sections(grid)
    
    #compare the changes, if they are still different, place roads again
    while old_grid != new_grid:
       
        grid = new_grid
        old_grid = copy.deepcopy(grid)
        new_grid = place_road_sections(grid)
    
    return new_grid

# for xc courses, start with one piece of road that will be extended through
# the park
def place_one_road(grid):
    
    i = np.random.randint(0,LENGTH-1)
    j = np.random.randint(0,WIDTH-1)
    
    g = grid[i][j]
    
    if g == 0:
        grid[i][j] = np.random.choice([Grid_Type.ROAD_H,Grid_Type.ROAD_V])
    else:
        place_one_road(grid)
        
    return grid

# create bridges to go over straight sections of river (cannot go over bends)
# also continue unfinished roads if there is nothing in the way
def place_bridge_sections(grid):

    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            # if a road has ended but could continue, continue it!
            if (g == Grid_Type.ROAD_H or g == Grid_Type.BRIDGE_H) and l_g == 0:
                grid[max(i-1,0)][j] = Grid_Type.ROAD_H
            if (g == Grid_Type.ROAD_H or g == Grid_Type.BRIDGE_H) and r_g == 0:
                grid[min(i+1,LENGTH-1)][j] = Grid_Type.ROAD_H
            if (g == Grid_Type.ROAD_V or g == Grid_Type.BRIDGE_V) and t_g == 0:
                grid[i][max(j-1,0)] = Grid_Type.ROAD_V
            if (g == Grid_Type.ROAD_V or g == Grid_Type.BRIDGE_V) and b_g == 0:
                grid[i][min(j+1,WIDTH-1)] = Grid_Type.ROAD_V
            
            # if a straight river section is encountered, build a bridge over it
            if any(g == right for right in Grid_Type.CHOICES_FROM_RIGHT) and l_g == Grid_Type.RIVER_V:
                grid[max(i-1,0)][j] = Grid_Type.BRIDGE_H
            if any(g == left for left in Grid_Type.CHOICES_FROM_LEFT) and r_g == Grid_Type.RIVER_V:
                grid[min(i+1,LENGTH-1)][j] = Grid_Type.BRIDGE_H
            if any(g == bottom for bottom in Grid_Type.CHOICES_FROM_BOTTOM) and t_g == Grid_Type.RIVER_H:
                grid[i][max(j-1,0)] = Grid_Type.BRIDGE_V
            if any(g == top for top in Grid_Type.CHOICES_FROM_TOP) and b_g == Grid_Type.RIVER_H:
                grid[i][min(j+1,WIDTH-1)] = Grid_Type.BRIDGE_V
                
    return grid

# iterate the bridge placement and road building until the grid remains unchanged
def place_bridges(grid):
    
    old_grid = copy.deepcopy(grid)
    new_grid = place_bridge_sections(grid)
    
    while old_grid != new_grid:
       
        grid = new_grid
        old_grid = copy.deepcopy(grid)
        new_grid = place_bridge_sections(grid)
        
    new_grid = place_roads(new_grid)
    
    return new_grid

# create parks in any remaining emtpy space (and in courtyards and cul-de-sacs)
def place_park(grid):
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            # if space is empty, place a park
            if g==0:
                grid[i][j] = Grid_Type.PARK
            # place park inbetween four or three houses, overwriting roads
            # but not overwriting houses (rivers could never be between three
            # or more houses)
            if g != Grid_Type.HOUSE:
                if l_g == Grid_Type.HOUSE and r_g == Grid_Type.HOUSE and t_g == Grid_Type.HOUSE:
                    grid[i][j] = Grid_Type.PARK
                if l_g == Grid_Type.HOUSE and r_g == Grid_Type.HOUSE and b_g == Grid_Type.HOUSE:
                    grid[i][j] = Grid_Type.PARK
                if l_g == Grid_Type.HOUSE and b_g == Grid_Type.HOUSE and t_g == Grid_Type.HOUSE:
                    grid[i][j] = Grid_Type.PARK
                if r_g == Grid_Type.HOUSE and b_g == Grid_Type.HOUSE and t_g == Grid_Type.HOUSE:
                    grid[i][j] = Grid_Type.PARK
                if l_g == Grid_Type.HOUSE and r_g == Grid_Type.HOUSE and t_g == Grid_Type.HOUSE and b_g == Grid_Type.HOUSE:
                    grid[i][j] = Grid_Type.PARK
                
    return grid

# if a river is now running through a park, make the background a park,
# otherwise leave it
def urban_rural_rivers(grid):
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            # is the square a river
            if any(g == rivers for rivers in Grid_Type.CHOICES_RIVER):
                area = [l_g,r_g,t_g,b_g]
                count = 0
                # are the surrounding adjacent squares park or river?
                for square in area:
                    if any(square == rural for rural in Grid_Type.CHOICES_RIVER_PARK):
                        count += 1
                
                # if more than one square is a park or a river, make it a rural river
                # these means only rivers going under bridges are urban 
                # it looks nicer needing only two squares
                if count>1:
                    grid[i][j] =  "rural_" + g
                    
    return grid

# for xc, place some bridges over the river for better access
def rural_bridges(grid):
    
    # how many squares are river straights
    num_river_straights = sum(x.count(Grid_Type.RIVER_R_H) for x in grid) + sum(x.count(Grid_Type.RIVER_R_V) for x in grid)
    # create the number of bridges
    num_bridges = round(np.random.randint(min_bridges,max_bridges+1))
    # put the bridgees at random locations along the river
    bridge_loc = sorted(np.random.randint(1,num_river_straights,num_bridges+1))
    
    count = 0
    
    # in the grid, if a square is a river straight, count it, if the count matches the 
    # location of a bridge, place a bridge there
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            if g == Grid_Type.RIVER_R_H or g == Grid_Type.RIVER_R_V:
                count += 1
                if any(count == bridges for bridges in bridge_loc):
                    if g == Grid_Type.RIVER_R_H:
                        grid[i][j] = Grid_Type.BRIDGE_V
                    if g == Grid_Type.RIVER_R_V:
                        grid[i][j] = Grid_Type.BRIDGE_H
                    
    return grid

# place a rectangular lake (will be updated later)
def place_lake_tile(grid, start_x, start_y, lake_length, lake_width):    
    
    for i in range(lake_length):
        for j in range(lake_width):
            grid[start_x+i][start_y+j] = Grid_Type.LAKE
            
    return grid

def place_basic_lake(grid):
    
    lake_length = np.random.randint(min_lake_length,max_lake_length+1)
    lake_width = np.random.randint(min_lake_length,max_lake_length+1)
    
    start_x = np.random.randint(0 + lake_length + 1, LENGTH - 2*lake_length)
    start_y = np.random.randint(0 + lake_width + 1, WIDTH - 2*lake_width)
    
    grid = place_lake_tile(grid, start_x , start_y, lake_length, lake_width)
        
    grid = place_lake_tile(grid, start_x + np.random.randint(round(lake_length/2)), start_y + np.random.choice([lake_width,round(-lake_width/2)]), \
                           round(lake_length/2),round(lake_width/2))
    grid = place_lake_tile(grid, start_x + np.random.choice([lake_length,round(-lake_length/2)]) ,start_y + np.random.randint(round(lake_width/2)), \
                           round(lake_length/2),round(lake_width/2))
        
    return grid

#def place_lake(grid):
#    
#    grid = place_basic_lake(grid)
#    
#    for i in range(LENGTH):
#        for j in range(WIDTH):
#            
#            g = grid[i][j]
#            l_g = get_left_tile(grid,i,j)
#            r_g = get_right_tile(grid,i,j)
#            t_g = get_top_tile(grid,i,j)
#            b_g = get_bottom_tile(grid,i,j)
#            
#            if g == Grid_Type.LAKE:
#                if l_g not in Grid_Type.CHOICES_LAKE and t_g not in Grid_Type.CHOICES_LAKE:
#                    grid[i][j] = Grid_Type.LAKE_LT
#                if l_g not in Grid_Type.CHOICES_LAKE and b_g not in Grid_Type.CHOICES_LAKE:
#                    grid[i][j] = Grid_Type.LAKE_LD
#                if r_g not in Grid_Type.CHOICES_LAKE and t_g not in Grid_Type.CHOICES_LAKE:
#                    grid[i][j] = Grid_Type.LAKE_RT
#                if r_g not in Grid_Type.CHOICES_LAKE and b_g not in Grid_Type.CHOICES_LAKE:
#                    grid[i][j] = Grid_Type.LAKE_RD
#                    
#    return grid

def place_lake(grid):
    
    # how many squares are parks
    num_park = sum(x.count(Grid_Type.PARK) for x in grid)
    # how many puddles
    num_mud = round(num_park*np.random.uniform(min_fraction_wet,max_fraction_wet))
    
    
    count = 0
    
    while count <= num_mud:
    
        start_x = np.random.randint(0, LENGTH)
        start_y = np.random.randint(0, WIDTH)
    
        grid = place_lake_tile(grid, start_x , start_y, 1, 1)
        
        count += 1
        
        
    return grid

# place a rectangular mud patch (will be updated later)
def place_mud_tile(grid, start_x, start_y, mud_length, mud_width):    
    
    for i in range(mud_length):
        for j in range(mud_width):
            if grid[start_x+i][start_y+j] == Grid_Type.PARK:
                grid[start_x+i][start_y+j] = Grid_Type.MUD
            
    return grid

def place_basic_mud(grid):
    
    # how many squares are parks
    num_park = sum(x.count(Grid_Type.PARK) for x in grid)
    # create the number of trees based on the number of parks
    num_mud = round(num_park*np.random.uniform(min_fraction_mud,max_fraction_mud))
    
    count = 0
    
    while count <= num_mud:
        
        mud_length = np.random.randint(min_mud_length,max_mud_length+1)
        mud_width = np.random.randint(min_mud_length,max_mud_length+1)
    
        start_x = np.random.randint(0 + max_mud_length, LENGTH - max_mud_length)
        start_y = np.random.randint(0 + max_mud_length, WIDTH - max_mud_length)
    
        grid = place_mud_tile(grid, start_x , start_y, mud_length, mud_width)
        
        count += mud_length*mud_width
        
        
    return grid

def place_mud(grid):
    
    grid = place_basic_mud(grid)
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            if g == Grid_Type.MUD:
                if l_g not in Grid_Type.CHOICES_MUD and t_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_LT
                if l_g not in Grid_Type.CHOICES_MUD and b_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_LD
                if r_g not in Grid_Type.CHOICES_MUD and t_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_RT
                if r_g not in Grid_Type.CHOICES_MUD and b_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_RD
                    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            l_g = get_left_tile(grid,i,j)
            r_g = get_right_tile(grid,i,j)
            t_g = get_top_tile(grid,i,j)
            b_g = get_bottom_tile(grid,i,j)
            
            if any(g == mud for mud in Grid_Type.CHOICES_MUD):
                if l_g not in Grid_Type.CHOICES_MUD and r_g not in Grid_Type.CHOICES_MUD and t_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_D
                if l_g not in Grid_Type.CHOICES_MUD and r_g not in Grid_Type.CHOICES_MUD and b_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_T
                if r_g not in Grid_Type.CHOICES_MUD and b_g not in Grid_Type.CHOICES_MUD and t_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_L
                if l_g not in Grid_Type.CHOICES_MUD and b_g not in Grid_Type.CHOICES_MUD and t_g not in Grid_Type.CHOICES_MUD:
                    grid[i][j] = Grid_Type.MUD_R
                    
    return grid

def place_puddles(grid):
    
    # how many squares are parks
    num_mud = sum(x.count(Grid_Type.MUD) for x in grid)
    # create the number of trees based on the number of parks
    num_puddles = int(round(num_mud*0.05))
    puddles_loc = sorted(np.random.randint(1,num_mud,num_puddles+1))
    
    count = 0
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            
            if g == Grid_Type.MUD:
                count += 1
                if any(count == puddle for puddle in puddles_loc):
                    grid[i][j] = Grid_Type.PUDDLE
                    
        
        
    return grid

def place_hill_tile(grid, hill_grid, start_x , start_y, bottom_hill_length, bottom_hill_width, ratio, hill_height):
    
    for i in range(bottom_hill_length):
        for j in range(bottom_hill_width):
            
            g = grid[start_x+i][start_y+j]
            contour_number = hill_height
                
            contour_spacing_x = bottom_hill_length*(1-ratio)/(2*contour_number)
            contour_spacing_y = bottom_hill_width*(1-ratio)/(2*contour_number)
            
            for height in range(contour_number):
                
                semi_major = round(bottom_hill_length/2 - height*contour_spacing_x)
                semi_minor = round(bottom_hill_width/2 - height*contour_spacing_y)
                
                if ellipse(i,j,round(bottom_hill_length/2),round(bottom_hill_width/2),semi_major,semi_minor) < 1 and \
                (g == Grid_Type.PARK or any(Grid_Type.HILL == hills for hills in hill_grid[start_x+i][start_y+j]) or (any(g == mud for mud in Grid_Type.CHOICES_MUD))\
                 or g == Grid_Type.PUDDLE):
                            
                    hill_grid[start_x+i][start_y+j][height] = Grid_Type.HILL  
                                              
    return hill_grid

def place_hill_mud_tile(grid, mud_grid, start_x , start_y, bottom_hill_length, bottom_hill_width, ratio, hill_height):
    
    for i in range(bottom_hill_length):
        for j in range(bottom_hill_width):
            
            g = grid[start_x+i][start_y+j]
            contour_number = hill_height
                
            contour_spacing_x = bottom_hill_length*(1-ratio)/(2*contour_number)
            contour_spacing_y = bottom_hill_width*(1-ratio)/(2*contour_number)
            
            for height in range(contour_number):
                
                semi_major = round(bottom_hill_length/2 - height*contour_spacing_x)
                semi_minor = round(bottom_hill_width/2 - height*contour_spacing_y)
                                    
                if ellipse(i,j,round(bottom_hill_length/2),round(bottom_hill_width/2),semi_major,semi_minor) < 1 and \
                (any(g == mud for mud in Grid_Type.CHOICES_MUD)):
                            
                    mud_grid[start_x+i][start_y+j][height] = Grid_Type.MUD
                
                elif ellipse(i,j,round(bottom_hill_length/2),round(bottom_hill_width/2),semi_major,semi_minor) < 1 and \
                g == Grid_Type.PUDDLE:
                            
                    mud_grid[start_x+i][start_y+j][height] = Grid_Type.PUDDLE
                                              
    return mud_grid
    

# place some hills
def place_hills(grid):
    
    # how many squares are parks
    num_park = sum(x.count(Grid_Type.PARK) for x in grid)
    # create the number of hills based on the number of parks
    num_hills = round(num_park*np.random.uniform(min_fraction_hill,max_fraction_hill))
    
    hill_grid = [[[0 for n in range(max_hill_height)] for i in range(WIDTH)] for i in range(LENGTH)]
    mud_grid = [[[0 for n in range(max_hill_height)] for i in range(WIDTH)] for i in range(LENGTH)]
    
    count = 0
    
    while count <= num_hills:
        
        bottom_hill_length = np.random.randint(min_hill_length,max_hill_length)
        bottom_hill_width = np.random.randint(min_hill_length,max_hill_length)
        
        ratio = np.random.uniform(0.25,0.1)
        
        hill_height = np.random.randint(min_hill_height,max_hill_height)
    
        start_x = np.random.randint(0, LENGTH - max_hill_length)
        start_y = np.random.randint(0, WIDTH - max_hill_length)
    
        hill_grid = place_hill_tile(grid, hill_grid, start_x , start_y, bottom_hill_length, bottom_hill_width, ratio, hill_height)
        mud_grid = place_hill_mud_tile(grid, mud_grid, start_x , start_y, bottom_hill_length, bottom_hill_width, ratio, hill_height)
        
        count += bottom_hill_length*bottom_hill_width
        
    for n in range(max_hill_height):                   
        for i in range(LENGTH):
            for j in range(WIDTH):
                
                g = hill_grid[i][j][n]
                l_g = get_left_tile(hill_grid,i,j)
                r_g = get_right_tile(hill_grid,i,j)
                t_g = get_top_tile(hill_grid,i,j)
                b_g = get_bottom_tile(hill_grid,i,j)
                
                if g == Grid_Type.HILL:
                    if l_g[n] not in Grid_Type.CHOICES_HILL and t_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_LT
                    if l_g[n] not in Grid_Type.CHOICES_HILL and b_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_LD
                    if r_g[n] not in Grid_Type.CHOICES_HILL and t_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_RT
                    if r_g[n] not in Grid_Type.CHOICES_HILL and b_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_RD
                        
                g = mud_grid[i][j][n]
                l_g = get_left_tile(mud_grid,i,j)
                r_g = get_right_tile(mud_grid,i,j)
                t_g = get_top_tile(mud_grid,i,j)
                b_g = get_bottom_tile(mud_grid,i,j)
                        
                if g == Grid_Type.MUD:
                    if l_g[n] not in Grid_Type.CHOICES_MUD and t_g[n] not in Grid_Type.CHOICES_MUD:
                        mud_grid[i][j][n] = Grid_Type.MUD_LT
                    if l_g[n] not in Grid_Type.CHOICES_MUD and b_g[n] not in Grid_Type.CHOICES_MUD:
                        mud_grid[i][j][n] = Grid_Type.MUD_LD
                    if r_g[n] not in Grid_Type.CHOICES_MUD and t_g[n] not in Grid_Type.CHOICES_MUD:
                        mud_grid[i][j][n] = Grid_Type.MUD_RT
                    if r_g[n] not in Grid_Type.CHOICES_MUD and b_g[n] not in Grid_Type.CHOICES_MUD:
                        mud_grid[i][j][n] = Grid_Type.MUD_RD
    
    for n in range(max_hill_height):              
        for i in range(LENGTH):
            for j in range(WIDTH):
                
                g = hill_grid[i][j][n]
                l_g = get_left_tile(hill_grid,i,j)
                r_g = get_right_tile(hill_grid,i,j)
                t_g = get_top_tile(hill_grid,i,j)
                b_g = get_bottom_tile(hill_grid,i,j)
                
                if any(g == hill for hill in Grid_Type.CHOICES_HILL):
                    if l_g[n] not in Grid_Type.CHOICES_HILL and r_g[n] not in Grid_Type.CHOICES_HILL and t_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_D
                    if l_g[n] not in Grid_Type.CHOICES_HILL and r_g[n] not in Grid_Type.CHOICES_HILL and b_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_T
                    if r_g[n] not in Grid_Type.CHOICES_HILL and b_g[n] not in Grid_Type.CHOICES_HILL and t_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_L
                    if l_g[n] not in Grid_Type.CHOICES_HILL and b_g[n] not in Grid_Type.CHOICES_HILL and t_g[n] not in Grid_Type.CHOICES_HILL:
                        hill_grid[i][j][n] = Grid_Type.HILL_R
                        
#                g = mud_grid[i][j][n]
#                l_g = get_left_tile(mud_grid,i,j)
#                r_g = get_right_tile(mud_grid,i,j)
#                t_g = get_top_tile(mud_grid,i,j)
#                b_g = get_bottom_tile(mud_grid,i,j)
#                        
#                if any(g == mud for mud in Grid_Type.CHOICES_MUD):
#                    if l_g[n] not in Grid_Type.CHOICES_MUD and r_g[n] not in Grid_Type.CHOICES_MUD and t_g[n] not in Grid_Type.CHOICES_MUD:
#                        mud_grid[i][j][n] = Grid_Type.MUD_D
#                    if l_g[n] not in Grid_Type.CHOICES_MUD and r_g[n] not in Grid_Type.CHOICES_MUD and b_g[n] not in Grid_Type.CHOICES_MUD:
#                        mud_grid[i][j][n] = Grid_Type.MUD_T
#                    if r_g[n] not in Grid_Type.CHOICES_MUD and b_g[n] not in Grid_Type.CHOICES_MUD and t_g[n] not in Grid_Type.CHOICES_MUD:
#                        mud_grid[i][j][n] = Grid_Type.MUD_L
#                    if l_g[n] not in Grid_Type.CHOICES_MUD and b_g[n] not in Grid_Type.CHOICES_MUD and t_g[n] not in Grid_Type.CHOICES_MUD:
#                        mud_grid[i][j][n] = Grid_Type.MUD_R
        
        
    return hill_grid
    
# create trees in the parks
def place_trees(grid,hill_grid):
    
    # how many squares are parks
    num_park = sum(x.count(Grid_Type.PARK) for x in grid)
    # create the number of trees based on the number of parks
    num_trees = round(num_park*np.random.uniform(min_fraction_trees,max_fraction_trees))
    # put the trees at random locations in the parks
    tree_loc = sorted(np.random.randint(1,num_park,num_trees+1))
    
    count = 0
    
    # in the grid, if a square is a park, count it, if the count matches the 
    # location of a tree, place a tree there
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = grid[i][j]
            if g == Grid_Type.PARK:
                count += 1
                if any(count == trees for trees in tree_loc):
                    grid[i][j] = Grid_Type.TREE
                    for n in range(max_hill_height):
                        if hill_grid[i][j][n] == Grid_Type.HILL:
                            hill_grid[i][j][n] = Grid_Type.TREE
                        
                    
    return grid, hill_grid

def clean_up_course(grid,hill_grid,course_grid):
    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = course_grid[i][j]
            l_g = get_left_tile(course_grid,i,j)
            r_g = get_right_tile(course_grid,i,j)
            t_g = get_top_tile(course_grid,i,j)
            b_g = get_bottom_tile(course_grid,i,j)
            
            if g == Course_Type.COURSE_H:
                if t_g == Course_Type.COURSE_V and any(r_g == course for course in Course_Type.CHOICES):
                    course_grid[i][j] = Course_Type.COURSE_B_RT
                if t_g == Course_Type.COURSE_V and any(l_g == course for course in Course_Type.CHOICES):
                    course_grid[i][j] = Course_Type.COURSE_B_LT
                if b_g == Course_Type.COURSE_V and any(r_g == course for course in Course_Type.CHOICES):
                    course_grid[i][j] = Course_Type.COURSE_B_RD
                if b_g == Course_Type.COURSE_V and any(l_g == course for course in Course_Type.CHOICES):
                    course_grid[i][j] = Course_Type.COURSE_B_LD
                
            if g == Course_Type.COURSE_V:
                if any(t_g == course for course in Course_Type.CHOICES) and r_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_B_RT
                if any(t_g == course for course in Course_Type.CHOICES) and l_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_B_LT
                if any(b_g == course for course in Course_Type.CHOICES) and r_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_B_RD
                if any(b_g == course for course in Course_Type.CHOICES) and l_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_B_LD
                    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            g = course_grid[i][j]
            l_g = get_left_tile(course_grid,i,j)
            r_g = get_right_tile(course_grid,i,j)
            t_g = get_top_tile(course_grid,i,j)
            b_g = get_bottom_tile(course_grid,i,j)
            
            if g == Course_Type.COURSE_B_LD:
                if t_g == Course_Type.COURSE_V:
                    course_grid[i][j] = Course_Type.COURSE_T_VL
                if r_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_T_HD
            if g == Course_Type.COURSE_B_LT:
                if b_g == Course_Type.COURSE_V:
                    course_grid[i][j] = Course_Type.COURSE_T_VL
                if r_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_T_HT
            if g == Course_Type.COURSE_B_RD:
                if t_g == Course_Type.COURSE_V:
                    course_grid[i][j] = Course_Type.COURSE_T_VR
                if l_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_T_HD
            if g == Course_Type.COURSE_B_RT:
                if b_g == Course_Type.COURSE_V:
                    course_grid[i][j] = Course_Type.COURSE_T_VR
                if l_g == Course_Type.COURSE_H:
                    course_grid[i][j] = Course_Type.COURSE_T_HT
                    
        
    course_grid_alt = [[[0 for n in range(max_hill_height)] for i in range(WIDTH)] for i in range(LENGTH)]
                    
    for i in range(LENGTH):
        for j in range(WIDTH):
            
            if course_grid[i][j] != 0 and any(grid[i][j] == road for road in [Grid_Type.ROAD_V,Grid_Type.ROAD_H]):
                grid[i][j] = Grid_Type.ROAD_CROSSING
                
            if course_grid[i][j] != 0 and grid[i][j] == Grid_Type.TREE:
                grid[i][j] = Grid_Type.PARK
            
            if course_grid[i][j] != 0 and grid[i][j] == Grid_Type.PUDDLE:
                grid[i][j] = Grid_Type.MUD
            
            for n in range(max_hill_height):
                
                if course_grid[i][j] != 0 and (any(hill_grid[i][j][n] == hill for hill in Grid_Type.CHOICES_HILL) or hill_grid[i][j][n] == Grid_Type.TREE):
                    
                    course_grid_alt[i][j][n] = course_grid[i][j]
                    
                    if hill_grid[i][j][n] == Grid_Type.TREE:
                        hill_grid[i][j][n] = Grid_Type.HILL                      
                        
                    
                    
                    
                    
    return course_grid, course_grid_alt

def ellipse(x,y,center_x,center_y,semi_major, semi_minor):
        
    return ((y-center_y)/semi_minor)**2 + ((x-center_x)/semi_major)**2
        