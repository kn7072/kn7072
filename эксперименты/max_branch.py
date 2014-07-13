import unittest

def LongestIncreasingSubsequence(X):
    """
    Find and return longest increasing subsequence of S.
    If multiple increasing subsequences exist, the one that ends
    with the smallest value is preferred, and if multiple
    occurrences of that value can end the sequence, then the
    earliest occurrence is preferred.
    """
    n = len(X)
    X = [None] + X  # Pad sequence so that it starts at X[1]
    M = [None]*(n+1)  # Allocate arrays for M and P
    P = [None]*(n+1)
    L = 0
    for i in range(1,n+1):
        if L == 0 or X[M[1]] >= X[i]:
            # there is no j s.t. X[M[j]] < X[i]]
            j = 0
        else:
            # binary search for the largest j s.t. X[M[j]] < X[i]]
            lo = 1      # largest value known to be <= j
            hi = L+1    # smallest value known to be > j
            while lo < hi - 1:
                mid = (lo + hi)//2
                if X[M[mid]] < X[i]:
                    lo = mid
                else:
                    hi = mid
            j = lo
        P[i] = M[j]
        if j == L or X[i] < X[M[j+1]]:
            M[j+1] = i
            L = max(L,j+1)
    # Backtrack to find the optimal sequence in reverse order
    output = []
    pos = M[L]
    while L > 0:
        output.append(X[pos])
        pos = P[pos]
        L -= 1
    output.reverse()
    return output

#t = LongestIncreasingSubsequence( [3,1,4,1,5,9,2,6,5,3,5,8,9,7,9])
t2 = LongestIncreasingSubsequence( [0, 3, 4, 5, 6, 10, 7, 8, 11, 2, 12, 6, 3, 7, 9])
print(t2)
#unittest.main()