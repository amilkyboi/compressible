# module tests
'''
Unit tests.
'''

import sys
import numpy as np
import pytest as pyt

sys.path.append("..")

import src.isentropic as isen # pylint: disable=import-error,wrong-import-position
import src.normal as norm     # pylint: disable=import-error,wrong-import-position

GAMMA:    float = 1.4
MACH_NUM: float = 2.0

def test_isentropic_relations():
    '''
    Testing isentropic relations.
    '''

    assert np.rad2deg(isen.ang(MACH_NUM))        == pyt.approx(29.9999999)
    assert np.rad2deg(isen.pma(GAMMA, MACH_NUM)) == pyt.approx(26.3797608)
    assert isen.pp0(GAMMA, MACH_NUM)             == pyt.approx(0.12780452)
    assert isen.rr0(GAMMA, MACH_NUM)             == pyt.approx(0.23004814)
    assert isen.tt0(GAMMA, MACH_NUM)             == pyt.approx(0.55555555)
    assert isen.pps(GAMMA, MACH_NUM)             == pyt.approx(0.24192491)
    assert isen.rrs(GAMMA, MACH_NUM)             == pyt.approx(0.36288736)
    assert isen.tts(GAMMA, MACH_NUM)             == pyt.approx(0.66666666)
    assert isen.aas(GAMMA, MACH_NUM)             == pyt.approx(1.68749999)

def test_normal_shock_relations():
    '''
    Testing normal shock relations.
    '''

    assert norm.ma2(GAMMA, MACH_NUM)    == pyt.approx(0.57735026)
    assert norm.p02p01(GAMMA, MACH_NUM) == pyt.approx(0.72087386)
    assert norm.p1p02(GAMMA, MACH_NUM)  == pyt.approx(0.17729110)
    assert norm.p2p1(GAMMA, MACH_NUM)   == pyt.approx(4.5)
    assert norm.r2r1(GAMMA, MACH_NUM)   == pyt.approx(2.66666666)
    assert norm.t2t1(GAMMA, MACH_NUM)   == pyt.approx(1.6875)
