# Convert to ctypes
chroms_self_python = [gr.chrom for gr in self.sequences]
chroms_self_c = (c_char_p * len(chroms_self_python))(*chroms_self_python)

[...]

# Call C-function
return ctypes_jaccardC(chroms_self_c, initials_self_c, finals_self_c, len(self), chroms_query_c, initials_query_c, finals_query_c, len(query))
