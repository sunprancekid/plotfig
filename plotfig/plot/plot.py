## Matthew A. Dorsey
## @sunprancekid
## constaints methods for generating plots using figure class


##############
## PACKAGES ##
##############
# from conda
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
# local
from plot.figure import Figure


################
## PARAMETERS ##
################
# defaults associated with scatter plot
default_plot_markersize = 2
default_plot_linewidth = 2
default_edgecolor = 'black'
default_colormap = 'coolwarm'
default_legendloc = 'best'
n_xfits = 100

# defaults associated with pie chart
default_prect_no_label_max = 0.05 # maximum precentage of total pie chart before label is not included
default_explode = 0.05


#############
## METHODS ##
#############
# scatter plot
def scatter (fig = None):

    # check that figure exists
    if fig is None:
        print("ERROR :: scatter :: must specify 'fig'.")
        exit()

    # establish scatter plot
    plt.figure(figsize=(7,5))
    leg = [] # empty list used for legend
    if fig.has_ivals():
        # if the figure has unique isolated values
        for i in fig.get_unique_ivals(rev = False):
            line = plt.scatter(fig.get_xval_list(i), fig.get_yval_list(i), marker = fig.get_marker(i), markersize = markersize) 
            leg.append(mlines.Line2D([], [], marker = fig.get_marker(i), ls = line[-1].get_ls(), label = fig.get_label(i), color = line[-1].get_color()))
    else:
        # otherwise the figure does not have isolated values, so just create one plot
        plt.scatter(fig.get_xval_list(), fig.get_yval_list(), marker = fig.get_marker(), markersize = markersize)

    # add xaxis min and max, used min and max to plot fits
    xlim = plt.xlim(fig.get_xaxis_min(), fig.get_xaxis_max())


    # set yaxis min and max, add labels
    ylim = plt.ylim(fig.get_yaxis_min(), fig.get_yaxis_max())
    if fig.get_title_label() is not None:
        plt.suptitle(fig.get_title_label().get_label(), fontsize = fig.get_title_label().get_size())
    if fig.get_subtitle_label() is not None:
        plt.title(fig.get_subtitle_label().get_label(), fontsize = fig.get_subtitle_label().get_size())
    plt.xlabel(fig.get_xaxis_label().get_label(), fontsize = fig.get_xaxis_label().get_size())
    plt.ylabel(fig.get_yaxis_label().get_label(), fontsize = fig.get_yaxis_label().get_size())
    # add the legend
    plt.legend(handles = leg, loc = legendloc) # TODO increase size of legend labels

    # add logscale
    if fig.xaxis_is_logscale():
        plt.xscale(fig.get_xaxis_scale(), base = fig.get_xaxis_scale_base())
    if fig.yaxis_is_logscale():
        plt.yscale(fig.get_yaxis_scale(), base = fig.get_yaxis_scale_base())

    if save:
        plt.savefig(fig.get_saveas(), dpi = fig.get_dpi(), bbox_inches='tight')
    if show:
        plt.show()

    plt.close()

# generate plot
def gen_plot (fig = None, linewidth = default_plot_linewidth, markersize = default_plot_markersize, legendloc = default_legendloc, fit = None, show = True, save = True):

    # if no figure was provided ..
    if fig is None:
        # if a figure has not been specified, we have a problem: cannot generate a default
        # if figure and data are seperate objects, then maybe figure can be default while data would be mandatory
        exit()
        
    ## TODO :: check figure 

    # f, ax = plt.subplots()
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    
    # plot scatter
    leg = [] # empty list used for legend
    if fig.has_ivals():
        n = len(fig.get_unique_ivals())
        # if the figure has unique isolated values
        for i in fig.get_unique_ivals(rev = False):
            line = plt.plot(fig.get_xval_list(i), fig.get_yval_list(i), linewidth = linewidth, marker = fig.get_marker(i), markersize = markersize, zorder = n) 
            leg.append(mlines.Line2D([], [], marker = fig.get_marker(i), ls = line[-1].get_ls(), label = fig.get_label(i), color = line[-1].get_color()))
            n -= 1
    else:
        # otherwise the figure does not have isolated values, so just create one plot
        plt.plot(fig.get_xval_list(), fig.get_yval_list(), linewidth = linewidth, marker = fig.get_marker(), markersize = markersize)

    # add xaxis min and max, used min and max to plot fits
    xlim = plt.xlim(fig.get_xaxis_min(), fig.get_xaxis_max())

    # add fits, if any were passed to the method
    if fit is not None:
        if type(fit) is not list:
            # then fit is only one item, pack fit into an interable list
            fit = [fit]

        # loop through fits
        for i in range(len(fit)):
            n = len(fig.get_unique_ivals()) + len(fit)
            if fit[i] is not None:
                # there is only one fit, add it to the graph
                line = plt.plot(fit[i].get_xval_list(lims = xlim, n = n_xfits, log = fig.xaxis_is_logscale()), fit[i].get_yval_list(lims = xlim, n = n_xfits, log = fig.xaxis_is_logscale()), linewidth = fit[i].get_linewidth(), marker = fit[i].get_marker(), markersize = fit[i].get_markersize(), ls = fit[i].get_linestyle(), color = fit[i].get_linecolor(), zorder = n)
                leg.append(mlines.Line2D([], [], marker = fit[i].get_marker(), ls = fit[i].get_linestyle(), label = fit[i].get_label().get_label(), color = fit[i].get_linecolor()))
                n -= 1

    # set yaxis min and max, add labels
    ylim = plt.ylim(fig.get_yaxis_min(), fig.get_yaxis_max())
    if fig.get_title_label() is not None:
        plt.suptitle(fig.get_title_label().get_label(), fontsize = fig.get_title_label().get_size())
    if fig.get_subtitle_label() is not None:
        plt.title(fig.get_subtitle_label().get_label(), fontsize = fig.get_subtitle_label().get_size())
    plt.xlabel(fig.get_xaxis_label().get_label(), fontsize = fig.get_xaxis_label().get_size())
    plt.ylabel(fig.get_yaxis_label().get_label(), fontsize = fig.get_yaxis_label().get_size())
    # add the legend
    plt.legend(handles = leg, loc = legendloc) # TODO increase size of legend labels
    # adjust major and minor ticks for x and y axis
    if fig.yaxis_has_major_ticks():
        plt.yticks(fig.get_yaxis_major_ticks())
        if fig.yaxis_has_minor_ticks():
            plt.yticks(fig.get_yaxis_minor_ticks(), minor = True)

    if fig.xaxis_has_major_ticks():
        plt.xticks(fig.get_xaxis_major_ticks())
        if fig.xaxis_has_minor_ticks():
            plt.xticks(fig.get_xaxis_minor_ticks(), minor = True)

    # add logscale
    if fig.xaxis_is_logscale():
        plt.xscale(fig.get_xaxis_scale(), base = fig.get_xaxis_scale_base())
    if fig.yaxis_is_logscale():
        plt.yscale(fig.get_yaxis_scale(), base = fig.get_yaxis_scale_base())

    if save:
        plt.savefig(fig.get_saveas(), dpi = fig.get_dpi(), bbox_inches='tight')
    if show:
        plt.show()

    plt.close()

# generate pie chart
def gen_pie_chart (fig = None, labels = None, legend = True, explode = default_explode, add_amount = False, curr = None, show = True, save = True):

    # check for fig
    if fig is None:
        exit()

    # get data and establish labels
    x = fig.get_xval_list()
    y = fig.get_yval_list()
    if labels is None:
        # if no labels were specified by the user, get them from the figure data
        labels = list(dict.fromkeys(x))
        # otherwise use the user specified date

    # accumulate data
    s = [0.] * len(labels) # amount organized by each catagorey
    t = 0. # total amount 
    for i in range(len(y)):
        if x[i] not in labels:
            continue
        s[labels.index(x[i])] += abs(y[i])
        t += abs(y[i])

    # remove any labels with 0., starting from the back
    pop_list = []
    for i in range(len(s)):
        if s[i] <= 0.01:
            pop_list.append(i)
    for i in reversed(pop_list):
        s.pop(i)
        labels.pop(i)

    # add the total amount to the label if asked
    if add_amount:
        for i in range(len(labels)):
            if curr is None:
                labels[i] = labels[i] + "\n({:0.2f})".format(s[i])
            else:
                labels[i] = labels[i] + "\n({:0.2f} {:s})".format(s[i], curr)

    # establish the explode array
    explode_array = None
    if explode is not None:
        explode_array = [default_explode] * len(s)
        print(explode_array)

    # add figure labels
    f = plt.figure()
    ax = plt.subplot(111)
    if fig.get_title_label() is not None:
        f.suptitle(fig.get_title_label().get_label(), fontsize = fig.get_title_label().get_size())
    if add_amount and not fig.has_subtitle_label():
        if curr is not None:
            ax.set_title("({:.2f} {:s})".format(t, curr), fontsize = fig.get_title_label().get_size())
        else:
            ax.set_title("({:.2f})".format(t), fontsize = fig.get_subtitle_label().get_size())
    else:
        ax.set_title(fig.get_subtitle_label().get_label(), fontsize = fig.get_title_label().get_size())

    # plot
    if legend:
        ax.pie(s, explode = explode_array)
        ax.legend(labels = labels, bbox_to_anchor=(0.075, 0.75))
    else:
        ax.pie(s, labels = labels, explode = explode_array)
    # save / show
    if save:
        plt.savefig(fig.get_saveas(), dpi = fig.get_dpi()) # bbox_inches='tight'
    if show:
        plt.show()
    # close
    plt.close()

""" method for generating bar chart """
def gen_bar_chart (fig = None, icol = None, xlabels = None, stack = True, show = True, save = False):

    ## TODO allow the user to specify the dimensions of the chart (length and width)

    # check for the figure
    if fig is None:
        exit()

    # get data and establish labels
    x = fig.get_xval_list()
    y = fig.get_yval_list()
    if xlabels is None:
        # if no labels were specified by the user, use the unique x_col values
        xlabels = list(dict.fromkeys(x))
        # otherwise use the user specified date

    # accumulate data
    s = [0.] * len(xlabels) # amount organized by each catagorey
    t = 0. # total amount 
    for i in range(len(y)):
        if x[i] not in xlabels:
            continue
        s[xlabels.index(x[i])] += abs(y[i])
        t += abs(y[i])

    # TODO sort values extra by an icol

    # plot
    f = plt.figure(figsize=(8,6))
    ax1 = plt.gca()

    if fig.has_ivals():

        # isolation values have been specified for the figure
        # determine if the bars should be placed next to each other, or stacked

        if not stack:
            pass

            # if the bars are not being stack on top of each other ..
            # they are place next to one another

        else:
            pass

            # the catagories should be stacked on top of one another

    else:
        

        # isolation values have not been specified
        ax1.bar(xlabels, s, edgecolor = default_edgecolor)

        # ax1.set_ylim(0., 5.)
        # ax1.tick_params(axis='both', which='major', labelsize=16)
        # # ax.set_yscale('log')
        # ax1.legend(loc='upper right')
        # ax1.set_ylabel(y_axis_label, fontsize=18)
        # ax1.set_xlabel(x_axis_label, fontsize=18)
        # ax1.tick_params(axis='both', which='major', labelsize=16)
        # ax1.legend(loc='upper left')

    # post plotting processing

    # "unbox" plot (remove the top and right plot lines)
    ax1.spines[['right', 'top']].set_visible(False)

    # set y-axis min and max, labels
    ylim = plt.ylim(fig.get_yaxis_min(), fig.get_yaxis_max())
    if fig.get_title_label() is not None:
        plt.suptitle(fig.get_title_label().get_label(), fontsize = fig.get_title_label().get_size())
    if fig.get_subtitle_label() is not None:
        plt.title(fig.get_subtitle_label().get_label(), fontsize = fig.get_subtitle_label().get_size())
    plt.xlabel(fig.get_xaxis_label().get_label(), fontsize = fig.get_xaxis_label().get_size())
    plt.ylabel(fig.get_yaxis_label().get_label(), fontsize = fig.get_yaxis_label().get_size())

    # assign yaxis ticks
    if fig.get_yaxis_major_ticks() is not None:
        ax1.set_yticks(fig.get_yaxis_major_ticks())
    if fig.get_yaxis_minor_ticks() is not None:
        ax1.set_yticks(fig.get_yaxis_minor_ticks(), minor = True)

    # save and show for user
    if save:
        plt.savefig(fig.get_saveas(), dpi = fig.get_dpi(), bbox_inches='tight')
    if show:
        plt.show()

    plt.close()




###############
## ARGUMENTS ##
###############
# none


############
## SCRIPT ##
############
# none
