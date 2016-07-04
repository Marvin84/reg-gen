from ctypes import *

# Determine path of shared library
me = os.path.abspath(os.path.dirname(__file__))
lib = cdll.LoadLibrary(os.path.join(me, "..", "librgt.so"))

# Bind library
ctypes_jaccardC = lib.jaccard

# Specify data types
ctypes_jaccardC.argtypes = [POINTER(c_char_p), POINTER(c_int), POINTER(c_int), c_int, POINTER(c_char_p), POINTER(c_int), POINTER(c_int), c_int]
ctypes_jaccardC.restype = c_double
