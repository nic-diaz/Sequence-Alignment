import numpy as np

ALPHA =     {('A', 'A'): 0, ('A', 'C'): 110, ('A','G'): 48, ('A', 'T'): 94,
             ('C', 'A'): 110, ('C','C'): 0, ('C','G'): 118, ('C','T'): 48,
             ('G', 'A'): 48, ('G','C'): 118, ('G','G'): 0, ('G', 'T'): 110,
             ('T', 'A'): 94, ('T','C'): 48, ('T', 'G'): 110, ('T','T'): 0}

DELTA = 30

def alignment(A, s1, s2, i, j):
    '''
    Finds optimal alignment after tracing back through A
    '''
    if i + j == 0: return []
    if i == 0: return [[i, k] for k in range(j-1,-1,-1)]
    if j == 0: return [[k, j] for k in range(i-1,-1,-1)]
    
    
    mismatch = ALPHA[(s1[i-1], s2[j-1])] + A[i-1,j-1]
    gap_left = DELTA + A[i-1, j]
    gap_up = DELTA + A[i, j-1]

    min_idx = np.argmin([mismatch, gap_up, gap_left])

    if min_idx == 0:
        return [[i-1,j-1]] + alignment(A, s1, s2, i-1,j-1)
    elif min_idx == 1:
        return [[i,j-1]] + alignment(A, s1, s2, i, j-1)
    else:
        return [[i-1,j]] + alignment(A, s1, s2, i-1, j)

def find_solution(s1, s2, alignment):
    '''
    Uses alignment to generate the final strings
    '''
    final_s1, final_s2 = "", ""

    for k in range(len(alignment)-1):

        x_k, y_k = alignment[k]

        if [x_k + 1, y_k + 1] == alignment[k+1]:
            final_s1 += s1[x_k]
            final_s2 += s2[y_k]
            
        elif [x_k + 1, y_k] == alignment[k+1]:
            final_s1 += s1[x_k]
            final_s2 += "_"
        else:
            final_s1 += "_"
            final_s2 += s2[y_k]

    return final_s1, final_s2

def validate(s1, s2):
    '''
    Helper function to check the final strings optimal costs
    '''
    print(len(s1), len(s2))
    total_costs = 0

    for i in range(len(s1)):
        total_costs += DELTA if (s1[i] == "_" or s2[i] == "_") else ALPHA[(s1[i], s2[i])]
    return total_costs

def basic(s1, s2):
    '''
    Calculates the A matrix containing the optimal costs from (0,0) to each (i,j) 
    '''
    
    m = len(s1) + 1
    n = len(s2) + 1

    A = np.zeros((m, n))

    A[:, 0] = np.arange(m) * DELTA
    A[0, :] = np.arange(n) * DELTA

    for i in range(1,m):
        for j in range(1,n):
            A[i, j] = min(ALPHA[(s1[i-1], s2[j-1])] + A[i-1,j-1], DELTA + A[i-1, j], DELTA + A[i, j-1])

    opt_alignment = alignment(A, s1, s2, len(s1), len(s2))
    final_s1, final_s2 = find_solution(s1, s2, opt_alignment[::-1]+[[len(s1),len(s2)]])

    return A[m-1,n-1], final_s1, final_s2

if __name__ == "__main__":
    s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG', 'TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG']
    # s1, s2 = ['ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG','TTATTATACGCGACGCGATTATACGCGACGCG']

    opt, final_s1, final_s2 = basic(s1, s2)
    validated_cost = validate(final_s1, final_s2)

    print(opt, validated_cost)
    print(final_s1[:50], final_s1[-50:])
    print(final_s2[:50], final_s2[-50:])