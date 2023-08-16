# module normal
'''
Computes flow relations through a normal shock.
'''

import math

# Calculated values

def ma2(gamma, mach_num):
    '''
    Calculates the Mach number downstream of the shock, M2.
    '''
    return math.sqrt(((gamma - 1) * mach_num**2 + 2)/(2 * gamma * mach_num**2 - (gamma - 1)))

def p2p1(gamma, mach_num):
    '''
    Calculates the static pressure ratio across the shock, p2/p1.
    '''
    return (2*gamma * mach_num**2 - (gamma - 1))/(gamma + 1)

def p02p01(gamma, mach_num):
    '''
    Calculates the total (stagnation) pressure ratio across the shock, p02/p01.
    '''
    return (((gamma + 1) * mach_num**2)/((gamma - 1) * mach_num**2 + 2))**(gamma/(gamma - 1)) * \
           ((gamma + 1)/(2 * gamma * mach_num**2 - (gamma - 1)))**(1/(gamma - 1))

def p1p02(gamma, mach_num):
    '''
    Calculates the static vs. the total (stagnation) pressure ratio across the shock, p1/p02.
    '''
    return (((gamma + 1) * mach_num**2)/2)**(-gamma/(gamma - 1)) * \
           ((gamma + 1)/(2 * gamma * mach_num**2 - (gamma - 1)))**(-1/(gamma - 1))

def r2r1(gamma, mach_num):
    '''
    Calculates the static density ratio across the shock, rho2/rho1.
    '''
    return ((gamma + 1) * mach_num**2)/((gamma - 1) * mach_num**2 + 2)

def t2t1(gamma, mach_num):
    '''
    Calculates the static temperature ratio across the shock, T2/T1.
    '''
    return ((2 * gamma * mach_num**2 - (gamma - 1)) * ((gamma - 1) * mach_num**2 + 2)) / \
           ((gamma + 1)**2 * mach_num**2)

# Conversions

def p2p1_to_ma(gamma, sp_ratio):
    '''
    Converts static pressure ratio to Mach number.
    '''
    return math.sqrt((sp_ratio * (gamma + 1) + (gamma - 1)) / (2 * gamma))
