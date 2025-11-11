## Matthew Dorsey
## @sunprancekid
## 19.02.2025
## class for containing information for figure properties which is consisten across all plots

##############
## PACKAGES ##
##############

import pandas as pd
import numpy as np
import os # used to check path
import itertools # used for iterating over markers


################
## PARAMETERS ##
################

## non zero exit codes for flagging errors
NONZERO_EXITCODE = 120

## constants, defaults for Label class
default_label_size = 12
minimum_label_size = 6

## constants, defaults used for Axis class
default_number_major_ticks = 3
default_number_minor_ticks = 4
default_major_format_string = "{:.2f}" # floating point number with two decimal places
default_padding_value = 0.05
scale_linear = "linear"
scale_log = "log"
default_scale = scale_linear
default_logscale_base = 10

## constants, defaults for Figure class
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


#############
## METHODS ##
#############

# none


#############
## CLASSES ##
#############

## Label class
class Label (object):
    """ stand initialization routine for Label object. """
    def __init__ (self, l = None, s = None):
        self.set_label(l)
        self.set_size(s)

    """ output Label object as string. """
    def __str__ (self):

        out = ""
        if self.label is None:
            out += "Empty Label"
        else:
            out += self.get_label()
        out += " (font size: {})".format(self.get_size())

        return out


    ## GETTERS AND SETTERS ##

    # set label
    """ set label as string. """
    def set_label (self, l = None):
        if l is None or not isinstance(l, str):
            # if l is not an object or not a string
            self.label = None
        else:
            # otherwise l is a string
            self.label = l

    # return label
    """ return label as string. """
    def get_label (self):
        if self.label is None:
            return ""
        else:
            return self.label

    # set label fontsize
    """ get label size as interger no less than minimum. """
    def set_size (self, s = None):
        if s is None or not isinstance(s, int):
            # if s is not an object or not an integer
            self.size = default_label_size
        else:
            # if an integer was passed to the method, check the value is not less than the minimum
            if (s < minimum_label_size):
                self.size = minimum_label_size
            else:
                # otherwise assign the value passed to the method
                self.size = s

    # return label font size
    """ return label font size as integer. """
    def get_size (self):
        return self.size

## Axis class
class Axis (object):

    """ standard initialization for Axis object. """
    def __init__ (self):
        self.reset_label() 
        self.reset_limits()
        self.reset_scale() 
        self.reset_major_ticks()
        self.reset_minor_ticks()
        # TODO :: add attribute to define scale type has being either catagories or numbers

    """ generates string describing Axis Object. """
    def ___str___ (self):
        pass

    ## AXIS LABEL

    """ resets axis label to empty object. """
    def reset_label (self):
        self.label = None

    """ assigns string and font size to label. """
    def set_label (self, l = None, s = None):
        # if the axis does not have a label yet
        if not self.has_label():
            # if no attributes have been passed to the method
            if l is None:
                # assign None type to the axis label
                self.label = None
            else:
                # assign a new label with new attributes to the axis
                self.label = Label(l, s)
        else:
            # update the existing label's attributes if they are not None type
            if l is not None:
                self.set_label_string(l)
            if s is not None:
                self.set_label_fontsize(s)

    """ returns label assigned to axis. returns None type if label has not been assigned. """
    def get_label (self):
        if self.label is None:
            return Label (l = "")
        else:
            return self.label

    """ returns boolean determining if a label has been assigned to the axis. """
    def has_label(self):
        return self.label is not None

    """ assigns string to label. """
    def set_label_string(self, l):
        # if a label has not been assigned to the axis, create a new one
        if not self.has_label():
            self.set_label("")
        if isinstance(l, str):
            self.label.set_label(l)
        else:
            print("ERROR :: Axis.set_label_string() :: label string 'l' must be string type.")
            exit(NONZERO_EXITCODE)

    """ assign fontsize to label. """
    def set_label_fontsize(self, s):
        # if a label has not been assigned to the axis, create a new one
        if not self.has_label():
            self.set_label("")
        if isinstance(s, int):
            self.label.set_size(s)
        elif isinstance(s, float):
            self.label.set_size(int(s))
        else:
            print("ERROR :: Axis.set_label_fontsize() :: label fontsize 's' must be integer or float type. ")
            exit(NONZERO_EXITCODE)

    ## AXIS LIMITS

    """ resets both minimum and maximum axis limits. """
    def reset_limits (self):
        self.reset_minimum()
        self.reset_maximum()

    """ sets both minimum and maximum axis limits. """
    def set_limits (self, min_val = None, max_val = None):
        self.set_maximum(max_val)
        self.set_minimum(min_val)

    """ reset / remove maximum value assigned to axis. """
    def reset_maximum (self):
        self.set_maximum()

    """ assign maximum value to axis. """
    def set_maximum(self, m = None):
        if isinstance(m, float) or isinstance(m, int):
            # check that the maximum is greater than the minimum, if one has been assigned
            if self.has_minimum() and self.get_minimum() > m:
                # the maximum passed to the method is less than the minimum already assigned to the axis
                print("ERROR :: Axis.set_maximum() :: unable to assign maximum ('{0}') to axis, lower than minimum value already assigned to axis ('{1}'). ".format(m, self.get_minimum()))
                # do not assign the maximum to axis
                self.max = None
            else:
                # a minimum has not been assigned to the maximum is greater than the minimum
                if isinstance(m, int):
                    self.max = float(m) # type cast the integer as a float
                else:
                    self.max = m # assign the float
        else:
            # if not double or integer, assign none
            self.max = None

    """ return maximum value assigned to axis. Otherwise, return None, if no maximum has been assigned. """
    def get_maximum (self):
        return self.max

    """ returns boolean that determines if maximum has been assigned to limit. """
    def has_maximum (self):
        return self.max is not None

    """ reset / remove minimum value assigned to axis. """
    def reset_minimum (self):
        self.set_minimum()

    """ assign minimum value to axis. """
    def set_minimum (self, m = None):
        if isinstance(m, float) or isinstance(m, int):
            # check that the minimum passed to the method is less than the maximum, if one has been assigned
            if self.has_maximum() and self.get_maximum() < m:
                # the minimum passed to the method is greater than the maximum already assigned to the axis
                print("ERROR :: Axis.set_minimum() :: Unable to assign minimum ('{0}'), higher than maximum value already assigned to axis ('{1}').".format(m, self.get_maximum()))
                # do not assign minimum to axis
                self.min = None
            else:
                # assign the minimum to the axis
                if isinstance(m, int):
                    self.min = float(m) # type cast the integer as a float
                else:
                    self.min = m # assign the float
        else:
            # if not int or double, assign None
            self.min = None

    """ return minimum assigned to axis. Otherwise, return None if no minimum has been assigned. """
    def get_minimum (self):
        return self.min

    """ check if minimum has been assigned to axis. """
    def has_minimum (self):
        return self.min is not None 


    ## AXIS SCALE

    """ set default scale. """
    def reset_scale(self):
        self.set_scale()

    """ set scale as either log or linear. """
    def set_scale (self, s = None, b = None):
        if not isinstance(s, str) or s is None:
            self.scale = default_scale
        else:
            if s == scale_linear:
                self.scale = scale_linear
            elif s == scale_log:
                self.scale = scale_log
            else:
                self.scale = default_scale

            # if the axis scale is logarithmic
            if self.scale == scale_log:
                # use default base if one has not been specified
                if b is None or (not isinstance(b, float)) or (not isinstance(b, float)):
                    self.base = default_logscale_base
                else:
                    self.base = abs(b)
            else:
                self.base = None

    """ returns boolean determining if the axis scale is logarithmic."""
    def is_logscale(self):
        return self.scale == scale_log

    """ returns boolean determining if the axis scale is linear."""
    def is_linearscale (self):
        return self.scale == scale_linear

    """ returns scale associated with axis."""
    def get_scale (self):
        return self.scale

    """ returns base associated with logscale. return none if axis scale is linear. """
    def get_logscale_base (self):
        if self.is_logscale():
            return self.base
        else:
            return None

    ## AXIS MAJOR TICKS

    """ resets tick marks assigned to object. """
    def reset_major_ticks (self):
        self.major_ticks = None

    """ creates major axis with labels ranging from 'minval' to 'maxval' with 'nticks' tick marks. if the scale assigned to the axis is logarithm, the ticks are spaces according to a logarithmic scale corresponding to the assigned base (default is 10); otherwise the tick marks are spaced linearly apart. minval and maxval must not be specified if the minimum and maximum values have already been assigned to the axis. """
    def set_major_ticks (self, minval = None, maxval = None, nticks = default_number_major_ticks, pad = default_padding_value):

        # boolean determining if input meet criteria
        has_minval = minval is not None and (isinstance(minval, float) or isinstance(minval, int))
        has_maxval = maxval is not None and (isinstance(maxval, float) or isinstance(maxval, int))
        has_nticks = nticks is not None and (isinstance(nticks, int)) and (nticks > 1)
        has_pad = pad is not None and (isinstance(pad, float)) and (pad > 0.001)

        # check the minimum value
        if has_minval:
            # if a mininimum value has been specified, reset the minimum limit
            self.set_minimum(minval)
        elif not has_minval and self.has_minimum():
            # if a minimum has not been provided but the axis already has a value, use that one
            minval = self.get_minimium()
        else:
            # unable to parse minimum value, throw error
            print("ERROR :: Axis.set_major_ticks() :: 'minval' not specified, must be float or integer.")
            return

        # check the maximum value
        if has_maxval:
            # if a maximum value has been specified, reset the maximum limit
            self.set_maximum(maxval)
        elif not has_maxval and self.has_maximum():
            # if a maximum has not been specified but the axis already as one, use that value
            maxval = self.get_maximum()
        else:
            # unable to parse maximum value, throw error
            print("ERROR :: Axis.set_major_ticks() :: 'maxval' not specified, must be float or integer.")
            return

        # check that the number of ticks has been specified
        if not has_nticks:
            # report to user
            print("ERROR :: Axis.set_major_ticks() :: 'nticks' not specified, must be integer 2 or greater.")
            return

        # check the padding
        if not has_pad:
            # if the padding is an incorrect value, use the default
            # print("ERROR :: Axis.set_major_ticks() :: unable to use 'pad' passed to  method ({0}), must be float greater than 0. Using default.".format(pad))
            pad = default_padding_value

        # pad the limits
        self.set_limits(min_val = minval - ((maxval - minval) * pad), max_val = maxval + (maxval - minval) * pad)
        # use the min and max values assigned to the axis to create the ticks
        step = (maxval - minval) / (nticks - 1)
        self.major_ticks = np.arange(minval, maxval + step, step)

    """ returns major ticks assigned to axis. """
    def get_major_ticks (self):
        return self.major_ticks

    """ returns boolean determining if major ticks have already been assigned to the axis."""
    def has_major_ticks (self):
        return self.major_ticks is not None

    ## AXIS MINOR TICKS

    # reset the minor ticks 
    def reset_minor_ticks (self):
        self.minor_ticks = None

    # set the minor axis ticks
    def set_minor_ticks(self, nticks = default_number_minor_ticks):

        # check the appropriate information has been passed to the method
        has_nticks = nticks is not None and isinstance(nticks, int) and (nticks > 0)

        if not has_nticks:
            # report to user
            print("ERROR :: Axis.set_minor_ticks() :: 'nticks' not specified, must be integer 1 or greater.")
            return

        if not self.has_major_ticks():
            # cannot assign minor ticks if major ticks have not been assigned
            print ("ERROR :: Axis.set_minor_ticks() :: cannot assign minor ticks to axis if major ticks have not been assigned.")
            return

        # parse the minimum and maximum values from the major axis
        minor_ticks = np.empty(0)
        for i in range(self.major_ticks.size - 1):
            step = (self.major_ticks[i + 1] - self.major_ticks[i]) / (nticks + 1)
            arr = np.arange(self.major_ticks[i] + step, self.major_ticks[i + 1], step)
            minor_ticks = np.append(minor_ticks, arr)

        self.minor_ticks = minor_ticks

    # return minor ticks
    def get_minor_ticks (self):
        return self.minor_ticks

    # return boolean determining if minor ticks have been assigned to axis
    def has_minor_ticks (self):
        return self.minor_ticks is None

## Figure class
class Figure (object):

    """ standard initialization routine for Figure object. """
    def __init__ (self):

        ## related to figure formatting, labelling
        self.set_title_label()
        self.set_subtitle_label()
        ## xaxis call (would it be possible to encaspulte all axis activities within one set of methods?)
        self.reset_xaxis()
        ## yaxis call
        self.reset_yaxis()
        ## color bar call
        # self.set_cbar_label()
        # self.set_cscheme()
        # self.set_max_cbar()
        # self.set_min_cbar()
        ## other
        self.set_linscale()
        self.set_dpi()
        self.set_saveas()
        # self.set_file_name() # TODO check file type
        # self.set_file_location() # TODO check that the location exists

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

    """ assign location, name, and type of save file. """
    def set_saveas(self, savedir = default_file_location, filename = default_file_name, filetype = default_file_type):

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

    """ return path to location of saved file. """
    def get_saveas(self):
        saveas = self.savedir + self.filename + self.filetype
        return saveas

    """ save data frame data to directory and with name associated with object."""
    def save_data(self):
        self.df.to_csv(self.savedir + self.filename + ".csv", index = False)

    ## GETTERS AND SETTERS ##

    ## DATA HANDLING ##

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
        self.reset_markers()
        self.reset_labels()
        self.reset_colors()

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

    # initialize list of labels that correspons to each unique ival in icol
    """ method initializes labels used to describe each unique ival in plots as that ival stored within that Figure dataframe. """
    def reset_labels(self):
        # create empty dictionary
        self.label_dict = {}
        for i in self.get_unique_ivals():
            self.label_dict.update({i: i}) # assign random marker to each ival

    # adjusts one label in label dictionary
    """ method changes one label in label dictionary to new string (not Label class). the label that is changed is the one that correspons to the ival used as a key in the label dictionary. """
    def set_label (self, ival = None, label = None):
        if ival in self.label_dict:
            self.label_dict[ival] = label

    # returns one label in label dictionary
    """ method returns label that correspons to ival in label dictionary. """
    def get_label (self, ival = None):
        return self.label_dict[ival]

    # resets colormap used for each ival according to default or map passed to method
    """ initializes the colors which correspond to each unique ival. """
    def reset_colors(self, cmap = None):
        
        # assign default cmap if none was specified
        if cmap is None:
            cmap = default_cmap

        # assign unique color to each unique ival
        # TODO :: check how I handled this with highlight plot

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
                return np.flip(l)
            else:
                return l
        else:
            # otherwise, if an icol has not been specified, return a list with empty string
            return [""]

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

    ## TITLE ##

    # sets the title label
    """ method for setting Figure title label. """
    def set_title_label(self, l = default_title_label, s = None):
        self.title_label = Label (l, s)

    # gets the title label as Label object
    """ method for returning Figure title as Label object. """
    def get_title_label (self):
        return self.title_label

    # gets the title label as string
    """ method for returning the Figure title as string. """
    def get_title_label_str (self):
        return str(self.title_label)

    # determines if title string is empty
    """ method for check if title label is empty by checking if the string assinged to the label is empty. """
    def has_title_label (self):
        return self.title_label.get_label()

    ## SUBTITLE ##

    # sets the subtitle label
    """ method for setting Figure subtitle label. """
    def set_subtitle_label (self, l = default_subtitle_label, s = None):
        self.subtitle_label = Label (l , s)

    # gets the subtitle label as Label object
    """ method for getting the Figure subtitle label as Label object. """
    def get_subtitle_label (self):
        return self.subtitle_label

    # get the subtitle label as string
    """ method for getting the Figure subtitle label as string. """
    def get_subtitle_label_str (self):
        return str(self.subtitle_label)

    # checks if the subtitle label is empty
    """ method that check if the subtitle label is empty by determining if an empty string is assigned to the label. """
    def has_subtitle_label (self):
        # if returns empty string, is evaluated as false in boolean context
        return self.subtitle_label.get_label()

    ## XAXIS ##

    # reset xaxis to empty Axis object with default attributes
    def reset_xaxis(self):
        self.xaxis = Axis()

    # adjust xaxis label properties
    def set_xaxis_label (self, l = None, s = None):
        self.xaxis.set_label(l, s)

    # gets xaxis label as object
    """ returns x-axis label as Label object. """
    def get_xaxis_label (self):
        return self.xaxis.get_label()

    # gets xaxis label as string
    """ returns x-axis label as string. """
    def get_xaxis_label_str (self):
        return str(self.xaxis.get_label())

    # sets the minimum and maximum limits for the xaxis
    """ method used to assign the xaxis minimum and maximum values at the same time. """
    def set_xaxis_limits (self, min_val = None, max_val = None):

        # if xaxis data has already been assigned to the figure object
        if self.xcol is not None:
            # pull min and max values from the list if they were not already provided to the method
            if min_val is None:
                min_val = min(self.df[self.xcol].to_list())
            if max_val is None:
                max_val = max(self.df[self.xcol].to_list())

        # assign the minimum and maximum values
        self.xaxis.set_limits(min_val, max_val)

    # sets the minimum value for the xaxis limit
    """ method used the assign the xaxis minimum limit as double. """
    def set_xaxis_min (self, val = None):
        self.xaxis.set_minimum(val)

    # sets the maximum value for the xaxis limit
    """ method used to assign the xaxis maximum as double. """
    def set_xaxis_max (self, val = None):
        self.xaxis.set_maximum(val)

    # gets the minimum value for the xaxis limit
    """ method that returns the minimum value assigned to the xaxis limit. returns 'None' if unassigned. """
    def get_xaxis_min (self):
        return self.xaxis.get_minimum()

    # gets the maximum value for the xaxis limit
    """ method that returns the maximum value assigned to the xaxis limit. returns 'None' if unassigned. """
    def get_xaxis_max (self):
        return self.xaxis.get_maximum()

    # set the xaxis as either linear or logscale
    """ method sets the xaxis as either a linear or logscale. logscale base set the logscale base as default if not specified by user. """
    def set_xaxis_scale (self, linear = False, log = False, logscale_base = default_logscale_base):
        if linear and log:
            return
        elif linear:
            self.xaxis.set_scale(s = scale_linear)
        elif log:
            self.xaxis.set_scale(s = scale_log, b = logscale_base)

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

    # initialize yaxis object
    def reset_yaxis(self):
        self.yaxis = Axis()

    # adjust yaxis label properties
    def set_yaxis_label (self, l = None, s = None):
        self.yaxis.set_label(l, s)

    # gets the y-axis label as object
    """ returns the y-axis label as string. """
    def get_yaxis_label (self):
        return self.yaxis.get_label()

    # gets the y-axis label as string
    """ returns the y-axis label as string. """
    def get_yaxis_label_str (self):
        return str(self.yaxis.get_label())

    # set the yaxis minimum and maximum values
    """ method that assigns minimum and maximum values to the yaxis limits. """
    def set_yaxis_limits (self, min_val = None, max_val = None):

        # if yaxis data has already been provided to the method
        if self.ycol is not None:
            # pull min and max values from the list if they were not already provided to the method
            if min_val is None:
                min_val = min(self.df[self.ycol].to_list())
            if max_val is None:
                max_val = max(self.df[self.ycol].to_list())

        # assign the minimum and maximum values
        self.yaxis.set_limits(min_val, max_val)

    # set yaxis minimum limit
    """ method that assigns a double as the yaxis minimum limit. """
    def set_yaxis_min (self, val):
        self.yaxis.set_minimum(val)

    # set yaxis maximum limit
    """ method that assigns a double as the yaxis maximum limit. """
    def set_yaxis_max (self, val):
        self.yaxis.set_maximum(val)

    # get the yaxis minimum limit
    """ method that returns the yaxis minimum limit as double. returns 'None' if unassigned. """
    def get_yaxis_min (self):
        return self.yaxis.get_minimum()

    # get the yaxis maximum limit
    """ method that returns the yaxis maximum limit as double. returns 'None' is unassigned. """
    def get_yaxis_max (self):
        return self.yaxis.get_maximum()

    # set the yaxis as either linear or logscale
    """ method sets the yaxis as either a linear or logscale. logscale base set the logscale base as default if not specified by user. """
    def set_yaxis_scale (self, linear = False, log = False, logscale_base = default_logscale_base):
        if linear and log:
            return
        elif linear:
            self.yaxis.set_scale(s = scale_linear)
        elif log:
            self.yaxis.set_scale(s = scale_log, b = logscale_base)

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

    # sets the figure dpi
    """ sets the dpi for the figure. """
    def set_dpi (self, d = None):
        # check that the value passed to the method is an integer greater than the minimum
        if d is None or not isinstance(d, int):
            self.dpi = default_dpi
        else:
            if d < minimum_dpi:
                self.dpi = minimum_dpi

    # gets the figure dpi
    """ return the figure dpi (dots per inch). """
    def get_dpi (self):
        return self.dpi

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
