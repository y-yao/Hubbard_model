'''
Generate FCIDUMP for the Hubbard model in site basis
Yuan Yao
Oct 2018
'''
import numpy as np
import math

## Generate FCIDUMP for real space orbitals
## of the Hubbard model

# Lattice size: M by N
M = 2 
N = 2

# Model parameters
t = 1.
U = 4.

nelec = 2 

# r space grid
pi = math.pi
x_array = range(M)
y_array = range(N)
r_grid = list(((x, y) for x in x_array for y in y_array))
orb_indices = np.arange(1, M*N+1, 1)
print(r_grid)
with open('FCIDUMP', 'w') as dump_file:
    # Header
    dump_file.write(' &FCI NORB=%d, NELEC=%d, MS2=2,\n' % (M*N, nelec))
    dump_file.write('  ORBSYM =')
    for i in orb_indices:
        dump_file.write('1,')
    dump_file.write('\n')
    dump_file.write('  ISYM=1,\n')
    dump_file.write(' &END\n')
    
    # two-body integrals
    for i_orb in orb_indices:
        dump_file.write('  %19.12E %3d %3d %3d %3d \n' %(U, i_orb, i_orb, i_orb, i_orb))
    
    # one-body integrals
    for i_orb in orb_indices:
        for j_orb in range(1, i_orb+1):
            i_coord = r_grid[i_orb-1]
            j_coord = r_grid[j_orb-1]
            x_diff = abs(i_coord[0] - j_coord[0])
            y_diff = abs(i_coord[1] - j_coord[1])
            if ((x_diff == 1 or x_diff == M-1) and y_diff == 0) \
                or (x_diff == 0 and (y_diff == 1 or y_diff == N-1)):
                dump_file.write('  %19.12E %3d %3d   0   0 \n' % (-t, i_orb, j_orb))
    

