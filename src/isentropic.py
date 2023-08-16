# module isentropic
'''
Computes flow relations assuming isentropic flow conditions.
'''

import math

# Calculated values

def ang(mach_num):
    '''
    Calculates the Mach angle in radians from the Mach number.
    '''
    return math.asin(1/mach_num)

def pma(gamma, mach_num):
    '''
    Calculates the Prandtl-Meyer angle using the Prandtl-Meyer function.
    '''
    return math.sqrt((gamma + 1)/(gamma - 1)) * \
           math.atan(math.sqrt((gamma - 1)/(gamma + 1) * (mach_num**2 - 1))) - \
           math.atan(math.sqrt(mach_num**2 - 1))

def pp0(gamma, mach_num):
    '''
    Calculates the total (stagnation) pressure ratio, p/p0.
    '''
    return (1 + (gamma - 1)/2 * mach_num**2)**(-gamma/(gamma - 1))

def p0ps(gamma):
    '''
    Calculates the total (stagnation) vs. the critical (sonic) pressure ratio, p0/p*.
    '''
    return (2/(gamma + 1))**(-gamma/(gamma - 1))

def pps(gamma, mach_num):
    '''
    Calculates the critical (sonic) pressure ratio, p/p*
    '''
    return pp0(gamma, mach_num)*p0ps(gamma)

def rr0(gamma, mach_num):
    '''
    Calculates the total (stagnation) density ratio, rho/rho0.
    '''
    return (1 + (gamma - 1)/2 * mach_num**2)**(-1/(gamma - 1))

def r0rs(gamma):
    '''
    Calculates the total (stagnation) vs. the critical (sonic) density ratio, rho0/rho*.
    '''
    return (2/(gamma + 1))**(-1/(gamma - 1))

def rrs(gamma, mach_num):
    '''
    Calculates the critical (sonic) density ratio, rho/rho*.
    '''
    return rr0(gamma, mach_num)*r0rs(gamma)

def tt0(gamma, mach_num):
    '''
    Calculates the total (stagnation) temperature ratio, T/T0.
    '''
    return (1 + (gamma - 1)/2 * mach_num**2)**-1

def t0ts(gamma):
    '''
    Calculates the total (stagnation) vs. the critical (sonic) temperature ratio, T0/T*.
    '''
    return (gamma + 1)/2

def tts(gamma, mach_num):
    '''
    Calculates the critical (sonic) temperature ratio, T/T*.
    '''
    return tt0(gamma, mach_num)*t0ts(gamma)

def aas(gamma, mach_num):
    '''
    Calculates the critical (sonic) area ratio, A/A*.
    '''
    return ((gamma + 1)/2)**(-(gamma + 1)/(2*(gamma - 1))) * \
           (1 + (gamma - 1)/2 * mach_num**2)**((gamma + 1)/(2*(gamma - 1))) * (1/mach_num)
