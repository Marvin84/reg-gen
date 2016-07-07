set xlabel 'Repeats'
set grid
set datafile separator ","
set ylabel 'Time [sec]'
set term pdf

# mm9
set output 'jaccard-test.pdf'
set title 'Jaccard mm9-chr19'
plot for [i=2:4] "plot-test.csv" using 1:i title columnhead with lines

# mm9
set output 'jaccard-mm9.pdf'
set title 'Jaccard mm9'
plot for [i=2:4] "plot-mm9.csv" using 1:i title columnhead with lines

exit
