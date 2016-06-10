from __future__ import print_function
import os.path
from ctypes import *

me = os.path.abspath(os.path.dirname(__file__))
lib = cdll.LoadLibrary(os.path.join(me, "librgt.so"))

chromA = c_char_p("A")
initialA = c_int(0)
finalA = c_int(2)

chromB = c_char_p("A")
initialB = c_int(5)
finalB = c_int(7)

chromC = "A"
initialC = c_int(0)
finalC = c_int(4)

chromD = "A"
initialD = c_int(5)
finalD = c_int(6)

# Determine whether GenomicRegions overlap
func = lib.overlap
func.argtypes = [POINTER(c_char), c_int, c_int, POINTER(c_char), c_int, c_int]
func.restype = c_bool

overlapping = func(chromA, initialA, finalA, chromB, initialB, finalB)
print("Overlapping? ", overlapping)

# Compare GenomicRegions
func = lib.compareGenomicRegions
func.argtypes = [POINTER(c_char), c_int, c_int, POINTER(c_char), c_int, c_int]
func.restype = c_int

compare = func(chromA, initialA, finalA, chromB, initialB, finalB)
print("Compare = ", compare)

# Intersect genomic regions using the overlap mode.
func = lib.intersectGenomicRegionSetsOverlap
StringArray = POINTER(c_char_p)
TwoStrings = c_char_p*2
TwoInts = c_int*2

chroms1 = TwoStrings(chromA, chromB)
chroms2 = TwoStrings(chromC, chromD)

initials1 = TwoInts(initialA, initialB)
initials2 = TwoInts(initialC, initialD)

finals1 = TwoInts(finalA, finalB)
finals2 = TwoInts(finalC, finalD)

indicesR = cast((c_int*2)(), POINTER(c_int))
initialsR = cast((c_int*2)(), POINTER(c_int))
finalsR = cast((c_int*2)(), POINTER(c_int))

sizeR = c_int()

func.argtypes = [POINTER(c_char_p), POINTER(c_int), POINTER(c_int), c_int, POINTER(c_char_p), POINTER(c_int), POINTER(c_int), c_int, POINTER(POINTER(c_int)), POINTER(POINTER(c_int)), POINTER(POINTER(c_int)), POINTER(c_int)]
func.restype = None
a = func(chroms1, initials1, finals1, 2, chroms1, initials2, finals2, 2, byref(indicesR), byref(initialsR), byref(finalsR), byref(sizeR))
print([[chroms1[indicesR[i]], initialsR[i], finalsR[i]] for i in range(sizeR.value)])


'''
http://johnstowers.co.nz/2011/07/15/interfacing-python-c-opencv-via-ctypes/
FROM EXAMPLE CODE:

func = lib.test_get_data_nulls
func.restype = POINTER(c_char)
func.argtypes = [POINTER(c_int)]

l = c_int()
data = func(byref(l))

print(data, l, data.contents)

lib.test_data_print(data,l)

func_out = lib.test_get_data_nulls_out
func_out.argtypes = [POINTER(POINTER(c_char)), POINTER(c_int)]
func.restype = None

l2 = c_int()
data2 = POINTER(c_char)()
func_out(byref(data2), byref(l2))

print(data2, l2, data2.contents)

lib.test_data_print(data2, l2)

print("equal ", data[0] == data2[0], data[1] == data2[1], data[2] == data2[2], data[3] == data2[3], data[4] == data2[4])

func = lib.test_get_fixed_array_size_2
func.argtypes = [POINTER(c_double)]
func.restype = None

data = (c_double * 2)()
func(data)
x,y = data
print("array ", x, y)
'''
