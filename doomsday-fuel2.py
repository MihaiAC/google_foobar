from __future__ import division
import numpy as np
from fractions import Fraction, gcd

# Find the least common multiple of a, b.
def lcm(a, b):
    return (a * b) // gcd(a, b)

# A terminal state is a state with no transitions.
def find_terminal_states(m):
    terminal_states = set()
    for ii in range(len(m)):
        sw = 1
        for jj in m[ii]:
            if(jj != 0):
                sw = 0
        if(sw):
            terminal_states.add(ii)
    return terminal_states

def rearrange_states_order(nr_states, nr_trans_states, terminal_states, m):
    # Rearrange states' order so that the terminal states' will be last.
    # Relative order of terminal/non-terminal states (respectively) is preserved 
    # (e.g nt1, t1, nt2, t2 -> nt1, nt2, t1, t2) 
    mapping = []
    inv_mapping = []
    for ii in range(nr_states):
        mapping.append(0)
        inv_mapping.append(0)

    new_state = 0
    new_term_state = nr_trans_states
    for ii in range(nr_states):
        if(ii not in terminal_states):
            mapping[ii] = new_state
            inv_mapping[new_state] = ii
            new_state += 1
        else:
            mapping[ii] = new_term_state
            inv_mapping[new_term_state] = ii
            new_term_state += 1

    m_arranged = np.zeros((nr_states, nr_states))
    for ii in range(nr_states):
        m_arranged[ii] = m[inv_mapping[ii]]
        
    # Fix the state references inside each state (by re-arranging the rows, we must also
    # rearrange the columns, since an element of the matrix references a specific row + 
    # we must rearrange the elements within each row in the same way).
    m_arranged = np.dot(m_arranged, np.eye(len(m_arranged[0]))[mapping])
    
    return m_arranged

def solution(m):
    
    # Handling the case the rock has only one state.
    if(len(m) == 1):
        return [1, 1]
    
    nr_states = len(m)
    
    # Compute the terminal states.
    terminal_states = find_terminal_states(m)

    # Number of transient states (non-terminal states).
    nr_trans_states = nr_states - len(terminal_states)
    
    # Handling the case in which all states are terminal (the rock remains in state 1).
    if(nr_trans_states == 0):
        ret = np.zeros(nr_states+1)
        ret[0] = 1
        ret[nr_states] = 1
        return ret
    
    # Re-arrange m, so terminal states will be last.
    m_arranged = rearrange_states_order(nr_states, nr_trans_states, terminal_states, m)
    
    # Build the transition matrix for our Markov Chain:
    
    # 1) For the transient states, calculate the transition probabilities.
    transition_matrix = np.zeros((nr_states, nr_states))
    m_arranged = np.array(m_arranged)
    for ii in range(nr_trans_states):
        transitions = np.sum(m_arranged[ii])
        transition_matrix[ii] = m_arranged[ii] / transitions
    
    # 2) For each terminal state, set the probability of the transition from 
    # itself to itself to 1.
    for ii in range(nr_trans_states, nr_states):
        transition_matrix[ii, ii] = 1
    
    # The steady state will technically be obtained for (probability vector 
    # corresponding to the initial state of the rock) * transition_matrix ^ N,
    # N tends to infinity.
    # In practice, for our situation this seems a good enough approximation.
    # Normally, we should check if we have converged to the steady state.
    for _ in range(30):
        transition_matrix = np.matmul(transition_matrix, transition_matrix)
    
    # This corresponds to our steady state (given that we always start in state 0).
    B = list(transition_matrix[0, :])
    
    # Select only the probabilities for the terminal states.
    B = B[nr_trans_states:]
    
    # Compute the fractions corresponding to our probabilities.
    frcs = []
    for abs_prob in B:
        frcs.append(Fraction(abs_prob).limit_denominator())

    # If we have only one terminal state: 
    if(len(frcs) == 1):
        numerator = frcs[0].numerator
        denominator = frcs[0].denominator
        #gcd_ = gcd(numerator, denominator)
        return [numerator, denominator]

    numerators = []
    denominators = []
    for frc in frcs:
        numerators.append(frc.numerator)
        denominators.append(frc.denominator)


    # Calculate the lcm of the denominators (lowest common denominator) of our
    # fractions.
    lcm_ = lcm(denominators[0], denominators[1])
    for denom in denominators[2:]:
        lcm_ = lcm(lcm_, denom)
    
    # Bring each fraction to the lowest common denominator.
    solution = []
    for ii in range(len(numerators)):
        solution.append(numerators[ii] * lcm_ // denominators[ii])
    
    solution.append(lcm_)

    return solution

a = [[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
b = [[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
#TODO: CHECK THIS : c = [[0]]
print(solution(a))

# TODO: Need to re-arrange nodes internally too!