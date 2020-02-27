from __future__ import division
from fractions import Fraction
from fractions import gcd
from math import factorial

# poly1 and poly2 are dictionaries;
# poly1[(1, 2)] = dictionary containing x1 * x2;
# poly[(1, 2)][(2, 3)] = coefficient for (x1 ** 2 * x2 ** 3)
# Destroys the dictionaries in the process.
# Order the values in the tuples ascending!!!!
def add(poly1, poly2):
    result_poly = dict()
    terms = set(poly1.keys()).union(set(poly2.keys()))
    for term in terms:
        result_poly[term] = dict()
        if(term in poly1 and term in poly2):
            powers = set(poly1[term].keys()).union(set(poly2[term].keys()))
            for power in powers:
                if(power in poly1[term] and power in poly2[term]):
                    result_poly[term][power] = poly1[term][power] + poly2[term][power]
                elif(power in poly1[term]):
                    result_poly[term][power] = poly1[term][power]
                else:
                    result_poly[term][power] = poly2[term][power]
        elif(term in poly1):
            for power in poly1[term].keys():
                result_poly[term][power] = poly1[term][power]
        else:
            for power in poly2[term].keys():
                result_poly[term][power] = poly2[term][power]
    return result_poly

def multvar(poly, var):
    result_poly = dict()
    for term in poly.keys():
        if(var in term):
            if(term not in result_poly):
                result_poly[term] = dict()
            idx = term.index(var)
            for power in poly[term].keys():
                ls = list(power)
                ls[idx] += 1
                tpl = tuple(ls)
                result_poly[term][tpl] = poly[term][power]
        else:
            idx = 0
            while(idx < len(term) and term[idx] < var):
                idx += 1
            old_term = list(term)
            new_term = old_term[0:idx] + [var] + old_term[idx:]
            new_term = tuple(new_term)
            if(new_term not in result_poly):
                result_poly[new_term] = dict()
            for power in poly[term].keys():
                old_power = list(power)
                new_power = old_power[0:idx] + [1] + old_power[idx:]
                new_power = tuple(new_power)
                result_poly[new_term][new_power] = poly[term][power]
    return result_poly

# ct has to be a Fraction
def multct(poly, ct):
    for term in poly:
        for power in poly[term]:
            poly[term][power] *= ct

def cycle_index(n):
    poly_curr = dict()
    poly_curr[(1, )] = dict()
    poly_curr[(1, )][(1, )] = Fraction(1, 1)

    mem_poly = dict()
    mem_poly[1] = poly_curr
    
    for ii in range(2, n+1):
        polynomials = []
        for jj in range(1, ii):
            polynomials.append(multvar(mem_poly[ii-jj], jj))
        
        poly_last = dict()
        poly_last[(ii, )] = dict()
        poly_last[(ii, )][(1, )] = Fraction(1, 1)
        polynomials.append(poly_last)

        poly_curr = polynomials[0]
        for poly in polynomials[1:]:
            poly_curr = add(poly_curr, poly)
        multct(poly_curr, Fraction(1, ii))
        mem_poly[ii] = poly_curr

    return poly_curr

def combine_two_terms(N, frac, denominator, term1, power1, term2, power2):
    ans = int(frac * denominator)
    for ii in range(len(term1)):
        for jj in range(len(term2)):
            ans *= N ** (power1[ii] * power2[jj] * gcd(term1[ii], term2[jj]))
    return ans

def solution(w, h, s):
    cycle_index_w = cycle_index(w)
    cycle_index_h = cycle_index(h)

    numerator = 0
    denominator = factorial(w) * factorial(h)
    for term1 in cycle_index_w:
        for power1 in cycle_index_w[term1]:
            for term2 in cycle_index_h:
                for power2 in cycle_index_h[term2]:
                    numerator += combine_two_terms(s, cycle_index_w[term1][power1] * cycle_index_h[term2][power2], denominator, term1, power1, term2, power2)
    
    return str(numerator // denominator)