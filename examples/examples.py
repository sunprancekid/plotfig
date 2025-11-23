
## Matthew Dorsey
## @sunprancekid
## 2025.11.10

## FILENAME: examples/examples.py
## PURPOUSE: demonstrate how plotfig package works

## MODULES
# native / conda
import sys, os
import pandas as pd
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
	# first plot - frequency sweep for different model parameters
	fig = Figure()
	fig.append_from_csv(filename = 'data/plot.csv', xcol = 'period', ycol = '10', icol = 'perm')
	fig.add_format("$K$ = {:.1e}")
	# xaxis formatting
	## TODO :: logscale formatting
	##		- automatically set limits, mask negative data
	## 		- set axis major and minor ticks for log vs. lin scale
	fig.set_xaxis_label("Cyclic Period ($s$)")
	fig.set_xaxis_limits() # automatically do this within logscale call
	fig.set_xaxis_scale(log = True)
	# yaxis formatting
	fig.set_yaxis_label("Dissipated Energy per Cycle ($kJ$)")
	# add unique colors
	fig.set_cmap('Set2')
	# show graph
	gen_plot(fig, markersize = 6, save = False)

	# second plot - model behavior against model parameters
	perm = []
	value = []
	tag = []
	# get the maximum energy dissipation and period at which maximum occurs
	for i in fig.get_unique_ivals():
		# # get the maximum energy dissipation
		# perm.append(i)
		# value.append(max(fig.get_yval_list(i)))
		# tag.append("Maximum Energy Dissipation")
		# print(perm[-1], value[-1], tag[-1])

		# get the period at which the maximum occurs
		perm.append(i)
		value.append(fig.get_xval_list(i)[fig.get_yval_list(i).index(max(fig.get_yval_list(i)))])
		tag.append("Critical Period")
		print(perm[-1], value[-1], tag[-1])

	# create figure and plot
	fig = Figure()
	fig.load_data(d = pd.DataFrame({'X': perm, 'Y': value, 'I': tag}), xcol = 'X', ycol = 'Y', icol = 'I')
	# xaxis formatting
	fig.set_xaxis_label('Model Permeability ($mm^4 / N \\cdot s$)')
	fig.set_xaxis_limits()
	fig.set_xaxis_scale(log = True)
	# fig.set_xaxis_ticks()
	fig.set_yaxis_label('Critical Period ($s$)')
	fig.set_yaxis_limits()
	fig.set_yaxis_scale(log = True) # order matters here
	# fig.set_yaxis_ticks(minval = min(value), maxval = max(value))
	fig.set_cmap('Set1')
	print(fig.yaxis_is_linearscale())
	gen_plot(fig, linewidth = 0, save = False)


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