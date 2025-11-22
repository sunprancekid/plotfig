
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


## METHODS ##
# none

## CLASSES ##
## Label class
class Label (object):

    """ contains information corresponding to a label in plotted figures.

    Attributes:
    -----------
    l : str
        string used to display label.
    s : int
        label font size

    Methods:
    --------
    set_label:
        assign label string.
    get_label:
        returns label string.
    set_size:
        assigns label font size.
    get_size:
        returns label font size.
    """

    def __init__ (self, l = None, s = None):
        """ initializes Label object.
        
        default label string is empty and default label size is 12.

        Parameters:
        -----------
        l : str
            str to used for label.
        s : int
            font size to display label.

        Returns:
        --------
        None

        """
        self.set_label(l)
        self.set_size(s)

    def __str__ (self):
        """ returns string representing current state of Label object.

        Parameters:
        -----------
        None

        Returns:
        --------
        str
            string representing current state of object.

        """

        out = ""
        if self.label is None:
            out += "Empty Label"
        else:
            out += self.get_label()
        out += " (font size: {})".format(self.get_size())

        return out


    ## GETTERS AND SETTERS ##

    def set_label (self, l = None):
        """ assigns label string.

        Parameters:
        -----------
        l : str
            string to assign to label.

        Returns:
        --------
        None

        """
        if l is None or not isinstance(l, str):
            # if l is not an object or not a string
            self.label = None
        else:
            # otherwise l is a string
            self.label = l

    def get_label (self):
        """ returns label string.

        Parameters:
        -----------
        None

        Returns:
        --------
        str
            string assigned to Label.
        """
        if self.label is None:
            return ""
        else:
            return self.label

    def set_size (self, s = None):
        """ assigns label font size.

        Parameter:
        ----------
        s : int
            integer greater than zero.

        Returns:
        --------
        None

        """
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

    def get_size (self):
        """ returns label font size.

        Parameters:
        -----------
        None

        Returns:
        --------
        int
            integer assigned to label font size.

        """
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
    reset_limits():
        resets the minimum and maximum limits.
    set_limits():
        assigns limits to minimum and / or maximum limits.
    reset_maximum():
        removes maximum limit.
    set_maximum():
        assigns real-numbered value to axis maximum limit.
    get_maximum():
        returns value assigned to axis maximum.
    has_maximum():
        returns 'True' if axis has maximum limit, else 'False'.
    reset_minimum():
        removes minimum limit.
    set_minimum():
        assigns real-numbered value to axis minimum limit.
    get_minimum():
        returns value assigned to axis minimum limit.
    has_minimum():
        returns 'True' if axis has minimum limit, else 'False'.
    reset_scale():
        assigns default scale to axis.
    set_scale():
        assign scale to axis, either linear or logarithmic.
    is_logscale():
        returns 'True' if axis is logarithmic scale, else 'False'.
    is_linearscale():
        returns 'True' if axis is linear scale, else 'False'.
    get_scale():
        returns scale assigned to Axis.
    get_logscale_base():
        returns logscale base if axis is logscale, else 'None'.
    reset_major_ticks():
        assigned 'None' to axis major ticks.
    set_major_ticks():
        generates major axis tick marks.
    get_major_ticks():
        returns major axis tick marks
    has_major_ticks():
        returns boolean determining if axis has major tick marks.
    reset_minor_ticks():
        assigns 'None' to minor axis tick marks.
    set_minor_ticks():
        generates minor axis ticks marks.
    get_major_ticks():
        returns minor axis tick marks.
    has_major_ticks():
        returns boolean determining if axis has minor tick marks.
    """

    def __init__ (self):
        """ initialize Axis object.

        limits, label, major and minor ticks are all 'None' type. default
        axis scale is 'linear'.

        Parameters:
        -----------
        None

        Returns:
        --------
        None

        """
        self.reset_label() 
        self.reset_limits()
        self.reset_scale() 
        self.reset_major_ticks()
        self.reset_minor_ticks()
        # TODO :: add attribute to define scale type has being either catagories or numbers

    def ___str___ (self):
        """ generate string describing state of Axis object attributes.

        Parameters:
        -----------
        None

        Returns:
        --------
        str
            string representing current state of object.

        """
        s = ""
        s.append("Axis Label String: {0}\nAxis Label Fontsize: {1}\n".format(self.get_label_string(), self.get_label_fontsize()))
        s.append("Axis Limits (min, max): ({0}, {1})\n".format(self.get_minimum(), self.get_maximum()))
        pass

    ## AXIS LABEL

    def reset_label (self):
        """ assigns None type to Axis Label 'l'.
        
        Parameters
        ----------
        None

        Returns
        -------
        None

        """
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
        Otherwise, returns None.

        Parameters:
        -----------
        None

        Returns:
        --------
        label
            Label object assigned to axis."""
        if self.label is None:
            return Label (l = "")
        else:
            return self.label

    def has_label(self):
        """ returns boolean determining if Label has been assigned to Axis.

        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            determines if Label has been assigned to axis already.
        """
        return self.label is not None

    def set_label_string(self, l):
        """ assigns string to Axis label.

        Parameters:
        -----------
        l : str
            string describing axis value.

        Returns:
        --------
        None
        """

        # if a label has not been assigned to the axis, create a new one
        if not self.has_label():
            self.set_label("")
        if isinstance(l, str):
            self.label.set_label(l)
        else:
            print("ERROR :: Axis.set_label_string() :: label string 'l' must be string type.")
            exit(NONZERO_EXITCODE)

    def set_label_fontsize(self, s):
        """ assigns fontsize to Axis label.

        Parameters:
        -----------
        s : int
            font size assigned to label in plot.

        Returns:
        --------
        None"""

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

    def reset_limits (self):
        """ resets the minimum and maximum limits.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """

        self.reset_minimum()
        self.reset_maximum()

    def set_limits (self, min_val = None, max_val = None):
        """ assigns limits to minimum and / or maximum limits.

        Parameters:
        -----------
        min_val : int or float
            maximum axis value
        min_val : int or float
            minimum axis value

        Returns:
        --------
        None
        """
        self.set_maximum(max_val)
        self.set_minimum(min_val)

    def reset_maximum (self):
        """ removes maximum limit.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        self.set_maximum()

    def set_maximum(self, m = None):
        """ assigns real-numbered value to axis maximum limit.

        accepts integer or float. if the value assigned to the method
        is an integer, it is then type cast as a float. If a minimum
        value has already been assigned to the axis and the maximum is
        less than the minimum, the value passed to the method ('m') is
        not assigned, and the maximum limit is set to the default 'None'
        type.

        Parameters:
        -----------
        m : int or float
            value to assign to maximum.

        Returns:
        --------
        None
        """
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

    def get_maximum (self):
        """ returns value assigned to axis maximum.

        Parameters:
        -----------
        None

        Returns:
        --------
        float
            value assgined to maximum axis limit, or None.
        """
        return self.max

    def has_maximum (self):
        """ returns 'True' if axis has maximum limit, else 'False'.

        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            determines if a maximum value has been assigned to the axis."""
        return self.max is not None

    def reset_minimum (self):
        """ removes minimum limit.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        self.set_minimum()

    def set_minimum (self, m = None):
        """ assigns real-numbered value to axis minimum limit.

        accepts either integer or float. if integer is passed to method,
        integer is type cast to float. Value is not assigned to minimum 
        limit if: (1) value type is not integer or float, or (2) the axis
        already has a maximum limit, and the value passed to the method
        is greater than the assigned maximum limit. In either of those
        cases, the minimum limit is set to 'None' type.

        Parameters:
        -----------
        m : int or float
            minimum value to assign to axis limit.

        Returns:
        --------
        None
        """
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

    def get_minimum (self):
        """ returns value assigned to axis minimum limit.

        Parameters:
        -----------
        None

        Returns:
        --------
        float
            value assigned to axis minimum limit, or 'None'.
        """
        return self.min

    def has_minimum (self):
        """ returns 'True' if axis has minimum limit, else 'False'.
        
        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            determines if value has been assigned to axis minimum limit.
        """
        return self.min is not None 


    ## AXIS SCALE

    def reset_scale(self):
        """ assigns default scale to axis.

        Parameters:
        -------------
        None

        Arguments:
        ----------
        None

        """

        self.set_scale()

    def set_scale (self, s = None, b = None):
        """ assign scale to axis, either linear or logarithmic.

        assigns one of two scales to axis. if the axis type passed to the
        method via 's' is not one of the two accepted types, the default
        ('linear') is assigned. If the scale assigned to the axis is 'log',
        a base 'b' which is real and positive is also required. If none is
        assigned, the default (10) is used.

        Parameters:
        -----------
        s : str
            accepts either 'linear' or 'log' as argument.
        b : float
            if scale is 'log', positive, real value for log base.

        Returns:
        --------
        None

        """
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

    def is_logscale(self):
        """ returns 'True' if axis is logarithmic scale, else 'False'.

        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            'True' if scale is 'log', else 'False'.

        """

        return self.scale == scale_log

    def is_linearscale (self):
        """ returns 'True' if axis is linear scale, else 'False'.

        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            'True' if axis scale is 'linear', else 'False'.
        
        """

        return self.scale == scale_linear

    def get_scale (self):
        """ returns scale assigned to Axis.

        Parameters:
        -----------
        None

        Returns:
        --------
        str
            either 'log' or 'linear'.
        """
        return self.scale

    def get_logscale_base (self):
        """ returns logscale base if axis is logscale, else 'None'.

        Parameters:
        -----------
        None

        Returns:
        --------
        float
            real, positive number.
        """
        if self.is_logscale():
            return self.base
        else:
            return None

    ## AXIS MAJOR TICKS

    def reset_major_ticks (self):
        """ assigns 'None' to axis major ticks. 

        Parameters:
        -----------
        None

        Returns:
        --------
        None

        """
        self.major_ticks = None

    def set_major_ticks (self, minval = None, maxval = None, nticks = default_number_major_ticks, pad = default_padding_value):
        """ generates major axis tick marks.

        generates ticks which are assigned to major axis. 'minval' and
        'maxval' can be unspecified if axis limits have already been
        assigned. 'nticks' is the total number of major ticks to generate.
        uses default if no value is assigned. 'pad' is a precentage  
        axis limits are increase by from relative to major axis limits.
        default pad is used if no value is assigned.

        Parameters:
        -----------
        minval : float or int
            (optional) minimum tick value
        maxval : float or int
            (optional) maximum tick value
        nticks : int
            (optional) number of major axis ticks.
        pad: float
            (optional) real number as precentage.

        Returns:
        --------
        None
        """

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

    def get_major_ticks (self):
        """ returns axis major tick marks.

        Parameters:
        -----------
        None

        Returns:
        --------
        numpy.array
            1D numpy array containing axis values in numerical order.

        """

        return self.major_ticks

    def has_major_ticks (self):
        """ returns boolean determining if axis has major tick marks.

        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            'True' if major axis has tick marks, else 'False'.
        """
        return self.major_ticks is not None

    ## AXIS MINOR TICKS

    def reset_minor_ticks (self):
        """ assign 'None' to major axis tick marks.

        Parameters:
        -----------
        None

        Returns:
        --------
        None

        """
        self.minor_ticks = None

    def set_minor_ticks(self, nticks = default_number_minor_ticks):
        """ generates minor axis ticks marks.

        can only generate minor ticks if major ticks have already been
        assigned. Uses major ticks to generate 'nticks' between major
        axis tick marks.

        Parameters:
        -----------
        nticks : int
            number of ticks between each set of major ticks.

        Returns:
        --------
        None

        """

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

    def get_minor_ticks (self):
        """ returns minor axis tick marks.

        Parameters:
        -----------
        None

        Returns:
        --------
        numpy.array
            1D numpy array containing axis values in numerical order.

        """
        return self.minor_ticks

    def has_minor_ticks (self):
        """returns boolean determining if axis has minor ticks marks.
        
        Parameters:
        -----------
        None

        Returns:
        --------
        boolean
            'True' if axis has minor axis tick marks, else 'False'.
        """
        return self.minor_ticks is not None

## ARGUMENTS
# none

## SCRIPT
# none