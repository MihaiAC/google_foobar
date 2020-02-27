import numpy as np
from collections import deque

# Returns the valid neighbors of node.
def get_neighbors(m, h, w, node):
    x, y = node
    neighbors = []   
    for (a, b) in [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]:
        if(a >= 0 and a < h and b >= 0 and b < w and m[a][b] == 0):
            neighbors.append((a, b))
    return neighbors


# Returns a dictionary cost such that cost[(i, j)] = minimum distance from (i, j) to start in matrix m.
def calculate_dist_map(m, start):
    h = len(m)
    w = len(m[0])

    x, y = start
    
    cost = dict()
    for ii in range(h):
        for jj in range(w):
            cost[(ii, jj)] = np.inf
    cost[start] = 1

    visited = set()
    visited.add((x, y))
    
    queue = deque()
    queue.appendleft((x, y))

    while(len(queue) > 0):
        curr_node = queue.pop()

        neighbors = get_neighbors(m, h, w, curr_node)
        for neighbor in neighbors:
            if(neighbor in visited):
                continue
            else:
                cost[neighbor] = cost[curr_node] + 1
                visited.add(neighbor)
                queue.appendleft(neighbor)
    return cost 

def calculate_min_dist(m, dist_entrance, dist_exit):
    min_escape_dist = dist_exit[(0, 0)]

    h = len(m)
    w = len(m[0])

    # For each wall between x and y, compare the min_escape_dist with dist_entrance[x]+1+dist_exit[y]
    # and with dist_entrance[y]+1+dist_exit[x] and update it with the lowest value of the 3.
    for ii in range(h):
        for jj in range(w):
            if(m[ii][jj] == 0):
                continue
            
            north = (ii+1, jj)
            south = (ii-1, jj)
            west = (ii, jj-1)
            east = (ii, jj+1)
            if(north in dist_entrance and south in dist_entrance):
                min_escape_dist = min(min_escape_dist, dist_entrance[north]+1+dist_exit[south], dist_entrance[south]+1+dist_exit[north])
            if(west in dist_entrance and east in dist_entrance):
                min_escape_dist = min(min_escape_dist, dist_entrance[west]+1+dist_exit[east], dist_entrance[east]+1+dist_exit[west])

    return min_escape_dist

def solution(m):
    h = len(m)
    w = len(m[0])

    dist_entrance = calculate_dist_map(m, (0, 0))
    dist_exit = calculate_dist_map(m, (h-1, w-1))

    return calculate_min_dist(m, dist_entrance, dist_exit)

m1 = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
m2 = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
print(solution(m1))
print(solution(m2))