import numpy as np
from collections import Counter

def set_sum(setx):
    setsum = 0
    for elem in setx:
        setsum += elem
    return setsum

'''
Returns (dist, nodes),
dist[i][j] = minimum distance between i and j;
nodes[i][j] = nodes on the path of minimum distance from i and j; 
'''
def floyd_warshall(times):
    nr_nodes = len(times)
    
    nodes = []
    for ii in range(nr_nodes):
        nodes.append(ii)

    dist = dict()    
    dist_prev = dict()
    dist_nodes = dict()
    for ii in range(nr_nodes):
        for jj in range(nr_nodes):
            new_set = set()
            new_set.add(ii)
            new_set.add(jj)
            dist_nodes[(ii, jj)] = new_set

            dist[(ii, jj)] = times[ii][jj]
            dist_prev[(ii, jj)] = times[ii][jj]
    
    # Do we need to account for indices size?
    for kk in nodes:
        for ii in nodes:
            for jj in nodes:
                curr_min_dist = dist_prev[(ii, jj)]
                potential_min_dist = dist_prev[(ii, kk)] + dist_prev[(kk, jj)]
                
                if(potential_min_dist == curr_min_dist):
                    dist[(ii, jj)] = curr_min_dist
                    length_curr = len(dist_nodes[(ii, jj)])
                    length_potential = len(dist_nodes[(ii, kk)].union(dist_nodes[(kk, jj)]))
                    if(length_potential > length_curr):
                        dist_nodes[(ii, jj)] = dist_nodes[(ii, kk)].union(dist_nodes[(kk, jj)])
                    # This tie-breaker may be wrong.
                    elif(length_potential == length_curr):
                        union = dist_nodes[(ii, kk)].union(dist_nodes[(kk, jj)])
                        if(set_sum(union) < set_sum(dist_nodes[(ii, jj)])):
                            dist_nodes[(ii, jj)] = dist_nodes[(ii, kk)].union(dist_nodes[(kk, jj)])
                elif(potential_min_dist < curr_min_dist):
                    dist[(ii, jj)] = potential_min_dist
                    dist_nodes[(ii, jj)] = dist_nodes[(ii, kk)].union(dist_nodes[(kk, jj)])
        
                else:
                    dist[(ii, jj)] = curr_min_dist
        dist, dist_prev = dist_prev, dist
    
    return (dist_prev, dist_nodes)

def build_solution(nr_nodes, min_dist, dist_nodes, time_limit):
    # Dictionary mapping path_nodes lengths to tuples (jump_path, path_nodes) which are solutions.
    solutions = dict()

    dist_nodes_two = dict()
    for ii in range(nr_nodes):
        for jj in range(nr_nodes):
            dist_nodes_two[(ii, jj)] = Counter(dist_nodes[(ii, jj)])
    del dist_nodes
    dist_nodes = dist_nodes_two

    # Each element in pool is a tuple (path_time, jump_path, path_nodes) where:
    # path_time = the time it takes to take the path;
    # jump_path = if x, y consecutive elements in jump_path => we went from x to y using the 
    # shortest path between them (hence a "jump");
    # path_nodes = all the positions we went through on our jump_path; (stored in a Counter = multiset object) 
    pool = []

    # All paths have to start from the first position (our initial position) and have to end at the last position (the bulkhead).
    start_node = 0
    end_node = nr_nodes-1
    all_nodes = set(range(nr_nodes))

    # Maximum length of all solutions found so far.
    max_length = len(dist_nodes[(start_node, end_node)])
    solutions[2] = [(min_dist[(start_node, end_node)], [start_node, end_node], dist_nodes[(start_node, end_node)])]
    
    # Early termination.
    if(len(solutions[2][0][2]) == nr_nodes):
        return list(range(nr_nodes))
    
    pool = [(min_dist[(start_node, end_node)], [start_node, end_node], dist_nodes[(start_node, end_node)])]

    # When do we add a node to a solution? 
    # When it adds new nodes to path_node + the path is an acceptable solution.
    # When do we stop? 
    # 1. We stop when solutions[nr_nodes] exists.
    # 2. We don't need another stop condition due to the way we add new nodes to a solution.

    # It can pe proven that if x -> y -> z -> t is an acceptable jump_path, x -> y -> t is also an acceptable path.
    for _ in range(nr_nodes):
        new_pool = []
        for (path_time, jump_path, path_nodes) in pool:
            for node in all_nodes:
                # Expanding our path with an identical node is meaningless.
                if(node == jump_path[-2]):
                    continue
                
                penult_node = jump_path[-2]
                
                new_path_nodes = path_nodes - dist_nodes[(penult_node, end_node)] + dist_nodes[(penult_node, node)] + dist_nodes[(node, end_node)]
                new_path_time = path_time - min_dist[(jump_path[-2], end_node)] + min_dist[(jump_path[-2], node)] + min_dist[(node, end_node)]        
                
                # If the new path time is greater than the time limit, the new path is not a solution.
                if(new_path_time > time_limit):
                    continue
                else:
                    # Expand the old jump_path:
                    new_jump_path = list(jump_path)
                    new_jump_path[-1] = node
                    new_jump_path.append(end_node)
                    
                    # If our path reaches all nodes (bunnies), terminate.
                    if(len(new_path_nodes) == nr_nodes):
                        return list(range(nr_nodes))
                    else:
                        # Add the new path to the new pool so it can be expanded the next iteration.
                        new_pool.append((new_path_time, new_jump_path, new_path_nodes))
                        if(node == nr_nodes - 1):
                            continue
                        if(len(new_path_nodes) not in solutions):
                            solutions[len(new_path_nodes)] = []
                        solutions[len(new_path_nodes)].append(new_pool[-1])
                        max_length = max(max_length, len(new_path_nodes))
        pool = new_pool

    # Select the solution with the lowest numbered bunnies.
    path_nodes_list = []
    min_sum = np.inf
    for (path_time, jump_path, path_nodes) in solutions[max_length]:
        path_nodes_set = list(set(path_nodes))
        path_nodes_set.sort()
        sum_nodes = sum(path_nodes_set)
        if(sum_nodes < min_sum):
            min_sum = sum_nodes
        path_nodes_list.append((sum_nodes, path_nodes_set))
    
    path_nodes_min_sum_list = []
    for (sum_nodes, path_nodes_set) in path_nodes_list:
        if(sum_nodes == min_sum):
            path_nodes_min_sum_list.append(path_nodes_set)
    
    path_nodes_min_sum_list.sort()
    return path_nodes_min_sum_list[0]


    

    

def solution(times, time_limit):
    min_dist, dist_nodes = floyd_warshall(times)
    nr_nodes = len(times)
    
    # Check if there are any negative weight cycles.
    # If there are, then all bunnies can be saved.
    for ii in range(nr_nodes):
        if(min_dist[(ii, ii)] < 0):
            return list(range(nr_nodes-2))
        
    solution = build_solution(nr_nodes, min_dist, dist_nodes, time_limit)

    solution = np.array(solution[1:-1]) - 1
    return list(solution)
    

ls = [[0, 2, 2, 2, -1], [9, 0, 2, 2, -1], [9, 3, 0, 2, -1], [9, 3, 2, 0, -1], [9, 3, 2, 2, 0]]
ls2 = [[0, 1, 1, 1, 1], [1, 0, 1, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0]]
print(solution(ls2, 3))
