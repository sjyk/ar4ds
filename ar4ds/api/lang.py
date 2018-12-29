# -*- coding: utf-8 -*-
"""This module contains some string processing to process the DSL.
"""

def _clean(str): 
    return str.replace("\n", "")

def preprocess(str):
    return str