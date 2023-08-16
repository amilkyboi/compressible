# module oblique
'''
Computes flow relations through an oblique shock.
'''

import math

# Calculated values

def mach_angle(mach_num):
    '''
    Calculates the Mach angle in radians from the Mach number.
    '''
    return math.asin(1/mach_num)

def turn_angle(gamma, mach_num, wave_angle):
    '''
    Calculates the turn angle of the flow caused by the shock.
    '''
    return math.atan(2 * (1/math.tan(wave_angle)) * \
           (mach_num**2 * math.sin(wave_angle)**2 - 1)/(mach_num**2 * \
           (gamma + math.cos(2 * wave_angle)) + 2))
