import numpy as np
import pandas as pd

#certain calculations require us to use simple percents
def simp_ret (ser):
    simp = ser/100

    return simp

#gives the final value of the cumulative returns
def cum_final (values, date, periods):
    if not isinstance(date, (str, unicode)):
        date = date.strftime('%Y%m%d')
    date_range = pd.date_range(date, periods=periods, freq='m')
    data_frame = pd.DataFrame(np.array(values), index=date_range)
    s_ret = simp_ret(data_frame)
    return ((np.cumprod(s_ret.values+1)-1)*100)[-1:,][0]

