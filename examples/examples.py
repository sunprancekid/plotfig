
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
# boolean for running the scatter example
scatter = ('scatter' in sys.argv) or ('all' in sys.argv)

## SCRIPT
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
	gen_plot(fig, linewidth = 0, legendloc = 'lower center', save = False)