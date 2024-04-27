import numpy as np
import copy

from models import Grid_Type, Course_Type, Course_Marker
from setup import LENGTH, WIDTH, GRID_LENGTH, BORDER_PADDING
from draw_features import min_street_length,max_street_length, min_block_length,max_block_length,max_fraction_trees,min_fraction_trees,draw_house,draw_road,draw_bend,draw_junction,draw_turning, draw_river, draw_river_bend, draw_bridge, draw_park, draw_tree, draw_course, draw_course_bend, draw_course_marker, draw_course_marker_start, draw_course_marker_finish


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

# create trees in the parks
def place_trees(grid):
    
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
                    
    return grid
        
# draw the features from the grid onto the image
def interpret_grid(grid,x_grid,y_grid,img):
    
    g = grid[x_grid][y_grid]
    # the coordinates of the grid need to be multiplied by the actual size of 
    # each grid square
    x_coord = x_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    y_coord = y_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    
    if g == Grid_Type.HOUSE:
        draw_house(img,x_coord,y_coord)
        
    if g == Grid_Type.ROAD_J:
        draw_junction(img,x_coord,y_coord) 
    if g == Grid_Type.ROAD_H or g == Grid_Type.ROAD_V:
        draw_road(img,x_coord,y_coord,g[-1])
    if g == Grid_Type.ROAD_B_LD or g == Grid_Type.ROAD_B_LT or g == Grid_Type.ROAD_B_RT or g == Grid_Type.ROAD_B_RD:
        draw_bend(img,x_coord,y_coord,g[len(g)-2:len(g)])    
    if g == Grid_Type.ROAD_T_HT or g == Grid_Type.ROAD_T_HD or g == Grid_Type.ROAD_T_VL or g == Grid_Type.ROAD_T_VR:
        draw_turning(img,x_coord,y_coord,g[len(g)-2:len(g)]) 
        
    if g == Grid_Type.RIVER_B_LD or g == Grid_Type.RIVER_B_LT or g == Grid_Type.RIVER_B_RT or g == Grid_Type.RIVER_B_RD:
        draw_river_bend(img,x_coord,y_coord,g[len(g)-2:len(g)])  
    if g == Grid_Type.RIVER_H or g == Grid_Type.RIVER_V:
        draw_river(img,x_coord,y_coord,g[-1])
    if g == Grid_Type.RIVER_R_B_LD or g == Grid_Type.RIVER_R_B_LT or g == Grid_Type.RIVER_R_B_RT or g == Grid_Type.RIVER_R_B_RD:
        draw_park(img,x_coord,y_coord)
        draw_river_bend(img,x_coord,y_coord,g[len(g)-2:len(g)])  
    if g == Grid_Type.RIVER_R_H or g == Grid_Type.RIVER_R_V:
        draw_park(img,x_coord,y_coord)
        draw_river(img,x_coord,y_coord,g[-1])
        
    if g == Grid_Type.BRIDGE_H or g == Grid_Type.BRIDGE_V:
        draw_bridge(img,x_coord,y_coord,g[-1])
    if g == Grid_Type.PARK:
        draw_park(img,x_coord,y_coord)
        
    if g == Grid_Type.TREE:
        draw_tree(img,x_coord,y_coord)
        
    if g == Course_Type.COURSE_H or g == Course_Type.COURSE_V:
        draw_course(img,x_coord,y_coord,g[-1])
    if g == Course_Type.COURSE_B_LD or g == Course_Type.COURSE_B_LT or g == Course_Type.COURSE_B_RT or g == Course_Type.COURSE_B_RD:
        draw_course_bend(img,x_coord,y_coord,g[len(g)-2:len(g)]) 

# put down the course markers       
def place_course_marker(grid, x_grid, y_grid, img):
    
    g = grid[x_grid][y_grid]
    # the coordinates of the grid need to be multiplied by the actual size of 
    # each grid square
    x_coord = x_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    y_coord = y_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    
    if g != 0:
        if g == Course_Marker.COURSE_M_S_H or g == Course_Marker.COURSE_M_S_V:
            draw_course_marker_start(img,x_coord,y_coord,g[-1])
        elif g == Course_Marker.COURSE_M_F_H or g == Course_Marker.COURSE_M_F_V:
            draw_course_marker_finish(img,x_coord,y_coord,g[-1])
        else:
            draw_course_marker(img,x_coord,y_coord,g) 
            

    
        