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



#----extend test

copy1 = deepcopy(bed1)
copy2 = deepcopy(bed1)
z = GenomicRegionSet(name=copy1.name)

for s in copy1.sequences[0:3]:
  print s
  s.extend(left=100, right=100)
  print "s changed"
  print s
  print "-----------"
  counter += 1

counter = 0
for s in copy2.sequences[0:3]:
  print s
  z.add(s.extend(left=100, right=100, w_return=True))
  print "s unchanged"
  print s
  counter += 1
  print "-----------"

print "this is z: " + str(z.sequences)


#----combine test

x = GenomicRegionSet(name="test1")
y = GenomicRegionSet(name="test2")
for s in bed1.sequences[0:3]:
 x.add(s)
for s in bed1.sequences[3:6]:
 y.add(s)
print x.sequences
print y.sequences
t = x.combine(y, change_name=True, output=True)
print "x unchanged"
print x.sequences
print "new sequence:"
print t.sequences
x.combine(y, change_name=True)
print "x changed"
print x.sequences

"""

#---projection test

for s in bed1.sequences[0:3]:
 print s
 s.extend(0,1)
 print s
