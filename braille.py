def solution(s):
    decoded_str = "The quick brown fox jumps over the lazy dog"
    
    encoded_str = "000001011110110010100010000000111110101001010100100100101000000000110000111010101010010111101110000000110100101010101101000000010110101001101100111100011100000000101010111001100010111010000000011110110010100010000000111000100000101011101111000000100110101010110110"
    
    cap_mark = "000001"
    encoded_str = encoded_str[6:]
    
    braille = dict()
    
    for ii in range(len(decoded_str)):
        braille[decoded_str[ii].lower()] = encoded_str[6*ii:(6*ii+6)]
    
    encoded_s = []
    
    for ch in s:
        if(ch == ' '):
            encoded_s.append(braille[ch])
        elif(ch == ch.upper()):
            encoded_s.append(cap_mark)
            encoded_s.append(braille[ch.lower()])
        else:
            encoded_s.append(braille[ch])
    
    return ''.join(encoded_s)


import sys
print(solution(sys.argv[1]))
