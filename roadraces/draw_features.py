import cv2 as c
import numpy as np

from setup import GRID_LENGTH

# set map feature parameters
house_length = round(0.6*GRID_LENGTH)
road_length = GRID_LENGTH
road_width = round(0.6*GRID_LENGTH)
river_length = GRID_LENGTH
river_width = round(0.2*GRID_LENGTH)

grass_thickness = round(0.05*GRID_LENGTH)

course_thickness = round(0.2*GRID_LENGTH)

max_street_length = 20
min_street_length = 5

max_block_length = 10
min_block_length = 1

max_fraction_trees = 0.5
min_fraction_trees = 0.1

house_colour = (63,103,155)
road_colour = (150,150,150)
curb_colour = (100,100,100)
river_colour = (180,119,31)
park_colour = (44,160,44)
grass_colour = (0,150,0)
tree_colour = (33,82,0)

course_colour = (50,50,50)

# define how each of the features is drawn

def draw_house(img, x_start, y_start):
    
    length = house_length
    colour = house_colour
    # centre house within the grid
    white_space = int(np.floor(0.5*(GRID_LENGTH - length)))
    
    start = (x_start+white_space,y_start+white_space)
    end = (x_start+white_space+length,y_start+white_space+length)
    
    c.rectangle(img,start,end,colour,-1)
    
def draw_road(img, x_start, y_start, orientation):
    
    length = road_length
    width = road_width
    colour = road_colour
    white_space = int(np.floor(0.5*(GRID_LENGTH - width)))
    
    if orientation == "h":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
        
    if orientation == "v":
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
 
    c.rectangle(img,start,end,colour,-1)
    

    
def draw_bend(img, x_start, y_start, orientation):
    
    length = round(road_length/2)
    width = road_width
    colour = road_colour
    
    c.circle(img, (x_start+length,y_start+length), round(road_width/2), colour, -1)
    white_space = int(np.floor(0.5*(GRID_LENGTH - width)))
    
    if orientation == "lt":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "ld":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space+width,y_start+length+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "rt":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "rd":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space+width,y_start+length+length)
        c.rectangle(img,start,end,colour,-1)
        
def draw_turning(img,x_start,y_start,orientation):
    
    
    if orientation == "ht":
        draw_bend(img,x_start,y_start,"rt")
        draw_road(img,x_start,y_start,"h")
    if orientation == "hd":
        draw_bend(img,x_start,y_start,"rd")
        draw_road(img,x_start,y_start,"h")
    if orientation == "vr":
        draw_bend(img,x_start,y_start,"rt")
        draw_road(img,x_start,y_start,"v")
    if orientation == "vl":
        draw_bend(img,x_start,y_start,"lt")
        draw_road(img,x_start,y_start,"v")

def draw_junction(img, x_start, y_start):
    
    draw_road(img,x_start,y_start,"h")
    draw_road(img,x_start,y_start,"v")
    
def draw_river(img, x_start, y_start, orientation):
    
    length = river_length
    width = river_width
    colour = river_colour
    white_space = int(np.floor(0.5*(GRID_LENGTH - width)))
    
    if orientation == "h":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
    if orientation == "v":
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
    
    c.rectangle(img,start,end,colour,-1)
    
def draw_river_bend(img, x_start, y_start, orientation):
    
    length = round(river_length/2)
    width = river_width
    colour = river_colour
    
    c.circle(img, (x_start+length,y_start+length), round(river_width/2), colour, -1)
    white_space = int(np.floor(0.5*(GRID_LENGTH - width)))
    
    if orientation == "lt":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "ld":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space+width,y_start+length+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "rt":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+width,y_start+length)
        c.rectangle(img,start,end,colour,-1)
    if orientation == "rd":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space+width)
        c.rectangle(img,start,end,colour,-1)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space+width,y_start+length+length)
        c.rectangle(img,start,end,colour,-1)
        
def draw_bridge(img, x_start, y_start, orientation):
    
    draw_road(img, x_start, y_start, orientation)
    
    length = road_length
    width = road_width
    colour = house_colour
    white_space = int(np.floor(0.5*(GRID_LENGTH - width)))
    
    if orientation == "h":
        start_1 = (x_start,y_start+white_space)
        end_1 = (x_start+length,y_start+white_space)
        start_2 = (x_start,y_start+white_space+width)
        end_2 = (x_start+length,y_start+white_space+width)
    if orientation == "v":
        start_1 = (x_start+white_space,y_start)
        end_1 = (x_start+white_space,y_start+length)
        start_2 = (x_start+white_space+width,y_start)
        end_2 = (x_start+white_space+width,y_start+length)
    
    c.line(img,start_1,end_1,colour,1)
    c.line(img,start_2,end_2,colour,1)
    
def draw_park(img, x_start, y_start):
    
    length = GRID_LENGTH
    width = GRID_LENGTH
    colour = park_colour
    
    start = (x_start,y_start)
    end = (x_start + length, y_start + width)
    
    c.rectangle(img,start,end,colour,-1)
    
#    colour = grass_colour
#    
#    blades_of_grass = 10
#    
#    for blades in range(blades_of_grass):
#        x_blade = np.random.randint(x_start,x_start + length)
#        y_blade = np.random.randint(y_start,y_start + width)
#        c.line(img,(x_blade,y_blade),(x_blade,y_blade+np.random.randint(0,2)),colour,1)
#    
#    colour = (255,255,255)
#    
#    radius = round(GRID_LENGTH/30)
#    center_x = np.random.randint(x_start,x_start + length)
#    center_y = np.random.randint(y_start,y_start + width)
#    
#    start_1 = (center_x, int(round(center_y-radius/2)))
#    start_2 = (int(center_x - round((radius/2)*np.sqrt(3)/2)),int(center_y + round(radius/4)))
#    start_3 = (int(center_x + round((radius/2)*np.sqrt(3)/2)),int(center_y + round(radius/4)))
#    
#    
#    c.circle(img,start_1,radius,colour,-1)
#    c.circle(img,start_2,radius,colour,-1)
#    c.circle(img,start_3,radius,colour,-1)
    
    
def draw_tree(img, x_start, y_start):
    
    draw_park(img, x_start, y_start)
    
    colour = tree_colour
    radius = round(GRID_LENGTH/4)
    center_x = x_start + round(GRID_LENGTH/2)
    center_y = y_start + round(GRID_LENGTH/2)
    
    start_1 = (center_x, int(round(center_y-radius/2)))
    start_2 = (int(center_x - round((radius/2)*np.sqrt(3)/2)),int(center_y + round(radius/4)))
    start_3 = (int(center_x + round((radius/2)*np.sqrt(3)/2)),int(center_y + round(radius/4)))
    
    
    c.circle(img,start_1,radius,colour,-1)
    c.circle(img,start_2,radius,colour,-1)
    c.circle(img,start_3,radius,colour,-1)
    
def draw_course(img, x_start, y_start, orientation):
    
    length = road_length
    colour = course_colour
    white_space = round(0.5*(GRID_LENGTH))
    
    if orientation == "h":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space)
    if orientation == "v":
        start = (x_start+white_space,y_start)
        end = (x_start+white_space,y_start+length)
    
    c.line(img,start,end,colour,course_thickness)
    
def draw_course_bend(img, x_start, y_start, orientation):
    
    length = round(road_length/2)
    colour = course_colour
    white_space = round(0.5*(GRID_LENGTH))
    
    if orientation == "lt":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space)
        c.line(img,start,end,colour,course_thickness)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space,y_start+length)
        c.line(img,start,end,colour,course_thickness)
    if orientation == "ld":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space)
        c.line(img,start,end,colour,course_thickness)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space,y_start+length+length)
        c.line(img,start,end,colour,course_thickness)
    if orientation == "rt":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space)
        c.line(img,start,end,colour,course_thickness)
        start = (x_start+white_space,y_start)
        end = (x_start+white_space,y_start+length)
        c.line(img,start,end,colour,course_thickness)
    if orientation == "rd":
        start = (x_start+length,y_start+white_space)
        end = (x_start+length+length,y_start+white_space)
        c.line(img,start,end,colour,course_thickness)
        start = (x_start+white_space,y_start+length)
        end = (x_start+white_space,y_start+length+length)
        c.line(img,start,end,colour,course_thickness)
        
def draw_course_marker(img, x_start, y_start, marker):
    
    colour = (0,0,0)
    font = c.FONT_HERSHEY_SIMPLEX
    
    if marker > 9:
        white_space = round(1.5*GRID_LENGTH)
    else:
        white_space = GRID_LENGTH
    
    c.putText(img,str(marker),(x_start - white_space,y_start),font,0.04*GRID_LENGTH,colour,1,c.LINE_AA)
    
def draw_course_marker_start(img, x_start, y_start, orientation):
    
    colour_text = (0,0,0)
    colour_tape = park_colour
    
    length = road_length
    
    font = c.FONT_HERSHEY_SIMPLEX
    
    white_space = round(0.5*(GRID_LENGTH))
    

    
    if orientation == "v":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space+course_thickness)
    if orientation == "h":
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+course_thickness,y_start+length)
      
    c.rectangle(img,start,end,colour_tape,-1)
    c.putText(img,"Start",(x_start + white_space + round(white_space/2),y_start),font,0.05*GRID_LENGTH,colour_text,1,c.LINE_AA)

# make a chequered line 
def draw_course_marker_finish(img, x_start, y_start, orientation):
    
    colour_text = (0,0,0)
    colour_tape_1 = (0,0,0)
    colour_tape_2 = (255,255,255)
    
    length = int(np.ceil(road_width/4))
    
    font = c.FONT_HERSHEY_SIMPLEX
    
    white_space = round(0.5*(GRID_LENGTH))
    
    if orientation == "v":
        
        start = (x_start,y_start+white_space)
        end = (x_start+GRID_LENGTH,y_start+white_space+2*course_thickness+1)
        c.rectangle(img,start,end,colour_tape_2,-1)
        
    if orientation == "h":
        
        start = (x_start+white_space,y_start)
        end = (x_start+white_space+2*course_thickness+1,y_start+GRID_LENGTH)
        c.rectangle(img,start,end,colour_tape_2,-1)
    
    
    for i in range(2):
        if orientation == "v":
            
            # dashed lines alternating colour
            start = (x_start+2*i*(length+1),y_start+white_space)
            end = (x_start+(2*i+1)*length+2*i,y_start+white_space+course_thickness)
            c.rectangle(img,start,end,colour_tape_1,-1)
            
            # second dashed line           
            start = (x_start+(2*i+1)*(length+1),y_start+white_space+course_thickness+1)
            end = (x_start+(2*i+2)*length+2*i+1,y_start+white_space + 2*course_thickness+1)
            c.rectangle(img,start,end,colour_tape_1,-1)
            

            
        if orientation == "h":
            
            # dashed lines alternating colour
            start = (x_start+white_space,y_start+2*i*(length+1))
            end = (x_start+white_space+course_thickness,y_start+(2*i+1)*length+2*i)
            c.rectangle(img,start,end,colour_tape_1,-1)
            
            
            # second dashed line          
            start = (x_start+white_space+course_thickness+1,y_start+(2*i+1)*(length+1))
            end = (x_start+white_space+2*course_thickness+1,y_start+(2*i+2)*length+2*i+1)
            c.rectangle(img,start,end,colour_tape_1,-1)
      
    c.putText(img,"Finish",(x_start + white_space + round(white_space/2),y_start),font,0.05*GRID_LENGTH,colour_text,1,c.LINE_AA)
        