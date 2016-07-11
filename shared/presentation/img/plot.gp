## General settings
set grid
set datafile separator ","
set ylabel 'Time [sec]'
set term pdf


## Timings
set xlabel 'Repeats'

# test
set output 'jaccard-test.pdf'
set title 'Jaccard mm9-chr19'
plot for [i=2:4] "plot-test.csv" using 1:i title columnhead with lines

# mm9
set output 'jaccard-mm9.pdf'
set title 'Jaccard mm9'
plot for [i=2:4] "plot-mm9.csv" using 1:i title columnhead with lines


## BigWig
set xlabel 'Number of wigs'

# access
set output 'SmallBigWig.pdf'
set title 'Access small (8M) BigWig File'
plot for [i=2:4] "Small.csv" using 1:i title columnhead with lines


## Finalise
exit
