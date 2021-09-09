#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Last modification: 09/2021
# Author: Amaël Ellien
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# modules
import xspec as xs
import numpy as np
import matplotlib.pyplot as plt
import os
from def_jitter_model import *

# add jitter model to Xspec
xs.AllModels.clear()
add_jitter()

# settings
xs.AllModels.setEnergies('0.1 200. 1000 log')
model = xs.Model('jitter')

# Cas A type spectrum
PhoIndex1 = 3.2
Ebreak1   = 1     # keV
beta1     = 0.5
PhoIndex2 = 1.75
Ebreak2   = 100   # keV
beta2     = 0.5
jratio    = 0.1
norm      = 1.0
list_input_par = [ PhoIndex1, Ebreak1, beta1, PhoIndex2, Ebreak2, beta2, jratio, norm ]

# Set parameter values in Xspec
for k in range( 1, model.nParameters + 1 ):
    model(k).values = list_input_par[ k - 1 ]

model.show()

# Plot Xspec
xs.Plot.commands   = ()
xs.Plot.device     = '/xs'
xs.Plot.add        = True
xs.Plot.xLog       = True
xs.Plot.yLog       = True
xs.Plot.xAxis      = 'keV'
xs.Plot('model')

# Plot plt
engs = np.arange( 0.1, 200, 0.001 ) # keV

plt.figure()
flux = jitter(engs = engs, params = list_input_par, flux = np.zeros(engs.size) )
plt.loglog(engs[:-1], norm * flux[:-1], color = 'black', label = 'PhoIndex1 = %1.1f, PhoIndex2 = %1.1f' %(PhoIndex1, PhoIndex2))
plt.ylim( bottom = 1E-5)
plt.title('Jitter model\n$\\beta_1$ = %1.1f, $\\beta_2$ = %1.1f, $E_{break,1}$ = %d keV, $E_{break,2}$ = %d keV, jratio = %1.1f'%(beta1, beta2, Ebreak1, Ebreak2, jratio))
plt.xlabel('keV')
plt.ylabel(r'Photon.cm$^{-2}$.s$^{-1}$.keV$^{-1}$')
plt.legend()
plt.savefig('jitter_model_examples.pdf', format = 'pdf')
plt.show()
