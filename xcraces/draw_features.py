import cv2 as c
import numpy as np

from setup import GRID_LENGTH, BORDER_PADDING
from models import Grid_Type, Course_Type, Course_Marker

# set map feature parameters
house_length = 6
road_length = GRID_LENGTH
road_width = 6
river_length = GRID_LENGTH
river_width = 2

course_thickness = 2

house_colour = (63,103,155)
puddle_colour = (43,85,85)
mud_colour = (60,119,119)
road_colour = (150,150,150)
crossing_colour = (0, 204, 204)
river_colour = (180,119,31)
park_1 = 44
park_2 = 160
park_3 = park_1
park_colour = (park_1,park_2,park_3)
tree_colour = (33,82,0)

hill_colour_multiplier = 15

# define how each of the features is drawn

def draw_house(img, x_start, y_start):
    
    length = house_length
    colour = house_colour
    # centre house within the grid
    white_space = int(np.floor(0.5*(GRID_LENGTH - length)))
    
    start = (x_start+white_space,y_start+white_space)
    end = (x_start+white_space+length,y_start+white_space+length)
    
    c.rectangle(img,start,end,colour,-1)

# for xc, start with park underneath
def draw_road(img, x_start, y_start, orientation):
    
    draw_park(img,x_start,y_start)
    
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
        draw_road(img,x_start,y_start,"h")
        draw_bend(img,x_start,y_start,"rt")
    if orientation == "hd":
        draw_road(img,x_start,y_start,"h")
        draw_bend(img,x_start,y_start,"rd")
    if orientation == "vr":
        draw_road(img,x_start,y_start,"v")
        draw_bend(img,x_start,y_start,"rt")
    if orientation == "vl":
        draw_road(img,x_start,y_start,"v")
        draw_bend(img,x_start,y_start,"lt")

def draw_junction(img, x_start, y_start):
    
    draw_road(img,x_start,y_start,"h")
    draw_road(img,x_start,y_start,"v")
    
def draw_road_crossing(img, x_start, y_start):
    
    length = GRID_LENGTH
    width = GRID_LENGTH
    colour = crossing_colour
    
    start = (x_start,y_start)
    end = (x_start + length, y_start + width)
    
    c.rectangle(img,start,end,colour,-1)
    
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
    
def draw_lake(img, x_start, y_start):
    
    radius = round(GRID_LENGTH/2)
    colour = river_colour
    
    start = (x_start+radius,y_start+radius)
    
    c.circle(img,start,radius,colour,-1)
    
def draw_lake_corner(img, x_start, y_start, corner):
    
    draw_park(img, x_start, y_start)
    
    radius = GRID_LENGTH
    colour = river_colour
    
    if corner == "lt":
        start = (x_start+GRID_LENGTH,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,180,270,colour,-1)
    if corner == "ld":
        start = (x_start+GRID_LENGTH,y_start)
        c.ellipse(img,start,(radius,radius),0,90,180,colour,-1)
    if corner == "rt":
        start = (x_start,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,270,360,colour,-1)
    if corner == "rd":
        start = (x_start,y_start)
        c.ellipse(img,start,(radius,radius),0,0,90,colour,-1)
        
def draw_mud(img, x_start, y_start, height):
    
    length = GRID_LENGTH
    width = GRID_LENGTH
    height_colour = (height*hill_colour_multiplier,height*hill_colour_multiplier,height*hill_colour_multiplier)
    colour = tuple(max(0,x-y) for x,y in zip(mud_colour,height_colour))
    
    start = (x_start,y_start)
    end = (x_start + length, y_start + width)
    
    c.rectangle(img,start,end,colour,-1)
    
def draw_mud_corner(img, x_start, y_start, height, corner):
    
    radius = GRID_LENGTH
    half_radius = round(radius/2)
    height_colour = (height*hill_colour_multiplier,height*hill_colour_multiplier,height*hill_colour_multiplier)
    colour = tuple(max(0,x-y) for x,y in zip(mud_colour,height_colour))
    
    if corner == "lt":
        start = (x_start+GRID_LENGTH,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,180,270,colour,-1)
    if corner == "ld":
        start = (x_start+GRID_LENGTH,y_start)
        c.ellipse(img,start,(radius,radius),0,90,180,colour,-1)
    if corner == "rt":
        start = (x_start,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,270,360,colour,-1)
    if corner == "rd":
        start = (x_start,y_start)
        c.ellipse(img,start,(radius,radius),0,0,90,colour,-1)
        
    if corner == "ll":
        start = (x_start,y_start+round(GRID_LENGTH/2))
        c.ellipse(img,start,(half_radius,half_radius),270,0,180,colour,-1)
    if corner == "rr":
        start = (x_start+GRID_LENGTH,y_start+round(GRID_LENGTH/2))
        c.ellipse(img,start,(half_radius,half_radius),90,0,180,colour,-1)
    if corner == "tt":
        start = (x_start+round(GRID_LENGTH/2),y_start)
        c.ellipse(img,start,(half_radius,half_radius),0,0,180,colour,-1)
    if corner == "dd":
        start = (x_start+round(GRID_LENGTH/2),y_start+GRID_LENGTH)
        c.ellipse(img,start,(half_radius,half_radius),180,0,180,colour,-1)
        
def draw_puddle(img, x_start, y_start, height):
    
    draw_mud(img, x_start, y_start,height)
    
    radius = round(GRID_LENGTH/2)
    start = (x_start + radius, y_start + radius)
    height_colour = (height*hill_colour_multiplier,height*hill_colour_multiplier,height*hill_colour_multiplier)
    colour = tuple(max(0,x-y) for x,y in zip(puddle_colour,height_colour))
    
    c.circle(img,start,radius,colour,-1)
    
def draw_hill(img, x_start, y_start, height):
    
    length = GRID_LENGTH
    width = GRID_LENGTH
    colour = (max(0,park_1-height*hill_colour_multiplier),max(0,park_2-height*hill_colour_multiplier),max(0,park_3-height*hill_colour_multiplier))
    
    start = (x_start,y_start)
    end = (x_start + length, y_start + width)
    
    c.rectangle(img,start,end,colour,-1)
    
def draw_hill_corner(img, x_start, y_start, height, corner):
    
    radius = GRID_LENGTH
    half_radius = round(radius/2)
    colour = (max(0,park_1-height*hill_colour_multiplier),max(0,park_2-height*hill_colour_multiplier),max(0,park_3-height*hill_colour_multiplier))
    
    if corner == "lt":
        start = (x_start+GRID_LENGTH,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,180,270,colour,-1)
    if corner == "ld":
        start = (x_start+GRID_LENGTH,y_start)
        c.ellipse(img,start,(radius,radius),0,90,180,colour,-1)
    if corner == "rt":
        start = (x_start,y_start+GRID_LENGTH)
        c.ellipse(img,start,(radius,radius),0,270,360,colour,-1)
    if corner == "rd":
        start = (x_start,y_start)
        c.ellipse(img,start,(radius,radius),0,0,90,colour,-1)
        
    if corner == "ll":
        start = (x_start,y_start+round(GRID_LENGTH/2))
        c.ellipse(img,start,(half_radius,half_radius),270,0,180,colour,-1)
    if corner == "rr":
        start = (x_start+GRID_LENGTH,y_start+round(GRID_LENGTH/2))
        c.ellipse(img,start,(half_radius,half_radius),90,0,180,colour,-1)
    if corner == "tt":
        start = (x_start+round(GRID_LENGTH/2),y_start)
        c.ellipse(img,start,(half_radius,half_radius),0,0,180,colour,-1)
    if corner == "dd":
        start = (x_start+round(GRID_LENGTH/2),y_start+GRID_LENGTH)
        c.ellipse(img,start,(half_radius,half_radius),180,0,180,colour,-1)
    
def draw_tree(img, x_start, y_start, height):
    
    draw_hill(img, x_start, y_start, height)
    
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
    
def draw_ribbons(img, x_start, y_start, orientation):
    
    length = GRID_LENGTH
    colour_ribbon = (26,140,255)
    num_ribbons = 2
    ribbon_thickness = 2
    ribbon_offset = round(length/num_ribbons)
    
    if orientation == "lt":
        start = (x_start, y_start)
        end_1 = (x_start, y_start - length)
        end_2 = (x_start - length, y_start)
        c.line(img,start,end_1,(255,255,255),ribbon_thickness)
        c.line(img,start,end_2,(255,255,255),ribbon_thickness)
        
        for i in range(num_ribbons):
            start_1 = (x_start - round(ribbon_thickness/2), y_start - i*ribbon_offset)
            start_2 = (x_start - i*ribbon_offset, y_start + round(ribbon_thickness/2))
            end_1 = (x_start + round(ribbon_thickness/2), y_start - (i+1)*ribbon_offset)
            end_2 = (x_start - (i+1)*ribbon_offset, y_start - round(ribbon_thickness/2))
            c.line(img,start_1,end_1,colour_ribbon,1)
            c.line(img,start_2,end_2,colour_ribbon,1)
        
#        start = (x_start + 2*length, y_start + 2*length)
#        end_1 = (x_start + 2*length, y_start - length + 2*length)
#        end_2 = (x_start - length + 2*length, y_start + 2*length)
#        c.line(img,start,end_1,(255,255,255),2)
#        c.line(img,start,end_2,(255,255,255),2)
    if orientation == "ld":
#        start = (x_start + 2*length, y_start - length)
#        end_1 = (x_start + 2*length, y_start)
#        end_2 = (x_start + length, y_start - length)
#        c.line(img,start,end_1,(255,255,255),2)
#        c.line(img,start,end_2,(255,255,255),2)
        
        start = (x_start, y_start - length + 2*length)
        end_1 = (x_start, y_start + 2*length)
        end_2 = (x_start + length - 2*length, y_start - length + 2*length)
        c.line(img,start,end_1,(255,255,255),ribbon_thickness)
        c.line(img,start,end_2,(255,255,255),ribbon_thickness)
        
        for i in range(num_ribbons):
            start_1 = (x_start - round(ribbon_thickness/2), y_start + i*ribbon_offset + length)
            start_2 = (x_start - i*ribbon_offset, y_start + length + round(ribbon_thickness/2))
            end_1 = (x_start + round(ribbon_thickness/2), y_start + (i+1)*ribbon_offset + length)
            end_2 = (x_start - (i+1)*ribbon_offset, y_start + length - round(ribbon_thickness/2))
            c.line(img,start_1,end_1,colour_ribbon,1)
            c.line(img,start_2,end_2,colour_ribbon,1)
        
        
    if orientation == "rt":
        start = (x_start + length, y_start)
        end_1 = (x_start + length, y_start - length)
        end_2 = (x_start + 2*length, y_start)
        c.line(img,start,end_1,(255,255,255),ribbon_thickness)
        c.line(img,start,end_2,(255,255,255),ribbon_thickness)
        
        for i in range(num_ribbons):
            start_1 = (x_start + length - round(ribbon_thickness/2), y_start - i*ribbon_offset)
            start_2 = (x_start + length + i*ribbon_offset, y_start + round(ribbon_thickness/2))
            end_1 = (x_start + length + round(ribbon_thickness/2), y_start - (i+1)*ribbon_offset)
            end_2 = (x_start + length + (i+1)*ribbon_offset, y_start - round(ribbon_thickness/2))
            c.line(img,start_1,end_1,colour_ribbon,1)
            c.line(img,start_2,end_2,colour_ribbon,1)
        
#        start = (x_start + length - 2*length, y_start + 2*length)
#        end_1 = (x_start + length - 2*length, y_start - length + 2*length)
#        end_2 = (x_start + 2*length- 2*length, y_start + 2*length)
#        c.line(img,start,end_1,(255,255,255),2)
#        c.line(img,start,end_2,(255,255,255),2)
    if orientation == "rd":
#        start = (x_start - length, y_start - length)
#        end_1 = (x_start - length, y_start)
#        end_2 = (x_start, y_start - length)
#        c.line(img,start,end_1,(255,255,255),2)
#        c.line(img,start,end_2,(255,255,255),2)
        
        start = (x_start - length + 2*length, y_start - length + 2*length)
        end_1 = (x_start - length + 2*length, y_start + 2*length)
        end_2 = (x_start + 2*length, y_start - length + 2*length)
        c.line(img,start,end_1,(255,255,255),ribbon_thickness)
        c.line(img,start,end_2,(255,255,255),ribbon_thickness)
        
        for i in range(num_ribbons):
            start_1 = (x_start + length - round(ribbon_thickness/2), y_start + length + i*ribbon_offset)
            start_2 = (x_start + length + i*ribbon_offset, y_start + length + round(ribbon_thickness/2))
            end_1 = (x_start + length + round(ribbon_thickness/2), y_start + length + (i+1)*ribbon_offset)
            end_2 = (x_start + length + (i+1)*ribbon_offset, y_start + length - round(ribbon_thickness/2))
            c.line(img,start_1,end_1,colour_ribbon,1)
            c.line(img,start_2,end_2,colour_ribbon,1)
    
def draw_course(img, x_start, y_start, orientation,height,background):
        
    length = road_length
    height_colour = (height*hill_colour_multiplier,height*hill_colour_multiplier,height*hill_colour_multiplier)
    
    if "river" in background:
        return
    if "crossing" in background:
        background_colour = crossing_colour
    if "park" in background:
        background_colour = park_colour
    if "mud" in background:
        background_colour = mud_colour
    
    colour = tuple(max(0,x-y-2*hill_colour_multiplier) for x,y in zip(background_colour,height_colour))
    white_space = round(0.5*(GRID_LENGTH))
    
    if orientation == "h":
        start = (x_start,y_start+white_space)
        end = (x_start+length,y_start+white_space)
    if orientation == "v":
        start = (x_start+white_space,y_start)
        end = (x_start+white_space,y_start+length)
    
    c.line(img,start,end,colour,course_thickness)
    
def draw_course_bend(img, x_start, y_start, orientation,height,background): 
    
    draw_ribbons(img, x_start, y_start, orientation)
    
    length = round(road_length/2)
    height_colour = (height*hill_colour_multiplier,height*hill_colour_multiplier,height*hill_colour_multiplier)
    
    if "river" in background:
        return
    if "crossing" in background:
        background_colour = crossing_colour    
    if "park" in background:
        background_colour = park_colour
    if "mud" in background:
        background_colour = mud_colour
    
    colour = tuple(max(0,x-y-2*hill_colour_multiplier) for x,y in zip(background_colour,height_colour))
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
        
def draw_course_turning(img,x_start,y_start,orientation,height,background):
    
    if orientation == "ht":
        draw_course_bend(img,x_start,y_start,"lt",height,background)
        draw_course_bend(img,x_start,y_start,"rt",height,background)
    if orientation == "hd":
        draw_course_bend(img,x_start,y_start,"ld",height,background)
        draw_course_bend(img,x_start,y_start,"rd",height,background)
    if orientation == "vr":
        draw_course_bend(img,x_start,y_start,"rd",height,background)
        draw_course_bend(img,x_start,y_start,"rt",height,background)
    if orientation == "vl":
        draw_course_bend(img,x_start,y_start,"ld",height,background)
        draw_course_bend(img,x_start,y_start,"lt",height,background)
        
def draw_course_marker(img, x_start, y_start, marker):
    
    colour = (0,0,0)
    font = c.FONT_HERSHEY_SIMPLEX
    
    if marker > 9:
        white_space = round(1.5*GRID_LENGTH)
    else:
        white_space = GRID_LENGTH
    
    c.putText(img,str(marker),(x_start - white_space,y_start),font,0.4,colour,1,c.LINE_AA)
    
def draw_course_marker_start(img, x_start, y_start, orientation):
    
    colour_text = (0,0,0)
    colour_tape = (0,0,255)
    
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
    c.putText(img,"Start",(x_start + white_space + round(white_space/2),y_start),font,0.5,colour_text,1,c.LINE_AA)

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
      
    c.putText(img,"Finish",(x_start + white_space + round(white_space/2),y_start),font,0.5,colour_text,1,c.LINE_AA)
    
def draw_title(img, x_start, y_start, title):
    
    colour_text = (0,0,0)
    font = c.FONT_HERSHEY_SIMPLEX
    
    c.putText(img,title,(x_start,y_start),font,0.5,colour_text,1,c.LINE_AA)
    
    
# draw the features from the grid onto the image
def interpret_grid(grid,x_grid,y_grid,n,img):
    
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
        draw_bend(img,x_coord,y_coord,g[len(g)-2:])    
    if g == Grid_Type.ROAD_T_HT or g == Grid_Type.ROAD_T_HD or g == Grid_Type.ROAD_T_VL or g == Grid_Type.ROAD_T_VR:
        draw_turning(img,x_coord,y_coord,g[len(g)-2:]) 
        
    if g == Grid_Type.RIVER_B_LD or g == Grid_Type.RIVER_B_LT or g == Grid_Type.RIVER_B_RT or g == Grid_Type.RIVER_B_RD:
        draw_river_bend(img,x_coord,y_coord,g[len(g)-2:])  
    if g == Grid_Type.RIVER_H or g == Grid_Type.RIVER_V:
        draw_river(img,x_coord,y_coord,g[-1])
    if g == Grid_Type.RIVER_R_B_LD or g == Grid_Type.RIVER_R_B_LT or g == Grid_Type.RIVER_R_B_RT or g == Grid_Type.RIVER_R_B_RD:
        draw_park(img,x_coord,y_coord)
        draw_river_bend(img,x_coord,y_coord,g[len(g)-2:])  
    if g == Grid_Type.RIVER_R_H or g == Grid_Type.RIVER_R_V:
        draw_park(img,x_coord,y_coord)
        draw_river(img,x_coord,y_coord,g[-1])
        
    if g == Grid_Type.ROAD_CROSSING:
        draw_road_crossing(img,x_coord,y_coord)
        
    if g == Grid_Type.BRIDGE_H or g == Grid_Type.BRIDGE_V:
        draw_bridge(img,x_coord,y_coord,g[-1])
    if g == Grid_Type.PARK:
        draw_park(img,x_coord,y_coord)
        
    if g == Grid_Type.LAKE:
        draw_lake(img,x_coord,y_coord)
        
    if g == Grid_Type.LAKE_LT or g == Grid_Type.LAKE_LD or g == Grid_Type.LAKE_RT or g == Grid_Type.LAKE_RD:
        draw_lake_corner(img,x_coord,y_coord,g[len(g)-2:])
        
    if g == Grid_Type.MUD:
        draw_mud(img,x_coord,y_coord,0)
        
    if g == Grid_Type.MUD_LT or g == Grid_Type.MUD_LD or g == Grid_Type.MUD_RT or g == Grid_Type.MUD_RD\
    or g == Grid_Type.MUD_L or g == Grid_Type.MUD_R or g == Grid_Type.MUD_T or g == Grid_Type.MUD_D:
        draw_mud_corner(img,x_coord,y_coord,0,g[len(g)-2:])
        
    if g == Grid_Type.PUDDLE:
        draw_puddle(img,x_coord,y_coord,0)
        
    if g == Grid_Type.TREE:
        draw_tree(img,x_coord,y_coord,0)
        
        
    if n != -1 and g != 0:
        
        if g[n] == Grid_Type.HILL:
            draw_hill(img,x_coord,y_coord,n+1)
            
        if g[n] == Grid_Type.TREE:
            draw_tree(img,x_coord,y_coord,n+1)
            
        if g[n] == Grid_Type.MUD:
            draw_mud(img,x_coord,y_coord,n+1)
            
        if g[n] == Grid_Type.MUD_LT or g[n] == Grid_Type.MUD_LD or g[n] == Grid_Type.MUD_RT or g[n] == Grid_Type.MUD_RD\
        or g[n] == Grid_Type.MUD_L or g[n] == Grid_Type.MUD_R or g[n] == Grid_Type.MUD_T or g[n] == Grid_Type.MUD_D:
            draw_mud_corner(img,x_coord,y_coord,n+1,g[n][len(g[n])-2:])
            
        if g[n] == Grid_Type.PUDDLE:
            draw_puddle(img,x_coord,y_coord,n+1)
            
        
        if g[n] == Grid_Type.HILL_LT or g[n] == Grid_Type.HILL_LD or g[n] == Grid_Type.HILL_RT or g[n] == Grid_Type.HILL_RD\
        or g[n] == Grid_Type.HILL_L or g[n] == Grid_Type.HILL_R or g[n] == Grid_Type.HILL_T or g[n] == Grid_Type.HILL_D:
            draw_hill_corner(img,x_coord,y_coord,n+1,g[n][len(g[n])-2:])
        
            
            
# draw the features from the grid onto the image
def interpret_course(grid,course_grid,x_grid,y_grid,n,img):
    
    g = course_grid[x_grid][y_grid]
    map_g = grid[x_grid][y_grid]
    
    # the coordinates of the grid need to be multiplied by the actual size of 
    # each grid square
    x_coord = x_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    y_coord = y_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    
    if any(map_g == river for river in Grid_Type.CHOICES_RIVER) or any(map_g == mud for mud in Grid_Type.CHOICES_MUD) or map_g == Grid_Type.ROAD_CROSSING:
        background = map_g
    else:
        background = Grid_Type.PARK
    
    if g == Course_Type.COURSE_H or g == Course_Type.COURSE_V:
        draw_course(img,x_coord,y_coord,g[-1],0, background)
        
    if g == Course_Type.COURSE_B_LD or g == Course_Type.COURSE_B_LT or g == Course_Type.COURSE_B_RT or g == Course_Type.COURSE_B_RD:
        draw_course_bend(img,x_coord,y_coord,g[len(g)-2:],0,background) 
        
    if g == Course_Type.COURSE_T_HT or g == Course_Type.COURSE_T_HD or g == Course_Type.COURSE_T_VL or g == Course_Type.COURSE_T_VR:
        draw_course_turning(img,x_coord,y_coord,g[len(g)-2:],0,background)
        
    if n != -1 and g != 0:
        
        background = Grid_Type.PARK
    
        if g[n] == Course_Type.COURSE_H or g[n] == Course_Type.COURSE_V:
            draw_course(img,x_coord,y_coord,g[n][-1],n+1,background)
            
        if g[n] == Course_Type.COURSE_B_LD or g[n] == Course_Type.COURSE_B_LT or g[n] == Course_Type.COURSE_B_RT or g[n] == Course_Type.COURSE_B_RD:
            draw_course_bend(img,x_coord,y_coord,g[n][len(g[n])-2:],n+1,background) 
            
        if g[n] == Course_Type.COURSE_T_HT or g[n] == Course_Type.COURSE_T_HD or g[n] == Course_Type.COURSE_T_VL or g[n] == Course_Type.COURSE_T_VR:
            draw_course_turning(img,x_coord,y_coord,g[n][len(g[n])-2:],n+1,background)
        
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
            
# put course title 
def place_course_title(laps,max_laps,distance,x_grid,y_grid,img):
    
    x_coord = x_grid*GRID_LENGTH + round(BORDER_PADDING/2)
    y_coord = y_grid*GRID_LENGTH + round(2*BORDER_PADDING/5)
    
    course = ""
    
    for i,lap in enumerate(laps):
        if i>=max_laps:
            pass
        else:
            course += lap + ", "
            
    if max_laps>len(laps):
        for i in range(max_laps-len(laps)):
            course += Course_Type.BIG_LAP + ", "
    
    course += "finish"
    
    title = str(distance) + "km" + ", " + course
    
    draw_title(img,x_coord,y_coord,title)
            
        