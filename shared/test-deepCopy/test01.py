## Core Classes
import sys

# GenomicRegion
from rgt.GenomicRegion import GenomicRegion
from copy import deepcopy

a = GenomicRegion(chrom="chr1", initial=12345000, final=12346000,
                  name="a_region", orientation="+")
len(a)
a.toString()
a.extend(left=500, right=500)
len(a)

b = GenomicRegion(chrom="chr1", initial=12344000, final=12345500,
                  name="b_region", orientation="+")
len(b)
a.overlap(b)
a
c = GenomicRegion(chrom="chr1", initial=12335000, final=12336000,
                  name="c_region", orientation="+")
a.overlap(c)
a.distance(c)

# GenomicRegionSet
from rgt.GenomicRegionSet import GenomicRegionSet

regions = GenomicRegionSet(name="abc")
regions.add(a)
regions.add(b)
regions.add(c)

len(regions)
regions.get_chrom()

bed1 = GenomicRegionSet("CDP_PU1")
bed2 = GenomicRegionSet("cDC_PU1")
bed1.read_bed("/home/laneskij/practices/3_rgt_viz/data/CDP_PU1_peaks.bed")
bed2.read_bed("/home/laneskij/practices/3_rgt_viz/data/cDC_PU1_peaks_test.bed")

"""
#--- Joseph code


a = deepcopy(bed1)
a.merge()
print "bed1 = " + str(bed1.sequences)
print "a = " + str(a.sequences)

len(bed1)
len(bed2)

inter = bed1.intersect(bed2)
len(inter)

sbed1 = bed1.subtract(bed2)
inter2 = sbed1.intersect(bed2)
len(inter2)

"""

#----extend test
print "---->Extend test<----"

copy1 = deepcopy(bed1)
copy2 = deepcopy(bed1)
z1 = GenomicRegionSet(name=copy1.name)
z2 = GenomicRegionSet(name=copy1.name)
z3 = GenomicRegionSet(name=copy1.name)
z4 = GenomicRegionSet(name=copy1.name)


#using default version
for s in copy1.sequences[0:3]:
  z3.add(deepcopy(s))
  s.extend(left=100, right=100)
  z4.add(s)

#using with flag set True
for s in copy2.sequences[0:3]:
  z1.add(s)

z2 = z1.extend(left=100, right=100, w_return=True)


print "Original Object: "
print z3.sequences
print "-----------"
print "New object returned by extend with flag set True: "
print z2.sequences
print "-----------"
print "Object unchanged after flag set True: "
print z1.sequences
print "-----------"
print "Object changed after flag set Default:"
print z4.sequences
print "-----------------------------------------"


#----combine test
print "--->Combine test<---"

x = GenomicRegionSet(name="test1")
y = GenomicRegionSet(name="test2")
for s in bed1.sequences[0:3]:
 x.add(s)
for s in bed1.sequences[3:6]:
 y.add(s)

print "original data:"
print x.sequences
print "sequence that will be combined with original"
print y.sequences
print "-----------"

#call with flag set True
t = x.combine(y, change_name=True, output=True)

print "The object returned by combine with Flag set True"
print t.sequences
print "x unchanged"
print x.sequences
print "-----------"

#defualt call
x.combine(y, change_name=True)
print "x changed with default call:"
print x.sequences

"""

#---projection test

for s in bed1.sequences[0:3]:
 print s
 s.extend(0,1)
 print s
"""
