from models import Grid_Type, Course_Type, Course_Marker
from draw_rules import get_left_tile, get_right_tile, get_top_tile, get_bottom_tile
from setup import LENGTH, WIDTH, GRID_LENGTH, GRID_SQUARE_SIZE, BORDER_PADDING, COURSE_MARKERS, UNIT_DISTANCE

# create a class that will run the course
class Runner:
    
    # intiate the direction and starting postion of the runner
    def __init__(self, direction, start_i, start_j):
    
        self.direction = direction
        self.i = start_i
        self.j = start_j
        
        # how far has the athlete run in grid squares
        self.distance_run = 0
        
        # this measures how many times you have returned to a square when 
        # pathfinding
        self.counter_grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
        
        # save the athlete coordinates and the distance
        self.coords = [[self.i*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2), self.j*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2), self.distance_run]]
        
    # the main function, if there is a straight road ahead or a single bend,
    # keep moving forward
    def move(self, map_grid, course_grid, course_markers):
        
        g = map_grid[self.i][self.j]
        l_g = get_left_tile(map_grid,self.i,self.j)
        r_g = get_right_tile(map_grid,self.i,self.j)
        t_g = get_top_tile(map_grid,self.i,self.j)
        b_g = get_bottom_tile(map_grid,self.i,self.j)
        
        # if there is a clear road ahead, keep moving in the same direction,
        # if there is a single bend, take the bend
        # if there is no clear road and a choice of turnings, turn
        # if there is a dead end and no turnings, backtrack until there is a turning
        
        if self.direction == self.DOWN:            
            if any(b_g == road for road in Grid_Type.CHOICES_ROAD_V):
                self.j += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_V
            elif any(b_g == road for road in [Grid_Type.ROAD_B_LT,Grid_Type.ROAD_B_RT]):
                self.j += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_B + b_g[len(b_g)-2:len(b_g)]
                self.direction = b_g[len(b_g)-2]
            elif b_g == Grid_Type.ROAD_T_HT:
                self.j += 1
                self.turn(map_grid,course_grid)
            else: 
                self.backtrack(map_grid, course_grid, course_markers)
                
        elif self.direction == self.UP:            
            if any(t_g == road for road in Grid_Type.CHOICES_ROAD_V):
                self.j -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_V
            elif any(t_g == road for road in [Grid_Type.ROAD_B_LD,Grid_Type.ROAD_B_RD]):
                self.j -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_B + t_g[len(t_g)-2:len(t_g)]
                self.direction = t_g[len(t_g)-2]
            elif t_g == Grid_Type.ROAD_T_HD:
                self.j -= 1
                self.turn(map_grid,course_grid)
            else: 
                self.backtrack(map_grid, course_grid, course_markers)
                
        elif self.direction == self.LEFT:            
            if any(l_g == road for road in Grid_Type.CHOICES_ROAD_H):
                self.i -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_H
            elif any(l_g == road for road in [Grid_Type.ROAD_B_RT,Grid_Type.ROAD_B_RD]):
                self.i -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_B + l_g[len(l_g)-2:len(l_g)]
                self.direction = l_g[len(l_g)-1]
            elif l_g == Grid_Type.ROAD_T_VR:
                self.i -= 1
                self.turn(map_grid,course_grid)
            else: 
                self.backtrack(map_grid, course_grid, course_markers)
                
        elif self.direction == self.RIGHT:            
            if any(r_g == road for road in Grid_Type.CHOICES_ROAD_H):
                self.i += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_H   
            elif any(r_g == road for road in [Grid_Type.ROAD_B_LT,Grid_Type.ROAD_B_LD]):
                self.i += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_B + r_g[len(r_g)-2:len(r_g)]
                self.direction = r_g[len(r_g)-1]
            elif r_g == Grid_Type.ROAD_T_VL:
                self.i += 1
                self.turn(map_grid,course_grid)
            else: 
                self.backtrack(map_grid, course_grid, course_markers)
        
        # count the distance run        
        self.distance_run += 1
        # reset the counter 
        self.counter_grid[self.i][self.j] = 0
        # add the new coordinates
        self.coords.append([self.i*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2),self.j*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2),self.distance_run*GRID_SQUARE_SIZE])
    
    # if there was a deadend and no turning, backtrack until you find
    # a turning            
    def backtrack(self, map_grid, course_grid, course_markers):
        
        g = map_grid[self.i][self.j]
        
        while g == Grid_Type.ROAD_H or g == Grid_Type.ROAD_V or g == Grid_Type.BRIDGE_H or g == Grid_Type.BRIDGE_V or any(g == bend for bend in Grid_Type.CHOICES_BENDS):
                        
            course_grid[self.i][self.j] = 0
            course_markers[self.i][self.j] = 0
            
            if any(g == bend for bend in Grid_Type.CHOICES_BENDS):
                
                if self.direction == self.DOWN or self.direction == self.UP:
                    self.direction = g[len(g)-2]
                    self.direction = self.opposite_direction
                elif self.direction == self.RIGHT or self.direction == self.LEFT:
                    self.direction = g[len(g)-1]
                    self.direction = self.opposite_direction
                
            if self.direction == self.DOWN:            
                self.j -= 1
                
            if self.direction == self.UP:            
                self.j += 1
                
            if self.direction == self.LEFT:            
                self.i += 1
                
            if self.direction == self.RIGHT:            
                self.i -= 1
                
            g = map_grid[self.i][self.j]
            
            # remove the distance travelled to the deadend
            self.distance_run -= 1
            #remove the athlete coordinates
            del self.coords[-1]
        
        self.distance_run -= 1
        del self.coords[-1]
        # once you get to the new turning, mark this on the counter and try again
        self.counter_grid[self.i][self.j] += 1
        
        # at the new turning, decide on the new direction to take
        self.choose_new_direction(map_grid,course_grid, course_markers)
    
    # choose a new direction to take at a turning or a junction
    def choose_new_direction(self, map_grid, course_grid, course_markers):
        
        g = map_grid[self.i][self.j]
        c = course_grid[self.i][self.j]
        counter = self.counter_grid[self.i][self.j]
        
        # if you have already been to this turning and tried each possible route
        # go back to the next turning
        if (counter >= 2 and any(g == turns for turns in Grid_Type.CHOICES_TURNINGS)) or (counter >= 3 and g == Grid_Type.ROAD_J):
            if self.direction == self.DOWN or self.direction == self.UP:
                self.direction = c[len(c)-2]
                self.direction = self.opposite_direction
                    
            elif self.direction == self.LEFT or self.direction == self.RIGHT:
                self.direction = c[len(c)-1]
                self.direction = self.opposite_direction
            
            course_grid[self.i][self.j] = 0
                
            if self.direction == self.LEFT:
                self.i += 1
            if self.direction == self.RIGHT:
                self.i -= 1
            if self.direction == self.UP:
                self.j += 1
            if self.direction == self.DOWN:
                self.j -= 1
                
            self.backtrack(map_grid, course_grid, course_markers)
        
        # if you can take the other turning, just carry on
        elif any(c == bends for bends in Course_Type.CHOICES_BENDS):
            course_grid[self.i][self.j] = self.flip(c)
            self.direction = self.opposite_direction
            self.move(map_grid, course_grid, course_markers)
        
        # if there is only one option for the new direction, take that turning
        # otherwise make a turn decision
        
        elif self.direction == self.DOWN or self.direction == self.UP:
            if any(g == turning for turning in [Grid_Type.ROAD_T_VL,Grid_Type.ROAD_T_VR]):
                course_grid[self.i][self.j] = Course_Type.COURSE_B + g[len(g)-1] + self.opposite_direction
                self.direction = g[len(g)-1]
            elif g == Grid_Type.ROAD_J:
                self.turn(map_grid,course_grid)
                
        elif self.direction == self.LEFT or self.direction == self.RIGHT:
            if any(g == turning for turning in [Grid_Type.ROAD_T_HT,Grid_Type.ROAD_T_HD]):
                course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + g[len(g)-1]
                self.direction = g[len(g)-1]
            elif g == Grid_Type.ROAD_J:
                self.turn(map_grid,course_grid)
    
    # when there are two options to take for a turning, turn such that
    # you are moving away from the closest edge
    def turn(self, map_grid, course_grid):
        
        if self.direction == self.DOWN or self.direction == self.UP:
            if self.i >= LENGTH/2:
                course_grid[self.i][self.j] = Course_Type.COURSE_B + self.LEFT + self.opposite_direction 
                self.direction = self.LEFT
            else:
                course_grid[self.i][self.j] = Course_Type.COURSE_B + self.RIGHT + self.opposite_direction 
                self.direction = self.RIGHT
                
        elif self.direction == self.RIGHT or self.direction == self.LEFT:
            if self.j >= WIDTH/2:
                course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.UP
                self.direction = self.UP
            else:
                course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.DOWN
                self.direction = self.DOWN
    
    # set the distance markers for the course          
    def set_course_markers(self,course_markers,race_distance):
        
        
        markers = [round(x*COURSE_MARKERS/GRID_SQUARE_SIZE) for x in range(1+round(race_distance*GRID_SQUARE_SIZE/COURSE_MARKERS))]
        
        if any(self.distance_run == marker for marker in markers):
            course_markers[self.i][self.j] = round(self.distance_run*GRID_SQUARE_SIZE/UNIT_DISTANCE)
    
    # set the start and finish lines        
    def set_course_start_finish(self, course_grid, start_finish_markers):
        
        c = course_grid[self.i][self.j]
        
        start_finish_markers[0][0] = Course_Marker.COURSE_M_S_H
        
            
        if self.direction == self.UP:
            if c == Course_Type.COURSE_H or c == Course_Type.COURSE_V:
                orientation = c[-1]
                step_i = 0
                step_j = 1
            else:
                orientation = "h"
                if c == Course_Type.COURSE_B_LT:
                    step_i = -1
                    step_j = 0
                elif c == Course_Type.COURSE_B_RT:
                    step_i = 1
                    step_j = 0   
                
        elif self.direction == self.DOWN:
            if c == Course_Type.COURSE_H or c == Course_Type.COURSE_V:
                orientation = c[-1]
                step_i = 0
                step_j = -1
            else:
                orientation = "h"
                if c == Course_Type.COURSE_B_LD:
                    step_i = -1
                    step_j = 0
                elif c == Course_Type.COURSE_B_RD:
                    step_i = 1
                    step_j = 0  

        elif self.direction == self.LEFT:
            if c == Course_Type.COURSE_H or c == Course_Type.COURSE_V:
                orientation = c[-1]
                step_i = 1
                step_j = 0
            else:
                orientation = "v"
                if c == Course_Type.COURSE_B_LT:
                    step_i = 0
                    step_j = -1
                elif c == Course_Type.COURSE_B_LD:
                    step_i = 0
                    step_j = 1  

        elif self.direction == self.RIGHT:
            if c == Course_Type.COURSE_H or c == Course_Type.COURSE_V:
                orientation = c[-1]
                step_i = -1
                step_j = 0
            else:
                orientation = "v"
                if c == Course_Type.COURSE_B_RT:
                    step_i = 0
                    step_j = -1
                elif c == Course_Type.COURSE_B_RD:
                    step_i = 0
                    step_j = 1

            
        start_finish_markers[self.i+step_i][self.j+step_j] = Course_Marker.COURSE_M_F_ + orientation
            
    # keep running until you have completed the distance           
    def run_course(self, map_grid, course_grid, course_markers, start_finish_markers, race_distance):
                
        while self.distance_run <= race_distance:
            
            #print(self.distance_run,self.direction, map_grid[self.i][self.j], course_grid[self.i][self.j], self.counter_grid[self.i][self.j], self.i, self.j)
            self.set_course_markers(course_markers, race_distance)
            self.move(map_grid, course_grid, course_markers)
        
        self.set_course_start_finish(course_grid, start_finish_markers)
        
        return course_grid, course_markers
    
    # turn around!    
    @property
    def opposite_direction(self):
        
        if self.direction == self.RIGHT:
            return self.LEFT
        if self.direction == self.LEFT:
            return self.RIGHT
        if self.direction == self.UP:
            return self.DOWN
        if self.direction == self.DOWN:
            return self.UP
    
    # flip the direction of a turn vertically
    def v_flip(self,course_type):
        
        if course_type == Course_Type.COURSE_B_LD:
            course_type = Course_Type.COURSE_B_LT
        elif course_type == Course_Type.COURSE_B_LT:
            course_type = Course_Type.COURSE_B_LD
        elif course_type == Course_Type.COURSE_B_RD:
            course_type = Course_Type.COURSE_B_RT
        elif course_type == Course_Type.COURSE_B_RT:
            course_type = Course_Type.COURSE_B_RD
            
        return course_type
    
    # flip the direction of a turn horizontally
    def h_flip(self,course_type):
        
        if course_type == Course_Type.COURSE_B_LD:
            course_type = Course_Type.COURSE_B_RD
        elif course_type == Course_Type.COURSE_B_LT:
            course_type = Course_Type.COURSE_B_RT
        elif course_type == Course_Type.COURSE_B_RD:
            course_type = Course_Type.COURSE_B_LD
        elif course_type == Course_Type.COURSE_B_RT:
            course_type = Course_Type.COURSE_B_LT
            
        return course_type
    
    # depending on your direction, flip the turn
    def flip(self,course_type):
        
        if self.direction == self.UP or self.direction == self.DOWN:
            return self.v_flip(course_type)
        if self.direction == self.LEFT or self.direction == self.RIGHT:
            return self.h_flip(course_type)
        
        
            
            
    # runner directions
    
    UP = 't'
    DOWN = 'd'
    LEFT = 'l'
    RIGHT = 'r'
    
    DIRECTIONS = [
            UP,
            DOWN,
            LEFT,
            RIGHT]



    
    