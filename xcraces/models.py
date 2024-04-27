# define all the possible course components in Course_Type
# define all the possible map components in Grid_Type

# collect these components in a variety of lists for use in other sections
# of the code

class Course_Marker:
    
    COURSE_M = "course_m_"
    COURSE_M_S_H = "course_m_s_h"
    COURSE_M_S_V = "course_m_s_v"
    COURSE_M_F_ = "course_m_f_"
    COURSE_M_F_H = "course_m_f_h"
    COURSE_M_F_V = "course_m_f_v"

class Course_Type:
    
    SMALL_LAP = "small lap"
    BIG_LAP = "big lap"
    
    COURSE_H = 'course_h'
    COURSE_V = 'course_v'
    
    COURSE_B = 'course_b_'
    
    COURSE_B_LT = 'course_b_lt'
    COURSE_B_LD = 'course_b_ld'
    COURSE_B_RT = 'course_b_rt'
    COURSE_B_RD = 'course_b_rd'
    
    COURSE_T_HT = 'course_t_ht'
    COURSE_T_HD = 'course_t_hd'
    COURSE_T_VR = 'course_t_vr'
    COURSE_T_VL = 'course_t_vl'
    
    CHOICES = [
            COURSE_H,
            COURSE_V,
            COURSE_B_LT,
            COURSE_B_LD,
            COURSE_B_RT,
            COURSE_B_RD
            ]
    
    CHOICES_BENDS = [
            COURSE_B_LT,
            COURSE_B_LD,
            COURSE_B_RT,
            COURSE_B_RD
            ]
    
class Grid_Type:
    
    EMPTY = "empty"
    HOUSE = "house"
    ROAD_H = "road_h"
    ROAD_V = "road_v"
    ROAD_B_LT = "road_bend_lt"
    ROAD_B_LD = "road_bend_ld"
    ROAD_B_RT = "road_bend_rt"
    ROAD_B_RD = "road_bend_rd"
    ROAD_T_HT = "road_turning_ht"
    ROAD_T_HD = "road_turning_hd"
    ROAD_T_VL = "road_turning_vl"
    ROAD_T_VR = "road_turning_vr"
    ROAD_J = "road_junction"
    ROAD_CROSSING = "road_crossing"
    RIVER_H = "river_h"
    RIVER_V = "river_v"
    RIVER_B_LT = "river_bend_lt"
    RIVER_B_LD = "river_bend_ld"
    RIVER_B_RT = "river_bend_rt"
    RIVER_B_RD = "river_bend_rd"
    RIVER_R_H = "rural_river_h"
    RIVER_R_V = "rural_river_v"
    RIVER_R_B_LT = "rural_river_bend_lt"
    RIVER_R_B_LD = "rural_river_bend_ld"
    RIVER_R_B_RT = "rural_river_bend_rt"
    RIVER_R_B_RD = "rural_river_bend_rd"
    BRIDGE_H = "bridge_h"
    BRIDGE_V = "bridge_v"
    PARK = "park"
    TREE = "tree"
    LAKE = "lake"
    LAKE_LT = "lake_lt"
    LAKE_LD = "lake_ld"
    LAKE_RT = "lake_rt"
    LAKE_RD = "lake_rd"
    MUD = "mud"
    MUD_LT = "mud_lt"
    MUD_LD = "mud_ld"
    MUD_RT = "mud_rt"
    MUD_RD = "mud_rd"
    MUD_L = "mud_ll"
    MUD_R = "mud_rr"
    MUD_T = "mud_tt"
    MUD_D = "mud_dd"
    PUDDLE = "puddle"
    HILL = "hill"
    HILL_LT = "hill_lt"
    HILL_LD = "hill_ld"
    HILL_RT = "hill_rt"
    HILL_RD = "hill_rd"
    HILL_L = "hill_ll"
    HILL_R = "hill_rr"
    HILL_T = "hill_tt"
    HILL_D = "hill_dd"
    
    CHOICES = [
            HOUSE,
            ROAD_H,
            ROAD_V,
            ROAD_B_LT,
            ROAD_B_LD,
            ROAD_B_RT,
            ROAD_B_RD,
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_T_VL,
            ROAD_T_VR,
            ROAD_J,
            RIVER_H,
            RIVER_V,
            RIVER_B_LT,
            RIVER_B_LD,
            RIVER_B_RT,
            RIVER_B_RD,
            BRIDGE_H,
            BRIDGE_V
            ]
    
    CHOICES_ROAD_H = [
            ROAD_H,
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_J,
            BRIDGE_H
            ]
    
    CHOICES_ROAD_V = [
            ROAD_V,
            ROAD_T_VL,
            ROAD_T_VR,
            ROAD_J,
            BRIDGE_V
            ]
    
    CHOICES_NOT_RIVER = [
            HOUSE,
            ROAD_H,
            ROAD_V,
            ROAD_B_LT,
            ROAD_B_LD,
            ROAD_B_RT,
            ROAD_B_RD,
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_T_VL,
            ROAD_T_VR,
            ROAD_J,
            BRIDGE_H,
            BRIDGE_V
            ] 
    
    CHOICES_LAKE = [
            LAKE,
            LAKE_LT,
            LAKE_LD,
            LAKE_RT,
            LAKE_RD
            ]
    
    CHOICES_MUD = [
            MUD,
            MUD_LT,
            MUD_LD,
            MUD_RT,
            MUD_RD,
            MUD_L,
            MUD_R,
            MUD_T,
            MUD_D
            ]
    
    CHOICES_HILL = [
            HILL,
            HILL_LT,
            HILL_LD,
            HILL_RT,
            HILL_RD,
            HILL_L,
            HILL_R,
            HILL_T,
            HILL_D
            ]
    
    CHOICES_HILL_CORNER = [
            HILL_LT,
            HILL_LD,
            HILL_RT,
            HILL_RD,
            HILL_L,
            HILL_R,
            HILL_T,
            HILL_D
            ]
    
    CHOICES_RIVER = [
            RIVER_H,
            RIVER_V,
            RIVER_B_LT,
            RIVER_B_LD,
            RIVER_B_RT,
            RIVER_B_RD,
            RIVER_R_H,
            RIVER_R_V,
            RIVER_R_B_LT,
            RIVER_R_B_LD,
            RIVER_R_B_RT,
            RIVER_R_B_RD
            ]
    
    CHOICES_RIVER_PARK = [
            RIVER_H,
            RIVER_V,
            RIVER_B_LT,
            RIVER_B_LD,
            RIVER_B_RT,
            RIVER_B_RD,
            RIVER_R_H,
            RIVER_R_V,
            RIVER_R_B_LT,
            RIVER_R_B_LD,
            RIVER_R_B_RT,
            RIVER_R_B_RD,
            PARK
            ]
    
    CHOICES_BENDS = [
            ROAD_B_LT,
            ROAD_B_LD,
            ROAD_B_RT,
            ROAD_B_RD
            ]
    
    CHOICES_TURNINGS = [
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_T_VL,
            ROAD_T_VR
            ]
    
    CHOICES_FROM_LEFT = [
            ROAD_H,
            ROAD_B_RT,
            ROAD_B_RD,
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_T_VR,
            ROAD_J,
            BRIDGE_H
            ]
    
    CHOICES_FROM_RIGHT = [
            ROAD_H,
            ROAD_B_LT,
            ROAD_B_LD,
            ROAD_T_HT,
            ROAD_T_HD,
            ROAD_T_VL,
            ROAD_J,
            BRIDGE_H
            ]
    
    CHOICES_FROM_TOP = [
            ROAD_V,
            ROAD_B_LD,
            ROAD_B_RD,
            ROAD_T_HD,
            ROAD_T_VL,
            ROAD_T_VR,
            ROAD_J,
            BRIDGE_V
            ]
    
    CHOICES_FROM_BOTTOM = [
            ROAD_V,
            ROAD_B_LT,
            ROAD_B_RT,
            ROAD_T_HT,
            ROAD_T_VL,
            ROAD_T_VR,
            ROAD_J,
            BRIDGE_V
            ]
