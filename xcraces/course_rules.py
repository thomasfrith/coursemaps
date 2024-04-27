from models import Grid_Type, Course_Type, Course_Marker
from draw_rules import get_left_tile, get_right_tile, get_top_tile, get_bottom_tile, max_hill_height
from setup import LENGTH, WIDTH, GRID_LENGTH, GRID_SQUARE_SIZE, BORDER_PADDING, COURSE_MARKERS, UNIT_DISTANCE

# create a class that will run the course
class Runner:
    
    # intiate the direction and starting postion of the runner
    def __init__(self, direction, turn, start_i, start_j):
    
        self.direction = direction
        self.turn = turn
        self.start_i = start_i
        self.start_j = start_j
        self.i = start_i
        self.j = start_j
        
        # how far has the athlete run in grid squares
        self.distance_run = 0
        
        # the altitude of the runner
        self.altitude = 0
        
        # is the the runner in mud
        self.mud = 0
        
        # how many laps did they get through
        self.laps = 0
        
        # this measures how many times you have returned to a square when 
        # pathfinding
        self.counter_grid = [[0 for i in range(WIDTH)] for i in range(LENGTH)]
        
        # save the athlete coordinates and the distance
        self.coords = [[self.i*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2), self.j*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2), self.distance_run, self.altitude, self.mud]]
        
    # the main function, if there is a straight road ahead or a single bend,
    # keep moving forward
    def move(self, map_grid, hill_grid, course_grid, course_markers, direction):
        
        g = course_grid[self.i][self.j]
        l_g = get_left_tile(map_grid,self.i,self.j)
        r_g = get_right_tile(map_grid,self.i,self.j)
        t_g = get_top_tile(map_grid,self.i,self.j)
        b_g = get_bottom_tile(map_grid,self.i,self.j)
        
        # if there is a clear road ahead, keep moving in the same direction,
        # if there is a single bend, take the bend
        # if there is no clear road and a choice of turnings, turn
        # if there is a dead end and no turnings, backtrack until there is a turning
        
        if direction == self.DOWN:            
            if not any(b_g == lake for lake in Grid_Type.CHOICES_LAKE) and b_g != Grid_Type.EMPTY:
                self.j += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_V
                self.counter_grid[self.i][self.j] += 1
            elif direction == self.direction:
                if g == Course_Type.COURSE_V:
                    course_grid[self.i][self.j] = Course_Type.COURSE_B + self.turn + self.opposite_direction
                self.move(map_grid, hill_grid, course_grid,course_markers,self.turn)
            else:
                self.backtrack(map_grid, course_grid, course_markers,direction)
                
        elif direction == self.UP:            
            if not any(t_g == lake for lake in Grid_Type.CHOICES_LAKE) and t_g != Grid_Type.EMPTY:
                self.j -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_V
                self.counter_grid[self.i][self.j] += 1
            elif direction == self.direction:
                if g == Course_Type.COURSE_V:
                    course_grid[self.i][self.j] = Course_Type.COURSE_B + self.turn + self.opposite_direction
                self.move(map_grid, hill_grid, course_grid,course_markers,self.turn)
            else:
                self.backtrack(map_grid, course_grid, course_markers,direction)
                
        elif direction == self.LEFT:            
            if not any(l_g == lake for lake in Grid_Type.CHOICES_LAKE) and l_g != Grid_Type.EMPTY:
                self.i -= 1
                course_grid[self.i][self.j] = Course_Type.COURSE_H
                self.counter_grid[self.i][self.j] += 1
            elif direction == self.direction:
                if g == Course_Type.COURSE_H:
                    course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.turn
                self.move(map_grid, hill_grid, course_grid,course_markers,self.turn)
            else:
                self.backtrack(map_grid, course_grid, course_markers, direction)
                
        elif direction == self.RIGHT:            
            if not any(r_g == lake for lake in Grid_Type.CHOICES_LAKE) and r_g != Grid_Type.EMPTY:
                self.i += 1
                course_grid[self.i][self.j] = Course_Type.COURSE_H 
                self.counter_grid[self.i][self.j] += 1
            elif direction == self.direction:
                if g == Course_Type.COURSE_H:
                    course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.turn
                self.move(map_grid, hill_grid, course_grid,course_markers,self.turn)
            else:
                self.backtrack(map_grid, course_grid, course_markers, direction)
                
        # count the distance run        
        self.distance_run += 1
        # reset the counter 

        
        # get the altitude
        # default to 0
        self.altitude = 0
        
        # but if on a hill, get the actual altitude
        for n in range(max_hill_height):
            if hill_grid[self.i][self.j][n] != 0:
                self.altitude = n+1
                
        # get the mud
        # default to 0
        self.mud = 0
        
        if any(map_grid[self.i][self.j] == mud for mud in Grid_Type.CHOICES_MUD) and self.altitude == 0:
            self.mud = 1
        
        # add the new coordinates
        self.coords.append([self.i*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2),self.j*GRID_LENGTH +round(GRID_LENGTH/2) + round(BORDER_PADDING/2),self.distance_run*GRID_SQUARE_SIZE,self.altitude, self.mud])
        
    # if there was a deadend and no turning, backtrack until you find
    # a turning            
    def backtrack(self, map_grid, course_grid, course_markers, direction):
        
        g = course_grid[self.i][self.j]
        
        while Course_Type.COURSE_B not in g:
            
            self.counter_grid[self.i][self.j] = 0
            course_grid[self.i][self.j] = 0
            course_markers[self.i][self.j] = 0
            
            if direction == self.DOWN:
                self.j -= 1
            if direction == self.UP:
                self.j += 1
            if direction == self.LEFT:
                self.i += 1
            if direction == self.RIGHT:
                self.i -= 1
            
            g = course_grid[self.i][self.j]
            
            # remove the distance travelled to the deadend
            self.distance_run -= 1
            #remove the athlete coordinates
            del self.coords[-1]
                
        self.distance_run -= 1
        del self.coords[-1]
        
        self.turn = self.opposite_turn
        
        if direction == self.DOWN:
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.turn
        if direction == self.UP:
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.opposite_direction + self.turn
        if direction == self.LEFT:
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.turn + self.opposite_direction
        if direction == self.RIGHT:
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.turn + self.opposite_direction
            
    
    # set the distance markers for the course          
    def set_course_markers(self,course_markers,race_distance):
        
        
        markers = [round(x*COURSE_MARKERS/GRID_SQUARE_SIZE) for x in range(1+round(race_distance*GRID_SQUARE_SIZE/COURSE_MARKERS))]
        
        if any(self.distance_run == marker for marker in markers):
            course_markers[self.i][self.j] = round(self.distance_run*GRID_SQUARE_SIZE/UNIT_DISTANCE)
    
    # set the start and finish lines        
    def set_course_start_finish(self, course_grid, start_finish_markers):
        
        c = course_grid[self.i][self.j]
        
        start_finish_markers[self.start_i][self.start_j] = Course_Marker.COURSE_M_S_H
        
            
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
        
    def get_lap_number(self):
        
        self.laps = max(0,max(max(x)-1 for x in self.counter_grid)) 
        return self.laps


    def get_new_direction(self,course_grid,lap):
        
        lap_number = self.get_lap_number()
        if lap_number >= len(lap):
            lap_type = Course_Type.BIG_LAP
        else:
            lap_type = lap[lap_number]
        
        if lap_type == Course_Type.SMALL_LAP:
            top_straight = self.start_j
            bottom_straight = round(WIDTH/2)
            right_straight = round(3*LENGTH/4)
            left_straight = self.start_i
        if lap_type == Course_Type.BIG_LAP:
            top_straight = self.start_j
            bottom_straight = WIDTH - self.start_j -1
            right_straight = LENGTH - self.start_i -1
            left_straight = self.start_i
            
        if self.i >= right_straight and self.direction == self.RIGHT:
            self.direction = self.DOWN
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.LEFT + self.direction
            if self.turn != self.RIGHT or self.turn != self.LEFT:
                self.turn = self.LEFT
        elif self.i <= left_straight and self.direction == self.LEFT:        
            self.direction = self.UP
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.RIGHT + self.direction
            if self.turn != self.RIGHT or self.turn != self.LEFT:
                self.turn = self.RIGHT
        elif self.j >= bottom_straight and self.direction == self.DOWN:
            self.direction = self.LEFT
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.direction + self.UP
            if self.turn != self.UP or self.turn != self.DOWN:
                self.turn = self.UP
        elif self.j <= top_straight and self.direction == self.UP:
            self.direction = self.RIGHT
            course_grid[self.i][self.j] = Course_Type.COURSE_B + self.direction + self.DOWN
            if self.turn != self.UP or self.turn != self.DOWN:
                self.turn = self.DOWN
            
        
    
    # keep running until you have completed the distance           
    def run_course(self, map_grid, hill_grid, course_grid, course_markers, start_finish_markers, race_distance, lap):
                
        while self.distance_run <= race_distance:
            
            #print(self.distance_run,self.direction, self.turn, map_grid[self.i][self.j], course_grid[self.i][self.j], self.counter_grid[self.i][self.j], self.i, self.j)
                
            self.set_course_markers(course_markers, race_distance)
            self.move(map_grid, hill_grid, course_grid, course_markers,self.direction)
            self.get_new_direction(course_grid,lap)
        
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
        
    @property
    def opposite_turn(self):
        
        if self.turn == self.RIGHT:
            return self.LEFT
        if self.turn == self.LEFT:
            return self.RIGHT
        if self.turn == self.UP:
            return self.DOWN
        if self.turn == self.DOWN:
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
    


    
    