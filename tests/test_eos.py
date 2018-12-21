# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2016, 2017, 2018 Caleb Bell <Caleb.Andrew.Bell@gmail.com>

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
import numpy as np
import pytest
from thermo import eos
from thermo.eos import *
from thermo.utils import allclose_variable
from scipy.misc import derivative
from fluids.constants import R
from math import log, exp, sqrt


@pytest.mark.slow
@pytest.mark.sympy
def test_PR_with_sympy():
    # Test with hexane
    from sympy import Rational, symbols, sqrt, solve, diff, integrate, N

    P, T, V = symbols('P, T, V')
    Tc = Rational('507.6')
    Pc = 3025000
    omega = Rational('0.2975')
    
    X = (-1 + (6*sqrt(2)+8)**Rational(1,3) - (6*sqrt(2)-8)**Rational(1,3))/3
    c1 = (8*(5*X+1)/(49-37*X)) # 0.45724
    c2 = (X/(X+3)) # 0.07780
    
    
    R_sym = Rational(R)
    a = c1*R_sym**2*Tc**2/Pc
    b = c2*R_sym*Tc/Pc
    
    kappa = Rational('0.37464')+ Rational('1.54226')*omega - Rational('0.26992')*omega**2
    
    a_alpha = a*(1 + kappa*(1-sqrt(T/Tc)))**2
    PR_formula = R_sym*T/(V-b) - a_alpha/(V*(V+b)+b*(V-b)) - P
    
    
    
    # First test - volume, liquid
    
    T_l, P_l = 299, 1000000
    PR_obj_l = PR(T=T_l, P=P_l, Tc=507.6, Pc=3025000, omega=0.2975)
    solns = solve(PR_formula.subs({T: T_l, P:P_l}))
    solns = [N(i) for i in solns]
    V_l_sympy = float([i for i in solns if i.is_real][0])
    V_l_sympy = 0.00013022212513965863

    assert_allclose(PR_obj_l.V_l, V_l_sympy)

    def numeric_sub_l(expr):
        return float(expr.subs({T: T_l, P:P_l, V:PR_obj_l.V_l}))

    # First derivatives
    dP_dT = diff(PR_formula, T)
    assert_allclose(numeric_sub_l(dP_dT), PR_obj_l.dP_dT_l)

    dP_dV = diff(PR_formula, V)
    assert_allclose(numeric_sub_l(dP_dV), PR_obj_l.dP_dV_l)
    
    dV_dT = -diff(PR_formula, T)/diff(PR_formula, V)
    assert_allclose(numeric_sub_l(dV_dT), PR_obj_l.dV_dT_l)
    
    dV_dP = -dV_dT/diff(PR_formula, T)
    assert_allclose(numeric_sub_l(dV_dP), PR_obj_l.dV_dP_l)
    
    # Checks out with solve as well
    dT_dV = 1/dV_dT
    assert_allclose(numeric_sub_l(dT_dV), PR_obj_l.dT_dV_l)
    
    dT_dP = 1/dP_dT
    assert_allclose(numeric_sub_l(dT_dP), PR_obj_l.dT_dP_l)
    
    # Second derivatives of two variables, easy ones
    
    d2P_dTdV = diff(dP_dT, V)
    assert_allclose(numeric_sub_l(d2P_dTdV), PR_obj_l.d2P_dTdV_l)
    
    d2P_dTdV = diff(dP_dV, T)
    assert_allclose(numeric_sub_l(d2P_dTdV), PR_obj_l.d2P_dTdV_l)
    
    
    # Second derivatives of one variable, easy ones
    d2P_dT2 = diff(dP_dT, T)
    assert_allclose(numeric_sub_l(d2P_dT2), PR_obj_l.d2P_dT2_l)
    d2P_dT2_maple = -506.2012523140132
    assert_allclose(d2P_dT2_maple, PR_obj_l.d2P_dT2_l)

    d2P_dV2 = diff(dP_dV, V)
    assert_allclose(numeric_sub_l(d2P_dV2), PR_obj_l.d2P_dV2_l)
    d2P_dV2_maple = 4.4821628180979494e+17
    assert_allclose(d2P_dV2_maple, PR_obj_l.d2P_dV2_l)
        
    # Second derivatives of one variable, Hard ones - require a complicated identity
    d2V_dT2 = (-(d2P_dT2*dP_dV - dP_dT*d2P_dTdV)*dP_dV**-2
              +(d2P_dTdV*dP_dV - dP_dT*d2P_dV2)*dP_dV**-3*dP_dT)
    assert_allclose(numeric_sub_l(d2V_dT2), PR_obj_l.d2V_dT2_l)
    d2V_dT2_maple = 1.1688517647207985e-09
    assert_allclose(d2V_dT2_maple, PR_obj_l.d2V_dT2_l)
    
    d2V_dP2 = -d2P_dV2/dP_dV**3
    assert_allclose(numeric_sub_l(d2V_dP2), PR_obj_l.d2V_dP2_l)
    d2V_dP2_maple = 9.103364399605894e-21
    assert_allclose(d2V_dP2_maple, PR_obj_l.d2V_dP2_l)


    d2T_dP2 = -d2P_dT2*dP_dT**-3
    assert_allclose(numeric_sub_l(d2T_dP2), PR_obj_l.d2T_dP2_l)
    d2T_dP2_maple = 2.5646844439707823e-15
    assert_allclose(d2T_dP2_maple, PR_obj_l.d2T_dP2_l)
    
    d2T_dV2 = (-(d2P_dV2*dP_dT - dP_dV*d2P_dTdV)*dP_dT**-2
              +(d2P_dTdV*dP_dT - dP_dV*d2P_dT2)*dP_dT**-3*dP_dV)
    assert_allclose(numeric_sub_l(d2T_dV2), PR_obj_l.d2T_dV2_l)
    d2T_dV2_maple = -291578743623.6926
    assert_allclose(d2T_dV2_maple, PR_obj_l.d2T_dV2_l)
    
    
    # Second derivatives of two variable, Hard ones - require a complicated identity
    d2T_dPdV = -(d2P_dTdV*dP_dT - dP_dV*d2P_dT2)*dP_dT**-3
    assert_allclose(numeric_sub_l(d2T_dPdV), PR_obj_l.d2T_dPdV_l)
    d2T_dPdV_maple = 0.06994168125617044
    assert_allclose(d2T_dPdV_maple, PR_obj_l.d2T_dPdV_l)
    
    d2V_dPdT = -(d2P_dTdV*dP_dV - dP_dT*d2P_dV2)*dP_dV**-3
    assert_allclose(numeric_sub_l(d2V_dPdT), PR_obj_l.d2V_dPdT_l)
    d2V_dPdT_maple = -3.772509038556849e-15
    assert_allclose(d2V_dPdT_maple, PR_obj_l.d2V_dPdT_l)
    
    # Cv integral, real slow
    # The Cv integral is possible with a more general form, but not here
    # The S and H integrals don't work in Sympy at present

    
    
def test_PR_quick():
    # Test solution for molar volumes
    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [(0.00013022212513965863+0j), (0.001123631313468268+0.0012926967234386068j), (0.001123631313468268-0.0012926967234386068j)]
    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.801262003434438, -0.006647930535193546, 1.6930139095364687e-05]
    a_alphas_fast = eos.a_alpha_and_derivatives(299, quick=True)
    assert_allclose(a_alphas, a_alphas_fast)
    a_alphas_slow = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_slow)
    
    # PR back calculation for T
    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, V=0.00013022212513965863, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.00013022212513965863, quick=False)
    assert_allclose(T_slow, 299)
    
    
    diffs_1 = [582232.4757941114, -3665179372374.127, 1.5885511093471238e-07, -2.7283794281321846e-13, 6295044.54792763, 1.7175270043741416e-06]
    diffs_2 = [-506.2012523140132, 4.4821628180979494e+17, 1.1688517647207979e-09, 9.103364399605888e-21, -291578743623.6926, 2.5646844439707823e-15]
    diffs_mixed = [-3.7725090385568464e-15, -20523296734.825127, 0.06994168125617044]
    departures = [-31134.750843460362, -72.475619319576, 25.165386034971817]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
    
    
    
    
    # Test Cp_Dep, Cv_dep
    assert_allclose(eos.Cv_dep_l, 25.165386034971814)
    assert_allclose(eos.Cp_dep_l, 44.505614171906245)
    
    # Exception tests
    a = GCEOS()        
    with pytest.raises(Exception):
        a.a_alpha_and_derivatives(T=300)
        
    with pytest.raises(Exception):
        PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299)
    
    # Integration tests
    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    # One gas phase property
    assert 'g' == PR(Tc=507.6, Pc=3025000, omega=0.2975, T=499.,P=1E5).phase

    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    
    B = eos.b*eos.P/R/eos.T
    A = eos.a_alpha*eos.P/(R*eos.T)**2
    D = -eos.T*eos.da_alpha_dT
    
    V = eos.V_l
    Z = eos.P*V/(R*eos.T)

    # Compare against some known  in Walas [2] functions
    phi_walas =  exp(Z - 1 - log(Z - B) - A/(2*2**0.5*B)*log((Z+(sqrt(2)+1)*B)/(Z-(sqrt(2)-1)*B)))
    phi_l_expect = 0.022212524527244346
    assert_allclose(phi_l_expect, eos.phi_l)
    assert_allclose(phi_walas, eos.phi_l)
    
    # The formula given in [2]_ must be incorrect!
#    S_dep_walas =  R*(-log(Z - B) + B*D/(2*2**0.5*A*eos.a_alpha)*log((Z+(sqrt(2)+1)*B)/(Z-(sqrt(2)-1)*B)))
#    S_dep_expect = -72.47559475426013
#    assert_allclose(-S_dep_walas, S_dep_expect)
#    assert_allclose(S_dep_expect, eos.S_dep_l)
    
    H_dep_walas = R*eos.T*(1 - Z + A/(2*2**0.5*B)*(1 + D/eos.a_alpha)*log((Z+(sqrt(2)+1)*B)/(Z-(sqrt(2)-1)*B)))
    H_dep_expect = -31134.750843460355
    assert_allclose(-H_dep_walas, H_dep_expect)
    assert_allclose(H_dep_expect, eos.H_dep_l)
    
    # Author's original H_dep, in [1]
    H_dep_orig = R*eos.T*(Z-1) + (eos.T*eos.da_alpha_dT-eos.a_alpha)/(2*2**0.5*eos.b)*log((Z+2.44*B)/(Z-0.414*B))
    assert_allclose(H_dep_orig, H_dep_expect, rtol=5E-3)
    
    # Author's correlation, with the correct constants this time
    H_dep_orig = R*eos.T*(Z-1) + (eos.T*eos.da_alpha_dT-eos.a_alpha)/(2*2**0.5*eos.b)*log((Z+(sqrt(2)+1)*B)/(Z-(sqrt(2)-1)*B))
    assert_allclose(H_dep_orig, H_dep_expect)
    
    # Test against Preos.xlsx
    # chethermo (Elliott, Richard and Lira, Carl T. - 2012 - Introductory Chemical Engineering Thermodynamics)
    # Propane
    e = PR(Tc=369.8, Pc=4.249E6, omega=0.152, T=298, P=1E5)
    assert_allclose(e.V_g, 0.024366034151169353)
    assert_allclose(e.V_l, 8.681724253858589e-05)
    
    
    # The following are imprecise as the approximate constants 2.414 etc were
    # used in chetherm
    assert_allclose(e.fugacity_g, 98364.041542871, rtol=1E-5)
    # not sure the problem with precision with the liquid
    assert_allclose(e.fugacity_l, 781433.379991859, rtol=1E-2)
    
    assert_allclose(e.H_dep_g, -111.99060081493053)
    assert_allclose(e.H_dep_l, -16112.7239108382, rtol=1E-5)

    assert_allclose(e.U_dep_g, -70.88415572220038)
    assert_allclose(e.U_dep_l, -13643.6966117489, rtol=1E-5)
    
    assert_allclose(e.S_dep_g, -0.23863903817819482)
    assert_allclose(e.S_dep_l, -71.158231517264, rtol=1E-6)
    
    # Volume solutions vs
    # Fallibility of analytic roots of cubic equations of state in low temperature region
    Tc = 464.80
    Pc = 35.60E5
    omega = 0.237
    # Props said to be from Reid et al
    
    b = PR(T=114.93, P=5.7E-6, Tc=Tc, Pc=Pc, omega=omega)
    V1, V2, V3 = b.raw_volumes
    assert_allclose(V3.real, 1.6764E8, rtol=1E-3)
    # Other two roots don't match
    
    # Example 05.11 Liquid Density using the Peng-Robinson EOS in Chemical Thermodynamics for Process Simulation
    V_l = PR(T=353.85, P=101325, Tc=553.60, Pc=40.750E5, omega=.2092).V_l
    assert_allclose(V_l, 0.00011087, atol=1e-8)
    # Matches to rounding
    
    
def test_PR_second_partial_derivative_shims():
    # Check the shims for the multi variate derivatives
    T = 400
    P = 1E6
    crit_params = {'Tc': 507.6, 'Pc': 3025000.0, 'omega': 0.2975}
    eos = PR(T=T, P=P, **crit_params)

    assert_allclose(1.0/eos.V_l, eos.rho_l)
    assert_allclose(1.0/eos.V_g, eos.rho_g)

    assert_allclose(eos.d2V_dTdP_l, eos.d2V_dPdT_l)
    assert_allclose(eos.d2V_dTdP_g, eos.d2V_dPdT_g)
    
    assert_allclose(eos.d2P_dVdT_l, eos.d2P_dTdV_l)
    assert_allclose(eos.d2P_dVdT_g, eos.d2P_dTdV_g)
    
    assert_allclose(eos.d2T_dVdP_l, eos.d2T_dPdV_l)
    assert_allclose(eos.d2T_dVdP_g, eos.d2T_dPdV_g)
    
    
def test_PR_density_derivatives():
    '''Sympy expressions:
        
    >>> f = 1/x
    >>> f
    1/x
    >>> diff(g(x), x)/diff(f, x)
    -x**2*Derivative(g(x), x)
    >>> diff(diff(g(x), x)/diff(f, x), x)/diff(f, x)
    -x**2*(-x**2*Derivative(g(x), x, x) - 2*x*Derivative(g(x), x))
    
    
    >>> diff(1/f(x), x)
    -Derivative(f(x), x)/f(x)**2
    >>> diff(diff(1/f(x), x), x)
    -Derivative(f(x), x, x)/f(x)**2 + 2*Derivative(f(x), x)**2/f(x)**3
    
    
    >>> diff(diff(1/f(x, y), x), y)
    -Derivative(f(x, y), x, y)/f(x, y)**2 + 2*Derivative(f(x, y), x)*Derivative(f(x, y), y)/f(x, y)**3
    '''
    # Test solution for molar volumes
    T = 400
    P = 1E6
    crit_params = {'Tc': 507.6, 'Pc': 3025000.0, 'omega': 0.2975}
    eos = PR(T=T, P=P, **crit_params)
    
    assert_allclose(eos.dP_drho_l, 16717.849183154118)
    assert_allclose(eos.dP_drho_g, 1086.6585648335506)

    assert_allclose(eos.drho_dP_g, 0.0009202522598744487)
    assert_allclose(eos.drho_dP_l, 5.981630705268346e-05)
    
    V = 'V_g'
    def d_rho_dP(P):
        return 1/getattr(PR(T=T, P=P, **crit_params), V)
    assert_allclose(eos.drho_dP_g, derivative(d_rho_dP, P, order=3))
    V = 'V_l'
    assert_allclose(eos.drho_dP_l, derivative(d_rho_dP, P), rtol=1e-5)
    
    # f = 1/x
    # >>> diff(diff(g(x), x)/diff(f, x), x)/diff(f, x)
    # -x**2*(-x**2*Derivative(g(x), x, x) - 2*x*Derivative(g(x), x))
    assert_allclose(eos.d2P_drho2_l, 22.670941865204274)
    assert_allclose(eos.d2P_drho2_g, -4.025199354171817)
    
    # Numerical tests
    assert_allclose(eos.d2rho_dP2_l, -4.852084485170919e-12)
    assert_allclose(eos.d2rho_dP2_g, 3.136953435966285e-09)
    V = 'V_g'
    assert_allclose(derivative(d_rho_dP, 1e6, n=2, order=11, dx=100), 3.136954499224254e-09, rtol=1e-3)
    V = 'V_l'
    assert_allclose(derivative(d_rho_dP, 1e6, n=2, order=11, dx=100), -4.852086129765671e-12, rtol=1e-3)


    # dT_drho tests - analytical
    assert_allclose(eos.dT_drho_l, -0.05794715601744427)  
    assert_allclose(eos.dT_drho_g, -0.2115805039516506)
    assert_allclose(eos.d2T_drho2_l, -2.7171270001507268e-05)
    assert_allclose(eos.d2T_drho2_g, 0.0019160984645184406)
    
    def dT_drho(rho):
        return PR(V=1.0/rho, P=P, **crit_params).T

    ans_numeric = derivative(dT_drho, 1/eos.V_l, n=1, dx=1e-2)
    assert_allclose(eos.dT_drho_l, ans_numeric, rtol=1e-5)   
    
    ans_numeric = derivative(dT_drho, 1/eos.V_g, n=1, dx=1e-2)
    assert_allclose(eos.dT_drho_g, ans_numeric)
    
    ans_numeric = derivative(dT_drho, 1/eos.V_l, n=2, dx=1, order=21)
    assert_allclose(eos.d2T_drho2_l, ans_numeric, rtol=1e-5)
    
    ans_numeric = derivative(dT_drho, 1/eos.V_g, n=2, dx=1, order=3)
    assert_allclose(eos.d2T_drho2_g, ans_numeric, rtol=1e-5)

    # drho_dT tests - analytical
    def drho_dT(T, V='V_l'):
        return 1.0/getattr(PR(T=T, P=P, **crit_params), V)
    
    assert_allclose(eos.drho_dT_g, -4.726333387638189)
    assert_allclose(eos.drho_dT_l, -17.25710231057694)
                    
    ans_numeric = derivative(drho_dT, eos.T, n=1, dx=1e-2, args=['V_l'])
    assert_allclose(ans_numeric, eos.drho_dT_l)
    
    ans_numeric = derivative(drho_dT, eos.T, n=1, dx=1e-2, args=['V_g'])
    assert_allclose(ans_numeric, eos.drho_dT_g)


    assert_allclose(eos.d2rho_dT2_l, -0.13964119596352564)
    assert_allclose(eos.d2rho_dT2_g, 0.20229767021600575)

    ans_numeric = derivative(drho_dT, eos.T, n=2, dx=3e-2, args=['V_l'])
    assert_allclose(eos.d2rho_dT2_l, ans_numeric, rtol=1e-6)
    ans_numeric = derivative(drho_dT, eos.T, n=2, dx=1e-2, args=['V_g'])
    assert_allclose(eos.d2rho_dT2_g, ans_numeric, rtol=1e-6)

    # Sympy and numerical derivative quite agree!
    # d2P_drho_dT
    def dP_drho(rho, T):
        return PR(T=T, V=1/rho, **crit_params).P
    
    def d2P_drhodT(T, rho):
        def to_diff(T):
            return derivative(dP_drho, rho, n=1, dx=1e-2, args=[T], order=3)
        return derivative(to_diff, T, n=1, dx=.1, order=3)
    
    ans_numerical = d2P_drhodT(eos.T, 1/eos.V_l)
    assert_allclose(eos.d2P_dTdrho_l, 121.15490035272644)
    assert_allclose(eos.d2P_dTdrho_l, ans_numerical)
    
    ans_numerical = d2P_drhodT(eos.T, 1/eos.V_g)
    assert_allclose(eos.d2P_dTdrho_g, 13.513868196361557)
    assert_allclose(eos.d2P_dTdrho_g, ans_numerical)

    # Numerical derivatives agree - d2T_dPdrho_g
    def dT_drho(rho, P):
        return PR(P=P, V=1.0/rho, **crit_params).T
    
    def d2T_drhodP(P, rho):
        def to_diff(P):
            return derivative(dT_drho, rho, n=1, dx=.1, args=[P], order=11)
        return derivative(to_diff, P, n=1, dx=100, order=11)
    
    
    ans_numerical = d2T_drhodP(eos.P, 1/eos.V_l)
    assert_allclose(ans_numerical, eos.d2T_dPdrho_l, rtol=2e-3)
    assert_allclose(eos.d2T_dPdrho_l, -1.6195726310475797e-09)
    
    ans_numerical = d2T_drhodP(eos.P, 1/eos.V_g)
    assert_allclose(ans_numerical, eos.d2T_dPdrho_g)
    assert_allclose(eos.d2T_dPdrho_g, -5.29734819740022e-07)

    # drho_DT_dP derivatives
    def drho_dT(T, P, V='V_l'):
        return 1.0/getattr(PR(T=T, P=P, **crit_params), V)
    
    def drho_dT_dP(T, P, V='V_l'):
        def to_dP(P):
            return derivative(drho_dT, T, n=1, dx=10e-1, args=[P, V], order=7)
        return derivative(to_dP, P, n=1, dx=10, order=5)
    
    
    ans_numerical = drho_dT_dP(eos.T, eos.P, 'V_l')
    assert_allclose(9.66343207820545e-07, eos.d2rho_dPdT_l)
    assert_allclose(ans_numerical, eos.d2rho_dPdT_l, rtol=1e-5)
    
    ans_numerical = drho_dT_dP(eos.T, eos.P, 'V_g')
    assert_allclose(ans_numerical, eos.d2rho_dPdT_g, rtol=1e-6)
    assert_allclose(-2.755552405262765e-05, eos.d2rho_dPdT_g)


def test_PR_Psat():
    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Cs_PR = [-3.3466262, -9.9145207E-02, 1.015969390, -1.032780679, 
             0.2904927517, 1.64073501E-02, -9.67894565E-03, 1.74161549E-03, 
             -1.56974110E-04, 5.87311295E-06]
    def Psat(T, Tc, Pc, omega):
        Tr = T/Tc
        e = PR(Tc=Tc, Pc=Pc, omega=omega, T=T, P=1E5)
        alpha = e.a_alpha/e.a
        tot = 0
        for k, Ck in enumerate(Cs_PR[0:4]):
            tot += Ck*(alpha/Tr-1)**((k+2)/2.)
        for k, Ck in enumerate(Cs_PR[4:]):
            tot += Ck*(alpha/Tr-1)**(k+3)
        P = exp(tot)*Tr*Pc
        return P
    
    Ts = np.linspace(507.6*0.32, 504)
    Psats_lit = [Psat(T, Tc=507.6, Pc=3025000, omega=0.2975) for T in Ts]
    Psats_eos = [eos.Psat(T) for T in Ts]
    assert_allclose(Psats_lit, Psats_eos, rtol=1.5E-3)
    
    # Check that fugacities exist for both phases    
    for T, P in zip(Ts, Psats_eos):
        eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=T, P=P)
        assert_allclose(eos.fugacity_l, eos.fugacity_g, rtol=2E-3)
        


def test_PR78():
    eos = PR78(Tc=632, Pc=5350000, omega=0.734, T=299., P=1E6)
    three_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    expect_props = [8.35196289693885e-05, -63764.67109328409, -130.7371532254518]
    assert_allclose(three_props, expect_props)
    
    # Test the results are identical to PR or lower things
    eos = PR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    PR_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    eos = PR78(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    PR78_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    assert_allclose(PR_props, PR78_props)


def test_PRSV():
    eos = PRSV(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6, kappa1=0.05104)
    three_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    expect_props = [0.0001301269135543934, -31698.926746698795, -74.16751538228138]
    assert_allclose(three_props, expect_props)
    
    # Test of a_alphas
    a_alphas = [3.812985698311453, -0.006976903474851659, 2.0026560811043733e-05]
    
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    
    a_alphas_fast = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_fast)
    
    # PR back calculation for T
    eos = PRSV(Tc=507.6, Pc=3025000, omega=0.2975, V=0.0001301269135543934, P=1E6, kappa1=0.05104)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.0001301269135543934, quick=False)
    assert_allclose(T_slow, 299)
    
    
    # Test the bool to control its behavior
    eos = PRSV(Tc=507.6, Pc=3025000, omega=0.2975, T=406.08, P=1E6, kappa1=0.05104)
    assert_allclose(eos.kappa, 0.7977689278061457)
    eos.kappa1_Tr_limit = True
    eos.__init__(Tc=507.6, Pc=3025000, omega=0.2975, T=406.08, P=1E6, kappa1=0.05104)
    assert_allclose(eos.kappa, 0.8074380841890093)
    
    # Test the limit is not enforced while under Tr =0.7
    eos = PRSV(Tc=507.6, Pc=3025000, omega=0.2975, T=304.56, P=1E6, kappa1=0.05104)
    assert_allclose(eos.kappa, 0.8164956255888178)
    eos.kappa1_Tr_limit = True
    eos.__init__(Tc=507.6, Pc=3025000, omega=0.2975, T=304.56, P=1E6, kappa1=0.05104)
    assert_allclose(eos.kappa, 0.8164956255888178)

    with pytest.raises(Exception):
        PRSV(Tc=507.6, Pc=3025000, omega=0.2975, P=1E6, kappa1=0.05104)

def test_PRSV2():
    eos = PRSV2(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6, kappa1=0.05104, kappa2=0.8634, kappa3=0.460)
    three_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    expect_props = [0.00013018825759153257, -31496.184168729033, -73.6152829631142]
    assert_allclose(three_props, expect_props)
    
    # Test of PRSV2 a_alphas
    a_alphas = [3.80542021117275, -0.006873163375791913, 2.3078023705053787e-05]
    
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    a_alphas_fast = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_fast)
    
    # PSRV2 back calculation for T
    eos = PRSV2(Tc=507.6, Pc=3025000, omega=0.2975, V=0.00013018825759153257, P=1E6, kappa1=0.05104, kappa2=0.8634, kappa3=0.460)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.00013018825759153257, quick=False)
    assert_allclose(T_slow, 299)

    # Check this is the same as PRSV
    eos = PRSV(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6, kappa1=0.05104)
    three_props_PRSV = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    eos = PRSV2(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6, kappa1=0.05104)
    three_props_PRSV2 = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    assert_allclose(three_props_PRSV, three_props_PRSV2)
    
    with pytest.raises(Exception):
        PRSV2(Tc=507.6, Pc=3025000, omega=0.2975, T=299.) 


def test_VDW():
    eos = VDW(Tc=507.6, Pc=3025000, T=299., P=1E6)
    three_props = [eos.V_l, eos.H_dep_l, eos.S_dep_l]
    expect_props = [0.00022332985608164609, -13385.727374687076, -32.65923125080434]
    assert_allclose(three_props, expect_props)
    
    # Test of a_alphas
    a_alphas = [2.4841053385218554, 0, 0]
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    
    # Back calculation for P
    eos = VDW(Tc=507.6, Pc=3025000, T=299, V=0.00022332985608164609)
    assert_allclose(eos.P, 1E6)
    
    # Back calculation for T
    eos = VDW(Tc=507.6, Pc=3025000, P=1E6, V=0.00022332985608164609)
    assert_allclose(eos.T, 299)

    with pytest.raises(Exception):
        VDW(Tc=507.6, Pc=3025000, P=1E6)


def test_VDW_Psat():
    eos = VDW(Tc=507.6, Pc=3025000,  T=299., P=1E6)
    Cs_VDW = [-2.9959015, -4.281688E-2, 0.47692435, -0.35939335, -2.7490208E-3,
              4.4205329E-2, -1.18597319E-2, 1.74962842E-3, -1.41793758E-4, 
              4.93570180E-6]
        
    def Psat(T, Tc, Pc, omega):
        Tr = T/Tc
        e = VDW(Tc=Tc, Pc=Pc, T=T, P=1E5)
        alpha = e.a_alpha/e.a
        tot = 0
        for k, Ck in enumerate(Cs_VDW[0:4]):
            tot += Ck*(alpha/Tr-1)**((k+2)/2.)
        for k, Ck in enumerate(Cs_VDW[4:]):
            tot += Ck*(alpha/Tr-1)**(k+3)
        P = exp(tot)*Tr*Pc
        return P
    
    Ts = np.linspace(507.6*.32, 506)
    Psats_lit = [Psat(T, Tc=507.6, Pc=3025000, omega=0.2975) for T in Ts]
    Psats_eos = [eos.Psat(T) for T in Ts]
    assert_allclose(Psats_lit, Psats_eos, rtol=2E-5)
    
    # Check that fugacities exist for both phases    
    for T, P in zip(Ts, Psats_eos):
        eos = VDW(Tc=507.6, Pc=3025000, T=T, P=P)
        assert_allclose(eos.fugacity_l, eos.fugacity_g, rtol=1E-6)

    
def test_RK_quick():
    # Test solution for molar volumes
    eos = RK(Tc=507.6, Pc=3025000, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [(0.00015189346878119082+0j), (0.0011670654270233137+0.001117116441729614j), (0.0011670654270233137-0.001117116441729614j)]
    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.279649770989796, -0.005484364165534776, 2.7513532603017274e-05]
    
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    
    # PR back calculation for T
    eos = RK(Tc=507.6, Pc=3025000,  V=0.00015189346878119082, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.00015189346878119082, quick=False)
    assert_allclose(T_slow, 299)
    
    
    diffs_1 = [400451.91036588483, -1773162956091.739, 2.258404446078257e-07, -5.63963958622347e-13, 4427904.849977206, 2.497178747596235e-06]
    diffs_2 = [-664.0592454189463, 1.5385254880211363e+17, 1.50351759964441e-09, 2.759680128116916e-20, -130527901462.75568, 1.034083761001255e-14]
    diffs_mixed = [-7.87047555851423e-15, -10000511760.82874, 0.08069819844971812]
    departures = [-26160.84248778514, -63.01313785205201, 39.84399938752266]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
    
    
    
    
    # Test Cp_Dep, Cv_dep
    assert_allclose(eos.Cv_dep_l, 39.8439993875226)
    assert_allclose(eos.Cp_dep_l, 58.57056977621366)
        
    # Integration tests
    eos = RK(Tc=507.6, Pc=3025000, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    # One gas phase property
    assert 'g' == RK(Tc=507.6, Pc=3025000, T=499.,P=1E5).phase



    # Compare against some known  in Walas [2] functions
    eos = RK(Tc=507.6, Pc=3025000, T=299., P=1E6)
    V = eos.V_l
    Z = eos.P*V/(R*eos.T)

    phi_walas = exp(Z - 1 - log(Z*(1 - eos.b/V)) - eos.a/(eos.b*R*eos.T**1.5)*log(1 + eos.b/V))
    phi_l_expect = 0.052632270169019224
    assert_allclose(phi_l_expect, eos.phi_l)
    assert_allclose(phi_walas, eos.phi_l)
    
    S_dep_walas = -R*(log(Z*(1 - eos.b/V)) - eos.a/(2*eos.b*R*eos.T**1.5)*log(1 + eos.b/V))
    S_dep_expect = -63.01313785205201
    assert_allclose(-S_dep_walas, S_dep_expect)
    assert_allclose(S_dep_expect, eos.S_dep_l)
    
    H_dep_walas = R*eos.T*(1 - Z + 1.5*eos.a/(eos.b*R*eos.T**1.5)*log(1 + eos.b/V))
    H_dep_expect = -26160.84248778514
    assert_allclose(-H_dep_walas, H_dep_expect)
    assert_allclose(H_dep_expect, eos.H_dep_l)
    

def test_RK_Psat():
    eos = RK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    
    Ts = np.linspace(507.6*0.32, 504, 100)
    Psats_eos = [eos.Psat(T) for T in Ts]
    fugacity_ls, fugacity_gs = [], []
    for T, P in zip(Ts, Psats_eos):
        eos = RK(Tc=507.6, Pc=3025000, omega=0.2975, T=T, P=P)
        fugacity_ls.append(eos.fugacity_l)
        fugacity_gs.append(eos.fugacity_g)
    
    # Fit is very good
    assert_allclose(fugacity_ls, fugacity_gs, rtol=3E-4)
        

def test_SRK_quick():
    # Test solution for molar volumes
    eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [0.0001468210773547258, (0.0011696016227365465+0.001304089515440735j), (0.0011696016227365465-0.001304089515440735j)]
    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.72718144448615, -0.007332994130304654, 1.9476133436500582e-05]
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    
    # PR back calculation for T
    eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, V=0.0001468210773547258, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.0001468210773547258, quick=False)
    assert_allclose(T_slow, 299)
    
    # Derivatives
    diffs_1 = [507071.3781579619, -2693848855910.7515, 1.882330469452149e-07, -3.7121607539555683e-13, 5312563.421932225, 1.97210894377967e-06]
    diffs_2 = [-495.5254299681785, 2.685151838840304e+17, 1.3462644444996599e-09, 1.3735648667748024e-20, -201856509533.585, 3.800656805086307e-15]
    diffs_mixed = [-4.991348993006751e-15, -14322101736.003756, 0.06594010907198579]
    departures = [-31754.66385964974, -74.3732720444703, 28.936530624645115]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
        
    # Integration tests
    eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    
    # Compare against some known  in Walas [2] functions
    eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    V = eos.V_l
    Z = eos.P*V/(R*eos.T)
    D = -eos.T*eos.da_alpha_dT
    
    S_dep_walas = R*(-log(Z*(1-eos.b/V)) + D/(eos.b*R*eos.T)*log(1 + eos.b/V))
    S_dep_expect = -74.3732720444703
    assert_allclose(-S_dep_walas, S_dep_expect)
    assert_allclose(S_dep_expect, eos.S_dep_l)
    
    H_dep_walas = eos.T*R*(1 - Z + 1/(eos.b*R*eos.T)*(eos.a_alpha+D)*log(1 + eos.b/V))
    H_dep_expect = -31754.663859649743
    assert_allclose(-H_dep_walas, H_dep_expect)
    assert_allclose(H_dep_expect, eos.H_dep_l)

    phi_walas = exp(Z - 1 - log(Z*(1 - eos.b/V)) - eos.a_alpha/(eos.b*R*eos.T)*log(1 + eos.b/V))
    phi_l_expect = 0.02174822767621325
    assert_allclose(phi_l_expect, eos.phi_l)
    assert_allclose(phi_walas, eos.phi_l)

def test_SRK_Psat():
    eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    
    # ERROR actually for RK not SRK
    Cs_SRK = [-3.0486334, -5.2157649E-2, 0.55002312, -0.44506984, 3.1735078E-2,
              4.1819219E-2, -1.18709865E-2, 1.79267167E-3, -1.47491666E-4, 
              5.19352748E-6]
              
    def Psat(T, Tc, Pc, omega):
        Tr = T/Tc
        e = SRK(Tc=Tc, Pc=Pc, omega=omega, T=T, P=1E5)
        alpha = e.a_alpha/e.a
        tot = 0
        for k, Ck in enumerate(Cs_SRK[0:4]):
            tot += Ck*(alpha/Tr-1)**((k+2)/2.)
        for k, Ck in enumerate(Cs_SRK[4:]):
            tot += Ck*(alpha/Tr-1)**(k+3)
        P = exp(tot)*Tr*Pc
        return P
    
    Ts = np.linspace(160, 504, 100)
    Psats_lit = [Psat(T, Tc=507.6, Pc=3025000, omega=0.2975) for T in Ts]
    Psats_eos = [eos.Psat(T) for T in Ts]
    assert_allclose(Psats_lit, Psats_eos, rtol=5E-2)
    # Not sure why the fit was so poor for the original author

    fugacity_ls, fugacity_gs = [], []
    for T, P in zip(Ts, Psats_eos):
        eos = SRK(Tc=507.6, Pc=3025000, omega=0.2975, T=T, P=P)
        fugacity_ls.append(eos.fugacity_l)
        fugacity_gs.append(eos.fugacity_g)
        
    assert allclose_variable(fugacity_ls, fugacity_gs, limits=[0, .1, .5], rtols=[3E-2, 1E-3, 3E-4])


def test_APISRK_quick():
    # Test solution for molar volumes
    eos = APISRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [(0.00014681828835112518+0j), (0.0011696030172383468+0.0013042038361510636j), (0.0011696030172383468-0.0013042038361510636j)]
    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.727476773890392, -0.007334914894987986, 1.948255305988373e-05]
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    a_alphas_slow = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_slow)

    # SRK back calculation for T
    eos = APISRK(Tc=507.6, Pc=3025000, omega=0.2975, V=0.00014681828835112518, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.00014681828835112518, quick=False)
    assert_allclose(T_slow, 299)
    # with a S1 set
    eos = APISRK(Tc=514.0, Pc=6137000.0, S1=1.678665, S2=-0.216396, P=1E6, V=7.045695070282895e-05)
    assert_allclose(eos.T, 299)
    eos = APISRK(Tc=514.0, Pc=6137000.0, omega=0.635, S2=-0.216396, P=1E6, V=7.184693818446427e-05)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=7.184693818446427e-05, quick=False)
    assert_allclose(T_slow, 299)

    
    eos = APISRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    # Derivatives
    diffs_1 = [507160.1972586132, -2694518622391.442, 1.882192214387065e-07, -3.7112380359519615e-13, 5312953.652428371, 1.9717635678142066e-06]
    diffs_2 = [-495.70334320516105, 2.6860475503881738e+17, 1.3462140892058852e-09, 1.3729987070697146e-20, -201893442624.3192, 3.8000241940176305e-15]
    diffs_mixed = [-4.990229443299593e-15, -14325363284.978655, 0.06593412205681573]
    departures = [-31759.40804708375, -74.3842308177361, 28.9464819026358]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
    # Test Cp_Dep, Cv_dep
    assert_allclose(eos.Cv_dep_l, 28.9464819026358)
    assert_allclose(eos.Cp_dep_l, 49.17375122882494)
        
    # Integration tests
    eos = APISRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    # Error checking
    with pytest.raises(Exception):
        APISRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299.) 
    with pytest.raises(Exception):
        APISRK(Tc=507.6, Pc=3025000, P=1E6,  T=299.)
    

def test_TWUPR_quick():
    # Test solution for molar volumes
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [0.0001301755417057077, (0.0011236546051852435+0.001294926236567151j), (0.0011236546051852435-0.001294926236567151j)]

    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.8069848647566698, -0.006971714700883658, 2.366703486824857e-05]
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    a_alphas_slow = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_slow)

    # back calculation for T
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, V=0.0001301755417057077, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.0001301755417057077, quick=False)
    assert_allclose(T_slow, 299)

    
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    # Derivatives
    diffs_1 = [592877.7698667824, -3683684905961.741, 1.6094692814449423e-07, -2.7146730122915294e-13, 6213228.245662597, 1.6866883037707698e-06]
    diffs_2 = [-708.1014081968287, 4.512485403434166e+17, 1.1685466035091765e-09, 9.027518486599707e-21, -280283776931.3797, 3.3978167906790706e-15]
    diffs_mixed = [-3.823707450118526e-15, -20741136287.632187, 0.0715233066523022]
    departures = [-31652.73712017438, -74.1128504294285, 35.18913741045412]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
    # Test Cp_Dep, Cv_dep
    assert_allclose(eos.Cv_dep_l, 35.18913741045409)
    assert_allclose(eos.Cp_dep_l, 55.40580968404073)
        
    # Integration tests
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    # Error checking
    with pytest.raises(Exception):
        TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, T=299.) 
        
    # Superctitical test
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, T=900., P=1E6)
    eos = TWUPR(Tc=507.6, Pc=3025000, omega=0.2975, V=0.007371700581036866, P=1E6)
    assert_allclose(eos.T, 900)
    
    
    
def test_TWUSRK_quick():
    # Test solution for molar volumes
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    Vs_fast = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha)
    Vs_slow = eos.volume_solutions(299, 1E6, eos.b, eos.delta, eos.epsilon, eos.a_alpha, quick=False)
    Vs_expected = [(0.00014689222296622437+0j), (0.001169566049930797+0.0013011782630948804j), (0.001169566049930797-0.0013011782630948804j)]

    assert_allclose(Vs_fast, Vs_expected)
    assert_allclose(Vs_slow, Vs_expected)
    
    # Test of a_alphas
    a_alphas = [3.7196696151053654, -0.00726972623757774, 2.305590221826195e-05]
    a_alphas_fast = eos.a_alpha_and_derivatives(299)
    assert_allclose(a_alphas, a_alphas_fast)
    a_alphas_slow = eos.a_alpha_and_derivatives(299, quick=False)
    assert_allclose(a_alphas, a_alphas_slow)

    # back calculation for T
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, V=0.00014689222296622437, P=1E6)
    assert_allclose(eos.T, 299)
    T_slow = eos.solve_T(P=1E6, V=0.00014689222296622437, quick=False)
    assert_allclose(T_slow, 299)

    
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299., P=1E6)
    # Derivatives
    diffs_1 = [504446.40946384973, -2676840643946.8457, 1.8844842729228471e-07, -3.7357472222386695e-13, 5306491.618786468, 1.982371132471433e-06]
    diffs_2 = [-586.1645169279949, 2.6624340439193766e+17, 1.308862239605917e-09, 1.388069796850075e-20, -195576372405.25787, 4.5664049232057565e-15]
    diffs_mixed = [-5.015405580586871e-15, -14235383353.785719, 0.0681656809901603]
    departures = [-31612.602587050424, -74.0229660932213, 34.24267346218354]
    known_derivs_deps = [diffs_1, diffs_2, diffs_mixed, departures]
    
    for f in [True, False]:
        main_calcs = eos.derivatives_and_departures(eos.T, eos.P, eos.V_l, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=f)
        
        for i, j in zip(known_derivs_deps, main_calcs):
            assert_allclose(i, j)
    
    # Test Cp_Dep, Cv_dep
    assert_allclose(eos.Cv_dep_l, 34.242673462183554)
    assert_allclose(eos.Cp_dep_l, 54.35178846652431)
        
    # Integration tests
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299.,V=0.00013)
    fast_vars = vars(eos)
    eos.set_properties_from_solution(eos.T, eos.P, eos.V, eos.b, eos.delta, eos.epsilon, eos.a_alpha, eos.da_alpha_dT, eos.d2a_alpha_dT2, quick=False)
    slow_vars = vars(eos)
    [assert_allclose(slow_vars[i], j) for (i, j) in fast_vars.items() if isinstance(j, float)]

    # Error checking
    with pytest.raises(Exception):
        TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, T=299.) 
    from thermo.eos import TWU_a_alpha_common
    with pytest.raises(Exception):
        TWU_a_alpha_common(299.0, 507.6, 0.2975, 2.5171086468571824, method='FAIL')
        
    # Superctitical test
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, T=900., P=1E6)
    eos = TWUSRK(Tc=507.6, Pc=3025000, omega=0.2975, V=0.007422212960199866, P=1E6)
    assert_allclose(eos.T, 900)


@pytest.mark.slow
def test_fuzz_dV_dT_and_d2V_dT2_derivatives():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('VDW')
    
    phase_extensions = {True: '_l', False: '_g'}
    derivative_bases_dV_dT = {0:'V', 1:'dV_dT', 2:'d2V_dT2'}
    
    def dV_dT(T, P, eos, order=0, phase=True, Tc=507.6, Pc=3025000., omega=0.2975):
        eos = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=T, P=P)
        phase_base = phase_extensions[phase]
        attr = derivative_bases_dV_dT[order]+phase_base
        return getattr(eos, attr)
    
    x, y = [], []
    for eos in range(len(eos_list)):
        for T in np.linspace(.1, 1000, 50):
            for P in np.logspace(np.log10(3E4), np.log10(1E6), 50):
                T, P = float(T), float(P)
                for phase in [True, False]:
                    for order in [1, 2]:
                        try:
                            # If dV_dx_phase doesn't exist, will simply abort and continue the loop
                            numer = derivative(dV_dT, T, dx=1E-4, args=(P, eos, order-1, phase))
                            ana = dV_dT(T=T, P=P, eos=eos, order=order, phase=phase)
                        except:
                            continue
                        x.append(numer)
                        y.append(ana)
    assert allclose_variable(x, y, limits=[.009, .05, .65, .93],rtols=[1E-5, 1E-6, 1E-9, 1E-10])


@pytest.mark.slow
def test_fuzz_dV_dP_and_d2V_dP2_derivatives():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('VDW')
    
    phase_extensions = {True: '_l', False: '_g'}
    derivative_bases_dV_dP = {0:'V', 1:'dV_dP', 2:'d2V_dP2'}
    
    def dV_dP(P, T, eos, order=0, phase=True, Tc=507.6, Pc=3025000., omega=0.2975):
        eos = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=T, P=P)
        phase_base = phase_extensions[phase]
        attr = derivative_bases_dV_dP[order]+phase_base
        return getattr(eos, attr)
    
    
    x, y = [], []
    for eos in range(len(eos_list)):
        for T in np.linspace(.1, 1000, 50):
            for P in np.logspace(np.log10(3E4), np.log10(1E6), 50):
                T, P = float(T), float(P)
                for phase in [True, False]:
                    for order in [1, 2]:
                        try:
                            # If dV_dx_phase doesn't exist, will simply abort and continue the loop
                            numer = derivative(dV_dP, P, dx=15., args=(T, eos, order-1, phase))
                            ana = dV_dP(T=T, P=P, eos=eos, order=order, phase=phase)
                        except:
                            continue
                        x.append(numer)
                        y.append(ana)
    assert allclose_variable(x, y, limits=[.02, .04, .04, .05, .15, .45, .95],
                            rtols=[1E-2, 1E-3, 1E-4, 1E-5, 1E-6, 1E-7, 1E-9])
    
@pytest.mark.slow
def test_fuzz_Psat():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('eos_list')
    eos_list.remove('GCEOS_DUMMY')
    
    Tc = 507.6
    Pc = 3025000
    omega = 0.2975
    # Basic test
    e = PR(T=400, P=1E5, Tc=507.6, Pc=3025000, omega=0.2975)
    Psats_expect = [22284.314987503185, 466204.89703879296, 2717294.407158156]
    assert_allclose([e.Psat(300), e.Psat(400), e.Psat(500)], Psats_expect)
    
    
    # Test the relative fugacity errors at the correlated Psat are small
    x = []
    for eos in range(len(eos_list)):
        for T in np.linspace(0.318*Tc, Tc*.99, 100):
            e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=T, P=1E5)
            Psat = e.Psat(T)
            e = e.to_TP(T, Psat)
            rerr = (e.fugacity_l - e.fugacity_g)/e.fugacity_g
            x.append(rerr)

    # Assert the average error is under 0.04%
    assert sum(abs(np.array(x)))/len(x) < 1E-4
    
    # Test Polish is working, and that its values are close to the polynomials
    Psats_solved = []
    Psats_poly = []
    for eos in range(len(eos_list)):
        for T in np.linspace(0.4*Tc, Tc*.99, 50):
            e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=T, P=1E5)
            Psats_poly.append(e.Psat(T))
            Psats_solved.append(e.Psat(T, polish=True))
    assert_allclose(Psats_solved, Psats_poly, rtol=1E-4)

    
@pytest.mark.slow
def test_fuzz_dPsat_dT():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('eos_list')
    eos_list.remove('GCEOS_DUMMY')
    
    Tc = 507.6
    Pc = 3025000
    omega = 0.2975
    
    e = PR(T=400, P=1E5, Tc=507.6, Pc=3025000, omega=0.2975)
    dPsats_dT_expect = [938.7777925283981, 10287.225576267781, 38814.74676693623]
    assert_allclose([e.dPsat_dT(300), e.dPsat_dT(400), e.dPsat_dT(500)], dPsats_dT_expect)
    
    # Hammer the derivatives for each EOS in a wide range; most are really 
    # accurate. There's an error around the transition between polynomials 
    # though - to be expected; the derivatives are discontinuous there.
    dPsats_derivative = []
    dPsats_analytical = []
    for eos in range(len(eos_list)):
        for T in np.linspace(0.2*Tc, Tc*.999, 50):
            e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=T, P=1E5)
            anal = e.dPsat_dT(T)
            numer = derivative(e.Psat, T, order=9)
            dPsats_analytical.append(anal)
            dPsats_derivative.append(numer)
    assert allclose_variable(dPsats_derivative, dPsats_analytical, limits=[.02, .06], rtols=[1E-5, 1E-7])


def test_Hvaps():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('eos_list')
    eos_list.remove('GCEOS_DUMMY')
    
    Tc = 507.6
    Pc = 3025000
    omega = 0.2975

    Hvaps = []
    Hvaps_expect = [31084.983490850733, 31710.358102130172, 31084.98349085074, 31034.20840963749, 31034.20840963749, 13004.118580400604, 26011.82023167917, 31715.130557858054, 31591.432176727412, 31562.24577655315]
    
    for eos in range(len(eos_list)):
        e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=300, P=1E5)
        Hvaps.append(e.Hvap(300))
    
    assert_allclose(Hvaps, Hvaps_expect)



def test_V_l_sats():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('eos_list')
    eos_list.remove('GCEOS_DUMMY')
    
    Tc = 507.6
    Pc = 3025000
    omega = 0.2975

    V_l_sats = []
    V_l_sats_expect = [0.00013065657957196664, 0.00014738493903429054, 0.00013065657957196664, 0.00013068338300846935, 0.00013068338300846935, 0.00022496914669071998, 0.0001526748088257479, 0.00014738204693974985, 0.00013061083054616748, 0.00014745855640370398]
    
    for eos in range(len(eos_list)):
        e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=300, P=1E5)
        V_l_sats.append(e.V_l_sat(300))
    
    assert_allclose(V_l_sats, V_l_sats_expect)


def test_V_g_sats():
    from thermo import eos
    eos_list = list(eos.__all__); eos_list.remove('GCEOS')
    eos_list.remove('ALPHA_FUNCTIONS'); eos_list.remove('eos_list')
    eos_list.remove('GCEOS_DUMMY')
    
    Tc = 507.6
    Pc = 3025000
    omega = 0.2975
    V_g_sats = []
    V_g_sats_expect = [0.11050460498444403, 0.11367516109277499, 0.11050460498444403, 0.10979758091064296, 0.10979758091064296, 0.009465797924575097, 0.04604551902418885, 0.11374291407753441, 0.11172605609973751, 0.1119691155539088]
    
    for eos in range(len(eos_list)):
        e = globals()[eos_list[eos]](Tc=Tc, Pc=Pc, omega=omega, T=300, P=1E5)
        V_g_sats.append(e.V_g_sat(300))
    
    assert_allclose(V_g_sats, V_g_sats_expect)
