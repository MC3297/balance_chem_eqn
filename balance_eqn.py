eqn = "_H3PO4 + _KOH -> _K3PO4 + _H2O"

# do some string parsing
eqn = eqn.replace(" ", "")
lhs, rhs = eqn.split("->")
print(eqn)
print(lhs,rhs)

lhs_terms = lhs.split("+")
rhs_terms = rhs.split("+")
print(lhs_terms, rhs_terms)

# convert string (can be empty string) to int
def to_int(s):
    if len(s) == 0: return 1
    else: return int(s)

# takes a molecule and split it into each atom's frequencies
# ex: H2O -> {'H':2, 'O':1}
def molecules_freq(str):
    ans = {}
    atom = ""
    num = ""
    for c in str:
        if c.islower():
            atom += c
        if c.isupper():
            ans[atom] = to_int(num)
            atom = c
            num = ""
        if c.isnumeric():
            num += c
    ans[atom] = to_int(num)
    ans.pop("")
    return ans

print(molecules_freq("PO4"))

eqns_per_atom = {}
for term in lhs_terms:
    freq = molecules_freq(term[1:])
    for k,v in freq:
        if k not in eqns_per_atom: eqns_per_atom[k] = []
        eqns_per_atom[k].append(v)