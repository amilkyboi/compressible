# module inverse
'''
Inverse isentropic relations.
'''

import math

def inv_stag_temp(gamma: float, stag_temp_ratio: float) -> float:
    '''
    _summary_

    Args:
        gamma (float): _description_
        stag_temp_ratio (float): _description_

    Returns:
        float: _description_
    '''

    return math.sqrt((2 / (gamma - 1)) * (stag_temp_ratio**(-1) - 1))

def inv_stag_pres(gamma: float, stag_pres_ratio: float) -> float:
    '''
    _summary_

    Args:
        gamma (float): _description_
        stag_pres_ratio (float): _description_

    Returns:
        float: _description_
    '''

    return math.sqrt((2 / (gamma - 1)) * (stag_pres_ratio**((1 - gamma) / gamma) - 1))

def inv_stag_dens(gamma: float, stag_dens_ratio: float) -> float:
    '''
    _summary_

    Args:
        gamma (float): _description_
        stag_dens_ratio (float): _description_

    Returns:
        float: _description_
    '''

    return math.sqrt((2 / (gamma - 1)) * (stag_dens_ratio**(1 - gamma) - 1))

def inv_mach_angl(mach_angl: float) -> float:
    '''
    _summary_

    Args:
        mach_angl (float): _description_

    Returns:
        float: _description_
    '''

    return 1 / math.sin(math.radians(mach_angl))

def inv_pran_angl(gamma: float, pran_angl: float) -> float:
    '''
    _summary_

    Args:
        gamma (float): _description_
        pran_angl (float): _description_

    Returns:
        float: _description_
    '''

    lmb     = math.sqrt((gamma - 1)/(gamma + 1))
    k_0     = 4/(3*math.pi)*(1 + 1/lmb)
    eta_inf = (3*math.pi/(2*lmb + 2*lmb**2))**(2/3)
    a_1     = 0.5*eta_inf
    a_2     = (3 + 8*lmb**2)/40*eta_inf**2
    a_3     = (-1 + 328*lmb**2 + 104*lmb**4)/2800*eta_inf**3
    d_1     = a_1 - 1 - (a_3 - k_0)/(a_2 - k_0)
    d_2     = a_2 - a_1 - ((a_1 - 1)*(a_3 - k_0))/(a_2 - k_0)
    d_3     = ((a_3 - k_0)*(a_1 - k_0))/(a_2 - k_0) - a_2 + k_0
    e_1     = -1 - (a_3 - k_0)/(a_2 - k_0)
    e_2     = -1 - e_1
    nu_inf  = 0.5*math.pi*(1/lmb-1)
    y_0     = (math.radians(pran_angl)/nu_inf)**(2/3)

    return (1 + d_1*y_0 + d_2*y_0**2 + d_3*y_0**3) / (1 + e_1*y_0 + e_2*y_0**2)
