import numpy as np
import pandas as pd
from time import mktime
import scipy as py
#import statsmodels.formula.api as sm
from decimal import Decimal

#create a dataframe for the fund monthly returns
dates = pd.date_range('20060531', periods=93, freq='m')
fund = pd.DataFrame(np.array([-3.104000, -0.255945, 0.907479, 3.148125, 1.683955,
	                       4.106766, 1.877651, 1.521993, 0.825686, -2.494735,
	                      1.209756, 4.193608, 2.776651, -1.501767, -1.387146,
                              1.450794, 5.658789, 3.179196, -2.792000, -0.633363,
	                      -3.857324, -1.894269, 1.089323, 2.011409, 0.319711,
	                    -4.718387, -0.781296, 0.308407, -5.447309, -5.574479,
	                    -3.050039, -2.429375, -4.684144, -4.994334, 3.193983,
                             3.329514, 2.736453, -0.168320, 3.824178, 0.800020,
	                     1.369205, -1.320985, 2.695861, 0.412463, -3.649863,
                             2.259430, 3.443910, -0.077815, -8.185154, -1.885265,
                             2.355027, -1.135664, 2.708877, 1.773395, -0.812169,
                             2.712260, 0.279937, 2.125974, -0.492975, 1.401751, 
                             -0.958304, -1.024985, -0.235049, -4.355007, -5.786226,
                             8.232815, 0.468001, 0.157758, 5.072329, 2.877774, 
                             1.444089, -0.664743, -5.852275, 3.377763, -0.757835,
                             1.668567, 0.872572, -1.961853, 0.131356, 0.885196, 
                             4.371533, 0.441362, 3.222805, 2.803799, 2.005546,
                             -2.368675, 5.072989, 0.015211, 2.136353, 2.667355,
                             1.764279, 3.461681, -2.070000]),
                             index=dates)


#create a dataframe for the benchmarks monthly returns
dates = pd.date_range('20060531', periods=93, freq='m')
bench = pd.DataFrame(np.array([-2.190000, -0.160000, 1.700000, 2.580000, 3.110000,
                               3.420000, 1.740000, 1.800000, 1.090000, -3.150000,
                               1.060000, 4.850000, 3.500000, -1.250000, -2.340000, 
                               1.990000, 4.100000, 1.510000, -4.210000, -0.740000,
                               -6.200000, -4.310000, 0.280000, 4.680000, 0.110000,
                               -8.840000, 0.520000, 1.200000, -7.650000, -16.480000,
                               -6.330000, -0.070000, -9.850000, -10.630000, 8.190000,
                               7.810000, 5.280000, 0.390000, 7.190000, 3.410000, 
                               2.950000, -1.070000, 6.030000, 0.850000, -3.680000,
                               2.530000, 5.900000, 1.150000, -9.190000, -5.060000,
                               6.740000, -4.830000, 7.770000, 3.580000, -0.090000,
                               6.800000, 2.430000, 3.130000, -0.400000, 2.654523,
                               -1.519769, -1.445557, -1.062092, -5.310000, -6.710000,
                               9.656022, 0.092204, 1.746858, 4.129151, 4.526749,
                               3.533015, -0.681345, -6.124688, 4.300000, 1.960000,
                               1.700000, 2.690000, -2.490000, 0.130000, 0.110000,
                               4.280000, 1.200000, 2.920000, 2.110000, 2.180000,
                               -1.740000, 4.865426, -3.070000, 2.350000, 4.610000,
                               2.920000, 2.660000, -4.140000]),
                                         index=dates)

def date_range(lst, date):

    # format date to string format if not done already
    if not isinstance(date, (str, unicode)):
        date = date.strftime('%Y%m%d')
        
    # return the date range
    return pd.date_range(date, periods=len(lst), freq='m')

def to_dataframe(lst, dates):
    return pd.DataFrame(np.array(lst), index=dates)  
   
def to_list(series):
    dic = series[0].to_dict()
    
    lst = []
    for i, a in dic.iteritems():
        date = int(mktime(i.timetuple())) * 1000
        val = float("%.2f" % a)
        lst.append([date, val])
        
    # sort it by date
    lst.sort(key = lambda row: row[0])
    
    return lst
                                         


# old func
def cum_final (lst, date, periods): # periods not used
    dates = date_range(lst, date)
    df = to_dataframe(lst, date)
    s_ret = simp_ret(df)
    return ((np.cumprod(s_ret.values+1)-1)*100)[-1:,][0]


  
# old func
def cum_ret (lst, date):

    dates = date_range(lst, date)
    ser = to_dataframe(lst, date)
    
    # divide by 100
    s_ret = simp(ser)
    
    scret = (np.cumprod(s_ret.values+1)-1)
    
    # multiply with 100, is this necessary?
    cret = simp2perc(scret)
    
    return to_list(pd.DataFrame(cret, index=dates))

# old func
def roll_mean(lst, date, window=12):
    series = to_dataframe(lst, date)
    roll_mean = pd.rolling_mean(series, window=window)
    return to_list(roll_mean)




#certain calculations require us to use simple percents
# to convert use the function
def simple (series):
    simple = series/100
    return simple


#returns simple percents to 100 based 
def simple2percent (series):
    simple2percent = series*100
    return simple2percent
    
    
#calculates the cumulative return based on returns
def cum_returns (series, dates):
    simple_returns = simple(series)
    simple_cum_returns = (np.cumprod(simple_returns.values+1)-1)
    cum_returns = simple2percent(simple_cum_returns)
    cum_returns = pd.DataFrame(cum_returns, index=dates)
    return cum_returns


#gives the final value of the cumulative returns
def cum_returns_final_val (series, dates):
    simple_returns = simple(series)
    simple_cum_returns = (np.cumprod(simple_returns.values+1)-1)
    cum_returns = simple2percent(simple_cum_returns)
    cum_returns_dates = pd.DataFrame(cum_returns, index=dates)
    cum_returns_final_val = pd.DataFrame.tail(cum_returns_dates,1)      
    return cum_returns_final_val 


#calculates simple cumulative return based on returns
def simple_cum_returns (series):
    simple_returns = simple(series)
    simple_cum_returns = (np.cumprod(simple_returns.values+1)-1)
    return simple_cum_returns


#calculates the delta between two return series (ser1 - ser2)
def delta_cum_returns (series1, series2, dates, dates2):
    delta_cum_returns = cum_returns(series1, dates) - cum_returns(series2, dates2)
    return delta_cum_returns


#Excess return 
# calculates the final value of delta_cum_ret
def delta_cum_returns_final_val (series1, series2):
    delta_cum_returns = (cum_returns(series1) - cum_returns(series2))
    delta_cum_returns_dates = pd.DataFrame(delta_cum_returns, index=dates)
    delta_cum_returns_final_val_dates = pd.DataFrame.tail(delta_cum_returns_dates,1) 
    return delta_cum_returns_final_val_dates


#calculates the rolling cumulative returns of a monthly returns series
# window = window=n,  step = [::n]
def roll_cum_returns (series, window):
    simple_returns = simple(series)
    simple_roll_cum_returns = pd.rolling_apply(simple_returns, window, lambda x: np.prod(1 + x) - 1)
    roll_cum_returns = simple2percent(simple_roll_cum_returns)
    return roll_cum_returns


def roll_delta_cum_returns (series1, series2, window):
    roll_delta_cum_returns = roll_cum_returns(series1, window=window) - roll_cum_returns(series2, window=window)
    return roll_delta_cum_returns


def roll_delta_cum_returns_final_val (series1, series2, window):
    roll_delta_cum_returns = roll_cum_returns(series1, window=window) - roll_cum_returns(series2, window=window)
    roll_delta_cum_returns_final_val = pd.DataFrame.tail(roll_delta_cum_returns,1)
    
    return roll_delta_cum_returns_final_val


#used in the calculation of the maximum drawdown of a returns series
def drawdown(series):
    max_drawdown = 0
    drawdown = 0
    peak = -99999
    
    for value in series:
        if (value > peak):
            peak = value
        else:
            drawdown = (peak - value) / peak
        if (drawdown > max_drawdown):
            maxdrawdown = drawdown
    drawdown = value.min()/peak
                          
    return drawdown

#calculate the maximum drawdown of a retrun series
def max_drawdown(series):
    simple_cum_return = simple_cum_returns(series)
    maxdrawdown = drawdown(simple_cum_return+1)-1
    max_drawdown = maxdrawdown*-100
       
    return max_drawdown


#calculate the plain sum of the return series
def sum (series):
    sum = series.sum(0)
    return sum


#calculate the rolling sum of the returns series
# window = window=n,  step = [::n]
def roll_sum (series, window):
    roll_sum = pd.rolling_sum(series, window=window)
    return roll_sum


#calculate the mean value of the return values
def mean (series):
    mean = series.mean(0)
    return mean
    
#calculate the rolling mean of the returns values
# window = window=n,  step = [::n]

def roll_mean (series, window):
    roll_mean = pd.rolling_mean(series, window=window)
    return roll_mean

#calculate the standard deviation of the return values
def standard_deviation (series):
    standard_deviation = series.std(0)
    return standard_deviation

#calculate the rolling standard deviation of the returns values
# window = window=n,  step = [::n]
def roll_standard_deviation (series, window):
    roll_standard_deviation = pd.rolling_std(series, window=window)
    return roll_standard_deviation

#calculate the modified standard deviation of the return values
def modified_standard_deviation(series):
    n = float(len(series))
    modified_standard_deviation = standard_deviation(series) * np.sqrt(n/(n-1))
    return modified_standard_deviation

#calculate the rolling modified standard deviation of the returns values
def roll_modified_standard_deviation (series, window):
    roll_modified_standard_deviation = pd.rolling_apply(series,window,lambda x: modified_standard_deviation(x))
    return roll_modified_standard_deviation


#calculate the standard deviation of the return values
def variance (series):
    variance = np.var(series, axis=0, ddof=1)
    return variance


#calculate the rolling standard deviation of the returns values
# window = window=n,  step = [::n]
def roll_variance (series, window):
    roll_variance = pd.rolling_apply(series, window, lambda x: variance(x))
    return roll_variance

# gives same results as VAR check ddof to be used???
#calculate the modified variance of the return values
def modified_variance (series):
    n = float(len(series))
    modified_variance = variance(series) * np.sqrt(n/(n-1))       
       
    return modified_variance

def roll_modified_variance(series, window):
    roll_modified_variance = pd.rolling_apply(series, window,lambda x: modified_variance(x))
    return roll_modified_variance


#calculate the skewness of the return values
def skewness (series):
    skewness = series.skew(0)
    return skewness
    
#calculate the rolling skewness of the returns values
#window = n  Freq = [::n]
def roll_skewness (series, window):
    roll_skewness = pd.rolling_skew(series, window=window)
    return roll_skewness


#calculate the kurtosis of the return values
def kurtosis (series):
    kurtosis = series.kurt(0)
    return kurtosis
    
#calculate the rolling kurtosis of the returns values
# window = n  Freq = [::n]
def roll_kurtosis (series, window):
    roll_kurtosis = pd.rolling_kurt(series, window=window)
    return roll_kurtosis


#f is the annualisation factor the number of periods in a year 
# it is set by default to 12 representing monthly data, if daily
# data is used then this should be changed to 252
def annualised_returns(series, f=12):
    n = len(series)
    simple_returns = simple(series)
    simple_annualised_returns = np.power(np.product(1 + simple_returns, axis=0), (f*1.0)/(n*1.0))-1
    annualised_returns = simple2percent(simple_annualised_returns)
    return annualised_returns

#window = n  Freq = [::n]

def roll_annualised_returns(series, f=12, window=12, LessThanWin=True):
    if LessThanWin:
        return pd.rolling_apply(series,window,lambda x: annualised_returns(x,f),min_periods=len(series)%window)
    else:
        return pd.rolling_apply(series,window,lambda x: annualised_returns(x,f),min_periods=window)


# f is the number of time periods in a year months = 12, days = 252 
# it is set by default to 12 representing monthly data, if daily
# data is used then this should be changed to 252
def volatility(series, f=12):
    simple_returns = simple(series)
    simple_volatility = modified_standard_deviation(simple_returns)*np.sqrt(f)
    volatility = simple2percent(simple_volatility)    
    return volatility

# calculates the rolling volatility of the 
def roll_volatility(series, window, f=12):
    r_vol = pd.rolling_apply(series, window, lambda x: volatility(x,f))
    return r_vol
    
#downside volatility
def downside_volatility(series, mar=0, f=12):
    series_ignoring_vals_above_mar = series[series-(mar/f)<0]
    n = len(series_ignoring_vals_above_mar)
    series_ignoring_vals_above_mar2 = np.power(series_ignoring_vals_above_mar, 2)
    downside_volatility =  np.sqrt(f)* np.sqrt(series_ignoring_vals_above_mar2.sum().div(n - 1))
    return downside_volatility


#########################
#LOOK AT THIS
#rolling downside volatility
def roll_downside_volatility_base(series, window, mar=0, f=12):
    series_ignoring_vals_above_mar = series[series-(mar/f)<0]
    roll_downside_volatility_base = modified_standard_deviation(series_ignoring_vals_above_mar)*np.sqrt(f)
    
    return roll_downside_volatility_base
##########################

def roll_downside_volatility(series, window, mar=0, f=12):
    roll_downside_volatility = pd.rolling_apply(series, window, lambda x: roll_downside_volatility_base(x,f))
    
    return roll_downside_volatility

#calculate sharpe ratio
def sharpe_ratio( series, f=12):
    simple_returns = simple(series)    
    numerator = annualised_returns(series)
    denominator = standard_deviation(series)*np.sqrt(f)
    
    sharpe_ratio = numerator/denominator
    
    return sharpe_ratio

#rolling sharpe ratio
def roll_sharpe_base( series, f=12):
    numerator = annualised_returns(series)
    denominator = modified_standard_deviation(series)*np.sqrt(f)
    
    roll_sharpe_base = numerator/denominator
    
    return roll_sharpe_base

def roll_sharpe_ratio(series, window, f=12):
    roll_sharpe_ratio = pd.rolling_apply(series, window, lambda x: roll_sharpe_base(x,f))

    return roll_sharpe_ratio


#calculate sortino ratio
def sortino_ratio( series, f=12):
    numerator = annualised_returns(series)
    denominator = downside_volatility(series)
    
    sortino_ratio = numerator/denominator
    
    return sortino_ratio

#rolling sortino ratio
def roll_sortino_base(series, f=12):
    numerator = annualised_returns(series)
    denominator = downside_volatility(series)
    roll_sortino_base = numerator/denominator
    
    return roll_sortino_base

def roll_sortino_ratio(series, window, f=12):
    roll_sortino = pd.rolling_apply(series, window, lambda x: sortino_ratio(x,f))

    return roll_sortino


#calculate the correlation of the returns series
def correlation (series1, series2, method='method'):
    correlation = series1.corrwith(series2)

    return correlation

#calculate the rolling correlation of two returns series
# window = n  Freq = [::n]

def roll_correlation (series1, series2, window):
    roll_correlation = pd.rolling_corr(series1,  series2, window=window)

    return roll_correlation

def covariance(series1,series2):
    X = np.hstack((series1,series2))
    cov1 = np.cov(series1,series2, rowvar=0)
    covariance = cov1[['0','1']]
            
    return covariance

#calculate the rolling covariance of two returns series
# window = n  Freq = [::n]
def roll_covariance(series1,series2,window):
    X = np.hstack((series1,series2))
    roll_covariance = pd.rolling_cov(series1,series2, window)
            
    return roll_covariance

# used to calculate the tracking error
def tracking_error(series1, series2, f=12):
    tracking = series1-series2
    tracking_error = np.sqrt(f)*standard_deviation(tracking)
     
    return tracking_error

####################################
#look at this
# used to calculate the rolling tracking error
def roll_tracking_error(series1, series2, window, f=12):
    tracking = series1-series2
    tracking_er  = np.sqrt(f)*modified_standard_deviation(tracking)
    roll_tracking_error = pd.rolling_apply(series1, series2, window, f, lambda x: tracking_error(x,f))
         
    return roll_tracking_error

def roll_tracking_error2(series1, series2, window, f=12):
    roll_tracking_error = pd.rolling_apply(series1, series2, window, lambda x: roll_tracking_error_base(x,f))
     
    return rol_tracking_error
   
 
#####################################


def beta(series1,series2):
    numerator = covariance(series1, series2)
    denominator = variance(series2)
    beta = numerator/denominator
    
    return beta

#def rollingbeta(ser1, ser2,window f=12)
def roll_beta(series1,series2, window):
    numerator = roll_covariance(series1, series2,window)
    denominator = roll_variance(series2, window)
    beta = numerator/denominator
    
    return beta    



def alpha(series1,series2):
    numerator = covariance(series1, series2)
    denominator = variance(ser2)
    beta = numerator/denominator
    alpha = mean(series1) - beta*mean(series2)

    return alpha

def roll_alpha(series1,series2, window):
    numerator = roll_covariance(series1, series2, window)
    denominator = roll_variance(series2, window)
    beta = numerator/denominator
    alpha = pd.rolling_mean(series1, window) - beta*pd.rolling_mean(series2, window)

    return alpha


def ols(series1, series2):
    model = sm.OLS(series1, series2).fit()
    results = model.summary()
    
    return results

def r2(series1, series2):
    model = sm.OLS(series1, series2)
    results = model.fit()     
    return results.rsquared


# Look at this
def roll_r2(series1, series2, window, f=12):
    roll_r2 = pd.rolling_apply(series1, series2, window, lambda x: r2(x,f))
    return roll_r2
 
def adjr2(series1, series2):
    model = sm.OLS(series1, series2)
    results = model.fit()
    return results.rsquared_adj

# Look at this
def roll_adjr2(series1, series2, window, f=12):
    roll_adjr2 = pd.rolling_apply(series1, series2, window, lambda x: adjr2(x,f))
    return roll_adjr2
    
#W22 - return histogram
def hist(series):
    hist = np.histogram(series, bins=20, range=(-10,10))
    return hist
  
