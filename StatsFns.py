#!/usr/bin/env python3.1
# StatsFns.py
# A pared-down module containing some functions commonly used
# to get statistics.

from math import sqrt

def corr(x, y):
    """Find the correlation between two lists of data."""
    
    assert len(x) == len(y), "lists must have equal length"
    
    xSum = sum(x)
    ySum = sum(y)
    
    xSumSq = sum([item**2 for item in x])
    ySumSq = sum([item**2 for item in y])
    
    iProd = 0.0
    for i in range(len(x)):
      iProd += x[i]*y[i]
    
    n = len(x)
    
    r = n*iProd - xSum*ySum
    r /= sqrt(n*xSumSq - xSum**2) * sqrt(n*ySumSq - ySum**2)
    return r

def corr3(data):
    """Find the correlation between three lists of data.
    
    The argument "data" is a list of lists, either
    [x, y] or [x, y, z], where "x" and "y" are lists,
    and "z" is a list if it exists.

    Out put is a tuple (rxy_z, rxz_y, ryz_x) of
    correlations between 2 data lists, holding the
    third fixed.

    To reduce computation, this function reduces to
    corr(x, y) if z == None.
    """
    
    x = data[0]
    y = data[1]
    z = data[2] if len(data) > 2 else None
    
    rxy = corr(x,y)
    rxz = corr(x,z) if z != None else 0
    ryz = corr(y,z) if z != None else 0
    
    # if no z-column, this gives rxy
    rxy_z = rxy - rxz * ryz
    rxy_z /= sqrt(1 - rxz**2) * sqrt(1 - ryz**2)

    # use symmetry of correlation to speed things up
    rzy = ryz
    
    # if no z-column, this gives zero
    rxz_y = rxz - rxy * rzy
    rxz_y /= sqrt(1 - rxy**2) * sqrt(1 - rzy**2)
    
    # speed up using symmetry
    ryx = rxy
    rzx = rxz
    
    # if no z-column, this gives zero
    ryz_x = ryz - ryx * rzx
    ryz_x /= sqrt(1 - ryx**2) * sqrt(1 - rzx**2)
    
    return (rxy_z, rxz_y, ryz_x)


