import numpy as np
from fractions import Fraction

'''
Solution summary:
We consider that each of the walls of the room is a mirror. 
We consider each of our shot as a line that stretches indefinitely.
A shot hits the guardian if it hits at least one of the guardian's reflections
before: it hits us, our reflection, a corner or a corner's reflection.

Thus, the following inelegant approach: calculate all our reflections and the corner's reflections
(within the maximum allowed shot distance) + the slopes between our position and those reflections.
We then calculate the coordinates of all the guardian's reflections which are within the max distance
AND for each of those reflections, we increment our shot count by one if the three conditions above 
are respected.
'''


def sq_euclidean_dist(point1, point2):
    return (point1[0] - point2[0])**2 + (point1[1] - point2[1])**2


# Function to find the maximum number of reflections we need to consider along an axis (controlled by signs and corners).
def find_max_nr_reflections(dimensions, signs, corners, your_position, distance):
    nr_reflections = 0
    current_corners = []
    current_corners.append(list(corners[0]))
    current_corners.append(list(corners[1]))
    distance_sq = distance ** 2

    while(True):
        if(sq_euclidean_dist(your_position, current_corners[0]) >= distance_sq and sq_euclidean_dist(your_position, current_corners[1]) >= distance_sq):
            return nr_reflections
        else:
            nr_reflections += 1
            for current_corner in current_corners:
                current_corner[0] = current_corner[0] + signs[0] * dimensions[0]
                current_corner[1] = current_corner[1] + signs[1] * dimensions[1]


# Initialisations functions.
def quadrant_expansion_signs():
    signs = dict()
    signs['ne'] = (1, 1)
    signs['nw'] = (-1, 1)
    signs['se'] = (1, -1)
    signs['sw'] = (-1, -1)
    return signs

def diagonal_expansion_corners(dimensions):
    first_corners = dict()
    first_corners['ne'] = (dimensions[0], dimensions[1])
    first_corners['nw'] = (0, dimensions[1])
    first_corners['se'] = (dimensions[0], 0)
    first_corners['sw'] = (0, 0)
    return first_corners

def axes_expansion_signs():
    direction_signs = dict()
    direction_signs['n'] = (0, 1)
    direction_signs['s'] = (0, -1)
    direction_signs['w'] = (-1, 0)
    direction_signs['e'] = (1, 0)
    return direction_signs


# We keep slopes in Fraction objects as it makes comparisons easier.
def calculate_slope(p1, p2):
    return Fraction(p2[1]-p1[1], p2[0]-p1[0])


# Calculate initial_point's reflection's absolute position in the frame (room reflection)
# specified by ii, jj and signs.
def calculate_reflection_position(dimensions, initial_point, signs, ii, jj):
    relative_origin_x = ii * signs[0] * dimensions[0]
    relative_origin_y = jj * signs[1] * dimensions[1]
    reflection_absolute_position = [0, 0]
    if(ii % 2 == 1):
        reflection_absolute_position[0] = relative_origin_x + dimensions[0] - initial_point[0]
    else:
        reflection_absolute_position[0] = relative_origin_x + initial_point[0]
    
    if(jj % 2 == 1):
        reflection_absolute_position[1] = relative_origin_y + dimensions[1] - initial_point[1]
    else:
        reflection_absolute_position[1] = relative_origin_y + initial_point[1]
    
    return reflection_absolute_position


def count_quadrant_shots(slopes_init, dimensions, your_position, guard_position, distance, signs, max_refl, quadrant, your_reflections):
    '''
        Count all the distinct and valid shots within a quadrant, considering only the room reflections up to max_refl.

            slopes_init = slopes of the corners + slopes of valid shots we've already counted;
            signs = signs for the quadrant;
            max_refl = maximum number of reflected rooms we need to consider in this quadrant;
            your_reflections = dictionary returning the closest forbidden point (your reflection or corner reflection) along the given slope
                               (relative to your position);
    '''
    max_distance = distance ** 2

    counts = 0
    slopes = slopes_init
    if(guard_position[0] != your_position[0]):
        forbidden_slope = calculate_slope(your_position, guard_position)
        slopes.add(forbidden_slope)

    for ii in range(1, max_refl[quadrant]+1):
        for jj in range(1, max_refl[quadrant]+1):
            refl_pos = calculate_reflection_position(dimensions, guard_position, signs[quadrant], ii, jj)
            
            aux_dist = sq_euclidean_dist(your_position, refl_pos)
            if(aux_dist > max_distance):
                continue

            new_slope = calculate_slope(your_position, refl_pos)
            if(new_slope in slopes or (new_slope in your_reflections and your_reflections[new_slope] < aux_dist)):
                continue
            slopes.add(new_slope)
            counts += 1

    return counts

# Find the slopes of the reflections of the given(real) points relative to your position, in the specified quadrant.
def find_all_reflections_in_quadrant(dimensions, real_points, distance, signs, max_refl, quadrant):
    max_distance = distance ** 2

    reflections = dict()

    for ii in range(1, max_refl[quadrant]+1):
        for jj in range(1, max_refl[quadrant]+1):
            for point in real_points: 
                refl_pos = calculate_reflection_position(dimensions, point, signs[quadrant], ii, jj)
                if(refl_pos[0] == point[0]):
                    continue
                new_slope = calculate_slope(point, refl_pos)
                dist_aux = sq_euclidean_dist(point, refl_pos)
                if(dist_aux <= max_distance):
                    if(new_slope in reflections):
                        continue
                    else:
                        reflections[new_slope] = dist_aux
    
    return reflections

# Same as count_quadrant_shots, but for the room reflections that are on the two axes (ii=0 or jj=0).
# Why a separate function? Because these reflections would overlap if we just used the previous function.
def count_OxOy_reflection_frames_shots(dimensions, your_position, guard_position, distance, max_refl_direction, sign, Ox, your_reflections):
    max_distance = distance ** 2

    counts = 0
    slopes = set()

    if(guard_position[0] != your_position[0]):
        slopes.add(calculate_slope(your_position, guard_position))
    
    for ii in range(1, max_refl_direction+1):
        refl_pos = (0, 0)
        if(Ox):
            refl_pos = calculate_reflection_position(dimensions, guard_position, sign, ii, 0)
        else:
            refl_pos = calculate_reflection_position(dimensions, guard_position, sign, 0, ii)
        
        aux_dist = sq_euclidean_dist(your_position, refl_pos)
        if(aux_dist > max_distance):
            continue
        
        new_slope = calculate_slope(your_position, refl_pos)
        if(new_slope in slopes or (new_slope in your_reflections and your_reflections[new_slope] < aux_dist)):
            continue

        slopes.add(new_slope)
        counts += 1
    
    return (counts, slopes)
        
def solution(dimensions, your_position, guard_position, distance):
    quadrant_signs = quadrant_expansion_signs()
    quadrants = quadrant_signs.keys()

    # Initialise "quadrant corners".
    first_corners = diagonal_expansion_corners(dimensions)

    axes_signs = axes_expansion_signs()
    axes = axes_signs.keys()

    # Corners corresponding to axes. 
    nswe_corners = dict()
    nswe_corners['n'] = [first_corners['nw'], first_corners['ne']]
    nswe_corners['s'] = [first_corners['sw'], first_corners['se']]
    nswe_corners['w'] = [first_corners['nw'], first_corners['sw']]
    nswe_corners['e'] = [first_corners['ne'], first_corners['se']]
    
    # Calculate the maximum number of room reflections we need to consider along each axis and quadrant.
    max_refl = dict()
    for axe in axes:
        max_refl[axe] = find_max_nr_reflections(dimensions, axes_signs[axe], nswe_corners[axe], your_position, distance)
    max_refl['ne'] = max(max_refl['n'], max_refl['e'])
    max_refl['nw'] = max(max_refl['n'], max_refl['w'])
    max_refl['sw'] = max(max_refl['s'], max_refl['w'])
    max_refl['se'] = max(max_refl['s'], max_refl['e'])
    
    # Add 1 to the total_count if the guard is withing our firing range.
    total_count = 0
    if(sq_euclidean_dist(your_position, guard_position) <= distance ** 2):
        total_count += 1

    # youcorners_reflections = slopes of reflections of corners and ourselves relative to our real position for each quadrant; 
    youcorner_reflections = dict()
    positions = [your_position] + first_corners.values()
    for quadrant in quadrants:
        youcorner_reflections[quadrant] = find_all_reflections_in_quadrant(dimensions, positions, distance, quadrant_signs, max_refl, quadrant)
    
    total_yourcorner_reflections = dict()
    for quadrant in quadrants:
        total_yourcorner_reflections.update(youcorner_reflections[quadrant])

    slopes_up = set()
    slopes_down = set()
    slopes_left = set()
    slopes_right = set()

    # Count the vertical shots we can take + mark the slopes of the shots in slopes_down and slopes_up (to be used in slopes_init).
    # A vertical shot is a shot that ends up hitting a reflection of the target which is in a vertical frame (ii=0).
    if(guard_position[0] != your_position[0]):
        count_up, slopes_up = count_OxOy_reflection_frames_shots(dimensions, your_position, guard_position, distance, max_refl['n'], (1, 1), False, total_yourcorner_reflections)
        count_down, slopes_down = count_OxOy_reflection_frames_shots(dimensions, your_position, guard_position, distance, max_refl['s'], (1, -1), False, total_yourcorner_reflections)
        total_count += count_up + count_down
    
    # Count the horizontal shots we can take + mark the slopes of the shots in slopes_left and slopes_right.
    # A horizontal shot is a shot that ends up hitting a reflection of the target which is in a horizontal frame (jj=0).
    if(guard_position[1] != your_position[1]):
        count_left, slopes_left = count_OxOy_reflection_frames_shots(dimensions, your_position, guard_position, distance, max_refl['w'], (-1, 1), True, total_yourcorner_reflections)
        count_right, slopes_right = count_OxOy_reflection_frames_shots(dimensions, your_position, guard_position, distance, max_refl['e'], (1, 1), True, total_yourcorner_reflections)
        total_count += count_left + count_right

    # Calculate corners' slopes.
    corners_slopes = dict()
    for quadrant in quadrants:
        corners_slopes[quadrant] = calculate_slope(your_position, first_corners[quadrant])

    # For each quadrant, initialise slopes_init correctly and count the number of valid shots we can take.
    slopes_init = set()
    for quadrant in quadrants:
        if(quadrant == 'ne'):
            slopes_init = slopes_up.union(slopes_right)
        elif(quadrant == 'nw'):
            slopes_init = slopes_up.union(slopes_left)
        elif(quadrant == 'sw'):
            slopes_init = slopes_down.union(slopes_left)
        else:
            slopes_init = slopes_down.union(slopes_right)
        slopes_init.add(corners_slopes[quadrant])
        total_count += count_quadrant_shots(slopes_init, dimensions, your_position, guard_position, distance, quadrant_signs, max_refl, quadrant, youcorner_reflections[quadrant])

    return total_count

print(solution([3,2], [1,1], [2,1], 4))
print(solution([300,275], [150,150], [185,100], 500))
print(solution([1250, 1250], [1,1], [2,3], 10000))
#TODO: Instead of Fraction, use a relative position maybe. SLOPE (TANGENT) IS DIFFERENT THAN FRACTION (CLASHES) (for calculating your_reflections) Fraction(1,-2), Fraction(-1, 2)
#TODO: Think if you need to calculate the reflections of the corners too :/. don't think so.
