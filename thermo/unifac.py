# -*- coding: utf-8 -*-
'''Chemical Engineering Design Library (ChEDL). Utilities for process modeling.
Copyright (C) 2017, 2018, 2019 Caleb Bell <Caleb.Andrew.Bell@gmail.com>

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

from __future__ import division

__all__ = ['UNIFAC_gammas','UNIFAC',  'GibbsExcess', 
           'UNIFAC_psi', 'DOUFMG', 'DOUFSG', 'UFSG', 'UFMG', 
           'DOUFIP2016', 'DOUFIP2006', 'UFIP', 'DDBST_UNIFAC_assignments', 
           'DDBST_MODIFIED_UNIFAC_assignments', 'DDBST_PSRK_assignments',
           'UNIFAC_RQ', 'Van_der_Waals_volume', 'Van_der_Waals_area',
           'load_group_assignments_DDBST', 'DDBST_UNIFAC_assignments', 
           'DDBST_MODIFIED_UNIFAC_assignments', 'DDBST_PSRK_assignments',
           'PSRKIP', 'PSRKSG']
import os
from thermo.utils import log, exp
from thermo.activity import GibbsExcess
from thermo.utils import R
folder = os.path.join(os.path.dirname(__file__), 'Phase Change')


class UNIFAC_subgroup(object):
    __slots__ = ['group', 'main_group_id', 'main_group', 'R', 'Q', 'smarts']
    
    def __repr__(self):
        return '<%s>' %self.group
        
    def __init__(self, group, main_group_id, main_group, R, Q, smarts=None):
        self.group = group
        self.main_group_id = main_group_id
        self.main_group = main_group
        self.R = R
        self.Q = Q
        self.smarts = smarts



# http://www.ddbst.com/published-parameters-unifac.html#ListOfMainGroups
#UFMG[No.] = ('Maingroup Name', subgroups)
UFMG = {}
UFMG[1] = ('CH2', [1, 2, 3, 4])
UFMG[2] = ('C=C', [5, 6, 7, 8, 70])
UFMG[3] = ('ACH', [9, 10])
UFMG[4] = ('ACCH2', [11, 12, 13])
UFMG[5] = ('OH', [14])
UFMG[6] = ('CH3OH', [15])
UFMG[7] = ('H2O', [16])
UFMG[8] = ('ACOH', [17])
UFMG[9] = ('CH2CO', [18, 19])
UFMG[10] = ('CHO', [20])
UFMG[11] = ('CCOO', [21, 22])
UFMG[12] = ('HCOO', [23])
UFMG[13] = ('CH2O', [24, 25, 26, 27])
UFMG[14] = ('CNH2', [28, 29, 30])
UFMG[15] = ('CNH', [31, 32, 33])
UFMG[16] = ('(C)3N', [34, 35])
UFMG[17] = ('ACNH2', [36])
UFMG[18] = ('PYRIDINE', [37, 38, 39])
UFMG[19] = ('CCN', [40, 41])
UFMG[20] = ('COOH', [42, 43])
UFMG[21] = ('CCL', [44, 45, 46])
UFMG[22] = ('CCL2', [47, 48, 49])
UFMG[23] = ('CCL3', [50, 51])
UFMG[24] = ('CCL4', [52])
UFMG[25] = ('ACCL', [53])
UFMG[26] = ('CNO2', [54, 55, 56])
UFMG[27] = ('ACNO2', [57])
UFMG[28] = ('CS2', [58])
UFMG[29] = ('CH3SH', [59, 60])
UFMG[30] = ('FURFURAL', [61])
UFMG[31] = ('DOH', [62])
UFMG[32] = ('I', [63])
UFMG[33] = ('BR', [64])
UFMG[34] = ('C=-C', [65, 66])
UFMG[35] = ('DMSO', [67])
UFMG[36] = ('ACRY', [68])
UFMG[37] = ('CLCC', [69])
UFMG[38] = ('ACF', [71])
UFMG[39] = ('DMF', [72, 73])
UFMG[40] = ('CF2', [74, 75, 76])
UFMG[41] = ('COO', [77])
UFMG[42] = ('SIH2', [78, 79, 80, 81])
UFMG[43] = ('SIO', [82, 83, 84])
UFMG[44] = ('NMP', [85])
UFMG[45] = ('CCLF', [86, 87, 88, 89, 90, 91, 92, 93])
UFMG[46] = ('CON(AM)', [94, 95, 96, 97, 98, 99])
UFMG[47] = ('OCCOH', [100, 101])
UFMG[48] = ('CH2S', [102, 103, 104])
UFMG[49] = ('MORPH', [105])
UFMG[50] = ('THIOPHEN', [106, 107, 108])
UFMG[51] = ('NCO', [109])
UFMG[55] = ('SULFONES', [118, 119])
UFMG[84] = ('IMIDAZOL', [178])
UFMG[85] = ('BTI', [179])


UFSG = {}
# UFSG[subgroup ID] = (subgroup formula, main group ID, subgroup R, subgroup Q)
# http://www.ddbst.com/published-parameters-unifac.html
UFSG[1] = UNIFAC_subgroup('CH3', 1, 'CH2', 0.9011, 0.848, smarts='[CX4;H3]')
UFSG[2] = UNIFAC_subgroup('CH2', 1, 'CH2', 0.6744, 0.54, smarts='[CX4;H2]')
UFSG[3] = UNIFAC_subgroup('CH', 1, 'CH2', 0.4469, 0.228, smarts='[CX4;H1]')
UFSG[4] = UNIFAC_subgroup('C', 1, 'CH2', 0.2195, 0, smarts='[CX4;H0]')
UFSG[5] = UNIFAC_subgroup('CH2=CH', 2, 'C=C', 1.3454, 1.176, smarts='[CX3;H2]=[CX3;H1]')
UFSG[6] = UNIFAC_subgroup('CH=CH', 2, 'C=C', 1.1167, 0.867, smarts='[CX3;H1]=[CX3;H1]') # Could restrict the next connection from being  H
UFSG[7] = UNIFAC_subgroup('CH2=C', 2, 'C=C', 1.1173, 0.988, smarts='[CX3;H2]=[CX3;H0]')
UFSG[8] = UNIFAC_subgroup('CH=C', 2, 'C=C', 0.8886, 0.676, smarts='[CX3;H1]=[CX3;H0]')
UFSG[9] = UNIFAC_subgroup('ACH', 3, 'ACH', 0.5313, 0.4, smarts='[cX3;H1]')
UFSG[10] = UNIFAC_subgroup('AC', 3, 'ACH', 0.3652, 0.12, smarts='[cX3;H0]')
UFSG[11] = UNIFAC_subgroup('ACCH3', 4, 'ACCH2', 1.2663, 0.968, smarts='[cX3;H0][CX4;H3]')
UFSG[12] = UNIFAC_subgroup('ACCH2', 4, 'ACCH2', 1.0396, 0.66, smarts='[cX3;H0][CX4;H2]')
UFSG[13] = UNIFAC_subgroup('ACCH', 4, 'ACCH2', 0.8121, 0.348, smarts='[cX3;H0][CX4;H1]')
UFSG[14] = UNIFAC_subgroup('OH', 5, 'OH', 1, 1.2, smarts='[OX2;H1]')
UFSG[15] = UNIFAC_subgroup('CH3OH', 6, 'CH3OH', 1.4311, 1.432, smarts='[CX4;H3][OX2;H1]') # One extra radical; otherwise perfect, six matches
UFSG[16] = UNIFAC_subgroup('H2O', 7, 'H2O', 0.92, 1.4, smarts='[OH2]')
UFSG[17] = UNIFAC_subgroup('ACOH', 8, 'ACOH', 0.8952, 0.68, smarts='[cX3;H0;R][OX2;H1]') # pretty good 5 extra
UFSG[18] = UNIFAC_subgroup('CH3CO', 9, 'CH2CO', 1.6724, 1.488, smarts='[CX4;H3][CX3](=O)')
UFSG[19] = UNIFAC_subgroup('CH2CO', 9, 'CH2CO', 1.4457, 1.18, smarts='[CX4;H2;!$([CX4,CX3;H0,H1][CX3](=O)[CX4;H2][CX3](=O)[CX4,CX3;H0,H1])][CX3;!$([CX4,CX3;H0,H1][CX3](=O)[CX4;H2][CX3](=O)[CX4,CX3;H0,H1])](=O)[#6;!$([CX4;H3]);!$([CX4,CX3;H0,H1][CX3](=O)[CX4;H2][CX3](=O)[CX4,CX3;H0,H1])]') # '[CX4;H2][CX3](=O)'
UFSG[20] = UNIFAC_subgroup('CHO', 10, 'CHO', 0.998, 0.948, smarts='[CX3H1](=O)')
UFSG[21] = UNIFAC_subgroup('CH3COO', 11, 'CCOO', 1.9031, 1.728, smarts='C(=O)[OH0]') # can't distinguish between 21, 22
UFSG[22] = UNIFAC_subgroup('CH2COO', 11, 'CCOO', 1.6764, 1.42, smarts='[CX4;H2][CX3](=[OX1])[OX2]') # Custom, lots of extra matches
UFSG[23] = UNIFAC_subgroup('HCOO', 12, 'HCOO', 1.242, 1.188, smarts='[CX3;H1](=[OX1])[OX2][#6;!$([CX3]=[#8])]')
UFSG[24] = UNIFAC_subgroup('CH3O', 13, 'CH2O', 1.145, 1.088, smarts='[CH3][O]')
UFSG[25] = UNIFAC_subgroup('CH2O', 13, 'CH2O', 0.9183, 0.78, smarts='[CH2][O]')
UFSG[26] = UNIFAC_subgroup('CHO', 13, 'CH2O', 0.6908, 0.468, smarts='[C;H1][O]')
UFSG[27] = UNIFAC_subgroup('THF', 13, 'CH2O', 0.9183, 1.1, smarts='[CX4,CX3;H2,H1;R][OX2;R]') # CX3, H1 needed to allow 290-67-5 and 255-37-8 but adds a lot of false positives; 
UFSG[28] = UNIFAC_subgroup('CH3NH2', 14, 'CNH2', 1.5959, 1.544, smarts='[CX4;H3][NX3;H2]') # Perfect
UFSG[29] = UNIFAC_subgroup('CH2NH2', 14, 'CNH2', 1.3692, 1.236, smarts='[CX4;H2][NX3;H2]')
UFSG[30] = UNIFAC_subgroup('CHNH2', 14, 'CNH2', 1.1417, 0.924, smarts='[CX4;H1][NX3;H2]')
UFSG[31] = UNIFAC_subgroup('CH3NH', 15, 'CNH', 1.4337, 1.244, smarts='[CX4;H3][NX3;H1]')
UFSG[32] = UNIFAC_subgroup('CH2NH', 15, 'CNH', 1.207, 0.936, smarts='[CX4;H2][NX3;H1]')
UFSG[33] = UNIFAC_subgroup('CHNH', 15, 'CNH', 0.9795, 0.624, smarts='[CX4;H1][NX3;H1]')
UFSG[34] = UNIFAC_subgroup('CH3N', 16, '(C)3N', 1.1865, 0.94, smarts='[CX4;H3][NX3;H0]')
UFSG[35] = UNIFAC_subgroup('CH2N', 16, '(C)3N', 0.9597, 0.632, smarts='[CX4;H2][NX3;H0]')
UFSG[36] = UNIFAC_subgroup('ACNH2', 17, 'ACNH2', 1.06, 0.816, smarts='[c][NX3;H2]')
UFSG[37] = UNIFAC_subgroup('C5H5N', 18, 'PYRIDINE', 2.9993, 2.113, smarts='[cX3;H1][cX3;H1][cX3;H1][cX3;H1][nX2;H0][cX3;H1]') # There is another match from ddbst 3,4-Didehydropyridine  but it is C5H3N and so wrong; only one real hit
UFSG[38] = UNIFAC_subgroup('C5H4N', 18, 'PYRIDINE', 2.8332, 1.833, smarts='[$([nX2;H0]1[cX3;H0][cX3;H1][cX3;H1][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H0][cX3;H1][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H0][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H1][cX3;H0][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H1][cX3;H1][cX3;H0]1)]') # Perfect hand made
UFSG[39] = UNIFAC_subgroup('C5H3N', 18, 'PYRIDINE', 2.667, 1.553, smarts='[$([nX2;H0]1[cX3;H0][cX3;H0][cX3;H1][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H0][cX3;H1][cX3;H0][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H0][cX3;H1][cX3;H1][cX3;H0][cX3;H1]1),$([nX2;H0]1[cX3;H0][cX3;H1][cX3;H1][cX3;H1][cX3;H0]1),$([nX2;H0]1[cX3;H1][cX3;H0][cX3;H0][cX3;H1][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H0][cX3;H1][cX3;H0][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H0][cX3;H1][cX3;H1][cX3;H0]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H0][cX3;H0][cX3;H1]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H0][cX3;H1][cX3;H0]1),$([nX2;H0]1[cX3;H1][cX3;H1][cX3;H1][cX3;H0][cX3;H0]1)]') # Very much not fun to make, 200 matches perfectly, 10 different ring combos
UFSG[40] = UNIFAC_subgroup('CH3CN', 19, 'CCN', 1.8701, 1.724, smarts='[CX4;H3][CX2]#[NX1]')
UFSG[41] = UNIFAC_subgroup('CH2CN', 19, 'CCN', 1.6434, 1.416, smarts='[CX4;H2][CX2]#[NX1]')
UFSG[42] = UNIFAC_subgroup('COOH', 20, 'COOH', 1.3013, 1.224, smarts='[CX3](=[OX1])[O;H1]') # Tried '[C][CX3](=[OX1])[OH1]' at first but fails for a few hundred
UFSG[43] = UNIFAC_subgroup('HCOOH', 20, 'COOH', 1.528, 1.532, smarts='[CX3;H1](=[OX1])[OX2;H1]') # effortlessly web - missing one hit
UFSG[44] = UNIFAC_subgroup('CH2CL', 21, 'CCL', 1.4654, 1.264, smarts='[CX4;H2;!$(C(Cl)(Cl))](Cl)') # Matches perfectly effortlessly web
UFSG[45] = UNIFAC_subgroup('CHCL', 21, 'CCL', 1.238, 0.952, smarts='[CX4;H1;!$(C(Cl)(Cl))](Cl)') # effortlessly web
UFSG[46] = UNIFAC_subgroup('CCL', 21, 'CCL', 1.0106, 0.724, smarts='[CX4;H0;!$(C(Cl)(Cl))](Cl)') # effortlessly web
UFSG[47] = UNIFAC_subgroup('CH2CL2', 22, 'CCL2', 2.2564, 1.988, smarts='[CX4;H2;!$(C(Cl)(Cl)(Cl))](Cl)(Cl)') # effortlessly web
UFSG[48] = UNIFAC_subgroup('CHCL2', 22, 'CCL2', 2.0606, 1.684, smarts='[CX4;H1;!$(C(Cl)(Cl)(Cl))](Cl)(Cl)') # effortlessly web
UFSG[49] = UNIFAC_subgroup('CCL2', 22, 'CCL2', 1.8016, 1.448, smarts='[CX4;H0;!$(C(Cl)(Cl)(Cl))](Cl)(Cl)') # effortlessly web
UFSG[50] = UNIFAC_subgroup('CHCL3', 23, 'CCL3', 2.87, 2.41, smarts='[CX4;H1;!$([CX4;H0](Cl)(Cl)(Cl)(Cl))](Cl)(Cl)(Cl)') # effortlessly web
UFSG[51] = UNIFAC_subgroup('CCL3', 23, 'CCL3', 2.6401, 2.184, smarts='[CX4;H0;!$([CX4;H0](Cl)(Cl)(Cl)(Cl))](Cl)(Cl)(Cl)') # effortlessly web
UFSG[52] = UNIFAC_subgroup('CCL4', 24, 'CCL4', 3.39, 2.91, smarts='[CX4;H0]([Cl])([Cl])([Cl])([Cl])')
UFSG[53] = UNIFAC_subgroup('ACCL', 25, 'ACCL', 1.1562, 0.844, smarts='aCl') # Does take up one of the carbon spaces on the ring
UFSG[54] = UNIFAC_subgroup('CH3NO2', 26, 'CNO2', 2.0086, 1.868, smarts='[CX4;H3][NX3](=[OX1])(=[OX1])') # untested
UFSG[55] = UNIFAC_subgroup('CH2NO2', 26, 'CNO2', 1.7818, 1.56, smarts='[CX4;H2][NX3](=[OX1])(=[OX1])') # untested
UFSG[56] = UNIFAC_subgroup('CHNO2', 26, 'CNO2', 1.5544, 1.248, smarts='[CX4;H1][NX3](=[OX1])(=[OX1])') # untested
UFSG[57] = UNIFAC_subgroup('ACNO2', 27, 'ACNO2', 1.4199, 1.104, smarts='[cX3][NX3](=[OX1])(=[OX1])')
UFSG[58] = UNIFAC_subgroup('CS2', 28, 'CS2', 2.057, 1.65, smarts='C(=S)=S') # Easy, compount smarts
UFSG[59] = UNIFAC_subgroup('CH3SH', 29, 'CH3SH', 1.877, 1.676, smarts='[SX2H][CX4;H3]') # perfect match
UFSG[60] = UNIFAC_subgroup('CH2SH', 29, 'CH3SH', 1.651, 1.368, smarts='[SX2H][CX4;H2]')
UFSG[61] = UNIFAC_subgroup('FURFURAL', 30, 'FURFURAL', 3.168, 2.484, smarts='c1cc(oc1)C=O') # Easy, compound smarts, 1 hit only
UFSG[62] = UNIFAC_subgroup('DOH', 31, 'DOH', 2.4088, 2.248, smarts='C(CO)O') # Probably going to cause problems, match too much
UFSG[63] = UNIFAC_subgroup('I', 32, 'I', 1.264, 0.992, smarts='[I]')
UFSG[64] = UNIFAC_subgroup('BR', 33, 'BR', 0.9492, 0.832, smarts='[Br]')
UFSG[65] = UNIFAC_subgroup('CH=-C', 34, 'C=-C', 1.292, 1.088, smarts='[CX2;H1]#[CX2;H0]')
UFSG[66] = UNIFAC_subgroup('C=-C', 34, 'C=-C', 1.0613, 0.784, smarts='[CX2;H0]#[CX2;H0]')
UFSG[67] = UNIFAC_subgroup('DMSO', 35, 'DMSO', 2.8266, 2.472, smarts='CS(=O)C') # Compound smarts; some extra matches
UFSG[68] = UNIFAC_subgroup('ACRY', 36, 'ACRY', 2.3144, 2.052, smarts='N#CC=C') # Easy, compount smarts
UFSG[69] = UNIFAC_subgroup('CL-(C=C)', 37, 'CLCC', 0.791, 0.724, smarts='Cl[CX3]=[CX3]')
UFSG[70] = UNIFAC_subgroup('C=C', 2, 'C=C', 0.6605, 0.485, smarts='[CX3;H0]=[CX3;H0]') # ddbst matches some of these into rings incorrectly
UFSG[71] = UNIFAC_subgroup('ACF', 38, 'ACF', 0.6948, 0.524, smarts='[cX3][F]') # Perfect for many, except 71671-89-1
UFSG[72] = UNIFAC_subgroup('DMF', 39, 'DMF', 3.0856, 2.736, smarts='CN(C)C=O') # Probably going to cause problems, match too much
UFSG[73] = UNIFAC_subgroup('HCON(CH2)2', 39, 'DMF', 2.6322, 2.12, smarts='[CX4;H2,H1,H3][CX4;H2,H1][NX3][CX3;H1](=[OX1])') # No idea why extra H3 was needed  to match one compound
UFSG[74] = UNIFAC_subgroup('CF3', 40, 'CF2', 1.406, 1.38, smarts='C(F)(F)F')
UFSG[75] = UNIFAC_subgroup('CF2', 40, 'CF2', 1.0105, 0.92, smarts='C(F)F') # Probably going to cause problems, match too much
UFSG[76] = UNIFAC_subgroup('CF', 40, 'CF2', 0.615, 0.46, smarts='C(F)') # Probably going to cause problems, match too much
UFSG[77] = UNIFAC_subgroup('COO', 41, 'COO', 1.38, 1.2, smarts='[CX3,cX3](=[OX1])[OX2,oX2]') # ddbst wants match into rings, thus the cX3, oX2
UFSG[78] = UNIFAC_subgroup('SIH3', 42, 'SIH2', 1.6035, 1.2632, smarts='[SiX4,SiX3,SiX5;H3]') # some db smiles compounds missing Hs, not matched not due to smarts
UFSG[79] = UNIFAC_subgroup('SIH2', 42, 'SIH2', 1.4443, 1.0063, smarts='[SiX4,SiX3,SiX5,SiX2;H2]') # some db smiles compounds missing Hs, not matched not due to smarts
UFSG[80] = UNIFAC_subgroup('SIH', 42, 'SIH2', 1.2853, 0.7494, smarts='[SiX4,SiX3,SiX5,SiX2,SiX1;H1]') # some db smiles compounds missing Hs, not matched not due to smarts
UFSG[81] = UNIFAC_subgroup('SI', 42, 'SIH2', 1.047, 0.4099, smarts='[Si]')
UFSG[82] = UNIFAC_subgroup('SIH2O', 43, 'SIO', 1.4838, 1.0621) # Cannot find; Si problems
UFSG[83] = UNIFAC_subgroup('SIHO', 43, 'SIO', 1.303, 0.7639) # Cannot find; Si problems
UFSG[84] = UNIFAC_subgroup('SIO', 43, 'SIO', 1.1044, 0.4657) # Cannot find; Si problems
UFSG[85] = UNIFAC_subgroup('NMP', 44, 'NMP', 3.981, 3.2, smarts='CN1CCCC1=O') # 1 compound
UFSG[86] = UNIFAC_subgroup('CCL3F', 45, 'CCLF', 3.0356, 2.644, smarts='C(F)(Cl)(Cl)Cl') # pure compound?
UFSG[87] = UNIFAC_subgroup('CCL2F', 45, 'CCLF', 2.2287, 1.916, smarts='C(F)(Cl)Cl')
UFSG[88] = UNIFAC_subgroup('HCCL2F', 45, 'CCLF', 2.406, 2.116, smarts='ClC(Cl)F')
UFSG[89] = UNIFAC_subgroup('HCCLF', 45, 'CCLF', 1.6493, 1.416, smarts='C(Cl)F')
UFSG[90] = UNIFAC_subgroup('CCLF2', 45, 'CCLF', 1.8174, 1.648, smarts='ClC(F)(F)')
UFSG[91] = UNIFAC_subgroup('HCCLF2', 45, 'CCLF', 1.967, 1.828, smarts='ClC(F)F')
UFSG[92] = UNIFAC_subgroup('CCLF3', 45, 'CCLF', 2.1721, 2.1, smarts='ClC(F)(F)F') # perfect
UFSG[93] = UNIFAC_subgroup('CCL2F2', 45, 'CCLF', 2.6243, 2.376, smarts='ClC(Cl)(F)F') # perfect
UFSG[94] = UNIFAC_subgroup('AMH2', 46, 'CON(AM)', 1.4515, 1.248, smarts='[CX3;H0](=[OX1])[NX3;H2]')
UFSG[95] = UNIFAC_subgroup('AMHCH3', 46, 'CON(AM)', 2.1905, 1.796, smarts='[CX3;H0](=[OX1])[NX3;H1][CX4;H3]') # 3 extra hits, effortlessly web
UFSG[96] = UNIFAC_subgroup('AMHCH2', 46, 'CON(AM)', 1.9637, 1.488, smarts='[CX3;H0](=[OX1])[NX3;H1][CX4;H2]') # 4 extra hits, effortlessly web
UFSG[97] = UNIFAC_subgroup('AM(CH3)2', 46, 'CON(AM)', 2.8589, 2.428, smarts='[CX3;H0](=[OX1])[NX3;H0]([CX4;H3])[CX4;H3]') # effortlessly web
UFSG[98] = UNIFAC_subgroup('AMCH3CH2', 46, 'CON(AM)', 2.6322, 2.12, smarts='[CX3;H0](=[OX1])[NX3;H0]([CX4;H3])[CX4;H2]') # 1 extra hits, effortlessly web
UFSG[99] = UNIFAC_subgroup('AM(CH2)2', 46, 'CON(AM)', 2.4054, 1.812, smarts='[CX3;H0](=[OX1])[NX3;H0]([CX4;H2])[CX4;H2]') # 2 extra hits, effortlessly web
UFSG[100] = UNIFAC_subgroup('C2H5O2', 47, 'OCCOH', 2.1226, 1.904, smarts='[CX4;H2]([OX2;H1])[CX4;H2][OX2;H0]') # Matches all; 53 extra hits
UFSG[101] = UNIFAC_subgroup('C2H4O2', 47, 'OCCOH', 1.8952, 1.592, smarts='[$([CX4;H1]([OX2;H1])[CX4;H2][OX2;H0]),$([CX4;H2]([OX2;H1])[CX4;H1][OX2;H0])]') # custom expression
UFSG[102] = UNIFAC_subgroup('CH3S', 48, 'CH2S', 1.613, 1.368, smarts='[CX4;H3][SX2]')
UFSG[103] = UNIFAC_subgroup('CH2S', 48, 'CH2S', 1.3863, 1.06, smarts='[CX4;H2][SX2]')
UFSG[104] = UNIFAC_subgroup('CHS', 48, 'CH2S', 1.1589, 0.748, smarts='[CX4,CX3,CX2;H1][S]') # S bond might need to be more restricted; C bond might need to be more restricted
UFSG[105] = UNIFAC_subgroup('MORPH', 49, 'MORPH', 3.474, 2.796, smarts='C1CNCCO1') # lots of extra hits 100
UFSG[106] = UNIFAC_subgroup('C4H4S', 50, 'THIOPHEN', 2.8569, 2.14, smarts='[cX3;H1][cX3;H1][cX3;H1][sX2;H0][cX3;H1]') # Custom tuned - matches perfectly no extras, might need to be more slack in the future
UFSG[107] = UNIFAC_subgroup('C4H3S', 50, 'THIOPHEN', 2.6908, 1.86, smarts='[$([cX3;H1][cX3;H1][cX3;H1][sX2;H0][cX3;H0]),$([cX3;H1][cX3;H0][cX3;H1][sX2;H0][cX3;H1])]') # 1 extra - custom tuned
UFSG[108] = UNIFAC_subgroup('C4H2S', 50, 'THIOPHEN', 2.5247, 1.58, smarts='[cX3;H1,H0;r5][cX3;H1,H0;r5][cX3;H0,H1;r5][sX2;H0;r5][cX3;H0,H1;r5]') # Not sure if this is right - probably not!!!
UFSG[109] = UNIFAC_subgroup('NCO', 51, 'NCO', 1.0567, 0.732, smarts='[NX2]=[CX2]=[OX1]') # Bonds might need to be different - but this smarts matches them all so far
UFSG[118] = UNIFAC_subgroup('(CH2)2SU', 55, 'SULFONES', 2.6869, 2.12, smarts='CC[SX4](=O)(=O)') # TYPO on their part; Makes no sense for there to be CH3 groups
UFSG[119] = UNIFAC_subgroup('CH2CHSU', 55, 'SULFONES', 2.4595, 1.808, smarts='[CX4;H2][CX4;H1][SX4](=O)(=O)') # 3 missing of 6
UFSG[178] = UNIFAC_subgroup('IMIDAZOL', 84, 'IMIDAZOL', 2.026, 0.868, smarts='c1cnc[nH]1') # untested
UFSG[179] = UNIFAC_subgroup('BTI', 85, 'BTI', 5.774, 4.932, smarts='C(F)(F)(F)S(=O)(=O)[N-]S(=O)(=O)C(F)(F)F') # untested


# http://www.ddbst.com/PublishedParametersUNIFACDO.html#ListOfSubGroupsAndTheirGroupSurfacesAndVolumes
#  subgroup = (subgroup, #maingroup, maingroup, R, Q)
DOUFSG = {}
DOUFSG[1] = UNIFAC_subgroup('CH3', 1, 'CH2', 0.6325, 1.0608)
DOUFSG[2] = UNIFAC_subgroup('CH2', 1, 'CH2', 0.6325, 0.7081)
DOUFSG[3] = UNIFAC_subgroup('CH', 1, 'CH2', 0.6325, 0.3554)
DOUFSG[4] = UNIFAC_subgroup('C', 1, 'CH2', 0.6325, 0)
DOUFSG[5] = UNIFAC_subgroup('CH2=CH', 2, 'C=C', 1.2832, 1.6016)
DOUFSG[6] = UNIFAC_subgroup('CH=CH', 2, 'C=C', 1.2832, 1.2489)
DOUFSG[7] = UNIFAC_subgroup('CH2=C', 2, 'C=C', 1.2832, 1.2489)
DOUFSG[8] = UNIFAC_subgroup('CH=C', 2, 'C=C', 1.2832, 0.8962)
DOUFSG[9] = UNIFAC_subgroup('ACH', 3, 'ACH', 0.3763, 0.4321)
DOUFSG[10] = UNIFAC_subgroup('AC', 3, 'ACH', 0.3763, 0.2113)
DOUFSG[11] = UNIFAC_subgroup('ACCH3', 4, 'ACCH2', 0.91, 0.949)
DOUFSG[12] = UNIFAC_subgroup('ACCH2', 4, 'ACCH2', 0.91, 0.7962)
DOUFSG[13] = UNIFAC_subgroup('ACCH', 4, 'ACCH2', 0.91, 0.3769)
DOUFSG[14] = UNIFAC_subgroup('OH(P)', 5, 'OH', 1.2302, 0.8927)
DOUFSG[15] = UNIFAC_subgroup('CH3OH', 6, 'CH3OH', 0.8585, 0.9938)
DOUFSG[16] = UNIFAC_subgroup('H2O', 7, 'H2O', 1.7334, 2.4561)
DOUFSG[17] = UNIFAC_subgroup('ACOH', 8, 'ACOH', 1.08, 0.975)
DOUFSG[18] = UNIFAC_subgroup('CH3CO', 9, 'CH2CO', 1.7048, 1.67)
DOUFSG[19] = UNIFAC_subgroup('CH2CO', 9, 'CH2CO', 1.7048, 1.5542)
DOUFSG[20] = UNIFAC_subgroup('CHO', 10, 'CHO', 0.7173, 0.771)
DOUFSG[21] = UNIFAC_subgroup('CH3COO', 11, 'CCOO', 1.27, 1.6286)
DOUFSG[22] = UNIFAC_subgroup('CH2COO', 11, 'CCOO', 1.27, 1.4228)
DOUFSG[23] = UNIFAC_subgroup('HCOO', 12, 'HCOO', 1.9, 1.8)
DOUFSG[24] = UNIFAC_subgroup('CH3O', 13, 'CH2O', 1.1434, 1.6022)
DOUFSG[25] = UNIFAC_subgroup('CH2O', 13, 'CH2O', 1.1434, 1.2495)
DOUFSG[26] = UNIFAC_subgroup('CHO', 13, 'CH2O', 1.1434, 0.8968)
DOUFSG[27] = UNIFAC_subgroup('THF', 43, 'CY-CH2O', 1.7023, 1.8784)
DOUFSG[28] = UNIFAC_subgroup('CH3NH2', 14, 'CH2NH2', 1.6607, 1.6904)
DOUFSG[29] = UNIFAC_subgroup('CH2NH2', 14, 'CH2NH2', 1.6607, 1.3377)
DOUFSG[30] = UNIFAC_subgroup('CHNH2', 14, 'CH2NH2', 1.6607, 0.985)
DOUFSG[31] = UNIFAC_subgroup('CH3NH', 15, 'CH2NH', 1.368, 1.4332)
DOUFSG[32] = UNIFAC_subgroup('CH2NH', 15, 'CH2NH', 1.368, 1.0805)
DOUFSG[33] = UNIFAC_subgroup('CHNH', 15, 'CH2NH', 1.368, 0.7278)
DOUFSG[34] = UNIFAC_subgroup('CH3N', 16, '(C)3N', 1.0746, 1.176)
DOUFSG[35] = UNIFAC_subgroup('CH2N', 16, '(C)3N', 1.0746, 0.824)
DOUFSG[36] = UNIFAC_subgroup('ACNH2', 17, 'ACNH2', 1.1849, 0.8067)
DOUFSG[37] = UNIFAC_subgroup('AC2H2N', 18, 'PYRIDINE', 1.4578, 0.9022)
DOUFSG[38] = UNIFAC_subgroup('AC2HN', 18, 'PYRIDINE', 1.2393, 0.633)
DOUFSG[39] = UNIFAC_subgroup('AC2N', 18, 'PYRIDINE', 1.0731, 0.353)
DOUFSG[40] = UNIFAC_subgroup('CH3CN', 19, 'CH2CN', 1.5575, 1.5193)
DOUFSG[41] = UNIFAC_subgroup('CH2CN', 19, 'CH2CN', 1.5575, 1.1666)
DOUFSG[42] = UNIFAC_subgroup('COOH', 20, 'COOH', 0.8, 0.9215)
DOUFSG[43] = UNIFAC_subgroup('HCOOH', 44, 'HCOOH', 0.8, 1.2742)
DOUFSG[44] = UNIFAC_subgroup('CH2CL', 21, 'CCL', 0.9919, 1.3654)
DOUFSG[45] = UNIFAC_subgroup('CHCL', 21, 'CCL', 0.9919, 1.0127)
DOUFSG[46] = UNIFAC_subgroup('CCL', 21, 'CCL', 0.9919, 0.66)
DOUFSG[47] = UNIFAC_subgroup('CH2CL2', 22, 'CCL2', 1.8, 2.5)
DOUFSG[48] = UNIFAC_subgroup('CHCL2', 22, 'CCL2', 1.8, 2.1473)
DOUFSG[49] = UNIFAC_subgroup('CCL2', 22, 'CCL2', 1.8, 1.7946)
DOUFSG[50] = UNIFAC_subgroup('CHCL3', 45, 'CHCL3', 2.45, 2.8912)
DOUFSG[51] = UNIFAC_subgroup('CCL3', 23, 'CCL3', 2.65, 2.3778)
DOUFSG[52] = UNIFAC_subgroup('CCL4', 24, 'CCL4', 2.618, 3.1836)
DOUFSG[53] = UNIFAC_subgroup('ACCL', 25, 'ACCL', 0.5365, 0.3177)
DOUFSG[54] = UNIFAC_subgroup('CH3NO2', 26, 'CNO2', 2.644, 2.5)
DOUFSG[55] = UNIFAC_subgroup('CH2NO2', 26, 'CNO2', 2.5, 2.304)
DOUFSG[56] = UNIFAC_subgroup('CHNO2', 26, 'CNO2', 2.887, 2.241)
DOUFSG[57] = UNIFAC_subgroup('ACNO2', 27, 'ACNO2', 0.4656, 0.3589)
DOUFSG[58] = UNIFAC_subgroup('CS2', 28, 'CS2', 1.24, 1.068)
DOUFSG[59] = UNIFAC_subgroup('CH3SH', 29, 'CH3SH', 1.289, 1.762)
DOUFSG[60] = UNIFAC_subgroup('CH2SH', 29, 'CH3SH', 1.535, 1.316)
DOUFSG[61] = UNIFAC_subgroup('FURFURAL', 30, 'FURFURAL', 1.299, 1.289)
DOUFSG[62] = UNIFAC_subgroup('DOH', 31, 'DOH', 2.088, 2.4)
DOUFSG[63] = UNIFAC_subgroup('I', 32, 'I', 1.076, 0.9169)
DOUFSG[64] = UNIFAC_subgroup('BR', 33, 'BR', 1.209, 1.4)
DOUFSG[65] = UNIFAC_subgroup('CH=-C', 34, 'C=-C', 0.9214, 1.3)
DOUFSG[66] = UNIFAC_subgroup('C=-C', 34, 'C=-C', 1.303, 1.132)
DOUFSG[67] = UNIFAC_subgroup('DMSO', 35, 'DMSO', 3.6, 2.692)
DOUFSG[68] = UNIFAC_subgroup('ACRY', 36, 'ACRY', 1, 0.92)
DOUFSG[69] = UNIFAC_subgroup('CL-(C=C)', 37, 'CLCC', 0.5229, 0.7391)
DOUFSG[70] = UNIFAC_subgroup('C=C', 2, 'C=C', 1.2832, 0.4582)
DOUFSG[71] = UNIFAC_subgroup('ACF', 38, 'ACF', 0.8814, 0.7269)
DOUFSG[72] = UNIFAC_subgroup('DMF', 39, 'DMF', 2, 2.093)
DOUFSG[73] = UNIFAC_subgroup('HCON(..', 39, 'DMF', 2.381, 1.522)
DOUFSG[74] = UNIFAC_subgroup('CF3', 40, 'CF2', 1.284, 1.266)
DOUFSG[75] = UNIFAC_subgroup('CF2', 40, 'CF2', 1.284, 1.098)
DOUFSG[76] = UNIFAC_subgroup('CF', 40, 'CF2', 0.8215, 0.5135)
DOUFSG[77] = UNIFAC_subgroup('COO', 41, 'COO', 1.6, 0.9)
DOUFSG[78] = UNIFAC_subgroup('CY-CH2', 42, 'CY-CH2', 0.7136, 0.8635)
DOUFSG[79] = UNIFAC_subgroup('CY-CH', 42, 'CY-CH2', 0.3479, 0.1071)
DOUFSG[80] = UNIFAC_subgroup('CY-C', 42, 'CY-CH2', 0.347, 0)
DOUFSG[81] = UNIFAC_subgroup('OH(S)', 5, 'OH', 1.063, 0.8663)
DOUFSG[82] = UNIFAC_subgroup('OH(T)', 5, 'OH', 0.6895, 0.8345)
DOUFSG[83] = UNIFAC_subgroup('CY-CH2O', 43, 'CY-CH2O', 1.4046, 1.4)
DOUFSG[84] = UNIFAC_subgroup('TRIOXAN', 43, 'CY-CH2O', 1.0413, 1.0116)
DOUFSG[85] = UNIFAC_subgroup('CNH2', 14, 'CH2NH2', 1.6607, 0.985)
DOUFSG[86] = UNIFAC_subgroup('NMP', 46, 'CY-CONC', 3.981, 3.2)
DOUFSG[87] = UNIFAC_subgroup('NEP', 46, 'CY-CONC', 3.7543, 2.892)
DOUFSG[88] = UNIFAC_subgroup('NIPP', 46, 'CY-CONC', 3.5268, 2.58)
DOUFSG[89] = UNIFAC_subgroup('NTBP', 46, 'CY-CONC', 3.2994, 2.352)
# Is 90 missing? 
DOUFSG[91] = UNIFAC_subgroup('CONH2', 47, 'CONR', 1.4515, 1.248)
DOUFSG[92] = UNIFAC_subgroup('CONHCH3', 47, 'CONR', 1.5, 1.08)
# 93, 98, 99 missing but inteaction parameters are available.
DOUFSG[100] = UNIFAC_subgroup('CONHCH2', 47, 'CONR', 1.5, 1.08)
DOUFSG[101] = UNIFAC_subgroup('AM(CH3)2', 48, 'CONR2', 2.4748, 1.9643)
DOUFSG[102] = UNIFAC_subgroup('AMCH3CH2', 48, 'CONR2', 2.2739, 1.5754)
DOUFSG[103] = UNIFAC_subgroup('AM(CH2)2', 48, 'CONR2', 2.0767, 1.1866)
DOUFSG[104] = UNIFAC_subgroup('AC2H2S', 52, 'ACS', 1.7943, 1.34)
DOUFSG[105] = UNIFAC_subgroup('AC2HS', 52, 'ACS', 1.6282, 1.06)
DOUFSG[106] = UNIFAC_subgroup('AC2S', 52, 'ACS', 1.4621, 0.78)
DOUFSG[107] = UNIFAC_subgroup('H2COCH', 53, 'EPOXIDES', 1.3601, 1.8031)
DOUFSG[108] = UNIFAC_subgroup('COCH', 53, 'EPOXIDES', 0.683, 0.3418)
DOUFSG[109] = UNIFAC_subgroup('HCOCH', 53, 'EPOXIDES', 0.9104, 0.6538)
DOUFSG[110] = UNIFAC_subgroup('(CH2)2SU', 56, 'SULFONE', 2.687, 2.12)
DOUFSG[111] = UNIFAC_subgroup('CH2SUCH', 56, 'SULFONE', 2.46, 1.808)
DOUFSG[112] = UNIFAC_subgroup('(CH3)2CB', 55, 'CARBONAT', 2.42, 2.4976)
DOUFSG[113] = UNIFAC_subgroup('(CH2)2CB', 55, 'CARBONAT', 2.42, 2.0018)
DOUFSG[114] = UNIFAC_subgroup('CH2CH3CB', 55, 'CARBONAT', 2.42, 2.2497)
DOUFSG[119] = UNIFAC_subgroup('H2COCH2', 53, 'EPOXIDES', 1.063, 1.123)
DOUFSG[153] = UNIFAC_subgroup('H2COC', 53, 'EPOXIDES', 0.9104, 0.6538)
DOUFSG[178] = UNIFAC_subgroup('C3H2N2+', 84, 'IMIDAZOL', 1.7989, 0.64)
DOUFSG[179] = UNIFAC_subgroup('BTI-', 85, 'BTI', 5.8504, 5.7513)
DOUFSG[184] = UNIFAC_subgroup('C3H3N2+', 84, 'IMIDAZOL', 2.411, 2.409)
DOUFSG[189] = UNIFAC_subgroup('C4H8N+', 87, 'PYRROL', 2.7986, 2.7744)
DOUFSG[195] = UNIFAC_subgroup('BF4-', 89, 'BF4', 4.62, 1.1707)
DOUFSG[196] = UNIFAC_subgroup('C5H5N+', 90, 'PYRIDIN', 2.4878, 2.474)
DOUFSG[197] = UNIFAC_subgroup('OTF-', 91, 'OTF', 3.3854, 2.009)
# 122, 123, 124, 201 Added Rev. 6
DOUFSG[122] = UNIFAC_subgroup('CH3S', 61, 'SULFIDES', 1.6130, 1.3680)
DOUFSG[123] = UNIFAC_subgroup('CH2S', 61, 'SULFIDES', 1.3863, 1.0600)
DOUFSG[124] = UNIFAC_subgroup('CHS', 61, 'SULFIDES', 1.1589, 0.7480)
DOUFSG[201] = UNIFAC_subgroup('-S-S-', 93, 'DISULFIDES', 1.0678, 2.2440)

#  subgroup = (group, (subgroup ids))
# http://www.ddbst.com/PublishedParametersUNIFACDO.html#ListOfMainGroups
DOUFMG = {}
DOUFMG[1] = ('CH2', [1, 2, 3, 4])
DOUFMG[2] = ('C=C', [5, 6, 7, 8, 70])
DOUFMG[3] = ('ACH', [9, 10])
DOUFMG[4] = ('ACCH2', [11, 12, 13])
DOUFMG[5] = ('OH', [14, 81, 82])
DOUFMG[6] = ('CH3OH', [15])
DOUFMG[7] = ('H2O', [16])
DOUFMG[8] = ('ACOH', [17])
DOUFMG[9] = ('CH2CO', [18, 19])
DOUFMG[10] = ('CHO', [20])
DOUFMG[11] = ('CCOO', [21, 22])
DOUFMG[12] = ('HCOO', [23])
DOUFMG[13] = ('CH2O', [24, 25, 26])
DOUFMG[14] = ('CH2NH2', [28, 29, 30, 85])
DOUFMG[15] = ('CH2NH', [31, 32, 33])
DOUFMG[16] = ('(C)3N', [34, 35])
DOUFMG[17] = ('ACNH2', [36])
DOUFMG[18] = ('PYRIDINE', [37, 38, 39])
DOUFMG[19] = ('CH2CN', [40, 41])
DOUFMG[20] = ('COOH', [42])
DOUFMG[21] = ('CCL', [44, 45, 46])
DOUFMG[22] = ('CCL2', [47, 48, 49])
DOUFMG[23] = ('CCL3', [51])
DOUFMG[24] = ('CCL4', [52])
DOUFMG[25] = ('ACCL', [53])
DOUFMG[26] = ('CNO2', [54, 55, 56])
DOUFMG[27] = ('ACNO2', [57])
DOUFMG[28] = ('CS2', [58])
DOUFMG[29] = ('CH3SH', [59, 60])
DOUFMG[30] = ('FURFURAL', [61])
DOUFMG[31] = ('DOH', [62])
DOUFMG[32] = ('I', [63])
DOUFMG[33] = ('BR', [64])
DOUFMG[34] = ('C=-C', [65, 66])
DOUFMG[35] = ('DMSO', [67])
DOUFMG[36] = ('ACRY', [68])
DOUFMG[37] = ('CLCC', [69])
DOUFMG[38] = ('ACF', [71])
DOUFMG[39] = ('DMF', [72, 73])
DOUFMG[40] = ('CF2', [74, 75, 76])
DOUFMG[41] = ('COO', [77])
DOUFMG[42] = ('CY-CH2', [78, 79, 80])
DOUFMG[43] = ('CY-CH2O', [27, 83, 84])
DOUFMG[44] = ('HCOOH', [43])
DOUFMG[45] = ('CHCL3', [50])
DOUFMG[46] = ('CY-CONC', [86, 87, 88, 89])
DOUFMG[47] = ('CONR', [91, 92, 100])
DOUFMG[48] = ('CONR2', [101, 102, 103])
DOUFMG[49] = ('HCONR', [93, 94]) # Added in Further Development of Modified UNIFAC (Dortmund):  Revision and Extension 5
DOUFMG[52] = ('ACS', [104, 105, 106])
DOUFMG[53] = ('EPOXIDES', [107, 108, 109, 119, 153])
DOUFMG[55] = ('CARBONAT', [112, 113, 114])
DOUFMG[56] = ('SULFONE', [110, 111])
DOUFMG[84] = ('IMIDAZOL', [178, 184])
DOUFMG[85] = ('BTI', [179])
DOUFMG[87] = ('PYRROL', [189])
DOUFMG[89] = ('BF4', [195])
DOUFMG[90] = ('PYRIDIN', [196])
DOUFMG[91] = ('OTF', [197])
# Added Rev 6
DOUFMG[61] = ('SULFIDES', [122, 123, 124])
DOUFMG[93] = ('DISULFIDES', [201])


NISTUFMG = {}
# From Kang and Diky and Chirico and Magee and Muzny and Abdulagatov and Kazakov and Frenkel - 2011 - A new method for evaluation of UNIFAC interaction parameters
# + Some information extracted from below
NISTUFMG[1] = ('CH2', [1, 2, 3, 4], 'Alkyl chains')
NISTUFMG[2] = ('C=C', [5, 6, 7, 8, 9], 'Double bonded alkyl chains')
NISTUFMG[3] = ('ACH', [15, 16, 17], 'Aromatic carbon')
NISTUFMG[4] = ('ACCH2', [18, 19, 20, 21], 'Aromatic carbon plus alkyl chain')
NISTUFMG[5] = ('OH', [34, 204, 205], 'Alcohols')
NISTUFMG[6] = ('CH3OH', [35], 'Methanol')
NISTUFMG[7] = ('H2O', [36], 'Water')
NISTUFMG[8] = ('ACOH', [37], 'Phenolic –OH groups ')
NISTUFMG[9] = ('CH2CO', [42, 43, 44, 45], 'Ketones')
NISTUFMG[10] = ('CHO', [48], 'Aldehydes')
NISTUFMG[11] = ('CCOO', [51, 52, 53, 54], 'Esters')
NISTUFMG[12] = ('HCOO', [55], 'Formates')
NISTUFMG[13] = ('CH2O', [59, 60, 61, 62, 63], 'Ethers')
NISTUFMG[14] = ('CNH2', [66, 67, 68, 69], 'Amines with 1-alkyl group')
NISTUFMG[15] = ('(C)2NH', [71, 72, 73], 'Amines with 2-alkyl groups')
NISTUFMG[16] = ('(C)3N', [74, 75], 'Amines with 3-alkyl groups')
NISTUFMG[17] = ('ACNH2', [79, 80, 81], 'Anilines')
NISTUFMG[18] = ('PYRIDINE', [76, 77, 78], 'Pyridines')
NISTUFMG[19] = ('CCN', [85, 86, 87, 88], 'Nitriles')
NISTUFMG[20] = ('COOH', [94, 95], 'Acids')
NISTUFMG[21] = ('CCl', [99, 100, 101], 'Chlorocarbons')
NISTUFMG[22] = ('CCl2', [102, 103, 104], 'Dichlorocarbons')
NISTUFMG[23] = ('CCl3', [105, 106], 'Trichlorocarbons')
NISTUFMG[24] = ('CCl4', [107], 'Tetrachlorocarbons')
NISTUFMG[25] = ('ACCl', [109], 'Chloroaromatics')
NISTUFMG[26] = ('CNO2', [132, 133, 134, 135], 'Nitro alkanes')
NISTUFMG[27] = ('ACNO2', [136], 'Nitroaromatics')
NISTUFMG[28] = ('CS2', [146], 'Carbon disulfide')
NISTUFMG[29] = ('CH3SH', [138, 139, 140, 141], 'Mercaptans')
NISTUFMG[30] = ('FURFURAL', [50], 'Furfural')
NISTUFMG[31] = ('DOH', [38], 'Ethylene Glycol')
NISTUFMG[32] = ('I', [128], 'Iodides')
NISTUFMG[33] = ('BR', [130], 'Bromides')
NISTUFMG[34] = ('C≡C', [13, 14], 'Triplebonded alkyl chains')
NISTUFMG[35] = ('DMSO', [153], 'Dimethylsulfoxide')
NISTUFMG[36] = ('ACRY', [90], 'Acrylic')
NISTUFMG[37] = ('ClC=C', [108], 'Chlorine attached to double bonded alkyl chain')
NISTUFMG[38] = ('ACF', [118], 'Fluoroaromatics')
NISTUFMG[39] = ('DMF', [161, 162, 163, 164, 165], 'Amides')
NISTUFMG[40] = ('CF2', [111, 112, 113, 114, 115, 116, 117], 'Fluorines')
NISTUFMG[41] = ('COO', [58], 'Esters')
NISTUFMG[42] = ('SiH2', [197, 198, 199, 200], 'Silanes')
NISTUFMG[43] = ('SiO', [201, 202, 203], 'Siloxanes')
NISTUFMG[44] = ('NMP', [195], 'N-Methyl-2-pyrrolidone')
NISTUFMG[45] = ('CClF', [120, 121, 122, 123, 124, 125, 126, 127], 'Chloro-Fluorides')
NISTUFMG[46] = ('CONCH2', [166, 167, 168, 169], 'Amides')
NISTUFMG[47] = ('OCCOH', [39, 40, 41], 'Oxygenated Alcohols')
NISTUFMG[48] = ('CH2S', [142, 143, 144, 145], 'Sulfides')
NISTUFMG[49] = ('MORPHOLIN', [196], 'Morpholine')
NISTUFMG[50] = ('THIOPHENE', [147, 148, 149], 'Thiophene')
NISTUFMG[51] = ('CH2(cy)', [27, 28, 29], 'Cyclic hydrocarbon chains')
NISTUFMG[52] = ('C=C(cy)', [30, 31, 32], 'Cyclic unsaturated hydrocarbon chains')
# Added

NISTUFSG = {}
NISTUFSG[1] = UNIFAC_subgroup('CH3', 1, 'CH2', 0.6325, 1.0608)
NISTUFSG[2] = UNIFAC_subgroup('CH2', 1, 'CH2', 0.6325, 0.7081)
NISTUFSG[3] = UNIFAC_subgroup('CH', 1, 'CH2', 0.6325, 0.3554)
NISTUFSG[4] = UNIFAC_subgroup('C', 1, 'CH2', 0.6325, 0)
NISTUFSG[5] = UNIFAC_subgroup('CH2=CH', 2, 'C=C', 1.2832, 1.6016)
NISTUFSG[6] = UNIFAC_subgroup('CH=CH', 2, 'C=C', 1.2832, 1.2489)
NISTUFSG[7] = UNIFAC_subgroup('CH2=C', 2, 'C=C', 1.2832, 1.2489)
NISTUFSG[8] = UNIFAC_subgroup('CH=C', 2, 'C=C', 1.2832, 0.8962)
NISTUFSG[70] = UNIFAC_subgroup('C=C', 2, 'C=C', 1.2832, 0.4582)
NISTUFSG[9] = UNIFAC_subgroup('ACH', 3, 'ACH', 0.3763, 0.4321)
NISTUFSG[10] = UNIFAC_subgroup('AC', 3, 'ACH', 0.3763, 0.2113)
NISTUFSG[11] = UNIFAC_subgroup('ACCH3', 4, 'ACCH2', 0.91, 0.949)
NISTUFSG[12] = UNIFAC_subgroup('ACCH2', 4, 'ACCH2', 0.91, 0.7962)
NISTUFSG[13] = UNIFAC_subgroup('ACCH', 4, 'ACCH2', 0.91, 0.3769)
NISTUFSG[195] = UNIFAC_subgroup('ACC', 4, 'ACCH2', 0.5847, 0.12)
NISTUFSG[14] = UNIFAC_subgroup('OH prim', 5, 'OH', 1.2302, 0.8927)
NISTUFSG[81] = UNIFAC_subgroup('OH sec', 5, 'OH', 1.063, 0.8663)
NISTUFSG[82] = UNIFAC_subgroup('OH tert', 5, 'OH', 0.6895, 0.8345)
NISTUFSG[15] = UNIFAC_subgroup('CH3OH', 6, 'CH3OH', 0.8585, 0.9938)
NISTUFSG[16] = UNIFAC_subgroup('H2O', 7, 'H2O', 1.7334, 2.4561)
NISTUFSG[17] = UNIFAC_subgroup('ACOH', 8, 'ACOH', 1.08, 0.975)
NISTUFSG[18] = UNIFAC_subgroup('CH3CO', 9, 'CH2CO', 1.7048, 1.67)
NISTUFSG[19] = UNIFAC_subgroup('CH2CO', 9, 'CH2CO', 1.7048, 1.5542)
NISTUFSG[301] = UNIFAC_subgroup('CHCO', 9, 'CH2CO', 1.7048, 1.5542)
NISTUFSG[302] = UNIFAC_subgroup('CCO', 9, 'CH2CO', 1.7048, 1.5542)
NISTUFSG[20] = UNIFAC_subgroup('CHO', 10, 'CHO', 0.7173, 0.771)
NISTUFSG[308] = UNIFAC_subgroup('HCHO', 10, 'CHO', 0.7173, 0.771)
NISTUFSG[21] = UNIFAC_subgroup('CH3COO', 11, 'CCOO', 1.27, 1.6286)
NISTUFSG[22] = UNIFAC_subgroup('CH2COO', 11, 'CCOO', 1.27, 1.4228)
NISTUFSG[23] = UNIFAC_subgroup('HCOO', 12, 'HCOO', 1.9, 1.8)
NISTUFSG[24] = UNIFAC_subgroup('CH3O', 13, 'CH2O', 1.1434, 1.6022)
NISTUFSG[25] = UNIFAC_subgroup('CH2O', 13, 'CH2O', 1.1434, 1.2495)
NISTUFSG[26] = UNIFAC_subgroup('CHO', 13, 'CH2O', 1.1434, 0.8968)
NISTUFSG[28] = UNIFAC_subgroup('CH3NH2', 14, 'CNH2', 1.6607, 1.6904)
NISTUFSG[29] = UNIFAC_subgroup('CH2NH2', 14, 'CNH2', 1.6607, 1.3377)
NISTUFSG[30] = UNIFAC_subgroup('CHNH2', 14, 'CNH2', 1.6607, 0.985)
NISTUFSG[85] = UNIFAC_subgroup('CNH2', 14, 'CNH2', 1.6607, 0.985)
NISTUFSG[31] = UNIFAC_subgroup('CH3NH', 15, 'CNH', 1.368, 1.4332)
NISTUFSG[32] = UNIFAC_subgroup('CH2NH', 15, 'CNH', 1.368, 1.0805)
NISTUFSG[33] = UNIFAC_subgroup('CHNH', 15, 'CNH', 1.368, 0.7278)
NISTUFSG[34] = UNIFAC_subgroup('CH3N', 16, '(C)3N', 1.0746, 1.176)
NISTUFSG[35] = UNIFAC_subgroup('CH2N', 16, '(C)3N', 1.0746, 0.824)
NISTUFSG[36] = UNIFAC_subgroup('ACNH2', 17, 'ACNH2', 1.1849, 0.8067)
NISTUFSG[306] = UNIFAC_subgroup('ACNH', 17, 'ACNH2', 1.1849, 0.732)
NISTUFSG[307] = UNIFAC_subgroup('ACN', 17, 'ACNH2', 1.1849, 0.61)
NISTUFSG[37] = UNIFAC_subgroup('AC2H2N', 18, 'Pyridine', 1.4578, 0.9022)
NISTUFSG[38] = UNIFAC_subgroup('AC2HN', 18, 'Pyridine', 1.2393, 0.633)
NISTUFSG[39] = UNIFAC_subgroup('AC2N', 18, 'Pyridine', 1.0731, 0.353)
NISTUFSG[196] = UNIFAC_subgroup('AC2H2NH', 94, 'Pyrrole', 1.325, 0.752)
NISTUFSG[197] = UNIFAC_subgroup('AC2HNH', 94, 'Pyrrole', 1.0976, 0.44)
NISTUFSG[198] = UNIFAC_subgroup('AC2NH', 94, 'Pyrrole', 0.8701, 0.212)
NISTUFSG[40] = UNIFAC_subgroup('CH3CN', 19, 'CCN', 1.5575, 1.5193)
NISTUFSG[41] = UNIFAC_subgroup('CH2CN', 19, 'CCN', 1.5575, 1.1666)
NISTUFSG[303] = UNIFAC_subgroup('CHCN', 19, 'CCN', 1.5575, 1.1666)
NISTUFSG[304] = UNIFAC_subgroup('CCN', 19, 'CCN', 1.5575, 1.1666)
NISTUFSG[42] = UNIFAC_subgroup('COOH', 20, 'COOH', 0.8, 0.9215)
NISTUFSG[44] = UNIFAC_subgroup('CH2Cl', 21, 'CCl', 0.9919, 1.3654)
NISTUFSG[45] = UNIFAC_subgroup('CHCl', 21, 'CCl', 0.9919, 1.0127)
NISTUFSG[46] = UNIFAC_subgroup('CCl', 21, 'CCl', 0.9919, 0.66)
NISTUFSG[47] = UNIFAC_subgroup('CH2Cl2', 22, 'CCl2', 1.8, 2.5)
NISTUFSG[48] = UNIFAC_subgroup('CHCl2', 22, 'CCl2', 1.8, 2.1473)
NISTUFSG[49] = UNIFAC_subgroup('CCl2', 22, 'CCl2', 1.8, 1.7946)
NISTUFSG[51] = UNIFAC_subgroup('CCl3', 23, 'CCl3', 2.65, 2.3778)
NISTUFSG[52] = UNIFAC_subgroup('CCl4', 52, 'CCl4', 2.618, 3.1863)
NISTUFSG[53] = UNIFAC_subgroup('ACCl', 53, 'ACCl', 0.5365, 0.3177)
NISTUFSG[54] = UNIFAC_subgroup('CH3NO2', 26, 'CNO2', 2.644, 2.5)
NISTUFSG[55] = UNIFAC_subgroup('CH2NO2', 26, 'CNO2', 2.5, 2.304)
NISTUFSG[56] = UNIFAC_subgroup('CHNO2', 26, 'CNO2', 2.887, 2.241)
NISTUFSG[305] = UNIFAC_subgroup('CNO2', 26, 'CNO2', 2.887, 2.241)
NISTUFSG[57] = UNIFAC_subgroup('ACNO2', 27, 'ACNO2', 0.4656, 0.3589)
NISTUFSG[58] = UNIFAC_subgroup('CS2', 28, 'CS2', 1.24, 1.068)
NISTUFSG[59] = UNIFAC_subgroup('CH3SH', 29, 'CH2SH', 1.289, 1.762)
NISTUFSG[60] = UNIFAC_subgroup('CH2SH', 29, 'CH2SH', 1.535, 1.316)
NISTUFSG[192] = UNIFAC_subgroup('CHSH', 29, 'CH2SH', 1.4232, 1.21)
NISTUFSG[193] = UNIFAC_subgroup('CSH', 29, 'CH2SH', 1.1958, 1.1401)
NISTUFSG[194] = UNIFAC_subgroup('ACSH', 29, 'CH2SH', 1.2887, 1.2)
NISTUFSG[61] = UNIFAC_subgroup('Furfural', 30, 'Furfural', 1.299, 1.289)
NISTUFSG[62] = UNIFAC_subgroup('CH2(OH)-CH2(OH)', 31, 'DOH', 3.7374, 3.2016)
NISTUFSG[205] = UNIFAC_subgroup('-CH(OH)-CH2(OH)', 31, 'DOH', 3.5642, 2.8225)
NISTUFSG[206] = UNIFAC_subgroup('-CH(OH)-CH(OH)-', 31, 'DOH', 3.391, 2.4434)
NISTUFSG[207] = UNIFAC_subgroup('>C(OH)-CH2(OH)', 31, 'DOH', 3.1847, 2.1144)
NISTUFSG[208] = UNIFAC_subgroup('>C(OH)-CH(OH)-', 31, 'DOH', 3.0175, 2.0562)
NISTUFSG[209] = UNIFAC_subgroup('>C(OH)-C(OH)<', 31, 'DOH', 2.644, 1.669)
NISTUFSG[63] = UNIFAC_subgroup('I', 32, 'I', 1.076, 0.9169)
NISTUFSG[64] = UNIFAC_subgroup('Br', 33, 'Br', 1.209, 1.4)
NISTUFSG[65] = UNIFAC_subgroup('CH#C', 34, 'C#C', 0.9214, 1.3)
NISTUFSG[66] = UNIFAC_subgroup('C#C', 34, 'C#C', 1.303, 1.132)
NISTUFSG[67] = UNIFAC_subgroup('DMSO', 35, 'DMSO', 3.6, 2.692)
NISTUFSG[68] = UNIFAC_subgroup('Acrylonitrile', 36, 'Acrylonitrile', 1, 0.92)
NISTUFSG[69] = UNIFAC_subgroup('Cl-(C=C)', 37, 'Cl-(C=C)', 0.5229, 0.7391)
NISTUFSG[71] = UNIFAC_subgroup('ACF', 38, 'ACF', 0.8814, 0.7269)
NISTUFSG[72] = UNIFAC_subgroup('DMF', 39, 'DMF', 2, 2.093)
NISTUFSG[73] = UNIFAC_subgroup('HCON(CH2)2', 39, 'DMF', 2.381, 1.522)
NISTUFSG[74] = UNIFAC_subgroup('CF3', 40, 'CF2', 2.7489, 2.7769)
NISTUFSG[75] = UNIFAC_subgroup('CF2', 40, 'CF2', 1.4778, 1.4738)
NISTUFSG[76] = UNIFAC_subgroup('CF', 40, 'CF2', 0.8215, 0.5135)
NISTUFSG[77] = UNIFAC_subgroup('COO', 41, 'COO', 1.6, 0.9)
NISTUFSG[78] = UNIFAC_subgroup('c-CH2', 42, 'c-CH2', 0.7136, 0.8635)
NISTUFSG[79] = UNIFAC_subgroup('c-CH', 42, 'c-CH2', 0.3479, 0.1071)
NISTUFSG[80] = UNIFAC_subgroup('c-C', 42, 'c-CH2', 0.347, 0)
NISTUFSG[27] = UNIFAC_subgroup('CH2-O-CH2', 43, 'c-CH2O', 1.7023, 1.8784)
NISTUFSG[83] = UNIFAC_subgroup('CH2-O-[CH2-O]1/2', 43, 'c-CH2O', 1.4046, 1.4)
NISTUFSG[84] = UNIFAC_subgroup('[O-CH2]1/2-O-[CH2-O]1/2', 43, 'c-CH2O', 1.0413, 1.0116)
NISTUFSG[43] = UNIFAC_subgroup('HCOOH', 44, 'HCOOH', 0.8, 1.2742)
NISTUFSG[50] = UNIFAC_subgroup('CHCl3', 45, 'CHCl3', 2.45, 2.8912)
NISTUFSG[86] = UNIFAC_subgroup('c-CON-CH3', 46, 'c-CONC', 3.981, 3.2)
NISTUFSG[87] = UNIFAC_subgroup('c-CON-CH2', 46, 'c-CONC', 3.7543, 2.892)
NISTUFSG[88] = UNIFAC_subgroup('c-CON-CH', 46, 'c-CONC', 3.5268, 2.58)
NISTUFSG[89] = UNIFAC_subgroup('c-CON-C', 46, 'c-CONC', 3.2994, 2.352)
NISTUFSG[92] = UNIFAC_subgroup('CONHCH3', 47, 'CONR', 1.5, 1.08)
NISTUFSG[100] = UNIFAC_subgroup('CONHCH2', 47, 'CONR', 1.5, 1.08)
NISTUFSG[101] = UNIFAC_subgroup('CON(CH3)2', 48, 'CONR2', 2.4748, 1.9643)
NISTUFSG[102] = UNIFAC_subgroup('CON(CH3)CH2', 48, 'CONR2', 2.2739, 1.5754)
NISTUFSG[103] = UNIFAC_subgroup('CON(CH2)2', 48, 'CONR2', 2.0767, 1.1866)
NISTUFSG[93] = UNIFAC_subgroup('HCONHCH3', 49, 'HCONR', 2.4617, 2.192)
NISTUFSG[94] = UNIFAC_subgroup('HCONHCH2', 49, 'HCONR', 2.4617, 1.842)
NISTUFSG[116] = UNIFAC_subgroup('ACCN', 50, 'ACCN', 1.2815, 0.96)
NISTUFSG[117] = UNIFAC_subgroup('CH3NCO', 51, 'NCO', 1.9578, 1.58)
NISTUFSG[118] = UNIFAC_subgroup('CH2NCO', 51, 'NCO', 1.731, 1.272)
NISTUFSG[119] = UNIFAC_subgroup('CHNCO', 51, 'NCO', 1.5036, 0.96)
NISTUFSG[120] = UNIFAC_subgroup('ACNCO', 51, 'NCO', 1.4219, 0.852)
NISTUFSG[104] = UNIFAC_subgroup('AC2H2S', 52, 'ACS', 1.7943, 1.34)
NISTUFSG[105] = UNIFAC_subgroup('AC2HS', 52, 'ACS', 1.6282, 1.06)
NISTUFSG[106] = UNIFAC_subgroup('AC2S', 52, 'ACS', 1.4621, 0.78)
NISTUFSG[107] = UNIFAC_subgroup('H2COCH', 53, 'Epoxy', 1.3601, 1.8031)
NISTUFSG[109] = UNIFAC_subgroup('HCOCH', 53, 'Epoxy', 0.9104, 0.6538)
NISTUFSG[121] = UNIFAC_subgroup('COOCO', 54, 'Anhydride', 1.7732, 1.52)
NISTUFSG[112] = UNIFAC_subgroup('(CH3O)2CO', 55, 'Carbonate', 3.0613, 2.816)
NISTUFSG[113] = UNIFAC_subgroup('(CH2O)2CO', 55, 'Carbonate', 2.6078, 2.2)
NISTUFSG[114] = UNIFAC_subgroup('(CH3O)COOCH2', 55, 'Carbonate', 2.8214, 2.508)
NISTUFSG[199] = UNIFAC_subgroup('(ACO)COOCH2', 55, 'Carbonate', 2.2854, 1.78)
NISTUFSG[200] = UNIFAC_subgroup('(ACO)CO(OAC)', 55, 'Carbonate', 1.9895, 1.36)
NISTUFSG[110] = UNIFAC_subgroup('CH2SuCH2', 56, 'Sulfone', 2.687, 2.12)
NISTUFSG[111] = UNIFAC_subgroup('CH2SuCH ', 56, 'Sulfone', 2.46, 1.808)
NISTUFSG[122] = UNIFAC_subgroup('ACSO2', 56, 'Sulfone', 1.7034, 1.16)
NISTUFSG[123] = UNIFAC_subgroup('ACCHO', 57, 'ACCHO', 1.3632, 1.068)
NISTUFSG[124] = UNIFAC_subgroup('ACCOOH', 58, 'ACCOOH', 1.6664, 1.344)
NISTUFSG[127] = UNIFAC_subgroup('AC-O-CO-CH3 ', 59, 'AC-O-CO', 2.2815, 1.848)
NISTUFSG[128] = UNIFAC_subgroup('AC-O-CO-CH2', 59, 'AC-O-CO', 2.0547, 1.54)
NISTUFSG[129] = UNIFAC_subgroup('AC-O-CO-CH', 59, 'AC-O-CO', 1.8273, 1.228)
NISTUFSG[130] = UNIFAC_subgroup('AC-O-CO-C', 59, 'AC-O-CO', 1.5999, 1)
NISTUFSG[131] = UNIFAC_subgroup('-O-CH2-CH2-OH', 60, 'OCCOH', 2.1226, 1.904)
NISTUFSG[132] = UNIFAC_subgroup('-O-CH-CH2-OH', 60, 'OCCOH', 1.8952, 1.592)
NISTUFSG[133] = UNIFAC_subgroup('-O-CH2-CH-OH', 60, 'OCCOH', 1.8952, 1.592)
NISTUFSG[134] = UNIFAC_subgroup('CH3-S-', 61, 'CH2S', 1.6131, 1.368)
NISTUFSG[135] = UNIFAC_subgroup('-CH2-S-', 61, 'CH2S', 1.3863, 1.06)
NISTUFSG[136] = UNIFAC_subgroup('>CH-S-', 61, 'CH2S', 1.1589, 0.748)
NISTUFSG[137] = UNIFAC_subgroup('->C-S-', 61, 'CH2S', 0.9314, 0.52)
NISTUFSG[187] = UNIFAC_subgroup('ACS', 61, 'CH2S', 1.0771, 0.64)
NISTUFSG[125] = UNIFAC_subgroup('c-CO-NH', 62, 'Lactam', 1.3039, 1.036)
NISTUFSG[126] = UNIFAC_subgroup('c-CO-O', 63, 'Lactone', 1.0152, 0.88)
NISTUFSG[138] = UNIFAC_subgroup('CH3O-(O)', 64, 'Peroxide', 1.3889, 1.328)
NISTUFSG[139] = UNIFAC_subgroup('CH2O-(O)', 64, 'Peroxide', 1.1622, 1.02)
NISTUFSG[140] = UNIFAC_subgroup('CHO-(O)', 64, 'Peroxide', 0.9347, 0.708)
NISTUFSG[141] = UNIFAC_subgroup('CO-(O)', 64, 'Peroxide', 1.0152, 0.88)
NISTUFSG[142] = UNIFAC_subgroup('ACO-(O)', 64, 'Peroxide', 0.853, 0.6)
NISTUFSG[143] = UNIFAC_subgroup('CFH', 65, 'CFH', 0.5966, 0.44)
NISTUFSG[144] = UNIFAC_subgroup('CFCl', 66, 'CFCl', 1.4034, 1.168)
NISTUFSG[145] = UNIFAC_subgroup('CFCl2', 67, 'CFCl2', 2.2103, 1.896)
NISTUFSG[146] = UNIFAC_subgroup('CF2H', 68, 'CF2H', 0.9736, 0.88)
NISTUFSG[147] = UNIFAC_subgroup('CF2ClH', 69, 'CF2ClH', 1.7396, 1.6)
NISTUFSG[148] = UNIFAC_subgroup('CF2Cl2', 70, 'CF2Cl2', 2.5873, 2.336)
NISTUFSG[149] = UNIFAC_subgroup('CF3H', 71, 'CF3H', 1.3507, 1.32)
NISTUFSG[150] = UNIFAC_subgroup('CF3Cl', 72, 'CF3Cl', 2.1575, 2.048)
NISTUFSG[151] = UNIFAC_subgroup('CF4', 73, 'CF4', 1.7278, 1.76)
NISTUFSG[152] = UNIFAC_subgroup('C(O)2', 74, 'Acetal', 0.7073, 0.48)
NISTUFSG[186] = UNIFAC_subgroup('CH(O)2', 74, 'Acetal', 0.9347, 0.708)
NISTUFSG[309] = UNIFAC_subgroup('CH2(O)2', 74, 'Acetal', 0.9347, 0.708)
NISTUFSG[153] = UNIFAC_subgroup('ACN(CH3)2', 75, 'ACNR2', 2.4529, 1.908)
NISTUFSG[154] = UNIFAC_subgroup('ACN(CH3)CH2', 75, 'ACNR2', 2.2261, 1.6)
NISTUFSG[155] = UNIFAC_subgroup('ACN(CH2)2', 75, 'ACNR2', 1.9993, 1.292)
NISTUFSG[156] = UNIFAC_subgroup('ACNHCH3', 76, 'ACNR', 1.7989, 1.364)
NISTUFSG[157] = UNIFAC_subgroup('ACNHCH2', 76, 'ACNR', 1.5722, 1.056)
NISTUFSG[158] = UNIFAC_subgroup('ACNHCH', 76, 'ACNR', 1.3448, 0.744)
NISTUFSG[159] = UNIFAC_subgroup('AC2H2O', 77, 'Furan', 1.3065, 1.04)
NISTUFSG[160] = UNIFAC_subgroup('AC2HO', 77, 'Furan', 1.1404, 0.76)
NISTUFSG[161] = UNIFAC_subgroup('AC2O', 77, 'Furan', 0.9743, 0.48)
NISTUFSG[188] = UNIFAC_subgroup('c-CH2-NH', 78, 'c-CNH', 1.207, 0.936)
NISTUFSG[162] = UNIFAC_subgroup('c-CH-NH', 78, 'c-CNH', 0.9796, 0.624)
NISTUFSG[163] = UNIFAC_subgroup('c-C-NH', 78, 'c-CNH', 0.7521, 0.396)
NISTUFSG[189] = UNIFAC_subgroup('c-CH2-NCH3', 79, 'c-CNR', 1.8609, 1.48)
NISTUFSG[190] = UNIFAC_subgroup('c-CH2-NCH2', 79, 'c-CNR', 1.6341, 1.172)
NISTUFSG[191] = UNIFAC_subgroup('c-CH2-NCH', 79, 'c-CNR', 1.4067, 0.86)
NISTUFSG[164] = UNIFAC_subgroup('c-CH-NCH3', 79, 'c-CNR', 1.6335, 1.168)
NISTUFSG[165] = UNIFAC_subgroup('c-CH-NCH2', 79, 'c-CNR', 1.4067, 0.86)
NISTUFSG[166] = UNIFAC_subgroup('c-CH-NCH', 79, 'c-CNR', 1.1793, 0.548)
NISTUFSG[170] = UNIFAC_subgroup('SiH3-', 80, 'SiH', 1.6035, 1.263)
NISTUFSG[171] = UNIFAC_subgroup('-SiH2-', 80, 'SiH', 1.4443, 1.006)
NISTUFSG[172] = UNIFAC_subgroup('>SiH-', 80, 'SiH', 1.2853, 0.749)
NISTUFSG[173] = UNIFAC_subgroup('>Si<', 80, 'SiH', 1.047, 0.41)
NISTUFSG[174] = UNIFAC_subgroup('-SiH2-O-', 81, 'SiO', 1.4838, 1.062)
NISTUFSG[175] = UNIFAC_subgroup('>SiH-O-', 81, 'SiO', 1.303, 0.764)
NISTUFSG[176] = UNIFAC_subgroup('->Si-O-', 81, 'SiO', 1.1044, 0.466)
NISTUFSG[309] = UNIFAC_subgroup('CH=NOH', 82, 'Oxime', 1.499, 1.46)
NISTUFSG[177] = UNIFAC_subgroup('C=NOH', 82, 'Oxime', 1.499, 1.46)
NISTUFSG[178] = UNIFAC_subgroup('ACCO', 83, 'ACCO', 1.1365, 0.76)
NISTUFSG[179] = UNIFAC_subgroup('C2Cl4', 86, 'C2Cl4', 3.381, 3.5845)
NISTUFSG[180] = UNIFAC_subgroup('c-CHH2', 92, 'c-CHNH2', 1.2261, 1.096)
NISTUFSG[201] = UNIFAC_subgroup('c-CH=CH', 95, 'c-C=C', 1.0897, 0.832)
NISTUFSG[202] = UNIFAC_subgroup('c-CH=C', 95, 'c-C=C', 0.8616, 0.644)
NISTUFSG[203] = UNIFAC_subgroup('c-C=C', 95, 'c-C=C', 0.5498, 0.244)
NISTUFSG[204] = UNIFAC_subgroup('Glycerol', 96, 'Glycerol', 5.4209, 4.4227)


PSRKSG = {}
PSRKSG[1] = UNIFAC_subgroup('CH3', 1, 'CH2', 0.9011, 0.8480)
PSRKSG[2] = UNIFAC_subgroup('CH2', 1, 'CH2', 0.6744, 0.5400)
PSRKSG[3] = UNIFAC_subgroup('CH', 1, 'CH2', 0.4469, 0.2280)
PSRKSG[4] = UNIFAC_subgroup('C', 1, 'CH2', 0.2195, 0.0000)
PSRKSG[5] = UNIFAC_subgroup('CH2=CH', 2, 'C=C', 1.3454, 1.1760)
PSRKSG[6] = UNIFAC_subgroup('CH=CH', 2, 'C=C', 1.1167, 0.8670)
PSRKSG[7] = UNIFAC_subgroup('CH2=C', 2, 'C=C', 1.1173, 0.9880)
PSRKSG[8] = UNIFAC_subgroup('CH=C', 2, 'C=C', 0.8886, 0.6760)
PSRKSG[9] = UNIFAC_subgroup('ACH', 3, 'ACH', 0.5313, 0.4000)
PSRKSG[10] = UNIFAC_subgroup('AC', 3, 'ACH', 0.3652, 0.1200)
PSRKSG[11] = UNIFAC_subgroup('ACCH3', 4, 'ACCH2', 1.2663, 0.9680)
PSRKSG[12] = UNIFAC_subgroup('ACCH2', 4, 'ACCH2', 1.0396, 0.6600)
PSRKSG[13] = UNIFAC_subgroup('ACCH', 4, 'ACCH2', 0.8121, 0.3480)
PSRKSG[14] = UNIFAC_subgroup('OH', 5, 'OH', 1.0000, 1.2000)
PSRKSG[15] = UNIFAC_subgroup('CH3OH', 6, 'CH3OH', 1.4311, 1.4320)
PSRKSG[16] = UNIFAC_subgroup('H2O', 7, 'H2O', 0.9200, 1.4000)
PSRKSG[17] = UNIFAC_subgroup('ACOH', 8, 'ACOH', 0.8952, 0.6800)
PSRKSG[18] = UNIFAC_subgroup('CH3CO', 9, 'CH2CO', 1.6724, 1.4880)
PSRKSG[19] = UNIFAC_subgroup('CH2CO', 9, 'CH2CO', 1.4457, 1.1800)
PSRKSG[20] = UNIFAC_subgroup('CHO', 10, 'CHO', 0.9980, 0.9480)
PSRKSG[21] = UNIFAC_subgroup('CH3COO', 11, 'CCOO', 1.9031, 1.7280)
PSRKSG[22] = UNIFAC_subgroup('CH2COO', 11, 'CCOO', 1.6764, 1.4200)
PSRKSG[23] = UNIFAC_subgroup('HCOO', 12, 'HCOO', 1.2420, 1.1880)
PSRKSG[24] = UNIFAC_subgroup('CH3O', 13, 'CH2O', 1.1450, 1.0880)
PSRKSG[25] = UNIFAC_subgroup('CH2O', 13, 'CH2O', 0.9183, 0.7800)
PSRKSG[26] = UNIFAC_subgroup('CHO', 13, 'CH2O', 0.6908, 0.4680)
PSRKSG[27] = UNIFAC_subgroup('THF', 13, 'CH2O', 0.9183, 1.1000)
PSRKSG[28] = UNIFAC_subgroup('CH3NH2', 14, 'CNH2', 1.5959, 1.5440)
PSRKSG[29] = UNIFAC_subgroup('CH2NH2', 14, 'CNH2', 1.3692, 1.2360)
PSRKSG[30] = UNIFAC_subgroup('CHNH2', 14, 'CNH2', 1.1417, 0.9240)
PSRKSG[31] = UNIFAC_subgroup('CH3NH', 15, 'CNH', 1.4337, 1.2440)
PSRKSG[32] = UNIFAC_subgroup('CH2NH', 15, 'CNH', 1.2070, 0.9360)
PSRKSG[33] = UNIFAC_subgroup('CHNH', 15, 'CNH', 0.9795, 0.6240)
PSRKSG[34] = UNIFAC_subgroup('CH3N', 16, '(C)3N', 1.1865, 0.9400)
PSRKSG[35] = UNIFAC_subgroup('CH2N', 16, '(C)3N', 0.9597, 0.6320)
PSRKSG[36] = UNIFAC_subgroup('ACNH2', 17, 'ACNH2', 1.0600, 0.8160)
PSRKSG[37] = UNIFAC_subgroup('C5H5N', 18, 'PYRIDINE', 2.9993, 2.1130)
PSRKSG[38] = UNIFAC_subgroup('C5H4N', 18, 'PYRIDINE', 2.8332, 1.8330)
PSRKSG[39] = UNIFAC_subgroup('C5H3N', 18, 'PYRIDINE', 2.6670, 1.5530)
PSRKSG[40] = UNIFAC_subgroup('CH3CN', 19, 'CCN', 1.8701, 1.7240)
PSRKSG[41] = UNIFAC_subgroup('CH2CN', 19, 'CCN', 1.6434, 1.4160)
PSRKSG[42] = UNIFAC_subgroup('COOH', 20, 'COOH', 1.3013, 1.2240)
PSRKSG[43] = UNIFAC_subgroup('HCOOH', 20, 'COOH', 1.5280, 1.5320)
PSRKSG[44] = UNIFAC_subgroup('CH2CL', 21, 'CCL', 1.4654, 1.2640)
PSRKSG[45] = UNIFAC_subgroup('CHCL', 21, 'CCL', 1.2380, 0.9520)
PSRKSG[46] = UNIFAC_subgroup('CCL', 21, 'CCL', 1.0106, 0.7240)
PSRKSG[47] = UNIFAC_subgroup('CH2CL2', 22, 'CCL2', 2.2564, 1.9880)
PSRKSG[48] = UNIFAC_subgroup('CHCL2', 22, 'CCL2', 2.0606, 1.6840)
PSRKSG[49] = UNIFAC_subgroup('CCL2', 22, 'CCL2', 1.8016, 1.4480)
PSRKSG[50] = UNIFAC_subgroup('CHCL3', 23, 'CCL3', 2.8700, 2.4100)
PSRKSG[51] = UNIFAC_subgroup('CCL3', 23, 'CCL3', 2.6401, 2.1840)
PSRKSG[52] = UNIFAC_subgroup('CCL4', 24, 'CCL4', 3.3900, 2.9100)
PSRKSG[53] = UNIFAC_subgroup('ACCL', 25, 'ACCL', 1.1562, 0.8440)
PSRKSG[54] = UNIFAC_subgroup('CH3NO2', 26, 'CNO2', 2.0086, 1.8680)
PSRKSG[55] = UNIFAC_subgroup('CH2NO2', 26, 'CNO2', 1.7818, 1.5600)
PSRKSG[56] = UNIFAC_subgroup('CHNO2', 26, 'CNO2', 1.5544, 1.2480)
PSRKSG[57] = UNIFAC_subgroup('ACNO2', 27, 'ACNO2', 1.4199, 1.1040)
PSRKSG[58] = UNIFAC_subgroup('CS2', 28, 'CS2', 2.0570, 1.6500)
PSRKSG[59] = UNIFAC_subgroup('CH3SH', 29, 'CH3SH', 1.8770, 1.6760)
PSRKSG[60] = UNIFAC_subgroup('CH2SH', 29, 'CH3SH', 1.6510, 1.3680)
PSRKSG[61] = UNIFAC_subgroup('FURFURAL', 30, 'FURFURAL', 3.1680, 2.4840)
PSRKSG[62] = UNIFAC_subgroup('DOH', 31, 'DOH', 2.4088, 2.2480)
PSRKSG[63] = UNIFAC_subgroup('I', 32, 'I', 1.2640, 0.9920)
PSRKSG[64] = UNIFAC_subgroup('BR', 33, 'BR', 0.9492, 0.8320)
PSRKSG[65] = UNIFAC_subgroup('CH=-C', 34, 'C=-C', 1.2920, 1.0880)
PSRKSG[66] = UNIFAC_subgroup('C=-C', 34, 'C=-C', 1.0613, 0.7840)
PSRKSG[67] = UNIFAC_subgroup('DMSO', 35, 'DMSO', 2.8266, 2.4720)
PSRKSG[68] = UNIFAC_subgroup('ACRY', 36, 'ACRY', 2.3144, 2.0520)
PSRKSG[69] = UNIFAC_subgroup('CL-(C=C)', 37, 'CLCC', 0.7910, 0.7240)
PSRKSG[70] = UNIFAC_subgroup('C=C', 2, 'C=C', 0.6605, 0.4850)
PSRKSG[71] = UNIFAC_subgroup('ACF', 38, 'ACF', 0.6948, 0.5240)
PSRKSG[72] = UNIFAC_subgroup('DMF', 39, 'DMF', 3.0856, 2.7360)
PSRKSG[73] = UNIFAC_subgroup('HCON(..', 39, 'DMF', 2.6322, 2.1200)
PSRKSG[74] = UNIFAC_subgroup('CF3', 40, 'CF2', 1.4060, 1.3800)
PSRKSG[75] = UNIFAC_subgroup('CF2', 40, 'CF2', 1.0105, 0.9200)
PSRKSG[76] = UNIFAC_subgroup('CF', 40, 'CF2', 0.6150, 0.4600)
PSRKSG[77] = UNIFAC_subgroup('COO', 41, 'COO', 1.3800, 1.2000)
PSRKSG[78] = UNIFAC_subgroup('SIH3', 42, 'SIH2', 1.6035, 1.2632)
PSRKSG[79] = UNIFAC_subgroup('SIH2', 42, 'SIH2', 1.4443, 1.0063)
PSRKSG[80] = UNIFAC_subgroup('SIH', 42, 'SIH2', 1.2853, 0.7494)
PSRKSG[81] = UNIFAC_subgroup('SI', 42, 'SIH2', 1.0470, 0.4099)
PSRKSG[82] = UNIFAC_subgroup('SIH2O', 43, 'SIO', 1.4838, 1.0621)
PSRKSG[83] = UNIFAC_subgroup('SIHO', 43, 'SIO', 1.3030, 0.7639)
PSRKSG[84] = UNIFAC_subgroup('SIO', 43, 'SIO', 1.1044, 0.4657)
PSRKSG[85] = UNIFAC_subgroup('NMP', 44, 'NMP', 3.9810, 3.2000)
PSRKSG[86] = UNIFAC_subgroup('CCL3F', 45, 'CCLF', 3.0356, 2.6440)
PSRKSG[87] = UNIFAC_subgroup('CCL2F', 45, 'CCLF', 2.2287, 1.9160)
PSRKSG[88] = UNIFAC_subgroup('HCCL2F', 45, 'CCLF', 2.4060, 2.1160)
PSRKSG[89] = UNIFAC_subgroup('HCCLF', 45, 'CCLF', 1.6493, 1.4160)
PSRKSG[90] = UNIFAC_subgroup('CCLF2', 45, 'CCLF', 1.8174, 1.6480)
PSRKSG[91] = UNIFAC_subgroup('HCCLF2', 45, 'CCLF', 1.9670, 1.8280)
PSRKSG[92] = UNIFAC_subgroup('CCLF3', 45, 'CCLF', 2.1721, 2.1000)
PSRKSG[93] = UNIFAC_subgroup('CCL2F2', 45, 'CCLF', 2.6243, 2.3760)
PSRKSG[94] = UNIFAC_subgroup('AMH2', 46, 'CON (AM)', 1.4515, 1.2480)
PSRKSG[95] = UNIFAC_subgroup('AMHCH3', 46, 'CON (AM)', 2.1905, 1.7960)
PSRKSG[96] = UNIFAC_subgroup('AMHCH2', 46, 'CON (AM)', 1.9637, 1.4880)
PSRKSG[97] = UNIFAC_subgroup('AM(CH3)2', 46, 'CON (AM)', 2.8589, 2.4280)
PSRKSG[98] = UNIFAC_subgroup('AMCH3CH2', 46, 'CON (AM)', 2.6322, 2.1200)
PSRKSG[99] = UNIFAC_subgroup('AM(CH2)2', 46, 'CON (AM)', 2.4054, 1.8120)
PSRKSG[100] = UNIFAC_subgroup('C2H5O2', 47, 'OCCOH', 2.1226, 1.9040)
PSRKSG[101] = UNIFAC_subgroup('C2H4O2', 47, 'OCCOH', 1.8952, 1.5920)
PSRKSG[102] = UNIFAC_subgroup('CH3S', 48, 'CH2S', 1.6130, 1.3680)
PSRKSG[103] = UNIFAC_subgroup('CH2S', 48, 'CH2S', 1.3863, 1.0600)
PSRKSG[104] = UNIFAC_subgroup('CHS', 48, 'CH2S', 1.1589, 0.7480)
PSRKSG[105] = UNIFAC_subgroup('MORPH', 49, 'MORPH', 3.4740, 2.7960)
PSRKSG[106] = UNIFAC_subgroup('C4H4S', 50, 'THIOPHEN', 2.8569, 2.1400)
PSRKSG[107] = UNIFAC_subgroup('C4H3S', 50, 'THIOPHEN', 2.6908, 1.8600)
PSRKSG[108] = UNIFAC_subgroup('C4H2S', 50, 'THIOPHEN', 2.5247, 1.5800)
PSRKSG[109] = UNIFAC_subgroup('H2C=CH2', 2, 'C=C', 1.3564, 1.3098)
PSRKSG[110] = UNIFAC_subgroup('CH=-CH', 34, 'C=-C', 0.7910, 0.7200)
PSRKSG[111] = UNIFAC_subgroup('NH3', 55, 'NH3', 0.8510, 0.7780)
PSRKSG[112] = UNIFAC_subgroup('CO', 63, 'CO', 0.7110, 0.8280)
PSRKSG[113] = UNIFAC_subgroup('H2', 62, 'H2', 0.4160, 0.5710)
PSRKSG[114] = UNIFAC_subgroup('H2S', 61, 'H2S', 1.2350, 1.2020)
PSRKSG[115] = UNIFAC_subgroup('N2', 60, 'N2', 0.8560, 0.9300)
PSRKSG[116] = UNIFAC_subgroup('AR', 59, 'AR', 1.1770, 1.1160)
PSRKSG[117] = UNIFAC_subgroup('CO2', 56, 'CO2', 1.3000, 0.9820)
PSRKSG[118] = UNIFAC_subgroup('CH4', 57, 'CH4', 1.1292, 1.1240)
PSRKSG[119] = UNIFAC_subgroup('O2', 58, 'O2', 0.7330, 0.8490)
PSRKSG[120] = UNIFAC_subgroup('D2', 62, 'H2', 0.3700, 0.5270)
PSRKSG[121] = UNIFAC_subgroup('SO2', 65, 'SO2', 1.3430, 1.1640)
PSRKSG[122] = UNIFAC_subgroup('NO', 66, 'NO', 0.7160, 0.6200)
PSRKSG[123] = UNIFAC_subgroup('N2O', 67, 'N2O', 0.9800, 0.8880)
PSRKSG[124] = UNIFAC_subgroup('SF6', 68, 'SF6', 2.3740, 2.0560)
PSRKSG[125] = UNIFAC_subgroup('HE', 69, 'HE', 0.8850, 0.9850)
PSRKSG[126] = UNIFAC_subgroup('NE', 70, 'NE', 0.8860, 0.9860)
PSRKSG[127] = UNIFAC_subgroup('KR', 71, 'KR', 1.1200, 1.1200)
PSRKSG[128] = UNIFAC_subgroup('XE', 72, 'XE', 1.1300, 1.1300)
PSRKSG[129] = UNIFAC_subgroup('HF', 73, 'HF', 1.0160, 1.2160)
PSRKSG[130] = UNIFAC_subgroup('HCL', 74, 'HCL', 1.0560, 1.2560)
PSRKSG[131] = UNIFAC_subgroup('HBR', 75, 'HBR', 1.0580, 1.2580)
PSRKSG[132] = UNIFAC_subgroup('HI', 76, 'HI', 1.3930, 1.2080)
PSRKSG[133] = UNIFAC_subgroup('COS', 77, 'COS', 1.6785, 1.3160)
PSRKSG[134] = UNIFAC_subgroup('CHSH', 29, 'CH3SH', 1.4250, 1.0600)
PSRKSG[135] = UNIFAC_subgroup('CSH', 29, 'CH3SH', 1.1990, 0.7520)
PSRKSG[136] = UNIFAC_subgroup('H2COCH', 51, 'EPOXY', 1.3652, 1.0080)
PSRKSG[137] = UNIFAC_subgroup('HCOCH', 51, 'EPOXY', 1.1378, 0.6960)
PSRKSG[138] = UNIFAC_subgroup('HCOC', 51, 'EPOXY', 0.9104, 0.4680)
PSRKSG[139] = UNIFAC_subgroup('H2COCH2', 51, 'EPOXY', 1.5926, 1.3200)
PSRKSG[140] = UNIFAC_subgroup('H2COC', 51, 'EPOXY', 1.1378, 0.7800)
PSRKSG[141] = UNIFAC_subgroup('COC', 51, 'EPOXY', 0.6829, 0.2400)
PSRKSG[142] = UNIFAC_subgroup('F2', 78, 'F2', 0.7500, 0.8800)
PSRKSG[143] = UNIFAC_subgroup('CL2', 79, 'CL2', 1.5300, 1.4400)
PSRKSG[144] = UNIFAC_subgroup('BR2', 80, 'BR2', 1.9000, 1.6600)
PSRKSG[145] = UNIFAC_subgroup('HCN', 81, 'HCN', 1.2000, 1.1900)
PSRKSG[146] = UNIFAC_subgroup('NO2', 82, 'NO2', 1.0000, 1.1000)
PSRKSG[147] = UNIFAC_subgroup('CF4', 83, 'CF4', 1.7800, 1.8200)
PSRKSG[148] = UNIFAC_subgroup('O3', 84, 'O3', 1.1000, 1.2700)
PSRKSG[149] = UNIFAC_subgroup('CLNO', 85, 'CLNO', 1.4800, 1.3400)
PSRKSG[152] = UNIFAC_subgroup('CNH2', 14, 'CNH2', 0.9147, 0.6140)


UFIP = {i: {} for i in list(range(1, 52)) + [55, 84, 85]}
with open(os.path.join(folder, 'UNIFAC original interaction parameters.tsv')) as f:
    for line in f:
        maingroup1, maingroup2, interaction_parameter = line.strip('\n').split('\t')
        # Index by both int, order maters, to only one parameter.
        UFIP[int(maingroup1)][int(maingroup2)] = float(interaction_parameter)

DOUFIP2006 = {i: {} for i in DOUFMG.keys()}
with open(os.path.join(folder, 'UNIFAC modified Dortmund interaction parameters 2006.tsv')) as f:
    for line in f:
        maingroup1, maingroup2, a, b, c = line.strip('\n').split('\t')
        DOUFIP2006[int(maingroup1)][int(maingroup2)] = (float(a), float(b), float(c))

DOUFIP2016 = {i: {} for i in list(DOUFMG.keys())+[50, 77, 98, 99]}
# Some of the groups have no public parameters unfortunately
with open(os.path.join(folder, 'UNIFAC modified Dortmund interaction parameters.tsv')) as f:
    for line in f:
        maingroup1, maingroup2, a, b, c = line.strip('\n').split('\t')
        DOUFIP2016[int(maingroup1)][int(maingroup2)] = (float(a), float(b), float(c))


#NISTUFIP = {i: {} for i in list(NISTUFMG.keys())}
NISTUFIP = {i: {} for i in range(400)}

with open(os.path.join(folder, 'UNIFAC modified NIST 2015 interaction parameters.tsv')) as f:
    for line in f:
        maingroup1, maingroup2, a, b, c, Tmin, Tmax = line.strip('\n').split('\t')
        NISTUFIP[int(maingroup1)][int(maingroup2)] = (float(a), float(b), float(c))

PSRKIP = {i: {} for i in range(400)}

with open(os.path.join(folder, 'PSRK interaction parameters.tsv')) as f:
    for line in f:
        maingroup1, maingroup2, a, b, c = line.strip('\n').split('\t')
        PSRKIP[int(maingroup1)][int(maingroup2)] = (float(a), float(b), float(c))




DDBST_UNIFAC_assignments = {}
DDBST_MODIFIED_UNIFAC_assignments = {}
DDBST_PSRK_assignments = {}

def load_group_assignments_DDBST():
    '''Data is stored in the format
    InChI key\tbool bool bool \tsubgroup count ...\tsubgroup count \tsubgroup count...
    where the bools refer to whether or not the original UNIFAC, modified
    UNIFAC, and PSRK group assignments were completed correctly.
    The subgroups and their count have an indefinite length.
    '''
    # Do not allow running multiple times
    if DDBST_UNIFAC_assignments:
        return None
    with open(os.path.join(folder, 'DDBST UNIFAC assignments.tsv')) as f:
        _group_assignments = [DDBST_UNIFAC_assignments, DDBST_MODIFIED_UNIFAC_assignments, DDBST_PSRK_assignments]
        for line in f.readlines():
            key, valids, original, modified, PSRK = line.split('\t')
            # list of whether or not each method was correctly identified or not
            valids = [True if i == '1' else False for i in valids.split(' ')]
            for groups, storage, valid in zip([original, modified, PSRK], _group_assignments, valids):
                if valid:
                    groups = groups.rstrip().split(' ')
                    d_data = {}
                    for i in range(int(len(groups)/2)):
                        d_data[int(groups[i*2])] = int(groups[i*2+1])
                    storage[key] = d_data


def UNIFAC_RQ(groups, subgroup_data=None):
    r'''Calculates UNIFAC parameters R and Q for a chemical, given a dictionary
    of its groups, as shown in [1]_. Most UNIFAC methods use the same subgroup
    values; however, a dictionary of `UNIFAC_subgroup` instances may be 
    specified as an optional second parameter.

    .. math::
        r_i = \sum_{k=1}^{n} \nu_k R_k 
        
        q_i = \sum_{k=1}^{n}\nu_k Q_k

    Parameters
    ----------
    groups : dict[count]
        Dictionary of numeric subgroup IDs : their counts
    subgroup_data : None or dict[UNIFAC_subgroup]
        Optional replacement for standard subgroups; leave as None to use the
        original UNIFAC subgroup r and q values.

    Returns
    -------
    R : float
        R UNIFAC parameter (normalized Van der Waals Volume)  [-]
    Q : float
        Q UNIFAC parameter (normalized Van der Waals Area)  [-]

    Notes
    -----
    These parameters have some predictive value for other chemical properties.

    Examples
    --------
    Hexane
    
    >>> UNIFAC_RQ({1:2, 2:4})
    (4.4998000000000005, 3.856)
    
    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    '''
    if subgroup_data is not None:
        subgroups = subgroup_data
    else:
        subgroups = UFSG
    ri = 0.
    qi = 0.
    for group, count in groups.items():
        ri += subgroups[group].R*count
        qi += subgroups[group].Q*count
    return ri, qi


def Van_der_Waals_volume(R):
    r'''Calculates a species Van der Waals molar volume with the UNIFAC method,
    given a species's R parameter.

    .. math::
        V_{wk} = 15.17R_k
        
    Parameters
    ----------
    R : float
        R UNIFAC parameter (normalized Van der Waals Volume)  [-]

    Returns
    -------
    V_vdw : float
        Unnormalized Van der Waals volume, [m^3/mol]

    Notes
    -----
    The volume was originally given in cm^3/mol, but is converted to SI here.

    Examples
    --------    
    >>> Van_der_Waals_volume(4.4998)
    6.826196599999999e-05
    
    References
    ----------
    .. [1] Wei, James, Morton M. Denn, John H. Seinfeld, Arup Chakraborty, 
       Jackie Ying, Nicholas Peppas, and George Stephanopoulos. Molecular 
       Modeling and Theory in Chemical Engineering. Academic Press, 2001.
    '''
    return R*1.517e-05


def Van_der_Waals_area(Q):
    r'''Calculates a species Van der Waals molar surface area with the UNIFAC 
    method, given a species's Q parameter.

    .. math::
        A_{wk} = 2.5\times 10^9 Q_k
        
    Parameters
    ----------
    Q : float
        Q UNIFAC parameter (normalized Van der Waals Area)  [-]

    Returns
    -------
    A_vdw : float
        Unnormalized Van der Waals surface area, [m^2/mol]

    Notes
    -----
    The volume was originally given in cm^2/mol, but is converted to SI here.

    Examples
    --------    
    >>> Van_der_Waals_area(3.856)
    964000.0
    
    References
    ----------
    .. [1] Wei, James, Morton M. Denn, John H. Seinfeld, Arup Chakraborty, 
       Jackie Ying, Nicholas Peppas, and George Stephanopoulos. Molecular 
       Modeling and Theory in Chemical Engineering. Academic Press, 2001.
    '''
    return Q*250000.0


def UNIFAC_psi(T, subgroup1, subgroup2, subgroup_data, interaction_data, 
               modified=False):
    r'''Calculates the interaction parameter psi(m, n) for two UNIFAC 
    subgroups, given the system temperature, the UNIFAC subgroups considered 
    for the variant of UNIFAC used, the interaction parameters for the 
    variant of UNIFAC used, and whether or not the temperature dependence is 
    modified from the original form, as shown below.

    Original temperature dependence:
        
    .. math::
        \Psi_{mn} = \exp\left(\frac{-a_{mn}}{T}\right)
        
    Modified temperature dependence:
        
    .. math::
        \Psi_{mn} = \exp\left(\frac{-a_{mn} - b_{mn}T - c_{mn}T^2}{T}\right)
        
    Parameters
    ----------
    T : float
        Temperature of the system, [K]
    subgroup1 : int
        First UNIFAC subgroup for identifier, [-]
    subgroup2 : int
        Second UNIFAC subgroup for identifier, [-]
    subgroup_data : dict[UNIFAC_subgroup]
        Normally provided as inputs to `UNIFAC`.
    interaction_data : dict[dict[tuple(a_mn, b_mn, c_mn)]]
        Normally provided as inputs to `UNIFAC`.
    modified : bool
        True if the modified temperature dependence is used by the interaction
        parameters, otherwise False

    Returns
    -------
    psi : float
        UNIFAC interaction parameter term, [-]

    Notes
    -----
    UNIFAC interaction parameters are asymmetric. No warning is raised if an
    interaction parameter is missing.

    Examples
    --------
    >>> from thermo.unifac import UFSG, UFIP, DOUFSG, DOUFIP2006
    
    >>> UNIFAC_psi(307, 18, 1, UFSG, UFIP)
    0.9165248264184787
    
    >>> UNIFAC_psi(373.15, 9, 78, DOUFSG, DOUFIP2006, modified=True)
    1.3703140538273264
    
    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    .. [2] Fredenslund, Aage, Russell L. Jones, and John M. Prausnitz. "Group
       Contribution Estimation of Activity Coefficients in Nonideal Liquid 
       Mixtures." AIChE Journal 21, no. 6 (November 1, 1975): 1086-99. 
       doi:10.1002/aic.690210607.
    '''
    main1 = subgroup_data[subgroup1].main_group_id
    main2 = subgroup_data[subgroup2].main_group_id
    if modified:
        try:
            a, b, c = interaction_data[main1][main2]
        except:
            return 1.
        return exp((-a/T -b - c*T))
    else:
        try:
            return exp(-interaction_data[main1][main2]/T)
        except:
            return 1.


def UNIFAC_gammas(T, xs, chemgroups, cached=None, subgroup_data=None, 
                  interaction_data=None, modified=False):
    r'''Calculates activity coefficients using the UNIFAC model (optionally 
    modified), given a mixture's temperature, liquid mole fractions, 
    and optionally the subgroup data and interaction parameter data of your 
    choice. The default is to use the original UNIFAC model, with the latest 
    parameters published by DDBST. The model supports modified forms (Dortmund, 
    NIST) when the `modified` parameter is True.
            
    Parameters
    ----------
    T : float
        Temperature of the system, [K]
    xs : list[float]
        Mole fractions of all species in the system in the liquid phase, [-]
    chemgroups : list[dict]
        List of dictionaries of subgroup IDs and their counts for all species 
        in the mixture, [-]
    subgroup_data : dict[UNIFAC_subgroup]
        UNIFAC subgroup data; available dictionaries in this module are UFSG
        (original), DOUFSG (Dortmund), or NISTUFSG ([4]_).
    interaction_data : dict[dict[tuple(a_mn, b_mn, c_mn)]]
        UNIFAC interaction parameter data; available dictionaries in this 
        module are UFIP (original), DOUFIP2006 (Dortmund parameters as 
        published by 2006), DOUFIP2016 (Dortmund parameters as published by 
        2016), and NISTUFIP ([4]_).
    modified : bool
        True if using the modified form and temperature dependence, otherwise
        False.

    Returns
    -------
    gammas : list[float]
        Activity coefficients of all species in the mixture, [-]

    Notes
    -----
    The actual implementation of UNIFAC is formulated slightly different than
    the formulas above for computational efficiency. DDBST switched to using 
    the more efficient forms in their publication, but the numerical results
    are identical.
    
    The model is as follows:
        
    .. math::
        \ln \gamma_i =  \ln \gamma_i^c + \ln \gamma_i^r
        
    **Combinatorial component**
    
    .. math::
        \ln \gamma_i^c = \ln \frac{\phi_i}{x_i} + \frac{z}{2} q_i 
        \ln\frac{\theta_i}{\phi_i} + L_i - \frac{\phi_i}{x_i}
        \sum_{j=1}^{n} x_j L_j
        
    .. math::
        \theta_i = \frac{x_i q_i}{\sum_{j=1}^{n} x_j q_j} 
        
    .. math::
         \phi_i = \frac{x_i r_i}{\sum_{j=1}^{n} x_j r_j}
         
    .. math::
         L_i = 5(r_i - q_i)-(r_i-1)
   
    **Residual component**
    
    .. math::
        \ln \gamma_i^r = \sum_{k}^n \nu_k^{(i)} \left[ \ln \Gamma_k
        - \ln \Gamma_k^{(i)} \right]
        
    .. math::
        \ln \Gamma_k = Q_k \left[1 - \ln \sum_m \Theta_m \Psi_{mk} - \sum_m 
        \frac{\Theta_m \Psi_{km}}{\sum_n \Theta_n \Psi_{nm}}\right]
        
    .. math::
        \Theta_m = \frac{Q_m X_m}{\sum_{n} Q_n X_n}
        
    .. math::
        X_m = \frac{ \sum_j \nu^j_m x_j}{\sum_j \sum_n \nu_n^j x_j}
        
    **R and Q**
    
    .. math::
        r_i = \sum_{k=1}^{n} \nu_k R_k 
        
    .. math::
        q_i = \sum_{k=1}^{n}\nu_k Q_k
    
    The newer forms of UNIFAC (Dortmund, NIST) calculate the combinatorial
    part slightly differently:
        
    .. math::
        \ln \gamma_i^c = 1 - {V'}_i + \ln({V'}_i) - 5q_i \left(1
        - \frac{V_i}{F_i}+ \ln\left(\frac{V_i}{F_i}\right)\right)
        
    .. math::
        V'_i = \frac{r_i^{3/4}}{\sum_j r_j^{3/4}x_j}
    
    .. math::
        V_i = \frac{r_i}{\sum_j r_j x_j}
        
    .. math::
        F_i = \frac{q_i}{\sum_j q_j x_j}
    
    Although this form looks substantially different than the original, it 
    infact reverts to the original form if only :math:`V'_i` is replaced by
    :math:`V_i`. This is more clear when looking at the full rearranged form as
    in [3]_.
    
    In some publications such as [5]_, the nomenclature is such that 
    :math:`\theta_i` and :math:`\phi` do not contain the top :math:`x_i`,
    making :math:`\theta_i = F_i` and  :math:`\phi_i = V_i`. [5]_ is also 
    notable for having supporting information containing very nice sets of
    analytical derivatives.
    
    UNIFAC LLE uses the original formulation of UNIFAC, and otherwise only 
    different interaction parameters.

    Examples
    --------
    >>> UNIFAC_gammas(T=333.15, xs=[0.5, 0.5], chemgroups=[{1:2, 2:4}, {1:1, 2:1, 18:1}])
    [1.4276025835624173, 1.3646545010104225]
    
    >>> UNIFAC_gammas(373.15, [0.2, 0.3, 0.2, 0.2], 
    ... [{9:6}, {78:6}, {1:1, 18:1}, {1:1, 2:1, 14:1}],
    ... subgroup_data=DOUFSG, interaction_data=DOUFIP2006, modified=True)
    [1.186431113706829, 1.440280133911197, 1.204479833499608, 1.9720706090299824]

    References
    ----------
    .. [1] Gmehling, Jurgen. Chemical Thermodynamics: For Process Simulation.
       Weinheim, Germany: Wiley-VCH, 2012.
    .. [2] Fredenslund, Aage, Russell L. Jones, and John M. Prausnitz. "Group
       Contribution Estimation of Activity Coefficients in Nonideal Liquid 
       Mixtures." AIChE Journal 21, no. 6 (November 1, 1975): 1086-99. 
       doi:10.1002/aic.690210607.
    .. [3] Jakob, Antje, Hans Grensemann, Jürgen Lohmann, and Jürgen Gmehling. 
       "Further Development of Modified UNIFAC (Dortmund):  Revision and 
       Extension 5." Industrial & Engineering Chemistry Research 45, no. 23 
       (November 1, 2006): 7924-33. doi:10.1021/ie060355c.
    .. [4] Kang, Jeong Won, Vladimir Diky, and Michael Frenkel. "New Modified 
       UNIFAC Parameters Using Critically Evaluated Phase Equilibrium Data." 
       Fluid Phase Equilibria 388 (February 25, 2015): 128-41. 
       doi:10.1016/j.fluid.2014.12.042.
    .. [5] Jäger, Andreas, Ian H. Bell, and Cornelia Breitkopf. "A 
       Theoretically Based Departure Function for Multi-Fluid Mixture Models."
       Fluid Phase Equilibria 469 (August 15, 2018): 56-69. 
       https://doi.org/10.1016/j.fluid.2018.04.015.
    '''
    cmps = range(len(xs))
    if subgroup_data is None:
        subgroups = UFSG
    else:
        subgroups = subgroup_data
    if interaction_data is None:
        interactions = UFIP
    else:
        interactions = interaction_data

    # Obtain r and q values using the subgroup values
    if not cached:
        rs = []
        qs = []
        for groups in chemgroups:
            ri = 0.
            qi = 0.
            for group, count in groups.items():
                ri += subgroups[group].R*count
                qi += subgroups[group].Q*count
            rs.append(ri)
            qs.append(qi)
        

        group_counts = {}
        for groups in chemgroups:
            for group, count in groups.items():
                if group in group_counts:
                    group_counts[group] += count
                else:
                    group_counts[group] = count
    else:
        rs, qs, group_counts = cached
    
    # Sum the denominator for calculating Xs
    group_sum = sum(count*xs[i] for i in cmps for count in chemgroups[i].values())

    # Caclulate each numerator for calculating Xs
    # Xms stored in group_count_xs, length number of independent groups
    group_count_xs = {}
    for group in group_counts:
        tot_numerator = sum(chemgroups[i][group]*xs[i] for i in cmps if group in chemgroups[i])        
        group_count_xs[group] = tot_numerator/group_sum
#    print(group_count_xs, 'group_count_xs')

    rsxs = sum([rs[i]*xs[i] for i in cmps])
    Vis = [rs[i]/rsxs for i in cmps]
    qsxs = sum([qs[i]*xs[i] for i in cmps])
    Fis = [qs[i]/qsxs for i in cmps]

    if modified:
        rsxs2 = sum([rs[i]**0.75*xs[i] for i in cmps])
        Vis2 = [rs[i]**0.75/rsxs2 for i in cmps]
        loggammacs = [1. - Vis2[i] + log(Vis2[i]) - 5.*qs[i]*(1. - Vis[i]/Fis[i]
                      + log(Vis[i]/Fis[i])) for i in cmps]
    else:
        loggammacs = [1. - Vis[i] + log(Vis[i]) - 5.*qs[i]*(1. - Vis[i]/Fis[i]
                      + log(Vis[i]/Fis[i])) for i in cmps]
#    print(loggammacs)

    Q_sum_term = sum([subgroups[group].Q*group_count_xs[group] for group in group_counts])
    
    # theta(m) for an overall mixture composition
    area_fractions = {group: subgroups[group].Q*group_count_xs[group]/Q_sum_term
                      for group in group_counts.keys()}
#    print('theta(m) for an overall mixture ', area_fractions)

    # This needs to not be a dictionary
    UNIFAC_psis = {k: {m:(UNIFAC_psi(T, m, k, subgroups, interactions, modified=modified))
                   for m in group_counts} for k in group_counts}

    loggamma_groups = {}
    # This is for the total mixture bit of the residual
    for k in group_counts:
        sum1, sum2 = 0., 0.
        for m in group_counts:
            sum1 += area_fractions[m]*UNIFAC_psis[k][m]
            # This term can be pre-calculated
            sum3 = sum(area_fractions[n]*UNIFAC_psis[m][n] for n in group_counts)
            sum2 -= area_fractions[m]*UNIFAC_psis[m][k]/sum3
        loggamma_groups[k] = subgroups[k].Q*(1. - log(sum1) + sum2)
    
    loggammars = []
    for groups in chemgroups:
        # Most of this is for the pure-component bit of the residual
        chem_loggamma_groups = {}
        chem_group_sum = sum(groups.values())
        
        # Xm = chem_group_count_xs
        chem_group_count_xs = {group: count/chem_group_sum for group, count in groups.items()}
#        print('Xm', chem_group_count_xs)
    
        # denominator of term used to compute Theta(m)
        Q_sum_term = sum([subgroups[group].Q*chem_group_count_xs[group] for group in groups])
        
        # Theta(m) = chem_area_fractions (dict indexed by main group)
        chem_area_fractions = {group: subgroups[group].Q*chem_group_count_xs[group]/Q_sum_term
                               for group in groups.keys()}
#        print('Theta(m)', chem_area_fractions)
        
        for k in groups:
            sum1, sum2 = 0., 0.
            for m in groups:
                sum1 += chem_area_fractions[m]*UNIFAC_psis[k][m]
                
                # sum3 should be cached
                sum3 = sum(chem_area_fractions[n]*UNIFAC_psis[m][n] for n in groups)
                sum2 -= chem_area_fractions[m]*UNIFAC_psis[m][k]/sum3

            chem_loggamma_groups[k] = subgroups[k].Q*(1. - log(sum1) + sum2)

        tot = sum([count*(loggamma_groups[group] - chem_loggamma_groups[group])
                   for group, count in groups.items()])
        loggammars.append(tot)

    return [exp(loggammacs[i]+loggammars[i]) for i in cmps]


def chemgroups_to_matrix(chemgroups):
    r'''
    Index by [group index][compound index]
    
    >>> chemgroups_to_matrix([{9: 6}, {2: 6}, {1: 1, 18: 1}, {1: 1, 2: 1, 14: 1}])
    [[0, 0, 1, 1], [0, 6, 0, 1], [6, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
    '''
    matrix = []
    keys = []
    all_keys = set()
    [all_keys.update(i.keys()) for i in chemgroups]
    for k in sorted(list(all_keys)):
        matrix.append([l[k] if k in l else 0 for l in chemgroups])
    return matrix


class UNIFAC(GibbsExcess):
    
    @staticmethod
    def from_subgroups(T, xs, chemgroups, subgroups=UFSG,
                       interaction_data=UFIP, version=0):
        rs = []
        qs = []
        for groups in chemgroups:
            ri = 0.
            qi = 0.
            for subgroup_idx, count in groups.items():
                ri += subgroups[subgroup_idx].R*count
                qi += subgroups[subgroup_idx].Q*count
            rs.append(ri)
            qs.append(qi)

        # Make a dictionary containing the subgroups as keys and their count - the total number
        # of them in ALL the compounds, regardless of mole fractions
        group_counts = {}
        for compound_subgroups in chemgroups:
            for subgroup, count in compound_subgroups.items():
                try:
                    group_counts[subgroup] += count
                except KeyError:
                    group_counts[subgroup] = count
        
        # Convert group counts into a list, sorted by index (lowest subgroup index is first element, highest subgroup index is the last)
        subgroup_list = list(sorted(group_counts.keys()))
        group_counts_list = [c for _, c in sorted(zip(group_counts.keys(), group_counts.values()))]

        Qs = [subgroups[group].Q for group in subgroup_list]
        vs = chemgroups_to_matrix(chemgroups)
        
        psi_a, psi_b, psi_c = [], [], []
        for sub1 in subgroup_list:
            a_row, b_row, c_row = [], [], []
            for sub2 in subgroup_list:
                main1 = subgroups[sub1].main_group_id
                main2 = subgroups[sub2].main_group_id
                try:
                    v = interaction_data[main1][main2]
                    try:
                        a_row.append(v[0])
                        b_row.append(v[1])
                        c_row.append(v[2])
                    except:
                        a_row.append(v)
                        b_row.append(0.0)
                        c_row.append(0.0)
                except KeyError:
                        a_row.append(0.0)
                        b_row.append(0.0)
                        c_row.append(0.0)
            psi_a.append(a_row), psi_b.append(b_row), psi_c.append(c_row)
            
            
        debug = (rs, qs, Qs, vs, (psi_a, psi_b, psi_c))
        return UNIFAC(T=T, xs=xs, rs=rs, qs=qs, Qs=Qs, vs=vs, psi_abc=(psi_a, psi_b, psi_c), version=version)
            
    def __init__(self, T, xs, rs, qs, Qs, vs, psi_coeffs=None, psi_abc=None,
                 version=0):
        self.T = T
        self.xs = xs
        
        # rs - 1d index by [component] parameter, calculated using the chemical's subgroups and their count
        self.rs = rs
        # qs - 1d index by [component] parameter, calculated using the chemical's subgroups and their count
        self.qs = qs
        self.Qs = Qs
        
        # [subgroup][component] = number of subgroup in component where subgroup
        # is an index, numbered sequentially by the number of subgroups in the mixture
        self.vs = vs


        # each psi_letter is a matrix of [subgroup_length][subgroups_length]
        # the diagonal is zero
        # Indexed by index of the subgroup in the mixture, again sorted lowest first
        if psi_abc is not None:
            self.psi_a, self.psi_b, self.psi_c = psi_abc
        
        else:
            if psi_coeffs is None:
                raise ValueError("Missing psis")
            self.psi_a = [[i[0] for i in l] for l in psi_coeffs]
            self.psi_b = [[i[1] for i in l] for l in psi_coeffs]
            self.psi_c = [[i[2] for i in l] for l in psi_coeffs]
        self.N_groups = len(self.psi_a)
        self.groups = range(self.N_groups) # iterator over the number of 
        self.N = N = len(rs)
        self.cmps = range(N)
        self.version = version
        if self.version == 1:
            self.rs_34 = [i**0.75 for i in rs]

        self.cmp_v_count = [sum(vs[group][i] for group in self.groups) for i in self.cmps]
        
        # Matrix of [component][list(indexes to groups in component)], list of list
        self.cmp_group_idx = [[j for j in self.groups if vs[j][i]] for i in self.cmps]

    def to_T_xs(self, T, xs):
        new = self.__class__.__new__(self.__class__)
        new.T = T
        new.xs = xs
        new.N = self.N
        new.cmps = self.cmps
        
        new.N_groups = self.N_groups
        new.groups = self.groups
        
        new.rs = self.rs
        new.qs = self.qs
        new.Qs = self.Qs
        new.vs = self.vs
        new.cmp_v_count = self.cmp_v_count
        new.cmp_group_idx = self.cmp_group_idx
        
        new.version = self.version
        
        new.psi_a, new.psi_b, new.psi_c = self.psi_a, self.psi_b, self.psi_c

        try:
            new.rs_34 = self.rs_34
        except AttributeError:
            pass
        
        if T == self.T:
            pass
        return new
#    
#    def Xms_chem(self):
#        # This variable has a temperature and mole fraction derivative of 0!
#        
#        # Indexed by [group][component]
#        groups, cmps = self.groups, self.cmps
#        vs = self.vs
#        # chem_group_sums = [number of groups in each component]
#        chem_group_sums = [sum([vs[i][j] for i in groups]) for j in cmps]
#
#        chem_group_count_xs = [[vs[i][j]/chem_group_sums[j] for j in cmps] for i in groups]        
#        return chem_group_count_xs


    def psis(self):
        try:
            return self._psis
        except AttributeError:
            pass
        T, groups = self.T, self.groups
        psi_a, psi_b, psi_c = self.psi_a, self.psi_b, self.psi_c
        
        mT_inv = -1.0/T
        self._psis = psis = []
        for i in groups:
            a_row, b_row, c_row = psi_a[i], psi_b[i], psi_c[i]
            psis.append([exp(a_row[j]*mT_inv - b_row[j] - c_row[j]*T) for j in groups])
        return psis
    
    def dpsis_dT(self):
        try:
            return self._dpsis_dT
        except AttributeError:
            pass
        try:
            psis = self._psis
        except AttributeError:
            psis = self.psis()
            
        T, groups = self.T, self.groups
        psi_a, psi_c = self.psi_a, self.psi_c
        
        T2_inv = 1.0/(T*T)
        self._dpsis_dT = dpsis_dT = []
        for i in groups:
            psis_row, a_row, c_row = psis[i], psi_a[i], psi_c[i]
            dpsis_dT.append([psis_row[j]*(a_row[j]*T2_inv - c_row[j])  for j in groups])
        return dpsis_dT

    def d2psis_dT2(self):
        try:
            return self._d2psis_dT2
        except AttributeError:
            pass
        try:
            psis = self._psis
        except AttributeError:
            psis = self.psis()
            
        T, groups = self.T, self.groups
        psi_a, psi_c = self.psi_a, self.psi_c
        mT2_inv = -1.0/(T*T)
        T3_inv_m2 = -2.0/(T*T*T)
        
        self._d2psis_dT2 = d2psis_dT2 = []
        for i in groups:
            psis_row, a_row, c_row = psis[i], psi_a[i], psi_c[i]
            row = []
            for j in groups:
                x0 = c_row[j] + mT2_inv*a_row[j]
                row.append((x0*x0 + T3_inv_m2*a_row[j])*psis_row[j])
            d2psis_dT2.append(row)
        return d2psis_dT2
    
    
    def d3psis_dT3(self):
        try:
            return self._d3psis_dT3
        except AttributeError:
            pass
        try:
            psis = self._psis
        except AttributeError:
            psis = self.psis()
            
        T, groups = self.T, self.groups
        psi_a, psi_c = self.psi_a, self.psi_c
        
        nT2_inv = -1.0/(T*T)
        T3_inv_6 = 6.0/(T*T*T)
        T4_inv_6 = 6.0/(T*T*T*T)
        
        self._d3psis_dT3 = d3psis_dT3 = []

        for i in groups:
            psis_row, a_row, c_row = psis[i], psi_a[i], psi_c[i]
            row = []
            for j in groups:
                x0 = c_row[j] + nT2_inv*a_row[j]
                row.append((x0*(T3_inv_6*a_row[j] - x0*x0) + T4_inv_6*a_row[j])*psis_row[j])

            d3psis_dT3.append(row)
        return d3psis_dT3
                
    def Vis(self):
        try:
            return self._Vis
        except:
            pass
        rs, xs, cmps = self.rs, self.xs, self.cmps
        tot = 0.0
        for i in cmps:
            tot += rs[i]*xs[i]
        tot = 1.0/tot
        self.rx_sum_inv = tot
        self._Vis = [rs[i]*tot for i in cmps]
        return self._Vis
    
    def dVis_dxs(self):
        try:
            return self._dVis_dxs
        except AttributeError:
            pass
        try:
            rx_sum_inv = self.rx_sum_inv
        except AttributeError:
            self.Vis()
            rx_sum_inv = self.rx_sum_inv
            
        rs = self.rs
        mrx_sum_inv2 = -rx_sum_inv*rx_sum_inv
        
        dVis = [[ri*rj*mrx_sum_inv2 for rj in rs] for ri in rs]
        self._dVis_dxs = dVis
        return dVis
    
    def d2Vis_dxixjs(self):
        try:
            return self._d2Vis_dxixjs
        except AttributeError:
            pass
        try:
            rx_sum_inv = self.rx_sum_inv
        except AttributeError:
            self.Vis()
            rx_sum_inv = self.rx_sum_inv
        rs = self.rs
        rx_sum_inv3_2 = 2.0*rx_sum_inv*rx_sum_inv*rx_sum_inv
        d2Vis = [[[ri*rj*rk*rx_sum_inv3_2 for rk in rs] for rj in rs] for ri in rs]
        self._d2Vis_dxixjs = d2Vis
        return d2Vis
    
    def d3Vis_dxixjxks(self):
        try:
            return self._d3Vis_dxixjxks
        except AttributeError:
            pass
        try:
            rx_sum_inv = self.rx_sum_inv
        except AttributeError:
            self.Vis()
            rx_sum_inv = self.rx_sum_inv
        rs = self.rs
        mrx_sum_inv4_6 = -6.0*rx_sum_inv*rx_sum_inv*rx_sum_inv*rx_sum_inv
        
        d3Vis = [[[[ri*rj*rk*rl*mrx_sum_inv4_6 for rl in rs] for rk in rs]
                                               for rj in rs] for ri in rs]
        self._d3Vis_dxixjxks = d3Vis
        return d3Vis

    def Fis(self):
        qs, xs, cmps = self.qs, self.xs, self.cmps
        tot = 0.0
        for i in cmps:
            tot += qs[i]*xs[i]
        tot = 1.0/tot
        Fis = [qs[i]*tot for i in cmps]
        self.qx_sum_inv = tot
        return Fis

    def dFis_dxs(self):
        try:
            return self._dFis_dxs
        except AttributeError:
            pass
        try:
            qx_sum_inv = self.qx_sum_inv
        except AttributeError:
            self.Fis()
            qx_sum_inv = self.qx_sum_inv
            
        qs = self.qs
        mqx_sum_inv2 = -qx_sum_inv*qx_sum_inv
        
        dFis = [[qi*qj*mqx_sum_inv2 for qj in qs] for qi in qs]
        self._dFis_dxs = dFis
        return dFis

    def d2Fis_dxixjs(self):
        try:
            return self._d2Fis_dxixjs
        except AttributeError:
            pass
        try:
            qx_sum_inv = self.qx_sum_inv
        except AttributeError:
            self.Fis()
            qx_sum_inv = self.qx_sum_inv
            
        qs = self.qs

        qx_sum_inv3_2 = 2.0*qx_sum_inv*qx_sum_inv*qx_sum_inv
        d2Fis = [[[qi*qj*qk*qx_sum_inv3_2 for qk in qs] for qj in qs] for qi in qs]
        self._d2Fis_dxixjs = d2Fis
        return d2Fis

    def d3Fis_dxixjxks(self):
        try:
            return self._d3Fis_dxixjxks
        except AttributeError:
            pass
        try:
            qx_sum_inv = self.qx_sum_inv
        except AttributeError:
            self.Fis()
            qx_sum_inv = self.qx_sum_inv
        qs = self.qs
        mqx_sum_inv4_6 = -6.0*qx_sum_inv*qx_sum_inv*qx_sum_inv*qx_sum_inv
        
        d3Fis = [[[[qi*qj*qk*ql*mqx_sum_inv4_6 for ql in qs] for qk in qs]
                                               for qj in qs] for qi in qs]
        self._d3Fis_dxixjxks = d3Fis
        return d3Fis


    def Vis_Dortmund(self):
        try:
            return self._Vis_Dortmund
        except:
            pass
        rs_34, xs, cmps = self.rs_34, self.xs, self.cmps
        tot = 0.0
        for i in cmps:
            tot += rs_34[i]*xs[i]
        tot = 1.0/tot
        self.r34x_sum_inv = tot
        self._Vis_Dortmund = [rs_34[i]*tot for i in cmps]
        return self._Vis_Dortmund
    
    def dVis_Dortmund_dxs(self):
        try:
            return self._dVis_Dortmund_dxs
        except AttributeError:
            pass
        try:
            r34x_sum_inv = self.r34x_sum_inv
        except AttributeError:
            self.Vis_Dortmund()
            r34x_sum_inv = self.r34x_sum_inv
            
        rs_34 = self.rs_34
        mr34x_sum_inv2 = -r34x_sum_inv*r34x_sum_inv
        
        dVis_Dortmund = [[ri*rj*mr34x_sum_inv2 for rj in rs_34] for ri in rs_34]
        self._dVis_Dortmund_dxs = dVis_Dortmund
        return dVis_Dortmund
    
    def d2Vis_Dortmund_dxixjs(self):
        try:
            return self._d2Vis_Dortmund_dxixjs
        except AttributeError:
            pass
        try:
            r34x_sum_inv = self.r34x_sum_inv
        except AttributeError:
            self.Vis_Dortmund()
            r34x_sum_inv = self.r34x_sum_inv
        rs_34 = self.rs_34
        r34x_sum_inv3_2 = 2.0*r34x_sum_inv*r34x_sum_inv*r34x_sum_inv
        d2Vis_Dortmund = [[[ri*rj*rk*r34x_sum_inv3_2 for rk in rs_34] for rj in rs_34] for ri in rs_34]
        self._d2Vis_Dortmund_dxixjs = d2Vis_Dortmund
        return d2Vis_Dortmund
    
    def d3Vis_Dortmund_dxixjxks(self):
        try:
            return self._d3Vis_Dortmund_dxixjxks
        except AttributeError:
            pass
        try:
            r34x_sum_inv = self.r34x_sum_inv
        except AttributeError:
            self.Vis_Dortmund()
            r34x_sum_inv = self.r34x_sum_inv
        rs_34 = self.rs_34
        mr34x_sum_inv4_6 = -6.0*r34x_sum_inv*r34x_sum_inv*r34x_sum_inv*r34x_sum_inv
        
        d3Vis_Dortmund = [[[[ri*rj*rk*rl*mr34x_sum_inv4_6 for rl in rs_34] for rk in rs_34]
                                               for rj in rs_34] for ri in rs_34]
        self._d3Vis_Dortmund_dxixjxks = d3Vis_Dortmund
        return d3Vis_Dortmund
    
    def Xs(self):
        try:
            return self._Xs
        except AttributeError:
            pass
        # [subgroup][component] = number of subgroup in component where subgroup
        # is an index, numbered sequentially by the number of subgroups in the mixture
        vs, xs = self.vs, self.xs
        cmps, groups = self.cmps, self.groups
        subgroup_sums = []
        for i in groups:
            tot = 0.0
            for j in cmps:
                tot += vs[i][j]*xs[j]
            subgroup_sums.append(tot)
            
        self.subgroup_sums = subgroup_sums # Used in several derivatives
        self.Xs_sum_inv = sum_inv = 1.0/sum(subgroup_sums)

        self._Xs = Xs = [subgroup_sums[i]*sum_inv for i in groups]

        return Xs
    
    def Thetas(self):
        try:
            return self._Thetas
        except AttributeError:
            pass
        Qs, groups = self.Qs, self.groups
        Xs = self.Xs()
        
        tot = 0.0
        for i in groups:
            tot += Xs[i]*Qs[i]
        self.Thetas_sum_inv = tot_inv = 1.0/tot
        self._Thetas = Thetas = [Qs[i]*Xs[i]*tot_inv for i in groups]
        return Thetas
    
    def dThetas_dxs(self):
        try:
            return self._dThetas_dxs
        except AttributeError:
            pass
        
        F = self.Xs_sum_inv
        G = self.Thetas_sum_inv
        Qs, cmps, groups, xs = self.Qs, self.cmps, self.groups, self.xs
        Xs = self.Xs()
        Thetas = self.Thetas()
        vs = self.vs
        
        VS = [sum(vs[j][i] for j in groups) for i in cmps]
        VSXS = [sum(vs[i][j]*xs[j] for j in cmps) for i in groups]
        
        # Index [subgroup][component]
        self._dThetas_dxs = dThetas_dxs = []
        for i in groups:
            Qi = Qs[i]
            row = []
            for j in cmps:
                tot = 0.0
                for k in groups:
                    tot += F*Qs[k]*VS[j]*VSXS[k] - Qs[k]*vs[k][j]
                
                v = F*G*Qi*(F*G*VSXS[i]*tot - F*VS[j]*VSXS[i] + vs[i][j])
                row.append(v)
            dThetas_dxs.append(row)
        return dThetas_dxs

    def d2Thetas_dxixjs(self):
        try:
            return self._d2Thetas_dxixjs
        except AttributeError:
            pass
                
        F = self.Xs_sum_inv
        G = self.Thetas_sum_inv
        Qs, cmps, groups, xs = self.Qs, self.cmps, self.groups, self.xs
        vs = self.vs
        
        
        VS = [sum(vs[j][i] for j in groups) for i in cmps]
        VSXS = [sum(vs[i][j]*xs[j] for j in cmps) for i in groups]
        
        QsVSXS = [Qs[i]*VSXS[i] for i in groups]
        QsVSXS_sum_inv = 1.0/sum(QsVSXS)
        
        # Index [comp][comp][subgroup]
        self._d2Thetas_dxixjs = d2Thetas_dxixjs = []
        for j in cmps:
            matrix = []
            for k in cmps:
                row = []
                for i in groups:
                    tot0, tot1, tot2 = 0.0, 0.0, 0.0
                    for n in groups:
                        tot0 += -2.0*F*Qs[n]*VS[j]*VS[k]*VSXS[n] + Qs[n]*VS[j]*vs[n][k] + Qs[n]*VS[k]*vs[n][j]
                        # These are each used in three places
                        tot1 += -F*Qs[n]*VS[j]*VSXS[n] + Qs[n]*vs[n][j]
                        tot2 += -F*Qs[n]*VS[k]*VSXS[n] + Qs[n]*vs[n][k]
                        
                    v = -F*VS[j]*vs[i][k] - F*VS[k]*vs[i][j]
                    v += 2.0*F*F*VS[j]*VS[k]*VSXS[i]
                    
                    v += F*VSXS[i]*tot0*QsVSXS_sum_inv
                    
                    v += 2.0*VSXS[i]*tot1*tot2*QsVSXS_sum_inv*QsVSXS_sum_inv

                    # For both of these duplicate terms, j goes with k; k with j                    
                    v -= vs[i][j]*tot2*QsVSXS_sum_inv
                    v -= vs[i][k]*tot1*QsVSXS_sum_inv
                    
                    v += F*VS[j]*VSXS[i]*tot2*QsVSXS_sum_inv
                    v += F*VS[k]*VSXS[i]*tot1*QsVSXS_sum_inv

                    # Constant multiplier
                    v *= Qs[i]*QsVSXS_sum_inv
                        
                    row.append(v)
                matrix.append(row)
            d2Thetas_dxixjs.append(matrix)
        return d2Thetas_dxixjs



    def lnGammas_subgroups(self):
        # Temperature and composition dependent!
        try:
            return self._lnGammas_subgroups
        except AttributeError:
            pass
        Thetas, Qs = self.Thetas(), self.Qs
        psis = self.psis()
        cmps, groups = self.cmps, self.groups
        
        self._lnGammas_subgroups = lnGammas_subgroups = []
        for k in groups:
            log_sum = 0.0
            for m in groups:
                log_sum += Thetas[m]*psis[m][k]
            log_sum = log(log_sum)
            
            last = 0.0
            for m in groups:
                sub_subs = 0.0
                for n in groups:
                    sub_subs += Thetas[n]*psis[n][m]
                last += Thetas[m]*psis[k][m]/sub_subs
                
            v = Qs[k]*(1.0 - log_sum - last)
            lnGammas_subgroups.append(v)
        return lnGammas_subgroups
    
    
    def dlnGammas_subgroups_dxs(self):
        try:
            return self._dlnGammas_subgroups_dxs
        except:
            pass
        Thetas, Qs = self.Thetas(), self.Qs
        psis = self.psis()
        dThetas_dxs = self.dThetas_dxs()

        cmps, groups = self.cmps, self.groups
        
        Theta_Psi_sum_invs = [1.0/sum(Thetas[k]*psis[k][j] for k in groups) for j in groups]
        self.Theta_Psi_sum_invs = Theta_Psi_sum_invs
        
        # Index by [subgroup][component]
        tot0s, tot1s = [], []
        for k in groups:
            row0, row1 = [], []
            for i in cmps:
                tot0, tot1 = 0.0, 0.0
                for m in groups:
                    tot0 += psis[m][k]*dThetas_dxs[m][i]
                    tot1 += psis[k][m]*dThetas_dxs[m][i]
                
                row0.append(tot0)
                row1.append(tot1)
            tot0s.append(row0)
            tot1s.append(row1)
            
        self._Ws = tot0s
        self._Ys = tot1s
                
        matrix = []
        for k in groups:
            row = []
            for i in cmps:
                tot = -tot0s[k][i]*Theta_Psi_sum_invs[k]
                for m in groups:
                    tot -= psis[k][m]*dThetas_dxs[m][i]*Theta_Psi_sum_invs[m]

                    tot += tot0s[m][i]*Thetas[m]*psis[k][m]*Theta_Psi_sum_invs[m]**2

                row.append(tot*Qs[k])
            matrix.append(row)
                
        
        
        self._dlnGammas_subgroups_dxs = matrix
        return matrix

    def d2lnGammas_subgroups_d2xs(self):
        try:
            return self._d2lnGammas_subgroups_d2xs
        except:
            pass
        Thetas, Qs = self.Thetas(), self.Qs
        psis = self.psis()
        dThetas_dxs, d2Thetas_dxixjs = self.dThetas_dxs(), self.d2Thetas_dxixjs()
        
        self.dlnGammas_subgroups_dxs() # make sure dependent variables are calculated

        cmps, groups = self.cmps, self.groups
        
        Zs = self.Theta_Psi_sum_invs
        Ws, Ys = self._Ws, self._Ys
        
        def K(k, i, j):
            # k: group
            # i, j : mole fracions derivavtive indexes
            tot = 0.0
            for m in groups:
                # Index [comp][comp][subgroup] for d2Thetas_dxixjs
                tot += psis[m][k]*d2Thetas_dxixjs[i][j][m]
            return tot
        
        self._d2lnGammas_subgroups_d2xs = d2lnGammas_subgroups_d2xs = []
        for i in cmps:
            matrix = []
            for j in cmps:
                row = []
                for k in groups:
                    v = Zs[k]*K(k, i, j)
                    v -= Ws[k][i]*Ws[k][j]*Zs[k]**2
                    for m in groups:
                        v -= Zs[m]**2*K(m, i, j)*Thetas[m]*psis[k][m]
                        
                        v += Zs[m]*psis[k][m]*d2Thetas_dxixjs[i][j][m]
                        
                        v -= Ws[m][j]*Zs[m]**2*psis[k][m]*dThetas_dxs[m][i] + Ws[m][i]*Zs[m]**2*psis[k][m]*dThetas_dxs[m][j]
                        
                        v += 2.0*Ws[m][i]*Ws[m][j]*Zs[m]**3*Thetas[m]*psis[k][m]
                    row.append(-v*Qs[k])
                matrix.append(row)
            d2lnGammas_subgroups_d2xs.append(matrix)
        return d2lnGammas_subgroups_d2xs
                    
        

    
    @staticmethod
    def dlnGammas_subgroups_dT_meth(groups, Qs, psis, dpsis_dT, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum):
        # TODO document
        row = []
        for i in groups:
            psisi, dpsis_dTi = psis[i], dpsis_dT[i]
            tot = 0.0
            for j in groups:
                tot += (psisi[j]*Theta_dPsidT_sum[j]*Theta_Psi_sum_invs[j]
                       - dpsis_dTi[j])*Theta_Psi_sum_invs[j]*Thetas[j]
            v = Qs[i]*(tot - Theta_dPsidT_sum[i]*Theta_Psi_sum_invs[i])
            row.append(v)
        return row
    
    def dlnGammas_subgroups_dT(self):
        try:
            return self._dlnGammas_subgroups_dT
        except:
            pass
        Xs, Thetas, Qs = self.Xs(), self.Thetas(), self.Qs
        psis, dpsis_dT = self.psis(), self.dpsis_dT()
        cmps, groups = self.cmps, self.groups
        
        Theta_Psi_sum_invs = [1.0/sum(Thetas[k]*psis[k][j] for k in groups) for j in groups]
        Theta_dPsidT_sum = [sum(Thetas[k]*dpsis_dT[k][j] for k in groups) for j in groups]
        
        row = UNIFAC.dlnGammas_subgroups_dT_meth(groups, Qs, psis, dpsis_dT, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum)
        
        self._dlnGammas_subgroups_dT = row
        return row

    @staticmethod
    def d2lnGammas_subgroups_dT2_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum):
        # TODO document

        Us_inv, Fs, Gs = Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum
        row = []
        for i in groups:
            # TODO optimize
            tot0 = 0.0
            for j in groups:
                tot0 += Thetas[j]*d2psis_dT2[i][j]*Us_inv[j]
                tot0 -= (Gs[j]*Thetas[j]*psis[i][j] + 2.0*Fs[j]*Thetas[j]*dpsis_dT[i][j])*Us_inv[j]*Us_inv[j]
                tot0 += 2.0*Fs[j]*Fs[j]*Thetas[j]*psis[i][j]*Us_inv[j]*Us_inv[j]*Us_inv[j]
                
            v = -Qs[i]*(Gs[i]*Us_inv[i] - Fs[i]*Fs[i]*Us_inv[i]*Us_inv[i] + tot0)
            row.append(v)
        return row


                
    def d2lnGammas_subgroups_dT2(self):
        try:
            return self._d2lnGammas_subgroups_dT2
        except:
            pass
        Xs, Thetas, Qs = self.Xs(), self.Thetas(), self.Qs
        psis, dpsis_dT, d2psis_dT2 = self.psis(), self.dpsis_dT(), self.d2psis_dT2()
        cmps, groups = self.cmps, self.groups

        Theta_Psi_sum_invs = [1.0/sum(Thetas[k]*psis[k][j] for k in groups) for j in groups]
        Theta_dPsidT_sum = [sum(Thetas[k]*dpsis_dT[k][j] for k in groups) for j in groups]
        Theta_d2PsidT2_sum = [sum(Thetas[k]*d2psis_dT2[k][j] for k in groups) for j in groups]
        
        row = UNIFAC.d2lnGammas_subgroups_dT2_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, Thetas, 
                                                   Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum)

        self._d2lnGammas_subgroups_dT2 = row
        return row

    @staticmethod
    def d3lnGammas_subgroups_dT3_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, d3psis_dT3, 
                                      Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum,
                                      Theta_d2PsidT2_sum, Theta_d3PsidT3_sum):
        # TODO document

        Us_inv, Fs, Gs, Hs = Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum, Theta_d3PsidT3_sum
        row = []
        for i in groups:
            tot = 0.0
            for j in groups:
                tot -= Thetas[j]*d3psis_dT3[i][j]*Us_inv[j]
                tot += Hs[j]*Thetas[j]*psis[i][j]*Us_inv[j]*Us_inv[j]
                tot -= 6.0*Fs[j]*Fs[j]*Thetas[j]*dpsis_dT[i][j]*Us_inv[j]*Us_inv[j]*Us_inv[j]
                tot += 3.0*Fs[j]*Thetas[j]*d2psis_dT2[i][j]*Us_inv[j]*Us_inv[j]
                
                tot += 3.0*Gs[j]*Thetas[j]*dpsis_dT[i][j]*Us_inv[j]*Us_inv[j]
                tot += 6.0*Fs[j]**3*Thetas[j]*psis[i][j]*Us_inv[j]**4
                tot -= 6.0*Fs[j]*Gs[j]*Thetas[j]*psis[i][j]*Us_inv[j]**3

                
            v = Qs[i]*(-Hs[i]*Us_inv[i] - 2.0*Fs[i]**3*Us_inv[i]**3 + 3.0*Fs[i]*Gs[i]*Us_inv[i]**2 + tot)
            row.append(v)
        return row

    def d3lnGammas_subgroups_dT3(self):
        try:
            return self._d3lnGammas_subgroups_dT3
        except:
            pass
        Xs, Thetas, Qs = self.Xs(), self.Thetas(), self.Qs
        psis, dpsis_dT, d2psis_dT2, d3psis_dT3 = self.psis(), self.dpsis_dT(), self.d2psis_dT2(), self.d3psis_dT3()
        cmps, groups = self.cmps, self.groups

        Theta_Psi_sum_invs = [1.0/sum(Thetas[k]*psis[k][j] for k in groups) for j in groups]
        Theta_dPsidT_sum = [sum(Thetas[k]*dpsis_dT[k][j] for k in groups) for j in groups]
        Theta_d2PsidT2_sum = [sum(Thetas[k]*d2psis_dT2[k][j] for k in groups) for j in groups]
        Theta_d3PsidT3_sum = [sum(Thetas[k]*d3psis_dT3[k][j] for k in groups) for j in groups]
        
        row = UNIFAC.d3lnGammas_subgroups_dT3_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, d3psis_dT3, 
                                      Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum,
                                      Theta_d2PsidT2_sum, Theta_d3PsidT3_sum)
        
        self._d3lnGammas_subgroups_dT3 = row
        return row
        
    def Xs_pure(self):
        try:
            return self._Xs_pure
        except AttributeError:
            pass
        # Independent of mole fractions and temperature
        vs, cmp_v_count = self.vs, self.cmp_v_count
        cmps, groups = self.cmps, self.groups
        
        Xs_pure = []
        for i in groups:
            row = []
            for j in cmps:
                row.append(vs[i][j]/cmp_v_count[j])
            Xs_pure.append(row)
        self._Xs_pure = Xs_pure
        return Xs_pure
    
    def Thetas_pure(self):
        # Composition and temperature independent
        try:
            return self._Thetas_pure
        except AttributeError:
            pass
        
        Xs_pure, Qs = self.Xs_pure(), self.Qs
        cmps, groups = self.cmps, self.groups
        Thetas_pure = []
        for i in cmps:
            # groups = self.cmp_group_idx[i]
            tot = 0.0
            for j in groups:
                tot += Qs[j]*Xs_pure[j][i]
            tot_inv = 1.0/tot
            row = [Qs[j]*Xs_pure[j][i]*tot_inv for j in groups]
            Thetas_pure.append(row)
        
        # Revised! Keep in order [component][subgroup]
#         Get indexing convention back to [subgroup][component]
        self._Thetas_pure = Thetas_pure# = list(map(list, zip(*Thetas_pure)))
        return Thetas_pure

    
    def lnGammas_subgroups_pure(self):
        # Temperature dependent only!
        try:
            return self._lnGammas_subgroups_pure
        except AttributeError:
            pass
        Xs_pure, Thetas_pure, Qs = self.Xs_pure(), self.Thetas_pure(), self.Qs
        psis = self.psis()
        cmps, groups = self.cmps, self.groups
        
        cmp_group_idx = self.cmp_group_idx
        
        matrix = []
        for i in cmps:
            groups2 = cmp_group_idx[i]
            row = []
            for k in groups:
                log_sum = 0.0
                for m in groups2:
                    log_sum += Thetas_pure[i][m]*psis[m][k]
                log_sum = log(log_sum)
                
                last = 0.0
                for m in groups2:
                    sub_subs = 0.0
                    for n in groups:
                        sub_subs += Thetas_pure[i][n]*psis[n][m]
                    last += Thetas_pure[i][m]*psis[k][m]/sub_subs

                v = Qs[k]*(1.0 - log_sum - last)
                if k not in groups2:
                    v = 0.0
                row.append(v)
            matrix.append(row)
            
        # Transpose
        self._lnGammas_subgroups_pure = lnGammas_subgroups_pure = list(map(list, zip(*matrix)))
        return lnGammas_subgroups_pure

    def dlnGammas_subgroups_pure_dT(self):
        try:
            return self._dlnGammas_subgroups_pure_dT
        except:
            pass

        Xs_pure, Thetas_pure, Qs = self.Xs_pure(), self.Thetas_pure(), self.Qs
        psis, dpsis_dT = self.psis(), self.dpsis_dT()
        cmps, groups = self.cmps, self.groups
        cmp_group_idx = self.cmp_group_idx
        
        # Index by [component][subgroup]
        Theta_Psi_sum_pure_invs = [[1.0/sum(Thetas_pure[i][k]*psis[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_dPsidT_sum_pure = [[sum(Thetas_pure[i][k]*dpsis_dT[k][j] for k in groups) for j in groups] for i in cmps]
        
        mat = []
        for m in cmps:
            groups2 = cmp_group_idx[m]
            Thetas = Thetas_pure[m]
            Theta_Psi_sum_invs = Theta_Psi_sum_pure_invs[m]
            Theta_dPsidT_sum = Theta_dPsidT_sum_pure[m]
            
            row = UNIFAC.dlnGammas_subgroups_dT_meth(groups, Qs, psis, dpsis_dT, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum)
            for i in groups:
                if i not in groups2:
                    row[i] = 0.0
            mat.append(row)
            
        mat = list(map(list, zip(*mat)))
        # Index by [subgroup][component]
        self._dlnGammas_subgroups_pure_dT = mat
        return mat

    def d2lnGammas_subgroups_pure_dT2(self):
        try:
            return self._d2lnGammas_subgroups_pure_dT2
        except:
            pass

        Xs_pure, Thetas_pure, Qs = self.Xs_pure(), self.Thetas_pure(), self.Qs
        psis, dpsis_dT, d2psis_dT2 = self.psis(), self.dpsis_dT(), self.d2psis_dT2()
        cmps, groups = self.cmps, self.groups
        cmp_group_idx = self.cmp_group_idx
        
        # Index by [component][subgroup]
        Theta_Psi_sum_pure_invs = [[1.0/sum(Thetas_pure[i][k]*psis[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_dPsidT_sum_pure = [[sum(Thetas_pure[i][k]*dpsis_dT[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_d2PsidT2_sum_pure = [[sum(Thetas_pure[i][k]*d2psis_dT2[k][j] for k in groups) for j in groups] for i in cmps]
        
        mat = []
        for m in cmps:
            groups2 = cmp_group_idx[m]
            Thetas = Thetas_pure[m]
            Theta_Psi_sum_invs = Theta_Psi_sum_pure_invs[m]
            Theta_dPsidT_sum = Theta_dPsidT_sum_pure[m]
            Theta_d2PsidT2_sum = Theta_d2PsidT2_sum_pure[m]
            
            row = UNIFAC.d2lnGammas_subgroups_dT2_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum)
            for i in groups:
                if i not in groups2:
                    row[i] = 0.0
            mat.append(row)
            
        mat = list(map(list, zip(*mat)))
        # Index by [subgroup][component]
        self._d2lnGammas_subgroups_pure_dT2 = mat
        return mat

    def d3lnGammas_subgroups_pure_dT3(self):
        try:
            return self._d3lnGammas_subgroups_pure_dT3
        except:
            pass

        Xs_pure, Thetas_pure, Qs = self.Xs_pure(), self.Thetas_pure(), self.Qs
        psis, dpsis_dT, d2psis_dT2, d3psis_dT3 = self.psis(), self.dpsis_dT(), self.d2psis_dT2(), self.d3psis_dT3()
        cmps, groups = self.cmps, self.groups
        cmp_group_idx = self.cmp_group_idx
        
        # Index by [component][subgroup]
        Theta_Psi_sum_pure_invs = [[1.0/sum(Thetas_pure[i][k]*psis[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_dPsidT_sum_pure = [[sum(Thetas_pure[i][k]*dpsis_dT[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_d2PsidT2_sum_pure = [[sum(Thetas_pure[i][k]*d2psis_dT2[k][j] for k in groups) for j in groups] for i in cmps]
        Theta_d3PsidT3_sum_pure = [[sum(Thetas_pure[i][k]*d3psis_dT3[k][j] for k in groups) for j in groups] for i in cmps]

        mat = []
        for m in cmps:
            groups2 = cmp_group_idx[m]
            Thetas = Thetas_pure[m]
            Theta_Psi_sum_invs = Theta_Psi_sum_pure_invs[m]
            Theta_dPsidT_sum = Theta_dPsidT_sum_pure[m]
            Theta_d2PsidT2_sum = Theta_d2PsidT2_sum_pure[m]
            Theta_d3PsidT3_sum = Theta_d3PsidT3_sum_pure[m]
            
            row = UNIFAC.d3lnGammas_subgroups_dT3_meth(groups, Qs, psis, dpsis_dT, d2psis_dT2, d3psis_dT3, Thetas, Theta_Psi_sum_invs, Theta_dPsidT_sum, Theta_d2PsidT2_sum, Theta_d3PsidT3_sum)
            for i in groups:
                if i not in groups2:
                    row[i] = 0.0
            mat.append(row)
            
        mat = list(map(list, zip(*mat)))
        # Index by [subgroup][component]
        self._d3lnGammas_subgroups_pure_dT3 = mat
        return mat
    
    def lngammas_r(self):
        try:
            return self._lngammas_r
        except AttributeError:
            pass
        lnGammas_subgroups_pure = self.lnGammas_subgroups_pure()
        lnGammas_subgroups = self.lnGammas_subgroups()
        vs = self.vs
        cmps, groups = self.cmps, self.groups
        
        self._lngammas_r = lngammas_r = []
        for i in cmps:
            tot = 0.0
            for k in groups:
                tot += vs[k][i]*(lnGammas_subgroups[k] - lnGammas_subgroups_pure[k][i])
            lngammas_r.append(tot)
            
        return lngammas_r
    
    def dlngammas_r_dT(self):
        try:
            return self._dlngammas_r_dT
        except AttributeError:
            pass
        dlnGammas_subgroups_pure_dT = self.dlnGammas_subgroups_pure_dT()
        dlnGammas_subgroups_dT = self.dlnGammas_subgroups_dT()
        vs = self.vs
        cmps, groups = self.cmps, self.groups
        
        self._dlngammas_r_dT = dlngammas_r_dT = []
        for i in cmps:
            tot = 0.0
            for k in groups:
                tot += vs[k][i]*(dlnGammas_subgroups_dT[k] - dlnGammas_subgroups_pure_dT[k][i])
            dlngammas_r_dT.append(tot)
            
        return dlngammas_r_dT
    dlngammas_dT = dlngammas_r_dT

    def d2lngammas_r_dT2(self):
        try:
            return self._d2lngammas_r_dT2
        except AttributeError:
            pass
        d2lnGammas_subgroups_pure_dT2 = self.d2lnGammas_subgroups_pure_dT2()
        d2lnGammas_subgroups_dT2 = self.d2lnGammas_subgroups_dT2()
        vs = self.vs
        cmps, groups = self.cmps, self.groups
        
        self._d2lngammas_r_dT2 = d2lngammas_r_dT2 = []
        for i in cmps:
            tot = 0.0
            for k in groups:
                tot += vs[k][i]*(d2lnGammas_subgroups_dT2[k] - d2lnGammas_subgroups_pure_dT2[k][i])
            d2lngammas_r_dT2.append(tot)
            
        return d2lngammas_r_dT2
    d2lngammas_dT2 = d2lngammas_r_dT2

    def d3lngammas_r_dT3(self):
        try:
            return self._d3lngammas_r_dT3
        except AttributeError:
            pass
        d3lnGammas_subgroups_pure_dT3 = self.d3lnGammas_subgroups_pure_dT3()
        d3lnGammas_subgroups_dT3 = self.d3lnGammas_subgroups_dT3()
        vs = self.vs
        cmps, groups = self.cmps, self.groups
        
        self._d3lngammas_r_dT3 = d3lngammas_r_dT3 = []
        for i in cmps:
            tot = 0.0
            for k in groups:
                tot += vs[k][i]*(d3lnGammas_subgroups_dT3[k] - d3lnGammas_subgroups_pure_dT3[k][i])
            d3lngammas_r_dT3.append(tot)
            
        return d3lngammas_r_dT3
    d3lngammas_dT3 = d3lngammas_r_dT3
    
    def GE(self):
        try:
            return self._GE
        except AttributeError:
            pass
        T, xs, cmps = self.T, self.xs, self.cmps
        lngammas_r = self.lngammas_r()
        lngammas_c = self.lngammas_c()
        GE = 0.0
        for i in cmps:
            GE += xs[i]*(lngammas_c[i] + lngammas_r[i])
        GE *= R*T
        self._GE = GE
        return GE

    def dGE_dT(self):
        try:
            return self._dGE_dT
        except AttributeError:
            pass
        T, xs, cmps = self.T, self.xs, self.cmps
        lngammas_r = self.lngammas_r()
        lngammas_c = self.lngammas_c()
        dlngammas_r_dT = self.dlngammas_r_dT()
        dGE_dT = 0.0
        tot0, tot1 = 0.0, 0.0
        for i in cmps:
            tot0 += xs[i]*dlngammas_r_dT[i]
            tot1 += xs[i]*(lngammas_c[i] + lngammas_r[i])
            
        dGE_dT = R*T*tot0 + R*tot1
        
        self._dGE_dT = dGE_dT
        return dGE_dT

    def d2GE_dT2(self):
        try:
            return self._d2GE_dT2
        except AttributeError:
            pass
        T, xs, cmps = self.T, self.xs, self.cmps
        dlngammas_r_dT = self.dlngammas_r_dT()
        d2lngammas_r_dT2 = self.d2lngammas_r_dT2()
        tot0, tot1 = 0.0, 0.0
        for i in cmps:
            tot0 += xs[i]*d2lngammas_r_dT2[i]
            tot1 += 2.0*xs[i]*(dlngammas_r_dT[i])
            
        d2GE_dT2 = R*(T*tot0 + tot1)
        self._d2GE_dT2 = d2GE_dT2
        return d2GE_dT2

    def d3GE_dT3(self):
        try:
            return self._d3GE_dT3
        except AttributeError:
            pass
        T, xs, cmps = self.T, self.xs, self.cmps
        d2lngammas_r_dT2 = self.d2lngammas_r_dT2()
        d3lngammas_r_dT3 = self.d3lngammas_r_dT3()

        tot0, tot1 = 0.0, 0.0
        for i in cmps:
            tot0 += xs[i]*d3lngammas_r_dT3[i]
            tot1 += 3.0*xs[i]*(d2lngammas_r_dT2[i])
            
        d3GE_dT3 = R*(T*tot0 + tot1)
        
        self._d3GE_dT3 = d3GE_dT3
        return d3GE_dT3

    def gammas(self):
        try:
            return self._gammas
        except:
            pass
        xs, cmps = self.xs, self.cmps
        lngammas_r = self.lngammas_r()
        lngammas_c = self.lngammas_c()
        self._gammas = [exp(lngammas_r[i] + lngammas_c[i]) for i in cmps]
        return self._gammas
    
    def lngammas_c(self):
        r'''
        
        .. math::
            \ln \gamma_i^c = 1 - {V'}_i + \ln({V'}_i) - 5q_i \left(1
            - \frac{V_i}{F_i}+ \ln\left(\frac{V_i}{F_i}\right)\right)
            
        .. math::
            V'_i = \frac{r_i^{3/4}}{\sum_j r_j^{3/4}x_j}
        
        .. math::
            V_i = \frac{r_i}{\sum_j r_j x_j}
            
        .. math::
            F_i = \frac{q_i}{\sum_j q_j x_j}

        '''
        try:
            return self._lngammas_c
        except AttributeError:
            pass
        Vis = self.Vis()
        cmps, version, qs = self.cmps, self.version, self.qs
        if self.version == 1:
            Vis_Dortmund = self.Vis_Dortmund()
        else:
            Vis_Dortmund = Vis
        Fis = self.Fis()
        
        lngammas_c = []
        for i in cmps:
            Vi_Fi = Vis[i]/Fis[i]
            val = (1.0 - Vis_Dortmund[i] + log(Vis_Dortmund[i])
                    - 5.0*qs[i]*(1.0 - Vi_Fi + log(Vi_Fi)))
            lngammas_c.append(val)
            
        self._lngammas_c = lngammas_c
        return lngammas_c
    
    def dlngammas_c_dT(self):
        return [0.0]*self.N
    
    def d2lngammas_c_dT2(self):
        return [0.0]*self.N
    
    def d3lngammas_c_dT3(self):
        return [0.0]*self.N
       
    def d2lngammas_c_dTdx(self):
        # Since T derivative is zero
        return [0.0]*self.N

            
    def dlngammas_c_dxs(self):
        r'''
        .. math::
            \frac{\partial \ln \gamma^c_i}{\partial x_j} = 
            -5q_i\left[ \left( \frac{\frac{\partial V_i}{\partial x_j}}{F_i} - \frac{V_i \frac{\partial F_i}{\partial x_j}}{F_i^2}
            \right)\frac{F_i}{V_i} - \frac{\frac{\partial V_i}{\partial x_j}}{F_i} 
            + \frac{V_i\frac{\partial F_i}{\partial x_j}}{F_i^2}
            \right]
              - \frac{\partial V_i'}{\partial x_j} 
              + \frac{\frac{\partial V_i'}{\partial x_j}}{V_i'}
              
        '''
        try:
            return self._dlngammas_c_dxs
        except AttributeError:
            pass
        cmps, version, qs = self.cmps, self.version, self.qs
        Vis = self.Vis()
        dVis_dxs = self.dVis_dxs()

        Fis = self.Fis()
        dFis_dxs = self.dFis_dxs()
        
        if self.version == 1:
            Vis_Dortmund = self.Vis_Dortmund()
            dVis_Dortmund_dxs = self.dVis_Dortmund_dxs()
        else:
            Vis_Dortmund = Vis
            dVis_Dortmund_dxs = dVis_dxs
            
        # index style - [THE GAMMA FOR WHICH THE DERIVATIVE IS BEING CALCULATED][THE VARIABLE BEING CHANGED CAUsING THE DIFFERENCE]
        
        dlngammas_c_dxs = []
        for i in cmps:
            row = []
            Fi_inv = 1.0/Fis[i]
            for j in cmps:
                val = -5.0*qs[i]*((dVis_dxs[i][j] - Vis[i]*dFis_dxs[i][j]*Fi_inv)/Vis[i]
                - dVis_dxs[i][j]*Fi_inv + Vis[i]*dFis_dxs[i][j]*Fi_inv*Fi_inv
                ) - dVis_Dortmund_dxs[i][j] + dVis_Dortmund_dxs[i][j]/Vis_Dortmund[i]
                row.append(val)
            
            dlngammas_c_dxs.append(row)
            
        self._dlngammas_c_dxs = dlngammas_c_dxs
        return dlngammas_c_dxs

    ''' Sympy code used to get these derivatives - not yet validated with numerical values from SymPy!
        Second and third derivative formulas generated with SymPy.
    from sympy import *
    
    N = 3
    cmps = range(N)
    xs = x0, x1, x2 = symbols('x0, x1, x2')
    rs = r0, r1, r2 = symbols('r0, r1, r2')
    qs = q0, q1, q2 = symbols('q0, q1, q2') # Pure component property (made from subgroups, but known)
    
    rsxs = sum([rs[i]*xs[i] for i in cmps])
    Vis = [rs[i]/rsxs for i in cmps]
    
    qsxs = sum([qs[i]*xs[i] for i in cmps])
    Fis = [qs[i]/qsxs for i in cmps]
    
    Vis = V0, V1, V2 = symbols('V0, V1, V2', cls=Function)
    VisD = V0D, V1D, V2D = symbols('V0D, V1D, V2D', cls=Function)
    Fis = F0, F1, F2 = symbols('F0, F1, F2', cls=Function)
    Vis = [Vis[i](x0, x1, x2) for i in cmps]
    VisD = [VisD[i](x0, x1, x2) for i in cmps]
    Fis = [Fis[i](x0, x1, x2) for i in cmps]
    
    loggammacs = [1 - VisD[i] + log(VisD[i]) - 5*qs[i]*(1 - Vis[i]/Fis[i]
                  + log(Vis[i]/Fis[i])) for i in cmps]
    # Variable to use for substitutions
    Vi, ViD, Fi, xj, xk, xm, qi = symbols('V_i, Vi\', F_i, x_j, x_k, x_m, q_i')
    
    # First derivative
    good_first = diff(loggammacs[0], x1).subs(V0(x0, x1, x2), Vi).subs(F0(x0, x1, x2), Fi).subs(V0D(x0, x1, x2), ViD).subs(x1, xj).subs(q0, qi)
    good_first = simplify(expand(simplify(good_first)))
    
    # Second derivative
    good_second = diff(loggammacs[0], x1, x2).subs(V0(x0, x1, x2), Vi).subs(F0(x0, x1, x2), Fi).subs(V0D(x0, x1, x2), ViD).subs(x1, xj).subs(x2, xk).subs(q0, qi)
    
    # Third derivative
    good_third = diff(loggammacs[0], x0, x1, x2).subs(V0(x0, x1, x2), Vi).subs(F0(x0, x1, x2), Fi).subs(V0D(x0, x1, x2), ViD).subs(x0, xj).subs(x1, xk).subs(x2, xm).subs(q0, qi)
    good_third = simplify(good_third)


    '''
    def d2lngammas_c_dxixjs(self):
        r'''
        .. math::
            \frac{\partial \ln \gamma^c_i}{\partial x_j \partial x_k} = 
            5 q_{i} \left(\frac{- \frac{d^{2}}{d x_{k}d x_{j}} V_{i} + \frac{V_{i}
            \frac{d^{2}}{d x_{k}d x_{j}} F_{i}}{F_{i}} + \frac{\frac{d}{d x_{j}} F_{i} 
            \frac{d}{d x_{k}} V_{i}}{F_{i}} + \frac{\frac{d}{d x_{k}} F_{i}
            \frac{d}{d x_{j}} V_{i}}{F_{i}} - \frac{2 V_{i} \frac{d}{d x_{j}}
            F_{i} \frac{d}{d x_{k}} F_{i}}{F_{i}^{2}}}{V_{i}} + \frac{\left(
            \frac{d}{d x_{j}} V_{i} - \frac{V_{i} \frac{d}{d x_{j}} F_{i}}
            {F_{i}}\right) \frac{d}{d x_{k}} V_{i}}{V_{i}^{2}}
            + \frac{\frac{d^{2}}{d x_{k}d x_{j}} V_{i}}{F_{i}} - \frac{\left(
            \frac{d}{d x_{j}} V_{i} - \frac{V_{i} \frac{d}{d x_{j}} F_{i}}{
            F_{i}}\right) \frac{d}{d x_{k}} F_{i}}{F_{i} V_{i}} - \frac{V_{i}
            \frac{d^{2}}{d x_{k}d x_{j}} F_{i}}{F_{i}^{2}} - \frac{\frac{d}
            {d x_{j}} F_{i} \frac{d}{d x_{k}} V_{i}}{F_{i}^{2}} 
            - \frac{\frac{d}{d x_{k}} F_{i} \frac{d}{d x_{j}} V_{i}}{F_{i}^{2}}
            + \frac{2 V_{i} \frac{d}{d x_{j}} F_{i} \frac{d}{d x_{k}} F_{i}}
            {F_{i}^{3}}\right) - \frac{d^{2}}{d x_{k}d x_{j}} Vi' 
            + \frac{\frac{d^{2}}{d x_{k}d x_{j}} Vi'}{Vi'} - \frac{\frac{d}
            {d x_{j}} Vi' \frac{d}{d x_{k}} Vi'}{Vi'^{2}}
            
        '''
        try:
            return self._d2lngammas_c_dxixjs
        except AttributeError:
            pass
        cmps, version, qs = self.cmps, self.version, self.qs
        Vis = self.Vis()
        dVis_dxs = self.dVis_dxs()
        d2Vis_dxixjs = self.d2Vis_dxixjs()

        Fis = self.Fis()
        dFis_dxs = self.dFis_dxs()
        d2Fis_dxixjs = self.d2Fis_dxixjs()
        
        if self.version == 1:
            Vis_Dortmund = self.Vis_Dortmund()
            dVis_Dortmund_dxs = self.dVis_Dortmund_dxs()
            d2Vis_Dortmund_dxixjs =self.d2Vis_Dortmund_dxixjs()
        else:
            Vis_Dortmund = Vis
            dVis_Dortmund_dxs = dVis_dxs
            d2Vis_Dortmund_dxixjs = d2Vis_dxixjs

        d2lngammas_c_dxixjs = []
        for i in cmps:
            Vi = Vis[i]
            qi = qs[i]
            ViD = Vis_Dortmund[i]
            ViD_inv2 = 1.0/(ViD*ViD)
            Fi = Fis[i]
            x1 = 1.0/Fi
            x4 = x1*x1
            Fi_inv3 = x1*x1*x1
            x5 = Vis[i]*x4
            x15 = 1.0/Vi
            Vi_inv2 = x15*x15
            matrix = []
            for j in cmps:
                x6 = dFis_dxs[i][j]
                x10 = dVis_dxs[i][j]
                dViD_dxj = dVis_Dortmund_dxs[i][j]
                row = []
                for k in cmps:
                    x0 = d2Vis_Dortmund_dxixjs[i][j][k]
                    x2 = d2Vis_dxixjs[i][j][k]
                    x3 = d2Fis_dxixjs[i][j][k]
                    x7 = dVis_dxs[i][k]
                    dViD_dxk = dVis_Dortmund_dxs[i][k]
                    x8 = x6*x7
                    x9 = dFis_dxs[i][k]
                    x11 = x10*x9
                    x12 = 2.0*x6*x9
                    
                    x13 = Vi*x1
                    x14 = x10 - x13*x6
                    
                    val = (5.0*qi*(-x1*x14*x15*x9 + x1*x2 - x11*x4
                                   + x15*(x1*x11 + x1*x8 - x12*x5 + x13*x3 - x2)
                                   - x3*x5 - x4*x8 + x14*x7*Vi_inv2 + Vi*x12*Fi_inv3) 
                            - x0 + x0/ViD - dViD_dxj*dViD_dxk*ViD_inv2
                            )
                    row.append(val)
                matrix.append(row)
            d2lngammas_c_dxixjs.append(matrix)
            
        self._d2lngammas_c_dxixjs = d2lngammas_c_dxixjs
        return d2lngammas_c_dxixjs

    def d3lngammas_c_dxixjxks(self):
        r'''
        
        .. math::
            \frac{\partial \ln \gamma^c_i}{\partial x_j \partial x_k
            \partial x_m} = - \frac{d^{3}}{d x_{m}d x_{k}d x_{j}} Vi' 
            + \frac{\frac{d^{3}}{d x_{m}d x_{k}d x_{j}} Vi'}{Vi'} 
            - \frac{\frac{d}{d x_{j}} Vi' \frac{d^{2}}{d x_{m}d x_{k}} Vi'}
            {Vi'^{2}} - \frac{\frac{d}{d x_{k}} Vi' \frac{d^{2}}{d x_{m}d 
            x_{j}} Vi'}{Vi'^{2}} - \frac{\frac{d}{d x_{m}} Vi' \frac{d^{2}}
            {d x_{k}d x_{j}} Vi'}{Vi'^{2}} + \frac{2 \frac{d}{d x_{j}} Vi' 
            \frac{d}{d x_{k}} Vi' \frac{d}{d x_{m}} Vi'}{Vi'^{3}} - \frac{5
            q_{i} \frac{d^{3}}{d x_{m}d x_{k}d x_{j}} V_{i}}{V_{i}} 
            + \frac{5 q_{i} \frac{d}{d x_{j}} V_{i} \frac{d^{2}}{d x_{m}d x_{k}} V_{i}}{V_{i}^{2}} 
            + \frac{5 q_{i} \frac{d}{d x_{k}} V_{i} \frac{d^{2}}{d x_{m}d x_{j}} V_{i}}{V_{i}^{2}} 
            + \frac{5 q_{i} \frac{d}{d x_{m}} V_{i} \frac{d^{2}}{d x_{k}d x_{j}} V_{i}}{V_{i}^{2}} 
            - \frac{10 q_{i} \frac{d}{d x_{j}} V_{i} \frac{d}{d x_{k}} V_{i} \frac{d}{d x_{m}} V_{i}}{V_{i}^{3}} 
            + \frac{5 q_{i} \frac{d^{3}}{d x_{m}d x_{k}d x_{j}} F_{i}}{F_{i}} 
            + \frac{5 q_{i} \frac{d^{3}}{d x_{m}d x_{k}d x_{j}} V_{i}}{F_{i}} 
            - \frac{5 V_{i} q_{i} \frac{d^{3}}{d x_{m}d x_{k}d x_{j}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{j}} F_{i} \frac{d^{2}}{d x_{m}d x_{k}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{j}} F_{i} \frac{d^{2}}{d x_{m}d x_{k}} V_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{k}} F_{i} \frac{d^{2}}{d x_{m}d x_{j}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{k}} F_{i} \frac{d^{2}}{d x_{m}d x_{j}} V_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{m}} F_{i} \frac{d^{2}}{d x_{k}d x_{j}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{m}} F_{i} \frac{d^{2}}{d x_{k}d x_{j}} V_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{j}} V_{i} \frac{d^{2}}{d x_{m}d x_{k}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{k}} V_{i} \frac{d^{2}}{d x_{m}d x_{j}} F_{i}}{F_{i}^{2}} 
            - \frac{5 q_{i} \frac{d}{d x_{m}} V_{i} \frac{d^{2}}{d x_{k}d x_{j}} F_{i}}{F_{i}^{2}} 
            + \frac{10 V_{i} q_{i} \frac{d}{d x_{j}} F_{i} \frac{d^{2}}{d x_{m}d x_{k}} F_{i}}{F_{i}^{3}} 
            + \frac{10 V_{i} q_{i} \frac{d}{d x_{k}} F_{i} \frac{d^{2}}{d x_{m}d x_{j}} F_{i}}{F_{i}^{3}} 
            + \frac{10 V_{i} q_{i} \frac{d}{d x_{m}} F_{i} \frac{d^{2}}{d x_{k}d x_{j}} F_{i}}{F_{i}^{3}} 
            + \frac{10 q_{i} \frac{d}{d x_{j}} F_{i} \frac{d}{d x_{k}} F_{i} \frac{d}{d x_{m}} F_{i}}{F_{i}^{3}} 
            + \frac{10 q_{i} \frac{d}{d x_{j}} F_{i} \frac{d}{d x_{k}} F_{i} \frac{d}{d x_{m}} V_{i}}{F_{i}^{3}} 
            + \frac{10 q_{i} \frac{d}{d x_{j}} F_{i} \frac{d}{d x_{m}} F_{i} \frac{d}{d x_{k}} V_{i}}{F_{i}^{3}} 
            + \frac{10 q_{i} \frac{d}{d x_{k}} F_{i} \frac{d}{d x_{m}} F_{i} \frac{d}{d x_{j}} V_{i}}{F_{i}^{3}} 
            - \frac{30 V_{i} q_{i} \frac{d}{d x_{j}} F_{i} \frac{d}{d x_{k}} F_{i} \frac{d}{d x_{m}} F_{i}}{F_{i}^{4}}
            
        '''
        try:
            return self._d3lngammas_c_dxixjxks
        except AttributeError:
            pass
        cmps, version, qs = self.cmps, self.version, self.qs
        Vis = self.Vis()
        dVis_dxs = self.dVis_dxs()
        d2Vis_dxixjs = self.d2Vis_dxixjs()
        d3Vis_dxixjxks = self.d3Vis_dxixjxks()

        Fis = self.Fis()
        dFis_dxs = self.dFis_dxs()
        d2Fis_dxixjs = self.d2Fis_dxixjs()
        d3Fis_dxixjxks = self.d3Fis_dxixjxks()
        
        if self.version == 1:
            Vis_Dortmund = self.Vis_Dortmund()
            dVis_Dortmund_dxs = self.dVis_Dortmund_dxs()
            d2Vis_Dortmund_dxixjs = self.d2Vis_Dortmund_dxixjs()
            d3Vis_Dortmund_dxixjxks = self.d3Vis_Dortmund_dxixjxks()
        else:
            Vis_Dortmund = Vis
            dVis_Dortmund_dxs = dVis_dxs
            d2Vis_Dortmund_dxixjs = d2Vis_dxixjs
            d3Vis_Dortmund_dxixjxks = d3Vis_dxixjxks
        
        d3lngammas_c_dxixjxks = []
        
        for i in cmps:
            Vi = Vis[i]
            ViD = Vis_Dortmund[i]
            Fi = Fis[i]
            qi = qs[i]
            third = []
            for j in cmps:
                hess = []
                for k in cmps:
                    row = []
                    for m in cmps:
                        x0 = d3Vis_Dortmund_dxixjxks[i][j][k][m]#Derivative(ViD, xj, xk, xm)
                        x1 = 1/Fis[i]#1/Fi
                        x2 = 5.0*qs[i]
                        x3 = x2*d3Fis_dxixjxks[i][j][k][m]#Derivative(Fi, xj, xk, xm)
                        x4 = x2*d3Vis_dxixjxks[i][j][k][m]#Derivative(Vi, xj, xk, xm)
                        x5 = Vis_Dortmund[i]**-2#ViD**(-2)
                        x6 = dVis_Dortmund_dxs[i][j]#Derivative(ViD, xj)
                        x7 = dVis_Dortmund_dxs[i][k]#Derivative(ViD, xk)
                        x8 = dVis_Dortmund_dxs[i][m]#Derivative(ViD, xm)
                        x9 = Fis[i]**-2#Fi**(-2)
                        x10 = x2*x9
                        x11 = dFis_dxs[i][j]#Derivative(Fi, xj)
                        x12 = d2Fis_dxixjs[i][k][m]#Derivative(Fi, xk, xm)
                        x13 = x11*x12
                        x14 = d2Vis_dxixjs[i][k][m]#Derivative(Vi, xk, xm)
                        x15 = d2Fis_dxixjs[i][j][m]#Derivative(Fi, xj, xm)
                        x16 = dFis_dxs[i][k]#Derivative(Fi, xk)
                        x17 = x10*x16
                        x18 = d2Vis_dxixjs[i][j][m]#Derivative(Vi, xj, xm)
                        x19 = d2Fis_dxixjs[i][j][k]#Derivative(Fi, xj, xk)
                        x20 = dFis_dxs[i][m]#Derivative(Fi, xm)
                        x21 = x10*x20
                        x22 = d2Vis_dxixjs[i][j][k]#Derivative(Vi, xj, xk)
                        x23 = dVis_dxs[i][j]#Derivative(Vi, xj)
                        x24 = dVis_dxs[i][k]#Derivative(Vi, xk)
                        x25 = dVis_dxs[i][m]#Derivative(Vi, xm)
                        x26 = x2/Vis[i]**2
                        x27 = Fis[i]**(-3)
                        x28 = 10*qs[i]
                        x29 = x27*x28
                        x30 = Vi*x29
                        x31 = x11*x16
                        x32 = x20*x29
                        x33 = x25*x28        
                        val = (-Vi*x3*x9 - x0 + x1*x3 + x1*x4 - x10*x11*x14 - x10*x12*x23 
                               - x10*x13 - x10*x15*x24 - x10*x19*x25 + x11*x24*x32 + x13*x30 
                               + x14*x23*x26 + x15*x16*x30 - x15*x17 + x16*x23*x32 - x17*x18 
                               + x18*x24*x26 + x19*x20*x30 - x19*x21 - x21*x22 + x22*x25*x26 
                               + x27*x31*x33 + x31*x32 - x5*x6*d2Vis_Dortmund_dxixjs[i][k][m]
                               - x5*x7*d2Vis_Dortmund_dxixjs[i][j][m]
                               - x5*x8*d2Vis_Dortmund_dxixjs[i][j][k]
                               + x0/ViD + 2*x6*x7*x8/ViD**3 - x4/Vi - x23*x24*x33/Vi**3 - 30*Vi*qi*x20*x31/Fi**4)
                        
                        row.append(val)
                    hess.append(row)
                third.append(hess)
            d3lngammas_c_dxixjxks.append(third)
        
        self._d3lngammas_c_dxixjxks = d3lngammas_c_dxixjxks
        return d3lngammas_c_dxixjxks
