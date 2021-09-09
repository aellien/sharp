#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Last modification: 09/2021
# Author: Amaël Ellien
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# modules
import xspec as xs
import numpy as np

# jitter model
def jitter(engs, params, flux):
    '''
    Calculates the photon spectrum of synchrotron plus jitter radiation. This
    function can be used with the 'addPyMod' method in PyXspec to implement it in
    the Xspec library. It can also be called directly from Python as a generic
    parametric function.

    Arguments
    ----------------

            engs        Energy array. If used in Xspec, this is set by currently
                        used spectrum. If used in Python, should be a Nump 1D array. # keV

            params      Tuple or list of parameter values.

            flux        Output flux array. If used in Xspec, this is set by currently
                        used spectrum. If used in Python, should be a Nump 1D array. # Photon/cm2/s/keV

    Output
    ----------------

            flux        Same as argument.

    '''

    PhoIndex1, Ebreak1, beta1, PhoIndex2, Ebreak2, beta2, jratio, norm = params

    for i in range(len(engs)-1):

        sync_flux = np.power( engs[i], -PhoIndex1 ) * np.exp( - np.power(engs[i]/Ebreak1, beta1) )
        jitter_flux = np.power( engs[i], -PhoIndex2 ) * np.exp( - np.power(engs[i]/Ebreak2, beta2) ) * jratio

        if sync_flux > jitter_flux:
            flux[i] = sync_flux
        elif jitter_flux >= sync_flux:
            flux[i] = jitter_flux

    return flux

# add model to Xspec
def add_jitter():
    '''
    Add jitter radiation model to Xspec library.
    '''

    # Parameter information
    param_info = ( 'PhoIndex1   \"\" 3 -3. -2. 10 10 0.01', \
                   'Ebreak1   keV 1.5 1. 1. 100 100 0.01', \
                   'beta1   \"\" 0.5 0. 0. 10 100 0.01', \
                   'PhoIndex2   \"\" 1.5 -3. -2. 10 10 0.01', \
                   'Ebreak2   keV 15.0 1. 1. 100 100 0.01', \
                   'beta2   \"\" 0.5 0. 0. 10 100 0.01', \
                   'jratio   \"\" 0.1 0. 0. 10 100 0.01' )

    # Add model to Xspec under name 'jitter'
    xs.AllModels.addPyMod(jitter, param_info, 'add')
