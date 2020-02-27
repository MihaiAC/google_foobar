import heapq

def cartesian(number):
    return (number//8, number%8)

def numberfy(cart):
    return cart[0]*8 + cart[1]

def calculate_next(curr):
    (x, y) = curr
    next_poss = [(x-2, y-1),(x-2, y+1),(x-1, y-2),(x-1, y+2),(x+1, y-2),(x+1, y+2),(x+2, y-1),(x+2, y+1)]
    return list(filter(lambda tp: tp[0] >= 0 and tp[0] <= 7 and tp[1] >= 0 and tp[1] <= 7, next_poss))
    

def solution(src, dest):
    visited = set()
    heap = []

    src_cart = cartesian(src)
    dest_cart = cartesian(dest)

    heapq.heappush(heap, (0, src_cart))
    visited.add(src_cart)

    while(len(heap) > 0):
        curr = heapq.heappop(heap)
        if(curr[1] == dest_cart):
            return curr[0]
        visited.add(curr[1])
        for next_poss in calculate_next(curr[1]):
            if(next_poss not in visited):
                heapq.heappush(heap, (curr[0]+1, next_poss))
                visited.add(next_poss)

import sys
src = int(sys.argv[1])
dest = int(sys.argv[2])
print(solution(src, dest))