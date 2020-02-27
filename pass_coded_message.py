def select_nmax(n, freq, indices, sol_freq):
    count = n
    
    while(count > 0):
        idx = indices[0]
        if(freq[idx] == 0):
            indices.remove(idx)
        else:
            freq[idx] -= 1
            sol_freq[idx] += 1
            count -= 1
    return

def solution(l):
    input_freq = []
    sol_freq = []
    
    if(len(l) == 0):
        return 0

    for _ in range(10):
        input_freq.append(0)
        sol_freq.append(0)
    
    m3, m31, m32 = 0, 0, 0
    m3_idx = [0,3,6,9]
    m31_idx = [7,4,1]
    m32_idx = [8,5,2]
    
    for elem in l:
        mod3 = elem % 3
        if(mod3 == 0):
            m3 += 1
            sol_freq[elem] += 1
        elif(mod3 == 1):
            m31 += 1
        else:
            m32 += 1
        input_freq[elem] += 1
    
    while(m31 > 3):
        select_nmax(3, input_freq, m31_idx, sol_freq)
        m31 -= 3
    
    while(m32 > 3):
        select_nmax(3, input_freq, m32_idx, sol_freq)
        m32 -= 3
    
    if(m31 == 3 and m32 == 3):
        select_nmax(3, input_freq, m31_idx, sol_freq)
        select_nmax(3, input_freq, m32_idx, sol_freq)
    elif((m31 == 3 or m31 == 2) and (m32 == 2 or m32 == 3)):
        select_nmax(2, input_freq, m31_idx, sol_freq)
        select_nmax(2, input_freq, m32_idx, sol_freq)
    elif(m31 == 3):
        select_nmax(3, input_freq, m31_idx, sol_freq)
    elif(m32 == 3):
        select_nmax(3, input_freq, m32_idx, sol_freq)
    elif(m31 == 0 or m32 == 0):
        pass
    else:
        select_nmax(1, input_freq, m31_idx, sol_freq)
        select_nmax(1, input_freq, m32_idx, sol_freq)
    
    sol = []
    for ii in range(9,-1,-1):
        for _ in range(sol_freq[ii]):
            sol.append(str(ii))

    if(len(sol) == 0 or sol[0] == '0'):
        return 0
    
    return ''.join(sol)
    
import sys
ls = []
for ii in sys.argv[1:]:        
    ls.append(int(ii))
print(solution(ls))