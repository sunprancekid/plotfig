
## Matthew Dorsey
## @sunprancekid
## 17.11.2025

## FILENAME: axis.py
## PURPOSEL: contains axis object

##############
## PACKAGES ##
##############
# conda / native 
import pandas as pd
import numpy as np
import os # used to check path
import itertools # used for iterating over markers


## PARAMETERS ## 

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


## METHODS ##
# none


## CLASSES ##
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

    """
    contains information corresponding to one axis in plotted figures.

    Attributes:
    -----------
    l : Label
        axis title as string and font size
    max_val : float
        maximum axis value
    min_val : float
        minimum axis vlue
    scale : string
        assigned type of either linear or log scale
    major_ticks : list of float
        list of numbers that correspond to major tick marks along axis
    minor_ticks : list of float
        list of real numbers that correspond to minor tick marks along axis

    Methods:
    --------
    reset_label():
        assigns None type to 'l'
    set_label():
        resent / update label string and / or font size to 'l'
    get_label():
        returns 'l' if not None type, otherwise returns empty Label
    has_label():
        returns True if 'l' is not None, else false
    get_label_string():
        returns string assigned to Label 'l'
    get_label_fontsize():
        returns fontsize assigned to Label 'l'
    """

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
        """ generate string listing Axis object attributes."""
        s = ""
        s.append("Axis Label String: {0}\nAxis Label Fontsize: {1}\n".format(self.get_label_string(), self.get_label_fontsize()))
        s.append("Axis Limits (min, max): ({0}, {1})\n".format(self.get_minimum(), self.get_maximum()))
        pass

    ## AXIS LABEL

    def reset_label (self):
        """ assigns None type to Axis Label 'l'."""
        self.label = None

    def set_label (self, l = None, s = None):
        """ assign string and font size to Axis Label 'l'.

        Accepts string and / or integer describing axis label. If method call 
        is empty, empty label is assigned to object. If Label is already
        assigned, attributes are updated.

        Parameters:
        -----------
        l : str
            string displayed below axis
        s : int
            font size of axis string display

        Returns:
        --------
        None
        """

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

    def get_label (self):
        """ returns label assigned to Axis object if one has been assigned.
        Otherwise, returns None."""
        if self.label is None:
            return Label (l = "")
        else:
            return self.label

    def has_label(self):
        """ Returns boolean determining if Label has been assigned to Axis."""
        return self.label is not None

    def set_label_string(self, l):
        """ Assigns string to Axis label."""

        # if a label has not been assigned to the axis, create a new one
        if not self.has_label():
            self.set_label("")
        if isinstance(l, str):
            self.label.set_label(l)
        else:
            print("ERROR :: Axis.set_label_string() :: label string 'l' must be string type.")
            exit(NONZERO_EXITCODE)

    def set_label_fontsize(self, s):
        """ Assigns fontsize to Axis label."""

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
        return self.minor_ticks is not None

## ARGUMENTS
# none

## SCRIPT
# none