'''
Generating FCIDUMP for the Hubbard model with complex k-orbitals (momentum eigenstates)

Yuan Yao
Oct 2018
'''
import numpy as np
import math

# Lattice size: M by N
M = 4 
N = 4

# Model parameters
t = 1.
U = 4.

nelec = 8 

# k space grid
pi = math.pi
kx_array = [(x+M//2)%(M) - M//2 for x in range(M)]
ky_array = [(y+M//2)%(M) - M//2 for y in range(N)]
k_grid = list(((kx, ky) for kx in kx_array for ky in ky_array))
k_grid.sort(key=lambda k: (np.linalg.norm(k), k[0], k[1]))
orb_indices = np.arange(1, M*N+1, 1)

print(k_grid)

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
#    for p_orb in orb_indices:
#        for q_orb in range(1, p_orb+1):
#            for r_orb in orb_indices:
#                for s_orb in range(1, r_orb+1):
#                    if (p_orb*(p_orb-1)/2+q_orb < (r_orb*(r_orb-1)/2+s_orb)):
#                        continue
    for p_orb in orb_indices:
        for q_orb in orb_indices:
            for r_orb in orb_indices:
                for s_orb in orb_indices:
                    p_point = k_grid[p_orb-1]
                    q_point = k_grid[q_orb-1]
                    r_point = k_grid[r_orb-1]
                    s_point = k_grid[s_orb-1]
                    kx_diff = q_point[0] + s_point[0] - p_point[0] - r_point[0]
                    ky_diff = q_point[1] + s_point[1] - p_point[1] - r_point[1]
                    if (kx_diff)%(M)==0 and (ky_diff)%(N)==0:
                        dump_file.write('  %19.12E %3d %3d %3d %3d \n' %(U/M/N, p_orb, q_orb, r_orb, s_orb))
    
    # one-body integrals
    for i_orb, k_point in zip(orb_indices, k_grid):
        kx = k_point[0]*2*pi/M
        ky = k_point[1]*2*pi/N
        dump_file.write('  %19.12E %3d %3d   0   0 \n' % (-2*t*(math.cos(kx)+math.cos(ky)), i_orb, i_orb))
