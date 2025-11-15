
## Matthew Dorsey
## @sunprancekid
## 2025.11.10

## FILENAME: examples/examples.py
## PURPOUSE: demonstrate how plotfig package works

## MODULES
# native / conda
import sys, os
# local
from plot.figure import Figure
from plot.plot import gen_plot, gen_scatter, gen_pie_chart

## CONSTANTS / PARAMETERS
# none

## METHODS 
# none

## CLASSES
# none

## ARGUMENTS
# boolean for running plot example
plot = ('plot' in sys.argv) or ('all' in sys.argv)
# boolean for running the scatter example
scatter = ('scatter' in sys.argv) or ('all' in sys.argv)
# boolean for running pie chart example
pie = ('pie' in sys.argv) or ('all' in sys.argv)

## TODO :: create formatting class which contains:
##			- figure dimensions
##			- font sizing and type
##			- dpi 
##			- linewidths, markersize, bar widths, ... 
##			- axis thickness, colors, size of marker labels
##			- or, could keep this all within Figure .. (easier)

## SCRIPT
if plot: # run plot example
	# load data
	fig = Figure()
	fig.append_from_csv('data/plot.csv', xcol = 'period', ycol = '10', icol = 'perm')
	fig.add_format("$K$ = {:.1e}")
	# xaxis formatting
	## TODO :: logscale formatting
	##			- automatically set limits, mask negative data
	##			- add padding algorithim to axis, for log vs. lin
	## 			- set axis major and minor ticks for log vs. lin scale
	fig.set_xaxis_label("Cyclic Period ($s$)")
	fig.set_xaxis_limits()
	fig.set_xaxis_scale(log = True)
	# yaxis formatting
	fig.set_yaxis_label("Dissipated Energy per Cycle ($kJ$)")
	# show graph
	gen_plot(fig, save = False)

## TODO :: add bar chart example
if pie:
	# load data from csv
	fig = Figure()
	fig.append_from_csv('data/pie.csv', xcol = 'subclass', ycol = 'amount')
	fig.set_title_label("Spending on Food in October 2025")
	# TODO :: make this method more generic, less specific to personal finances
	# TODO :: fix legend issue
	gen_pie_chart(fig, add_amount = True, show = True, save = False)

if scatter: # run scatter example
	# load data from csv
	fig = Figure()
	fig.append_from_csv('data/scatter.csv', xcol = 'mag_val', ycol = 'ss_val', ccol = 'den', label = 'SS')
	fig.append_from_csv('data/scatter.csv', xcol = 'mag_val', ycol = 'ht_val', ccol = 'den', label = 'HT')
	# adjust plot attributes
	fig.set_xaxis_label('Magnetism Order Parameter ($M$)')
	fig.set_yaxis_label('$SS$ or $HT$ Order Parameter')
	fig.set_label(ival = "HT", label = "Head-to-Tail ($HT$)")
	fig.set_label(ival = "SS", label = "Side-to-Side ($SS$)")
	fig.set_yaxis_ticks(minval = 0., maxval = 1., nmajorticks = 6)
	fig.set_xaxis_ticks(minval = 0., maxval = 1., nmajorticks = 6)
	fig.reset_markers(['D', '^'])
	# show scatter
	# TODO :: add major and minor gridlines
	gen_scatter(fig, legendloc = 'above', save = False)