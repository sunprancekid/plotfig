## Matthew Dorsey
## @sunprancekid
## 19.02.2025
## class for containing information for figure properties which is consisten across all plots

##############
## PACKAGES ##
##############
# native / conda packages
import pandas as pd
import numpy as np
import os # used to check path
import itertools # used for iterating over markers
from matplotlib import colormaps as mcmaps
# local
from plot.axis import Label, Axis
from plot.color import Scheme, Color


################
## PARAMETERS ##
################

## non zero exit codes for flagging errors
NONZERO_EXITCODE = 120

## constants, defaults for Figure class
accepted_axes = ['x', 'y', 'y2', 'c', 'l']
default_title_label = None
default_subtitle_label = None
default_xaxis_label = None
default_yaxis_label = None
default_dpi = 200
minimum_dpi = 100
default_file_location = "./"
default_file_name = "figure"
default_file_type = ".png"
default_markerset = ["D", "^", "v", "<", "o", "s", "p", "*"]
default_logscale_base = 10
minimum_logscale_base = 0.1
accepted_filetypes = [".png", ".tif"]
default_cmap = "tab10"
# defaults used for figures used in publications
pubdefault_dpi = 300
pubdefault_label_size = 18
# pubdefault_tick_size
default_number_major_ticks = 3
default_number_minor_ticks = 4
scale_linear = "linear"
scale_log = "log"
default_scale = scale_linear
default_padding_value = 0.05

## corresponding to color maps
default_matplotlib_cmaps = list(mcmaps)
discrete_matplotlib_cmaps = ['Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2',
                      'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                      'tab20c']


#############
## METHODS ##
#############

# none


#############
## CLASSES ##
#############

## TODO :: rename - ano.viz!
## TODO :: docstring figure
## TODO :: update data handling methods, add for loading lists, appending, (more diversity)
## TODO :: new columns, x1, x2, ..., y1, y2, ..., i1, i2, ...., c1, c2, ....
##          - I see these being a set of accepted axis that can be stored and accessed
##          - the challenging part will be loading and handling data sets with different arrays
## TODO :: create color and scheme classes 
##          - color has the properties of individual colors
##          - schedme handles generating color arrays

## Figure class
class Figure (object):

    """ contains data and formatting for plotting figures with plot package.

    Attributes:
    -----------
    axes_dict : Dict[Axis]
        dictionary containing all figure axes.
    title_label : Label
        string and font size used for figure title.
    subtitle_label : Label
        string and font size used for figure title.
    dpi : int
        dpi assigned to figure
    col_dict : # TODO :: add this
    col_type_dict : # TODO :: add this
    df : DataFrame
    xaxis : Axis
    yaxis : Axis
    marker_dict : 
    color_dict : 

    Methods:
    --------
    reset_axes:
        resets all axes dictionary.
    has_axis:
        checks if axis key exists in axis dictionary.
    set_axis_label:
        assigns label to axis if it exists.
    get_axis_label:
        get the label corresponding to the specified axis.
    get_axis_label_str:
        return string representation of axis label.
    axis_has_label:
        determines if label has been assigned to axis.
    set_axis_limits:
        assigns the minimum and / or maximum values to the specified axis.
    set_axis_minimum_value:
        assigns minimum value to the specified axis.
    set_axis_maximum_value:
        assigns maximum value to the specified axis.
    get_axis_minimum_value:
        returns the minimum value assigned to the specified axis.
    get_axis_maximum_value:
        returns the maximum value assigned to the specified axis.
    set_title_label:
        assign title label string and size.
    get_title_label:
        returns title label.
    get_title_label_str:
        returns the string representation of title label.
    has_title_label:
        determines if string has been assigned to title label.
    set_subtitle_label:
        assign subtitle label string and size.
    get_subtitle_label:
        returns subtitle label.
    get_subtitle_label_str:
        return string representation of subtitle lable.
    has_subtitle_label:
        determines if string has been assigned to subtitle label.
    set_dpi:
        assigns dpi used for generating figure.
    get_dpi:
        returns dpi assigned for generating figure.
    set_saveas:
        assigns filename and location when saving figure.
    get_saveas:
        returns save path, including directory, filename, and filetype.
    save_data:
        saves data used for generate figure as csv in save directory.

    """

    """ standard initialization routine for Figure object. """
    def __init__ (self):

        ## related to figure formatting, labelling
        self.set_title_label()
        self.set_subtitle_label()
        self.reset_axes()
        ## color bar call
        # self.set_cbar_label()
        # self.set_cscheme()
        # self.set_max_cbar()
        # self.set_min_cbar()
        ## io
        self.set_linscale()
        self.set_dpi()
        self.set_saveas()

        ## related to data and specification
        self.reset_data()

    """ output Figure object as string."""
    def __str__ (self):
        out = ""

        # add title string
        out += "\nTitle: {}".format(self.get_title_label_str())

        # add subtitle string
        out += "\nSub-Title: {}".format(self.get_subtitle_label_str())

        # add xaxis label string
        out += "\n\nX-Axis"
        out += "\nLabel: {}".format(self.get_xaxis_label_str())
        out += "\nMinimum Axis Limit: {}".format(self.get_xaxis_min())
        out += "\nMaximum Axis Limit: {}".format(self.get_xaxis_max())

        # add yaxis label string
        out += "\n\nY-Axis"
        out += "\nLabel: {}".format(self.get_yaxis_label_str())
        out += "\nMinimum Axis Limit: {}".format(self.get_yaxis_min())
        out += "\nMaximum Axis Limit: {}".format(self.get_yaxis_max())

        # add figure dpi
        out += "\nDPI: {}".format(self.dpi)

        ## TODO add data to string output

        # return to user
        return out

    """ adjust figure limits according to data passed to method. """
    def adjust_limits(self, df = None, xcol = None, ycol = None, ccol = None):

        # check for df
        if df is None or not isinstance(df, pd.DataFrame):
            # if df is not data frame, exit without adjusting axis limits
            return

        # set xaxis limits
        self.set_xaxis_limits(l = df[xcol].to_list())

        # set yaxis limits
        self.set_yaxis_limits(l = df[ycol].to_list())

        # set cbar limits

    """ method sets fontsizes for labels, ticks, etc. to presets for figures in publications. """
    def set_publication(self):
        self.filename = self.filename + "_pub"
        # adjust axis labels size
        self.set_xaxis_label(s = pubdefault_label_size)
        self.set_yaxis_label(s = pubdefault_label_size)
        # self.set_caxis_label(s = pubdefault_label_size)
        # adjust tick size
        # adjust legend label size
        # adjust dpi
        self.set_dpi (d = pubdefault_dpi)


    ## DATA HANDLING ##

    ## GOAL :: append in multiple method calls, with differing structures

    # method used to initialize data stored withing figure object
    """ initializes data stored withing figure object. dataframe is removed, x, y, c, and i columns are reset. """
    def reset_data (self):
        self.df = None
        self.xcol = None
        self.ycol = None
        self.ccol = None
        self.icol = None
        self.icol_marker_dict = None
        self.icol_label_dict = None
        self.icol_color_dict = None

    # load data from csv file
    def append_from_csv (self, filename = None, xcol = None, ycol = None, ccol = None, icol = None, label = None):
        pass
        # create data frame from file
        df_load = pd.read_csv(filename)

        # check each coloumn exists, if specified
        if (xcol is not None) and (xcol not in df_load.columns):
            # throw error
            print("ERROR :: Figure.append_from_csv :: '{:s}' column does not exist in '{:s}'.".format(xcol, filename))
            return
        if (ycol is not None) and (ycol not in df_load.columns):
            # throw error
            print("ERROR :: Figure.append_from_csv :: '{:s}' column does not exist in '{:s}'.".format(ycol, filename))
            return
        if (ccol is not None) and (ccol not in df_load.columns):
            print("ERROR :: Figure.append_from_csv :: '{:s}' column does not exist in '{:s}'.".format(ccol, filename))
            return
        if (icol is not None) and (icol not in df_load.columns):
            print("ERROR :: Figure.append_from_csv :: '{:s}' column does not exist in '{:s}'.".format(icol, filename))
            return

        # if a data frame has not already been created, pass data frame to load_data method
        if self.df is None:
            self.load_data(d = df_load, xcol = xcol, ycol = ycol, ccol = ccol, icol = icol, label = label)
        else:
            # append data to existing dataframe
            df_dict = {}
            if xcol is not None:
                df_dict.update({self.xcol: df_load[xcol].to_list()})

            if ycol is not None:
                df_dict.update({self.ycol: df_load[ycol].to_list()})

            if ccol is not None:
                df_dict.update({self.ccol: df_load[ccol].to_list()})

            if icol is not None:
                df_dict.update({self.icol: df_load[icol].to_list()})
            elif label is not None and self.icol is not None:
                df_dict.update({self.icol: [label for _ in range(len(df_dict[self.xcol]))]})

            # update dataframe
            self.df = pd.concat([self.df, pd.DataFrame(df_dict)], ignore_index = True)
            self.set_xaxis_limits(padval = default_padding_value)
            self.set_yaxis_limits(padval = default_padding_value)
            self.reset_markers()
            self.reset_labels()
            self.reset_colors()

    # method that loads data from dataframe into figure object
    """ loads data from data frame into Figure object. xcol specifies the xaxis data, ycol specifies the yaxis data, ccol specifies the color column data, icol specifies the isolation column data. """
    def load_data (self, d = None, xcol = None, ycol = None, ccol = None, icol = None, label = None):

        # data frame must be passed to method
        if d is None:
            # df has not been specified, cannot load data
            print("ERROR :: Figure.load_data() :: must pass dataframe to method as 'd'.")
            return

        if xcol is None or ycol is None:
            print("ERROR :: Figure.load_data() :: must specify 'xcol' and 'ycol'.")
            return

        # reset data and load
        self.reset_data()
        df_dict = {}

        # add xcol if it is specified
        if xcol is not None:
            self.xcol = xcol
            df_dict.update({xcol: d[xcol].to_list()})

        # add ycol if it is specified
        if ycol is not None:
            self.ycol = ycol
            df_dict.update({ycol: d[ycol].to_list()})

        # add ccol if it is specified
        if ccol is not None:
            self.ccol = ccol
            df_dict.update({ccol: d[ccol].to_list()})

        # add icol if it is specified
        if icol is not None:
            self.icol = icol
            df_dict.update({icol: d[icol].to_list()})
        elif label is not None:
            self.icol = 'icol'
            df_dict.update({'icol': [label for _ in range(len(df_dict[xcol]))]})

        self.df = pd.DataFrame(df_dict)
        self.set_xaxis_limits(padval = default_padding_value)
        self.set_yaxis_limits(padval = default_padding_value)
        self.reset_markers()
        self.reset_labels()
        self.reset_colors()

    # method that returns list of xvalues
    """ returns list of xvals contained within xcol. if ival is specified, xvals returned are those which share the same ival in icol (if any). """
    def get_xval_list (self, ival = None):
        if ival is None:
            # return all xvals as a list
            return self.df[self.xcol].to_list()
        else:
            # return xvals which share the same ival (if any)
            tmpdf = self.df[self.df[self.icol] == ival]
            return tmpdf[self.xcol].to_list()

    # method that returns list of yvalues
    """ returns list of yvals contained within ycol. if ival is specified, yvals returned are those which share the same ival in icol (if any)."""
    def get_yval_list (self, ival = None):
        if ival is None:
            # return all yvals as a list
            return self.df[self.ycol].to_list()
        else:
            # return yvales which share the same ival (if any)
            tmpdf = self.df[self.df[self.icol] == ival]
            return tmpdf[self.ycol].to_list()

    # initialize list of labels that correspons to each unique ival in icol
    """ method initializes labels used to describe each unique ival in plots as that ival stored within that Figure dataframe. """
    def reset_labels(self):
        # create empty dictionary
        self.label_dict = {}
        for i in self.get_unique_ivals():
            self.label_dict.update({i: i}) # assign random marker to each ival
        # empty format string
        self.format_string = None

    # adjusts one label in label dictionary
    """ method changes one label in label dictionary to new string (not Label class). the label that is changed is the one that correspons to the ival used as a key in the label dictionary. """
    def set_label (self, ival = None, label = None):
        if ival in self.label_dict:
            self.label_dict[ival] = label

    # returns one label in label dictionary
    """ method returns label that corresponds to ival in label dictionary. """
    def get_label (self, ival = None):
        if self.format_string is None:
            # if the format string is empty, return the label
            return self.label_dict[ival]
        else:
            # the format string is not empty, return the formatted data label
            return self.format_string.format(self.label_dict[ival])

    # format label with string
    """ provide string with formats each ival when called."""
    def add_format(self, format_string = None):
        self.format_string = format_string

    # method that determines if isolation column has been specified within the dataframe
    """ returns boolean the determines if isolation column has been specified within dataframe. """
    def has_ivals(self):
        return self.icol is not None

    # method that returns unique values for the isolation column
    """ returns list of all unique values contained within icol. """
    def get_unique_ivals (self, rev = False):
        if self.icol is not None:
            # if an icol has been specified return all unique items
            l = self.df[self.icol].unique()
            if rev:
                return list(np.flip(l))
            else:
                return list(l)
        else:
            # otherwise, if an icol has not been specified, return a list with empty string
            return [""]

    ## MARKERS ## 

    ## GOAL :: encapsulate marker calls within color and scheme

    # initialize set of random set of markers that can be used for each unique ival in icol
    """ method generates a random set of markers than can be used with matplotlib. """
    def reset_markers(self, markerset = None):

        # create interable list
        if markerset is None or type(markerset) is not list:
            # if the marker set is not passed to the method, or is not a list
            markerset = default_markerset
        else:
            # that marker set passed to the method is a list
            # check that the marker set contains the correct number of markers
            # if it does not, add to the marker list from the default until it contains the appropriate number
            if len(markerset) < len(self.get_unique_ivals()):
                n_default = len(default_markerset)
                i = 0
                while True:
                    if default_markerset[i] not in markerset or (i >= len(default_markerset)):
                        markerset.append(default_markerset[i])
                    i+=1
                    if len(markerset) >= len(self.get_unique_ivals()):
                        break

        # create empty dictionary
        marks = itertools.cycle(markerset)
        self.marker_dict = {} # empty dictionary
        for i in self.get_unique_ivals():
            self.marker_dict.update({i: next(marks)}) # assign random marker to each ival

    # adjusts one marker in marker dictionary
    """ method changes one marker in the marker dictionary to a new marker type. the marker that is changed is the one that corresponds to the ival used as a key in the marker dictionary. """
    def set_marker(self, ival = None, marker = None):
        if ival in self.marker_dict:
            self.marker_dict[ival] = marker

    # return marker corresponding to ival
    """ method returns marker that correspons to ival in marker dictionary. """
    def get_marker (self, ival = None):
        if ival is None:
            return default_markerset[0]
        else:
            return self.marker_dict[ival]

    ## COLORS ## 

    def has_cmap (self):
        """ returns boolean determining if Figure has assigned color map.
        
        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            'True' if colormap has been assigned to Figure, else 'False'.

        """

        return self.cmap is not None

    def reset_colors(self):
        """ resets colors assigned to dataset to None. 
        
        Parameters:
        -----------
        None

        Returns:
        --------
        None

        """

        self.cmap = None
        self.color_dict = None

    def set_cmap (self, cmap = None):
        
        # check color map
        if isinstance(cmap, str):
            # if the color cmap is a string, check if it matches the accepted
            # color maps in matplot lib
            if cmap not in default_matplotlib_cmaps:
                print ("ERROR :: Figure.set_cmap() :: Unknown cmap '{0}', not found in 'default_matplotlib_cmaps'.".format(cmap))
                return
        else:
            print ("ERROR :: Figure.set_cmap() :: Unknown cmap type '{0}'.".format(type(cmap)))
            return

        # assign color map
        self.cmap = cmap
        # update the color dictionary
        self.update_colors()

    def update_colors (self):
        
        if not self.has_cmap():
            # if a color map has not been assigned, skip this routine
            return

        # if not self.has_ivals():
        #     # if isolation values have not been assigned, skip this routine
        #     return

        # loop through each ival, assign a color
        self.color_dict = {} # empty dictionary
        if self.cmap in default_matplotlib_cmaps:
            if self.cmap in discrete_matplotlib_cmaps:
                # the color map is discrete
                # the colors are sequentially spaced
                colormap = mcmaps[self.cmap]
                self.color_dict = {}
                for i in range(len(self.get_unique_ivals())):
                    self.color_dict.update({self.get_unique_ivals()[i]: colormap(i)})
            else:
                # the color map is continuous
                # the colors are linearly spaced
                colormap = mcmaps[self.cmap]
                cmap_ivals = np.linspace(0.,1.,len(self.get_unique_ivals()), endpoint = True)
                for i in range(len(self.get_unique_ivals())):
                    self.color_dict.update({self.get_unique_ivals()[i]: colormap(cmap_ivals[i])})
        else:
            # if the colormap is not defined in matplotlib, cannot parse colors
            print("ERROR :: Figure.update_colors() :: Unable to parse colors from colormap of type '{0}'.".format(type(self.cmap)))

        # print(self.color_dict)
        # self.color_dict = None

    def add_color (self):
        pass

    def get_color (self, ival = None):

        if not self.has_cmap():
            return None

        if ival is None:
            # if ival is not specified, return the first color in the color map
            return self.color_dict[""]
        elif ival not in self.get_unique_ivals():
            # if ival is not in the list
            print("ERROR :: Figure.get_color() :: ival '{0}' does not exist, or ivals have not been assigned.")
            return None
        else:
            if self.has_cmap():
                return self.color_dict[ival]
            else:
                # a color map has not been assigned, return None quitely
                return None


    ## AXES ##

    ## GOAL :: reduce number of methods needed for handling axes

    ## AXES - LABEL ##

    def reset_axes (self): 
        """ resets all axes assigned to Figure.

        Arguments:
        ----------
        None

        Returns:
        --------
        None
        """
        self.dict_axes = {}
        # TODO :: only initialize axis when data is added
        self.dict_axes.update({'y': Axis(), 'x': Axis()})
        # from previous implementation, depricate
        self.reset_xaxis()
        self.reset_yaxis()

    def has_axis(self, akey):
        """ checks if axis key exists in axes dictionary.

        Arguments:
        ----------
        axis : str
            key to check for in dictionary

        Returns:
        --------
        bool
            boolean that determines if the axis is in the dictionary.
        """
        return (akey in self.dict_axes.keys())

    def set_axis_label (self, akey = None, l = None, s = None):
        """ assigns label to axes if it exists.

        Arguments:
        ----------
        akey : str
            axis key which already exists in axes dict.
        l : str
            string assigned to axis label.
        s : int
            font size assigned to axis label.

        Returns:
        --------
        None
        """
        # check that the axes already exists
        if not self.has_axis(akey): return
        # assign label and font size to specified axis
        self.dict_axes[akey].set_label(l, s)

    def get_axis_label (self, akey = None):
        """ get the label corresponding to the specified axis.

        Parameters:
        -----------
        akey : str
            corresponds to axis in 'axes_dict'.

        Returns:
        --------
        Label
            label assigned to axes.
        """
        # check that the axes already exists in the dictionary
        if not self.has_axis(akey): return
        # return the label corresponding to the axis
        return self.dict_axes[akey].get_label()

    def get_axis_label_str (self, akey = None):
        """ return string representation of axis label.

        Parameters:
        -----------
        akey : str
            corresponds to axis in 'axes_dict'

        Returns:
        --------
        str
            string representation of label.
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        # return the label corresponding to the axis as a string
        return str(self.dict_axes[akey].get_label())

    def axis_has_label (self, akey = None):
        """ determines if label has been assign to axis.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.

        Returns:
        --------
        bool
            'True' if axis has label, else 'False'.
        """
        # check that the axis exists in the axes dictionary
        if not self.has_axis(akey): return
        # return a boolean representation of the axis label status
        return bool(self.dict_axes[akey].get_label())

    ## AXES - LIMITS ## 

    ## TODO :: akey corresponds to column in figure dataframe
    ## TODO :: akey corresponds to axis data type

    def set_axis_limits (self, akey = None, min_val = None, max_val = None, pad_val = None):
        """ assigns the mininmum and / or maximum values to the axis.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.
        min_val : float or int (optional, default is 'None')
            axis lower bounds when plotting.
        max_val: float or int (optional, default is 'None')
            axis upper bounds when plotting.
        pad_val: float (optional, default is 'None')
            precentage to scale upper and lower bounds when plotting

        Returns:
        --------
        None
        """
        # check that the key exists in the dictionary
        if not self.has_axis(akey): return
        # determine the data column corresponding to the axis
        if akey == 'x':
            col = self.xcol
        elif akey == 'y':
            col = self.ycol
        else:
            print("ERROR :: Figure.set_axis_limits() :: axis key '{0}' has no assigned column.".format(akey))
            return
        # if the column has not been assigned yet, return
        if col is None:
            return
        # check the data type corresponding to the column
        # cannot set minimum or maximum for non-numerical formats
        if (self.df[col].dtype != float) and (self.df[col].dtype != int):
            print("ERROR :: Figure.set_axis_limits() :: cannot set limits to axis '{0}' for dtype '{1}'".format(akey, self.df[col].dtype))
            return
        # if the minimum or maximum values are unassigned, get them from the dataframe
        if min_val is None:
            min_val = min(self.df[col].to_list())
        if max_val is None:
            max_val = max(self.df[col].to_list())
        # assign minimum and maximum values to the axis, pad limits
        self.dict_axes[akey].set_limits(min_val, max_val)
        self.dict_axes[akey].pad_limits(padval)

    def set_axis_minimum_value (self, akey = None, val = None):
        """ assigns minimum value to axis.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.
        val : float or int
            axis lower bounds when plotting.

        Returns:
        --------
        None
        """
        # check that the key exists in the dictionary
        if not self.has_axis(akey): return
        # TODO :: check the axis data type
        # pass the minimum value to the axis
        self.dict_axes[akey].set_minimum(val)

    def set_axis_maximum_value (self, akey = None, val = None):
        """ assigns maximum value to axis.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.
        val : float or int
            axis upper bounds when plotting.

        Returns:
        --------
        None
        """
        # check that the key exists in the dictionary
        if not self.has_axis(akey): return
        # TODO :: check the axis data type
        # pass the maximum value to the axis
        self.dict_axes[akey].set_maximum(val)

    def get_axis_minimum_value (self, akey = None):
        """ get the lower bound value assigned to the axis limits.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.

        Returns:
        --------
        float
            lower bounds assigned to specified axis when plotting.
        """
        # check that the key exists in the axes dictionary
        if not self.has_axis(akey): return
        # return the lower bounds assigned to the axis
        return self.dict_axes[akey].get_minimum()

    def get_axis_maximum_value (self, akey = None):
        """ get the upper bound value assigned to axis limits.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in 'dict_axes'.

        Returns:
        --------
        float
            upper bounds assigned to specified axis when plotting.
        """
        # check that the key exists in the axes dictionary
        if not self.has_axis(akey): return
        # return the upper bounds assigned to the axis
        return self.dict_axes[akey].get_maximum()

    ## AXIS - SCALE ##

    def set_axis_scale (self, akey = None, linear = False, log = False, logscale_base = default_logscale_base):
        """ assigns scale to specified axis.

        Parameters:
        -----------
        akey : str
            key corresponding to specified axis.
        linear : bool
            determines if linear scale assign to axis.
        log : bool
            determines if log scale is assigned to axis.
        logscale_base : int
            Postitive real number assigned to log scale.

        Returns:
        --------
        None
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        # assign the scale
        if linear:
            self.dict_axes[akey].set_scale(s = scale_linear)
        elif log:
            self.dict_axes[akey].set_scale(s = scale_log, base = logscale_base)
            # reset the limits with padding
            self.dict_axes[akey].pad_limits(padval = 0.05)

    def axis_is_logscale (self, akey = None):
        """ determines if the specified axis is set to logscale.

        Parameters:
        -----------
        akey : str
            key corresponding to axis is axes dictionary.

        Returns:
        --------
        bool
            'True' if axis is set to logscale, else 'False'.
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        return self.dict_axes[akey].is_logscale()

    def axis_is_linearscale (self, akey = None):
        """ determines if the specified axis is set to linear scale.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in axes dictionary.

        Returns:
        --------
        bool
            'True' if the axis is set to linear scale, else 'False'.
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        return self.dict_axes[akey].is_linearscale()

    def get_axis_scale (self, akey = None):
        """ returns the scale assigned to the axis.

        Parameters:
        -----------
        akey : str
            key coresponding to axis in axes dictionary.

        Returns:
        --------
        str
            string representation of scale assigned to axis.
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        return self.dict_axes[akey].get_scale()

    def get_axis_scale_base (self, akey = None):
        """ if specified axis is logscale, return base. otherwise returns None.

        Parameters:
        -----------
        akey : str
            key corresponding to axis in axes dictionary.

        Returns:
        --------
        float
            base assigned to specified axis if logscale.
        """
        # check that the axis exists in the dictionary
        if not self.has_axis(akey): return
        return self.dict_axes[akey].get_logscale_base()

    ## AXIS - TICKS ## 

    ## TITLE ##

    def set_title_label(self, l = default_title_label, s = None):
        """ assign title label string and size.

        Arguments:
        ----------
        l : str
            figure title.
        s : int
            font size used for title label.

        Returns:
        --------
        None
        """
        self.title_label = Label (l, s)

    def get_title_label (self):
        """ returns title label.

        Arguments:
        ----------
        None

        Returns:
        --------
        Label
            string and font size used for figure title
        """
        return self.title_label

    def get_title_label_str (self):
        """ returns the string representation of title label.

        Arguments:
        ----------
        None

        Returns:
        --------
        str
            title label state as string.
        """
        return str(self.title_label)

    def has_title_label (self):
        """ determines if string has been assigned to label.

        Label object returns empty string if unassigned, which is evaluated
        to be 'False' in the boolean context.

        Arguments:
        ----------
        None

        Returns:
        --------
        bool
            'True' title label has non-empty string, else 'False'.
        """
        return bool(self.title_label.get_label())

    ## SUBTITLE ##

    def set_subtitle_label (self, l = default_subtitle_label, s = None):
        """ assign subtitle label string and font size.

        Arguments:
        ----------
        l : str (optional, default is 'default_subtitle_label')
            string assigned to subtitle.
        s : int (optional, default is 'None')
            font size assigned to subtitle.

        Returns:
        --------
        None
        """
        self.subtitle_label = Label (l , s)

    def get_subtitle_label (self):
        """ returns subtitle string and font size as Label.

        Arguments:
        ----------
        None

        Returns:
        --------
        Label
            string and font size assigned to subtitle label.
        """
        return self.subtitle_label

    def get_subtitle_label_str (self):
        """ returns string representation of subtitle label.

        Arguments:
        ----------
        None

        Returns:
        --------
        str
            subtitle label state as string."""
        return str(self.subtitle_label)

    def has_subtitle_label (self):
        """ returns boolean determining if label has been assigned to subtitle.

        Arguments:
        ----------
        None

        Returns:
        --------
        bool
            'True' if subtitle label has non-emptry string, else 'False'.
        """
        return bool(self.subtitle_label.get_label())

    ## XAXIS ##

    def reset_xaxis(self):
        self.xaxis = Axis()

    def set_xaxis_label (self, l = None, s = None):
        self.set_axis_label('x', l, s)

    def get_xaxis_label (self):
        return self.get_axis_label('x')

    def get_xaxis_label_str (self):
        return self.get_axis_label_str('x')

    def set_xaxis_limits (self, min_val = None, max_val = None, padval = None):
        self.set_axis_limits('x', min_val, max_val, padval)

    def set_xaxis_min (self, val = None):
        self.set_axis_minimum_value('x', val)

    def set_xaxis_max (self, val = None):
        self.set_axis_maximum_value('x', val)

    def get_xaxis_min (self):
        return self.get_axis_minimum_value('x')

    def get_xaxis_max (self):
        return self.get_axis_maximum_value('x')

    # set the xaxis as either linear or logscale
    """ method sets the xaxis as either a linear or logscale. logscale base set the logscale base as default if not specified by user. """
    def set_xaxis_scale (self, linear = False, log = False, logscale_base = default_logscale_base):
        if linear and log:
            return
        elif linear:
            self.xaxis.set_scale(s = scale_linear)
        elif log:
            self.xaxis.set_scale(s = scale_log, b = logscale_base)
            # reset limits with padding
            self.set_xaxis_limits(padval = 0.05)

    # check if xaxis is logscale
    """ method returns boolean determining if the xaxis is logscale or not. """
    def xaxis_is_logscale (self):
        return self.xaxis.is_logscale()

    # checks if xaxis is linear
    def xaxis_is_linearscale (self):
        return self.xaxis.is_linearscale()

    # returns the scale assigned to xaxis
    """ method that returns scale used for xaxis as either 'log' or 'linear' """
    def get_xaxis_scale (self):
        return self.xaxis.get_scale()

    # returns scale base assigned to xaxis
    """ method that returns log base assigned to xaxis. if linear scale, returns None. """
    def get_xaxis_scale_base (self):
        return self.xaxis.get_logscale_base()

    # method used to set the tick marks for the major and minor xaxis
    """ method sets the tick marks used for the xaxis."""
    def set_xaxis_ticks(self, minval = None, maxval = None, nmajorticks = default_number_major_ticks, nminorticks = default_number_minor_ticks):
        self.xaxis.set_major_ticks(minval = minval, maxval = maxval, nticks = nmajorticks)
        self.xaxis.set_minor_ticks(nminorticks)

    """ assigns major ticks to xaxis. """
    def set_xaxis_major_ticks(self, minval = None, maxval = None, nticks = default_number_major_ticks):
        self.xaxis.set_major_ticks(minval, maxval, nticks)

    """ returns the major ticks assigned to the xaxis. """
    def get_xaxis_major_ticks(self):
        return self.xaxis.get_major_ticks()

    # returns boolean determining if the xaxis has major ticks
    def xaxis_has_major_ticks(self):
        return self.xaxis.has_major_ticks()

    """ assigns the minor ticks for the xaxis. """
    def set_xaxis_minor_ticks(self, nticks = default_number_minor_ticks):
        self.xaxis.set_minor_ticks(nticks)

    """ returns the minor ticks assigned to the x_axis. """
    def get_xaxis_minor_ticks(self):
        return self.xaxis.get_minor_ticks()

    """ returns boolean determining if minor ticks have been assigned to the x-axis. """
    def xaxis_has_minor_ticks(self):
        return self.xaxis.has_minor_ticks()

    # assigns values to ticks used for

    ## YAXIS ##

    def reset_yaxis(self):
        self.yaxis = Axis()

    def set_yaxis_label (self, l = None, s = None):
        self.set_axis_label('y', l, s)

    def get_yaxis_label (self):
        return self.get_axis_label('y')

    def get_yaxis_label_str (self):
        return self.get_axis_label_str('y')

    def set_yaxis_limits (self, min_val = None, max_val = None, padval = None):
        self.set_axis_limits('y', min_val = min_val, max_val = max_val, pad_val = padval)

    def set_yaxis_min (self, val):
        self.set_axis_minimum_value('y', val)

    def set_yaxis_max (self, val):
        self.set_axis_maximum_value('y', val)

    def get_yaxis_min (self):
        return self.get_axis_minimum_value('y')

    def get_yaxis_max (self):
        return self.get_axis_maximum_value('y')

    # set the yaxis as either linear or logscale
    """ method sets the yaxis as either a linear or logscale. logscale base set the logscale base as default if not specified by user. """
    def set_yaxis_scale (self, linear = False, log = False, logscale_base = default_logscale_base):
        if linear and log:
            return
        elif linear:
            self.yaxis.set_scale(s = scale_linear)
        elif log:
            self.yaxis.set_scale(s = scale_log, b = logscale_base)
            # reset limits with padding
            self.set_yaxis_limits(padval = 0.05)

    # check if yaxis is logscale
    """ method returns boolean determining if the yaxis is logscale or not. """
    def yaxis_is_logscale(self):
        return self.yaxis.is_logscale()

    # check if yaxis is linearscale
    def yaxis_is_linearscale (self):
        return self.yaxis.is_linearscale()

    # returns the scale assigned to yaxis
    """ method that returns scale used for yaxis as either 'log' or 'linear' """
    def get_yaxis_scale (self):
        return self.yaxis.get_scale()

    # returns scale base assigned to yaxis
    """ method that returns log base assigned to yaxis. if linear scale, returns None. """
    def get_yaxis_scale_base (self):
        return self.yaxis.get_logscale_base()

    # method used to set the tick marks and tick labels for the major and minor yaxis
    """ method sets the tick marks used for the yaxis."""
    def set_yaxis_ticks(self, minval = None, maxval = None, nmajorticks = default_number_major_ticks, nminorticks = default_number_minor_ticks):
        self.yaxis.set_major_ticks(minval = minval, maxval = maxval, nticks = nmajorticks)
        self.yaxis.set_minor_ticks(nminorticks)

    """ assigns major ticks to yaxis. """
    def set_yaxis_major_ticks(self, minval = None, maxval = None, nticks = default_number_major_ticks):
        self.yaxis.set_major_ticks(minval, maxval, nticks)

    """ returns the major ticks assigned to the yaxis. """
    def get_yaxis_major_ticks(self):
        return self.yaxis.get_major_ticks()

    # returns boolean determining if the yaxis has major ticks
    def yaxis_has_major_ticks(self):
        return self.yaxis.has_major_ticks()

    """ assigns the minor ticks for the yaxis. """
    def set_yaxis_minor_ticks(self, nticks = default_number_minor_ticks):
        self.yaxis.set_minor_ticks(nticks)

    """ returns the minor ticks assigned to the y_axis. """
    def get_yaxis_minor_ticks(self):
        return self.yaxis.get_minor_ticks()

    """ returns boolean determining if minor ticks have been assigned to the y-axis. """
    def yaxis_has_minor_ticks(self):
        return self.yaxis.has_minor_ticks()

    ## DPI ##

    def set_dpi (self, d = None):
        """ assign dpi used for figure.

        If unassigned, 'default_dpi' is used.

        Arguments:
        ----------
        d : int
            dpi used when generating figure with plot.

        Returns:
        --------
        None
        """
        if d is None or not isinstance(d, int):
            self.dpi = default_dpi
        else:
            if d < minimum_dpi:
                self.dpi = minimum_dpi

    def get_dpi (self):
        """ returns the dpi assigned to the figure.

        Arguments:
        ----------
        None

        Returns:
        --------
        int
            dpi used for generating figure.
        """
        return self.dpi

    ## IO ##

    def set_saveas(self, savedir = default_file_location, filename = default_file_name, filetype = default_file_type):
        """ assigns filename and location when saving figure.

        Arguments:
        ----------
        savedir : str
            path to save directory.
        filename : str
            name of file without extension.
        filetype : str
            must be within 'accepted_filetypes'.

        Returns:
        --------
        None
        """

        # check the save directory passed to the method
        if not os.path.exists(savedir):
            # if the directory does not exist, make it
            os.makedirs(savedir)
            self.savedir = savedir
        else:
            self.savedir = savedir

        # check the filename passed to the method
        if type(filename) is not str:
            self.filename = default_file_name
        else:
            self.filename = filename

        # check the filetype passed to the method
        if filetype not in accepted_filetypes:
            self.filetype = default_file_type
        else:
            self.filetype = filetype

    def get_saveas(self):
        """ returns save path, including directory, filename, and filetype.

        Arguments:
        ----------
        None

        Returns:
        --------
        str
            complete path to save file.
        """
        saveas = self.savedir + self.filename + self.filetype
        return saveas

    def save_data(self):
        """ saves data used for generate figure as csv in save directory.

        Arguments:
        ----------
        None

        Returns:
        --------
        None
        """
        self.df.to_csv(self.savedir + self.filename + ".csv", index = False)

    ## LINEAR OR LOG SCALE ##

    # sets scale for all axis to be linear
    """ method sets the scale for x, y, and c axis to be linear. """
    def set_linscale (self):

        # set x scale to be linear
        self.set_xaxis_scale(linear = True)

        # set y scale to be linear
        self.set_yaxis_scale(linear = True)

        # set c scale to be linear
        # self.set_caxis_scale(linear = True)

    def set_logscale (self, base = default_logscale_base, logx = True, logy = True):

        if logx:
            # set the xaxis scale to be log
            self.set_xaxis_scale(log = True, logscale_base = base)
            self.set_xaxis_ticks()

        if logy:
            # set the yaxis scale to be log
            self.set_yaxis_scale(log = True, logscale_base = base)
            self.set_yaxis_ticks()

        # set the xaxis scale to be log
        # self.set_caxis_scale(log = True, logscale_base = base)

############
## SCRIPT ##
############

# none
