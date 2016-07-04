def jaccard(self, query, use_c=True):
        if use_c:
            return self.jaccard_c(query)
        else:
            return self.jaccard_python(query)
