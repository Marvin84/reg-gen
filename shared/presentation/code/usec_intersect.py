def intersect(self, y, mode=OverlapType.OVERLAP, rm_duplicates=False, use_c=True):
        if use_c:
            return self.intersect_c(y, mode, rm_duplicates)
        else:
            return self.intersect_python(y, mode, rm_duplicates)
