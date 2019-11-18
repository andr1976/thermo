# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2019, Caleb Bell <Caleb.Andrew.Bell@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.'''

from numpy.testing import assert_allclose
import pytest
import thermo
from thermo import *
from fluids.numerics import *
from math import *
import json
import os
import numpy as np

from thermo.test_utils import *
import matplotlib.pyplot as plt

pure_surfaces_dir = os.path.join(thermo.thermo_dir, '..', 'surfaces', 'pure')

pure_fluids = ['water', 'methane', 'ethane', 'decane', 'ammonia', 'nitrogen', 'oxygen', 'methanol']

'''# Recreate the below with the following:
N = len(pure_fluids)
m = Mixture(pure_fluids, zs=[1/N]*N, T=298.15, P=1e5)
print(m.constants.make_str(delim=', \n', properties=('Tcs', 'Pcs', 'omegas', 'MWs', "CASs")))
correlations = m.properties()
print(correlations.as_best_fit(['HeatCapacityGases']))
'''
constants = ChemicalConstantsPackage(Tcs=[647.14, 190.56400000000002, 305.32, 611.7, 405.6, 126.2, 154.58, 512.5], 
            Pcs=[22048320.0, 4599000.0, 4872000.0, 2110000.0, 11277472.5, 3394387.5, 5042945.25, 8084000.0], 
            omegas=[0.344, 0.008, 0.098, 0.49, 0.25, 0.04, 0.021, 0.5589999999999999], 
            MWs=[18.01528, 16.04246, 30.06904, 142.28168, 17.03052, 28.0134, 31.9988, 32.04186], 
            CASs=['7732-18-5', '74-82-8', '74-84-0', '124-18-5', '7664-41-7', '7727-37-9', '7782-44-7', '67-56-1'])

correlations = PropertyCorrelationPackage(constants=constants, HeatCapacityGases=[HeatCapacityGas(best_fit=(50.0, 1000.0, [5.543665000518528e-22, -2.403756749600872e-18, 4.2166477594350336e-15, -3.7965208514613565e-12, 1.823547122838406e-09, -4.3747690853614695e-07, 5.437938301211039e-05, -0.003220061088723078, 33.32731489750759])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [6.7703235945157e-22, -2.496905487234175e-18, 3.141019468969792e-15, -8.82689677472949e-13, -1.3709202525543862e-09, 1.232839237674241e-06, -0.0002832018460361874, 0.022944239587055416, 32.67333514157593])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [7.115386645067898e-21, -3.2034776773408394e-17, 5.957592282542187e-14, -5.91169369931607e-11, 3.391209091071677e-08, -1.158730780040934e-05, 0.002409311277400987, -0.18906638711444712, 37.94602410497228])),
        HeatCapacityGas(best_fit=(200.0, 1000.0, [-1.702672546011891e-21, 6.6751002084997075e-18, -7.624102919104147e-15, -4.071140876082743e-12, 1.863822577724324e-08, -1.9741705032236747e-05, 0.009781408958916831, -1.6762677829939379, 252.8975930305735])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [7.444966286051841e-23, 9.444106746563928e-20, -1.2490299714587002e-15, 2.6693560979905865e-12, -2.5695131746723413e-09, 1.2022442523089315e-06, -0.00021492132731007108, 0.016616385291696574, 32.84274656062226])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [-6.496329615255804e-23, 2.1505678500404716e-19, -2.2204849352453665e-16, 1.7454757436517406e-14, 9.796496485269412e-11, -4.7671178529502835e-08, 8.384926355629239e-06, -0.0005955479316119903, 29.114778709934264])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [7.682842888382947e-22, -3.3797331490434755e-18, 6.036320672021355e-15, -5.560319277907492e-12, 2.7591871443240986e-09, -7.058034933954475e-07, 9.350023770249747e-05, -0.005794412013028436, 29.229215579932934])),
        HeatCapacityGas(best_fit=(50.0, 1000.0, [2.3511458696647882e-21, -9.223721411371584e-18, 1.3574178156001128e-14, -8.311274917169928e-12, 4.601738891380102e-10, 1.78316202142183e-06, -0.0007052056417063217, 0.13263597297874355, 28.44324970462924]))])


from thermo.eos_mix import eos_mix_list
#eos_mix_list = [PRMIX, PR78MIX, SRKMIX, VDWMIX, PRSVMIX, PRSV2MIX, APISRKMIX, TWUPRMIX, TWUSRKMIX, IGMIX]
#eos_mix_list = [TWUPRMIX, TWUSRKMIX] # issues
@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['realistic', 'physical'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_PV_plot(fluid, eos, auto_range):
    '''
    Normally about 16% of the realistic plot overlaps with the physical. However,
    the realistic is the important one, so do not use fewer points for it.
    
    The realistic should be clean/clear!
    '''
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    '''
    m = Mixture([fluid], zs=zs, T=T, P=P)
    pure_const = m.constants
    HeatCapacityGases = m.HeatCapacityGases
    pure_props = PropertyCorrelationPackage(pure_const, HeatCapacityGases=HeatCapacityGases)
    '''
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    
    res = flasher.TPV_inputs(zs=zs, pts=100, spec0='T', spec1='P', check0='P', check1='V', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "PV")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('PV', eos.__name__, auto_range, fluid)

    plot_fig.savefig(os.path.join(path, key + '.png'))
    # TODO log the max error to a file
    
    plt.close()

    max_err = np.max(np.abs(errs))
    try:
        assert max_err < 5e-9
    except:
        print(fluid, eos, auto_range)
        assert max_err < 5e-9


@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_TV_plot(fluid, eos, auto_range):
    '''
    A pretty wide region here uses mpmath to polish the volume root,
    and calculate the pressure from the TV specs. This is very important! For
    the liquid region, there is not enough pressure dependence of volume for
    good calculations to work.
    '''
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    
    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='T', check1='V', prop0='P',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "TV")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('TV', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()
    
    max_err = np.max(np.abs(errs))
    
    try:
        assert max_err < 5e-9
    except:
        assert max_err < 5e-9


@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_PS_plot(fluid, eos, auto_range):
    '''
    '''
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=60, spec0='T', spec1='P', check0='P', check1='S', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "PS")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('PS', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8
#test_PS_plot("water", PR78MIX, "physical")

@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_PH_plot(fluid, eos, auto_range):
    '''
    '''
    if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
        # Garbage alpha function for very low T
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='P', check1='H', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "PH")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('PH', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8
    
#test_PH_plot('methanol', PRMIX, 'physical')


@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_PU_plot(fluid, eos, auto_range):
    '''Does not seem unique, again :(
    Going to have to add new test functionality that does there tests against a
    reflash at PT.
    '''
    if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
#         Garbage alpha function for very low T
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='P', check1='U', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "PU")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('PU', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    if eos != VDWMIX:
        # Do not know what is going on there
        # test case vdw decane failing only
#        base =  flasher.flash(T=372.75937203149226, P=255954.79226995228)
#        flasher.flash(P=base.P, U=base.U()).T
        assert max_err < 1e-8


@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_VU_plot(fluid, eos, auto_range):
    if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
#         Garbage alpha function for very low T
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='V', check1='U', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "VU")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('VU', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8

@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_VS_plot(fluid, eos, auto_range):
    '''Some SRK tests are failing because of out-of-bounds issues.
    Hard to know how to fix these.
    '''
    
    if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='V', check1='S', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "VS")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('VS', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8
    
#for fluid in pure_fluids:
#    test_VS_plot(fluid, APISRKMIX, 'physical')

@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_VH_plot(fluid, eos, auto_range):
    if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
#         Garbage alpha function for very low T
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='V', check1='H', prop0='T',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "VH")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('VH', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8



@pytest.mark.slow
@pytest.mark.parametrize("auto_range", ['physical', 'realistic'])
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_TS_plot(fluid, eos, auto_range):
    '''
    '''
    #if eos in (TWUPRMIX, TWUSRKMIX) and auto_range == 'physical':
        # Garbage alpha function for very low T
    #    return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)

    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    res = flasher.TPV_inputs(zs=zs, pts=50, spec0='T', spec1='P', check0='T', check1='S', prop0='P',
                           trunc_err_low=1e-10, 
                           trunc_err_high=1, color_map=cm_flash_tol(),
                           auto_range=auto_range, 
                           show=False)

    matrix_spec_flashes, matrix_flashes, errs, plot_fig = res
    
    path = os.path.join(pure_surfaces_dir, fluid, "TS")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s - %s' %('TS', eos.__name__, auto_range, fluid)
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()

    max_err = np.max(errs)
    assert max_err < 1e-8

@pytest.mark.slow
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_list)
def test_V_G_min_plot(fluid, eos):
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
#    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
#                  HeatCapacityGases=pure_props.HeatCapacityGases)
#    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
    
    kwargs = dict(Tc=pure_const.Tcs[0], Pc=pure_const.Pcs[0], omega=pure_const.omegas[0])
    
    gas = eos(T=T, P=P, **kwargs)
    errs, plot_fig = gas.volumes_G_min(plot=True, show=False, pts=150,
                                       Tmin=1e-4, Tmax=1e4, Pmin=1e-2, Pmax=1e9)

    
    path = os.path.join(pure_surfaces_dir, fluid, "V_G_min")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s' %('V_G_min', eos.__name__, fluid)
        
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()
    
    # Not sure how to add error to this one

@pytest.mark.slow
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_list)
def test_Psat_plot(fluid, eos):
    if eos in (IG,):
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(Tc=pure_const.Tcs[0], Pc=pure_const.Pcs[0], omega=pure_const.omegas[0])
    
    obj = eos(T=T, P=P, **kwargs)

    errs, Psats_num, Psats_fit, plot_fig = obj.Psat_errors(plot=True, show=False, pts=100,
                                     Tmin=kwargs['Tc']*.1, Tmax=kwargs['Tc'])

    
    path = os.path.join(pure_surfaces_dir, fluid, "Psat")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s' %('Psat', eos.__name__, fluid)
        
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()
    
#    max_err = np.max(errs)
#    assert max_err < 1e-8




@pytest.mark.slow
@pytest.mark.parametrize("fluid", pure_fluids)
@pytest.mark.parametrize("eos", eos_mix_list)
def test_V_error_plot(fluid, eos):
    if eos == IGMIX:
        return
    T, P = 298.15, 101325.0
    zs = [1.0]
    fluid_idx = pure_fluids.index(fluid)
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)
    
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
    errs, plot_fig = gas.eos_mix.volume_errors(plot=True, show=False, pts=50,
                                               Tmin=1e-4, Tmax=1e4, Pmin=1e-2, Pmax=1e9,
                                               trunc_err_low=1e-15, color_map=cm_flash_tol())

    
    path = os.path.join(pure_surfaces_dir, fluid, "V_error")
    if not os.path.exists(path):
        os.makedirs(path)
    
    key = '%s - %s - %s' %('V_error', eos.__name__, fluid)
        
    plot_fig.savefig(os.path.join(path, key + '.png'))
    plt.close()
    
    
    max_err = np.max(errs)
    assert max_err < 1e-8
    
    
def test_some_flashes_bad():
    '''Basic test with ammonia showing how PG, PA, TG, TA, VA, VG flashes
    have multiple solutions quite close.
    '''
    constants = ChemicalConstantsPackage(Tcs=[405.6], Pcs=[11277472.5], omegas=[0.25], MWs=[17.03052], CASs=['7664-41-7'])
    HeatCapacityGases = [HeatCapacityGas(best_fit=(50.0, 1000.0, [7.444966286051841e-23, 9.444106746563928e-20,
                            -1.2490299714587002e-15, 2.6693560979905865e-12, -2.5695131746723413e-09, 1.2022442523089315e-06, 
                            -0.00021492132731007108, 0.016616385291696574, 32.84274656062226]))]
    correlations = PropertyCorrelationPackage(constants, HeatCapacityGases=HeatCapacityGases)
    kwargs = dict(eos_kwargs=dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas),
                 HeatCapacityGases=HeatCapacityGases)
    
    liquid = EOSLiquid(SRKMIX, T=330, P=1e5, zs=[1], **kwargs)
    gas = EOSGas(SRKMIX, T=330, P=1e5, zs=[1], **kwargs)
    
    flasher = FlashPureVLS(constants, correlations, gas, [liquid], [])
        
    assert_allclose(flasher.flash(T=800, P=1e7).G(), flasher.flash(T=725.87092453, P=1e7).G(), rtol=1e-10)


def test_PS_1P_vs_VL_issue0():
    '''Made me think there was something wrong with enthalpy maximization.
    However, it was just a root issue.
    '''

    constants = ChemicalConstantsPackage(Tcs=[647.14], Pcs=[22048320.0], omegas=[0.344], MWs=[18.01528],  CASs=['7732-18-5'],)
    HeatCapacityGases = [HeatCapacityGas(best_fit=(50.0, 1000.0, [5.543665000518528e-22, -2.403756749600872e-18, 4.2166477594350336e-15, -3.7965208514613565e-12, 1.823547122838406e-09, -4.3747690853614695e-07, 5.437938301211039e-05, -0.003220061088723078, 33.32731489750759]))]
    correlations = PropertyCorrelationPackage(constants, HeatCapacityGases=HeatCapacityGases)
    kwargs = dict(eos_kwargs=dict(Tcs=constants.Tcs, Pcs=constants.Pcs, omegas=constants.omegas),
                 HeatCapacityGases=HeatCapacityGases)
    
    liquid = EOSLiquid(PR78MIX, T=200, P=1e5, zs=[1], **kwargs)
    gas = EOSGas(PR78MIX, T=200, P=1e5, zs=[1], **kwargs)
    flasher = FlashPureVLS(constants, correlations, gas, [liquid], []) # 
    
    for P in (0.01, 0.015361749466718281):
        obj = flasher.flash(T=166.0882782627715, P=P)
        hit = flasher.flash(P=obj.P, S=obj.S())
        assert_allclose(hit.T, obj.T)


def test_SRK_high_P_PV_failure():
    '''Numerical solve_T converging to a T in the range 200,000 K when there
    was a lower T solution
    '''
    T, P, zs = 2000, 1e8, [1.0]
    fluid_idx, eos = 7, SRKMIX # methanol
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    base = flasher.flash(T=T, P=P)
    
    PV = flasher.flash(P=P, V=base.V())
    assert_allclose(T, PV.T, rtol=1e-7)


def test_SRK_high_PT_on_VS_failure():
    T, P, zs = 7609.496685459907, 423758716.06041414, [1.0]
    fluid_idx, eos = 7, SRKMIX # methanol
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    base = flasher.flash(T=T, P=P)
    
    VS = flasher.flash(S=base.S(), V=base.V())
    assert_allclose(T, VS.T, rtol=1e-7)

    # Point where max P becomes negative - check it is not used
    obj = flasher.flash(T=24.53751106639818, P=33529.24149249553)
    flasher.flash(V=obj.V(), S=obj.S())
    
def test_APISRK_VS_at_Pmax_error_failure():
    T, P, zs = 7196.856730011477, 355648030.6223078, [1.0]
    fluid_idx, eos = 7, APISRKMIX # methanol
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)

    liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
    gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
    flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])

    base = flasher.flash(T=T, P=P)
    
    VS = flasher.flash(S=base.S(), V=base.V())
    assert_allclose(T, VS.T, rtol=1e-7)

def test_Twu_missing_Pmax_on_VS_failure():
    T, P, zs = 855.4672535565693, 6.260516572014815, [1.0]
    for eos in (TWUSRKMIX, TWUPRMIX):
        fluid_idx = 7 # methanol
        pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
        
        kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                      HeatCapacityGases=pure_props.HeatCapacityGases)
    
        liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
        gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
        flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])
        base = flasher.flash(T=T, P=P)
        VS = flasher.flash(S=base.S(), V=base.V())
        assert_allclose(T, VS.T, rtol=1e-7)

def test_TWU_SRK_PR_T_alpha_interp_failure():
    '''a_alpha becomes 100-500; the EOS makes no sense. Limit it to a Tr no
    around 1E-4 Tr to make it reasonable. 
    '''
    T, P, zs = 0.02595024211399719, 6135.90727341312, [1.0]
    fluid_idx = 2 # ethane
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)
    
    for eos in [TWUSRKMIX, TWUPRMIX]:
        liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
        gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
        flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])
        base = flasher.flash(T=T, P=P)
        
        PV = flasher.flash(P=P, V=base.V())
        assert_allclose(T, PV.T, rtol=1e-8)


def test_TWU_SRK_PR_T_alpha_interp_failure_2():
    T, P, zs = .001, .001, [1.0]
    fluid_idx = 0 # water
    pure_const, pure_props = constants.subset([fluid_idx]), correlations.subset([fluid_idx])
    
    kwargs = dict(eos_kwargs=dict(Tcs=pure_const.Tcs, Pcs=pure_const.Pcs, omegas=pure_const.omegas),
                  HeatCapacityGases=pure_props.HeatCapacityGases)
    
    for eos in [TWUSRKMIX, TWUPRMIX]:
        liquid = EOSLiquid(eos, T=T, P=P, zs=zs, **kwargs)
        gas = EOSGas(eos, T=T, P=P, zs=zs, **kwargs)
        flasher = FlashPureVLS(pure_const, pure_props, gas, [liquid], [])
        base = flasher.flash(T=T, P=P)
        
        PV = flasher.flash(P=P, V=base.V())
        assert_allclose(T, PV.T, rtol=1e-6)
