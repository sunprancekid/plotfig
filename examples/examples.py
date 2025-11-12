
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
from plot.plot import gen_plot

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

## SCRIPT
if plot: # run plot example
	# load data
	fig = Figure()
	fig.append_from_csv('data/plot.csv', xcol = 'period', ycol = '10', icol = 'perm')
	fig.add_format("$K$ = {:.1e}")
	# TODO :: format label with string
	# xaxis formatting
	## TODO :: logscale formatting
	##			- automatically set limits, filter negative data
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
## TODO :: add pie chart example
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
	fig.set_yaxis_ticks(minval = 0., maxval = 1., nmajorticks = 3)
	fig.set_xaxis_ticks(minval = 0., maxval = 1., nmajorticks = 4)
	fig.reset_markers(['D', '^'])
	# show scatter
	# TODO :: change scatter from plot to new scatter plot
	gen_plot(fig, linewidth = 0, legendloc = 'lower center', save = False)