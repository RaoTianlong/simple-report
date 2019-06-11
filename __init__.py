# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 14:46:20 2019

@author: r00386
"""

__version__ = '0.0.0'

#from . import auxiliary_func, table, report
from .table import Table 
from .report import Report
from .auxiliary_func import tobs
import pandas as pd
pd.set_option('display.float_format',lambda x: '-' if x==0 else '{}'.format(x))