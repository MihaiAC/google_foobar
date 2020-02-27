def solution(l):
    # nrmult_right[ii]=n <=> there are n multiples of l[ii] in l[ii+1:]
    nrmult_right = []
    nr_passcodes = 0
    for _ in range(len(l)):
        nrmult_right.append(0)
    
    for ii in range(len(l)-2,-1,-1):
        for jj in range(ii+1, len(l)):
            if(l[ii] > l[jj]):
                continue
            elif(l[jj] % l[ii] == 0):
                nrmult_right[ii] += 1
                nr_passcodes += nrmult_right[jj]
    return nr_passcodes

import sys
ls = []
for ii in sys.argv[1:]:
    ls.append(int(ii))
print(solution(ls))
