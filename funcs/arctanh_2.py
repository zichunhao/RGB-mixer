import numpy as np

def arctanh(x, y):
    return np.arctanh(y / x)

func = arctanh
# Not the actual minimum value, but the minimum value for normalization
func_min = -1
func_max = 1
