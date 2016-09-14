from numpy import *
import sys

a = array([1, 2, 3])
b = matrix(a)

print(a.shape)
print(b.shape)
print(type(b))

c = array(b)[0]
print(c.shape)

d = asarray(b).reshape(-1)
print(d.shape)