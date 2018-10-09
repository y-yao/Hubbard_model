import numpy as np
import math

# Lattice size: M by N
M = 4
N = 4

# Model parameters
t = 1.
U = 4.

nelec = 4 

# k space grid
pi = math.pi
kx_array = [(2*pi*m/M + pi)%(2*pi) - pi for m in range(M)]
ky_array = [(2*pi*n/N + pi)%(2*pi) - pi for n in range(N)]
k_grid = list(((kx, ky) for kx in kx_array for ky in ky_array))
orb_indices = np.arange(1, M*N+1, 1)

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
    for p_orb in orb_indices:
        for q_orb in range(1, p_orb+1):
            for r_orb in orb_indices:
                for s_orb in range(1, r_orb+1):
                    if (p_orb*(p_orb-1)+q_orb < (r_orb*(r_orb-1)+s_orb)):
                        continue
#    for p_orb in orb_indices:
#        for q_orb in orb_indices:
#            for r_orb in orb_indices:
#                for s_orb in orb_indices:
                    p_point = k_grid[p_orb-1]
                    q_point = k_grid[q_orb-1]
                    r_point = k_grid[r_orb-1]
                    s_point = k_grid[s_orb-1]
                    kx_diff = q_point[0] + s_point[0] - p_point[0] - r_point[0]
                    ky_diff = q_point[1] + s_point[1] - p_point[1] - r_point[1]
                    if (kx_diff)%(2*pi)==0 and (ky_diff)%(2*pi)==0:
                        dump_file.write('  %19.12E %3d %3d %3d %3d \n' %(U/M/N, p_orb, q_orb, r_orb, s_orb))
    
    # one-body integrals
    for i_orb, k_point in zip(orb_indices, k_grid):
        dump_file.write('  %19.12E %3d %3d   0   0 \n' % (-2*t*(math.cos(k_point[0])+math.cos(k_point[1])), i_orb, i_orb))
    

