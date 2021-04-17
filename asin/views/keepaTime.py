# -*- coding: utf-8 -*-
"""
Module to convert keepa time
"""
import datetime
import numpy as np

# hardcoded ordinal time from 
keepa_st_ordinal = np.datetime64('2011-01-01')

def KeepaMinutesToTime(minutes, to_datetime=True):

    # Convert to timedelta64 and shift
    dt = np.array(minutes, dtype='timedelta64[m]')
    dt = dt + keepa_st_ordinal # shift from ordinal

    # Convert to datetime if requested
    if to_datetime:
        return dt.astype(datetime.datetime)
    else:
        return dt
