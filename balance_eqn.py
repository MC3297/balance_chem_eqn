# eqn = "_H3PO4 + _KOH -> _K3PO4 + _H2O"
# eqn = "_K + _B2O3 -> _K2O + _B"
# eqn = "_HCl + _NaOH -> _NaCl + _H2O"
eqn = "_Na + _NaNO3 -> _Na2O + _N2"

# do some string parsing
eqn = eqn.replace(" ", "")
eqn_lhs, eqn_rhs = eqn.split("->")
##print(eqn)
##print(eqn_lhs,eqn_rhs)

lhs_terms = eqn_lhs.split("+")
rhs_terms = eqn_rhs.split("+")
##print(lhs_terms, rhs_terms)

# convert string (can be empty string) to int
def to_int(s):
    if len(s) == 0: return 1
    else: return int(s)

# takes a molecule and split it into each element's frequencies
# ex: H2O -> {'H':2, 'O':1}
def molecules_freq(str):
    ans = {}
    element = ""
    num = ""
    
    for c in str:
        if c.islower():
            element += c
        if c.isupper():
            ans[element] = to_int(num)
            element = c
            num = ""
        if c.isnumeric():
            num += c
        
    ans[element] = to_int(num)
    ans.pop("")
    return ans

eqns_per_element = {}

# for each element, find its corresponding linear eqn coeffs
for i in range(len(lhs_terms)):
    term = lhs_terms[i]
    freq = molecules_freq(term[1:])
    
    for k,v in freq.items():
        if k not in eqns_per_element:
            eqns_per_element[k] = [0]*(len(lhs_terms)+len(rhs_terms))
        
        eqns_per_element[k][i] = v

for i in range(len(rhs_terms)):
    term = rhs_terms[i]
    freq = molecules_freq(term[1:])
    
    for k,v in freq.items():
        if k not in eqns_per_element:
            eqns_per_element[k] = [0]*(len(rhs_terms)+len(rhs_terms))
        
        eqns_per_element[k][i+len(lhs_terms)] = -v

##print(eqns_per_element)

# this is a homogenous linear system
# note there's an implicit zero column
M = list(eqns_per_element.values())
for i in M: print(i)
print()

# returns the rref form of matrix
def row_reduce(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    m = [row[:] for row in matrix]# basically deep copy
    
    for pivot in range(min(rows, cols)):
        # find the maximum element in the current column
        max_row = max(range(pivot, rows), key=lambda r: abs(m[r][pivot]))# python's neat

        # if max row is 0, move on
        if m[max_row][pivot] != 0:
            m[pivot], m[max_row] = m[max_row], m[pivot]# swap
        else:
            continue

        # normalize the pivot row
        pivot_val = m[pivot][pivot]
        m[pivot] = [i/pivot_val for i in m[pivot]]

        # elim the column
        for row in range(pivot+1, rows):
            factor = m[row][pivot]
            m[row] = [m[row][col] - factor*m[pivot][col] for col in range(cols)]

    # back substitution cuz we have ref form
    for pivot in range(min(rows, cols)-1, -1, -1):
        if m[pivot][pivot] == 0:
            continue
        
        # elim the rows above curr row
        for row in range(pivot-1, -1, -1):
            factor = m[row][pivot]
            m[row] = [m[row][col] - factor*m[pivot][col] for col in range(cols)]

    return m

M_rref = row_reduce(M)
##for i in M_rref: print(i)

ans = [0]*(len(lhs_terms)+len(rhs_terms))

# since our system is underdetermined, we guarantee a zero row
ans[-1] = -1
for i in range(len(ans)-1):
    ans[i] = M_rref[i][-1]

from math import gcd
def lcm(a,b):
    return a*b//gcd(a,b)

# let's make everything integers
factor = 1
for i in ans:
    frac = i-int(i)
    if frac != 0:
        factor = lcm(factor, int(1/frac))

# scale to int, round to 4 places, then take abs value
for i in range(len(ans)): ans[i] = abs(round(ans[i]*factor, 4))

print(ans)