# module inverse
'''
Inverse isentropic relations.
'''

import math

from newton import newton_raphson

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

    return 1 / math.sin(mach_angl)

def inv_pran_angl(gamma: float, pran_angl: float, method: str) -> float:
    '''
    Calculates the Mach number of the flow based on the Prandtl-Meyer angle using numerical
    inversion. Option 'newton' uses the Newton-Raphson method, option 'composite' uses an
    approximate method based on Taylor series expansions.

    Args:
        gamma (float): ratio of specific heats
        pran_angl (float): Prandtl-Meyer angle in [rad]
        method: which method is used to calculate the inverse Prandtl-Meyer function, either newton
                or composite

    Returns:
        float: Mach number
    '''

    # Approximate method adapted from "Inversion of the Prandtl-Meyer Relation," by I. M. Hall,
    # published Sept. 1975. Gives M with an error of less than 0.05% over the whole range with an
    # uncertainty in nu of less than 0.015 degrees.
    if method == 'composite':
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
        y_0     = (pran_angl/nu_inf)**(2/3)

        mach_num = (1 + d_1*y_0 + d_2*y_0**2 + d_3*y_0**3)/(1 + e_1*y_0 + e_2*y_0**2)

        return mach_num

    # Traditional root finding technique using the Newton-Raphson method
    if method == 'newton':
        def func(mach_num):
            return math.sqrt((gamma + 1)/(gamma - 1)) * \
                   math.atan(math.sqrt((mach_num**2 - 1) * (gamma - 1)/(gamma + 1))) - \
                   math.atan(math.sqrt(mach_num**2 - 1)) - pran_angl

        def dfunc(mach_num):
            return (math.sqrt(mach_num**2 - 1))/(mach_num + (gamma - 1)/2*mach_num**3)

        # Initial guess for Mach number
        # TODO: find a better initial guess for the Mach number based on gamma and the angle
        mach_0  = 2

        mach_num, _ = newton_raphson(func, dfunc, mach_0)

        return mach_num

    raise ValueError('Please enter either newton or composite.')

def inv_area_ratio(gamma: float, area_ratio: float, flow_type: str) -> float:
    '''
    _summary_

    Args:
        gamma (float): _description_
        mach_num (float): _description_
        flow_type (str): _description_

    Returns:
        float: _description_
    '''

    # https://www.grc.nasa.gov/www/winddocs/utilities/b4wind_guide/mach.html

    p_1 = 2 / (gamma + 1)
    q_1 = 1 - p_1
    e_1 = 1 / q_1

    if flow_type == 'subsonic':
        r_1 = area_ratio**2
        a_1 = p_1**(1 / q_1)
        r_2 = (r_1 - 1) / (2 * a_1)
        x_1 = 1 / ((1 + r_2) + math.sqrt(r_2 * (r_2 + 2)))

        def func_sub(x_1):
            return (p_1 + q_1 * x_1)**e_1 - r_1 * x_1

        def dfunc_sub(x_1):
            return (p_1 + q_1 * x_1)**(e_1 - 1) - r_1

        x_new, _ = newton_raphson(func_sub, dfunc_sub, x_1)

        return math.sqrt(x_new)

    if flow_type == 'supersonic':
        r_1 = area_ratio**(2 * q_1 / p_1)
        a_1 = q_1**(1 / p_1)
        r_2 = (r_1 - 1) / (2 * a_1)
        x_1 = 1 / ((1 + r_2) + math.sqrt(r_2 * (r_2 + 2)))

        def func_sup(x_1):
            return (q_1 + p_1 * x_1)**(1 / p_1) - r_1 * x_1

        def dfunc_sup(x_1):
            return (q_1 + p_1 * x_1)**(1 / p_1 - 1) - r_1

        x_new, _ = newton_raphson(func_sup, dfunc_sup, x_1)

        return 1 / math.sqrt(x_new)

    raise ValueError('Please enter either subsonic or supersonic.')
