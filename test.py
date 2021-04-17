import datetime

tstr = '20200330'
tdatetime = datetime.datetime.strptime(tstr, '%Y%m%d').strftime("%Y/%m/%d")
print(type(tdatetime))

import numpy as np

import datetime

keepa_st_ordinal = np.datetime64('2011-01-01')

def keepaMinutesToTime(minutes, to_datetime=True):

    # Convert to timedelta64 and shift
    dt = np.array(minutes, dtype='timedelta64[m]')
    dt = dt + keepa_st_ordinal # shift from ordinal

    # Convert to datetime if requested
    if to_datetime:
        return dt.astype(datetime.datetime)
    else:
        return dt

reslt = keepaMinutesToTime(4419870,True)

print(type(reslt))
print(reslt)

import matplotlib.font_manager as fm

for val in fm.findSystemFonts():
    print(val)