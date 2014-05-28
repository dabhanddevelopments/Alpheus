from tastypie import fields
from alpheus.base_resources import MainBaseResource
from tastypie.resources import Resource, ModelResource
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from v2.models import *
from alpheus.utils import cumulative_return
from alpheus.calcs import *
from datetime import datetime, timedelta
import decimal
import numpy as np
import pandas as pd
from django.utils.datastructures import SortedDict
from operator import itemgetter
from django.db.models import Sum
from random import randint

class AdministratorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Administrator.objects.all()

class AlarmResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Alarm.objects.all()

class GroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = AlpheusGroup.objects.all()

class AssetClassResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = AssetClass.objects.all()

class AuditorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Auditor.objects.all()

class BenchComponentResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = BenchComponent.objects.all()

class BenchPeerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = BenchPeer.objects.all()

class BrokerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Broker.objects.all()

class CounterPartyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = CounterParty.objects.all()

class CountryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Country.objects.all()

class CurrencyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Currency.objects.all()

class CurrencyRateResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = CurrencyRate.objects.all()

class CustodianResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Custodian.objects.all()

class FeeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Fee.objects.all()

class FundStyleResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundStyle.objects.all()

class GicsCategoryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = GicsCategory.objects.all()

class HfSectorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HfSector.objects.all()

class IcbCategoryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IcbCategory.objects.all()

class IndustryGroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustryGroup.objects.all()

class IndustrySectorResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustrySector.objects.all()

class IndustrySubGroupResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IndustrySubGroup.objects.all()

class IssuerIndustryResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = IssuerIndustry.objects.all()

class ManagerResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Manager.objects.all()

class RegionResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Region.objects.all()

class ClientPositionAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientPositionAudit.objects.all()

class ClientResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Client.objects.all()

class ClientTransactionsResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientTransaction.objects.all()

class ClientValAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = ClientValAudit.objects.all()

class FundFeeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundFee.objects.all()
  

    def alter_list_data_to_serialize(self, request, data):   
          
        fund = request.GET.get('fund', False)  
        
        # W15 - Fund Summary
        if request.GET.get('summary', False):
        
            fees = FundFee.objects.filter(fund=fund).select_related('fee').only('fee__name', 'fee__formula')
            
            data['objects'] = []
            new_data = {}
            for fee in fees:
            
                if fee.fee.formula == None:
                    formula = 'n/a'
                else:
                    formula = fee.fee.formula
                    
                new_data = {
                    'name': fee.fee.name,
                    'formula': formula
                }
                new_obj = self.build_bundle(data = new_data)
                data['objects'].insert(0, new_obj)
                
        return super(FundFeeResource, self) \
                .alter_list_data_to_serialize(request, data)
                
                
class FundFeeAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundFeeAudit.objects.all()

"""
class FundPositionAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundPositionAudit.objects.all()
"""

class FundResource(MainBaseResource):
    benchpeer = fields.ForeignKey(BenchPeer, "benchpeer")
    
    class Meta(MainBaseResource.Meta):
        queryset = Fund.objects.all()
    

    def alter_detail_data_to_serialize(self, request, data):   
    
        # W15 - Fund Summary
        if request.GET.get('summary', False):
        
            try:
                first = FundReturnDaily.objects.filter(fund=data.data['id']) \
                    .only('value_date', 'nav').order_by('value_date')[0]
            except IndexError:
                try:
                    first = FundReturnMonthly.objects.filter(fund=data.data['id']) \
                        .only('value_date', 'nav').order_by('value_date')[0]
                except IndexError:
                    return
               
            try: 
                last = FundReturnDaily.objects.filter(fund=data.data['id']) \
                    .only('value_date', 'nav').order_by('-value_date')[0]
            except IndexError:
                last = FundReturnMonthly.objects.filter(fund=data.data['id']) \
                   .only('value_date', 'nav').order_by('-value_date')[0]
                
            flows = FundReturnMonthly.objects.aggregate(Sum('inflow'), Sum('outflow'))
            
            data.data['launch_date'] = first.value_date
            data.data['start_nav'] = first.nav
            data.data['end_nav'] = last.nav
            data.data['net_flow'] = flows['inflow__sum'] + flows['outflow__sum']
                
        return super(FundResource, self) \
                .alter_detail_data_to_serialize(request, data)
                

class FundPeerResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundPeer.objects.all()
        
class FundCharAuditResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundCharAudit.objects.all()


# Base class for both monthly and daily
class FundReturnResource(MainBaseResource):

    def alter_list_data_to_serialize(self, request, data):   
    
        def holding_data(holding):
            if date_type == 'monthly':
                h_data = HoldingMonthly.objects.filter(holding=holding).only('performance')
            else:
                h_data = HoldingDaily.objects.filter(holding=holding).only('performance')
            return [row.performance for row in h_data]
            
        def start_date():
            if date_type == 'monthly':
                first = FundReturnMonthly.objects.order_by('value_date').only('value_date')[0]
            else:
                first = FundReturnDaily.objects.order_by('value_date').only('value_date')[0]
            return first.value_date
            
        data_type = request.GET.get('data_type', 'graph')
        fund = request.GET.get('fund', False)    
        metric = request.GET.get('metric', False)  
        date_from = request.GET.get('value_date__gte', False)
        date_to = request.GET.get('value_date__lte', False)
        date_type = request.GET.get('date_type', False)  
        
        window = request.GET.get('window', False) 
        layer = request.GET.get('layer', False) 
        axis = request.GET.get('axis', False) 
        plot = request.GET.get('plot', False) 
        mar = request.GET.get('mar', False) 
        rfr = request.GET.get('rfr', False) 
        step = request.GET.get('step', False) 
        under = request.GET.get('under', False) 
        sec_under = request.GET.get('sec_under', False) 
        position = request.GET.get('position', False) 
        yaxis = request.GET.get('yaxis', False) 
        xaxis = request.GET.get('xaxis', False) 
        
        widget = request.GET.get("widget", False)
        
        
        if date_type == 'monthly':
            freq = 'm'
            factor = 12 #Annualisation Factor
        else:
            freq = 'WEEKDAY'
            factor = 252 #Annualisation Factor
        
        # W151 & W155 Two metric scatter plot
        if rfr is not False \
            and mar is not False \
            and under is not False \
            and sec_under is not False \
            and yaxis is not False \
            and xaxis is not False:
            
            date_from = start_date()
            
            unders = under.split(',')
            axis = [yaxis, xaxis]
            
            
            if sec_under == 'benchpeer':
                lst2 = [row.data['bench_perf'] for row in data['objects']]
                
            elif sec_under[:5] == 'metric': 
                lst2 = lst_vals[unders[i][6:]]
                
            elif sec_under.isdigit():
                lst2 = holding_data(unders[i])
                #color = 'peer'
             
            else:
                lst2 = [row.data['bench_perf'] for row in data['objects']]
                #color = 'blue'
                
                    
            # remove any empty strings in the list that might exist
            lst2 = filter(None, lst2)
            
            # save prior values for other underlying metrics
            try:
                lst_vals2[i] = lst2
            except:
                lst_vals2 = []
            
            dates2 = date_range(lst2, date_from, freq)
            df2 = to_dataframe(lst2, dates2)

            series = []
            
            for u in unders:
            
                if u == 'benchpeer':
                    lst = [row.data['bench_perf'] for row in data['objects']]
                    #color = 'green'
                    name = data['objects'][0].data['fund__benchpeer__name']
                    
                elif u[:5] == 'metric': 
                    lst = lst_vals[u[6:]]
                    #color = 'pink'
                    if m == "delta_cum_returns_final_val":
	                    name = "Excess Return"
                    if m == "tracking_error":
	                    name = "Tracking Error"                               
                    if m == "correlation":
	                    name = "Correlation"
                    if m == "alpha":
	                    name = "Alpha"
                    if m == "beta":
	                    name = "Beta"
                    if m == "r2":
	                    name = "RSQ"
                    if m == "mean":
	                    name = "Average"
                    if m == "standard_deviation":
	                    name = "Standard Deviation"
                    if m == "variance":
	                    name = "Variance"
                    if m == "max_drawdown":
	                    name = "Maximum DrawDown"
                    if m == "cum_returns_final":
	                    name = "Final Value Cumulative Return"
                    if m == "skewness":
	                    name = "Skewness"
                    if m == "kurtosis":
	                    name = "Kurtosis"
                    if m == "annualised_returns":
	                    name = "Annualised Return"
                    if m == "annualised_volatility":
	                    name = "Annualised Volatility"
                    if m == "downside_volatility":
	                    name = "Downside Volatility"
                    if m == "sortino_ratio":
	                    name = "Sortino Ratio"
                    if m == "sharpe_ratio":
	                    name = "Sharpe Ratio"
	                    
                elif u.isdigit():
                    lst = holding_data(u)
                    #color = 'peer'
                    name = 'fundpeer'
                
                else:
                    lst = [row.data['fund_perf'] for row in data['objects']]
                    color = 'blue'
                    name = 'fund'
                    
                # remove any empty strings in the list that might exist
                lst = filter(None, lst)
                
                # save prior values for other underlying metrics
                try:
                    lst_vals[i] = lst
                except:
                    lst_vals = []
                
                dates = date_range(lst, date_from, freq)
                df = to_dataframe(lst, dates)
                
                val = []
                
                
                for m in axis:    
                    
                    if m == "delta_cum_returns_final_val":
                        values = delta_cum_returns_final_val(df, df2, dates, dates2)[0]
                    if m == "tracking_error":
                        values = tracking_error(df, df2)
                    if m == "correlation":
                        values = correlation(df, df2)
                    if m == "alpha":
                        values = alpha(df, df2)
                    if m == "beta":
                        values = beta(df, df2)
                    if m == "r2":
                        values = r2(df, df2)
                    if m == "mean":
                        values = mean(df)
                    if m == "standard_deviation":
                        values = standard_deviation(df)
                    if m == "variance":
                        values = variance(df)
                    if m == "max_drawdown":
                        values = max_drawdown(df)
                    if m == "cum_returns_final":
                        values = cum_returns_final_val(df, dates)
                    if m == "skewness":
                        values = skewness(df)
                    if m == "kurtosis":
                        values = kurtosis(df)
                    if m == "annualised_returns":
                        values = annualised_returns(df, freq)
                    if m == "annualised_volatility":
                        values = volatility(df, freq)
                    if m == "downside_volatility":
                        values = downside_volatility(df, mar, freq)
                    if m == "sortino_ratio":
                        values = sortino_ratio(df, freq)
                    if m == "sharpe_ratio":
                        values = sharpe_ratio(df, freq)
                    
                    val.append(float(values[0]))
                #assert False
                    
                series.append({
                    'data': [val],
                    'name': name,
                    #'color': color,
                })
            return series    
            
        
        """
        W18 Fund Historical Stats
        """
        if metric is not False \
            and window is not False \
            and layer is not False \
            and axis is not False \
            and rfr is not False \
            and plot is not False \
            and mar is not False \
            and step is not False \
            and under is not False \
            and sec_under is not False \
            and position is not False:
            
            # look up the start date 
            date_from = start_date()
                
            
            metrics = metric.split(',')
            windows = window.split(',')
            layers = layer.split(',')
            axis = axis.split(',')
            plots = plot.split(',')
            mars = mar.split(',')
            steps = step.split(',')
            unders = under.split(',')
            sec_unders = sec_under.split(',')
            positions = position.split(',')

            series = []
            table = {}
            
            for i, u in enumerate(unders):
            
                if unders[i] == 'benchpeer':
                    lst = [row.data['bench_perf'] for row in data['objects']]
                    color = 'green'
                    
                elif unders[i][:5] == 'metric': 
                    lst = lst_vals[unders[i][6:]]
                    color = 'pink'
                    
                elif unders[i].isdigit():
                    lst = holding_data(unders[i])
                    color = 'peer'
                
                elif unders[i][:5] == 'flash': 
                
                    obj = Fund.objects.get(id=unders[i][5:])
                    #assert False
                
                else:
                    lst = [row.data['fund_perf'] for row in data['objects']]
                    color = 'blue'    
                    
                    
                if sec_unders[i] == 'benchpeer':
                    lst2 = [row.data['bench_perf'] for row in data['objects']]
                    
                elif sec_unders[i][:5] == 'metric': 
                    lst2 = lst_vals[sec_unders[i][6:]]
                    
                elif sec_unders[i].isdigit():
                    lst2 = holding_data(sec_unders[i])
                    #color = 'peer'
                 
                else:
                    lst2 = [row.data['fund_perf'] for row in data['objects']]
                    #color = 'blue'
                    
                    
                # remove any empty strings in the list that might exist
                lst = filter(None, lst)
                lst2 = filter(None, lst2)
                
                # save prior values for other underlying metrics
                try:
                    lst_vals[i] = lst
                except:
                    lst_vals = []
                
                try:
                    lst_vals2[i] = lst2
                except:
                    lst_vals2 = []
                
                dates = date_range(lst, date_from, freq)
                df = to_dataframe(lst, dates)
                dates2 = date_range(lst2, date_from, freq)
                df2 = to_dataframe(lst2, dates2)
                
                win = int(windows[i])
                step = int(steps[i])
                
                values = []

                if metrics[i] == "cumulative": 
                    values = cum_returns(df, dates)
                    name = "Cumulative Return"
                    label = '%'
                     
                if metrics[i] == "return":
                    values = df
                    name = "Returns"  
                    label = '%'
                        
                if metrics[i] == "roll_average":
                    values = roll_mean(df, win)
                    name = "Rolling Average"
                    label = '%'
                     
                if metrics[i] == "delta": 
                    values = delta_cum_returns(df, df2, dates, dates2)
                    name = "Delta Cumulative Return"
                    label = '%'
                    
                if metrics[i] == "roll_deviation":
                    values = roll_standard_deviation(df, win)
                    #values = roll_standard_deviation(df, win)[::12]
                    name = "Rolling Standard Deviation"
                    label = '%'
                    
                if metrics[i] == "roll_cumulative":
                    values = roll_cum_returns(df, win)
                    name = "Rolling Cumulative Return"                
                    label = '%'
                
                if metrics[i] == "roll_skewness":
                    values = roll_skewness (df, win)
                    name = "Rolling Skewness"
                    label = ''
                    
                    
                if metrics[i] == "roll_kurtosis":
                    values = roll_kurtosis (df, win)
                    name = "Rolling Kurtosis"
                    label = ''
                    
                if metrics[i] == "roll_annualised":
                    values = roll_annualised_returns(df, factor, win, LessThanWin=True)
                    name = "Rolling Annualised Return"
                    label = '%'
                    
                if metrics[i] == "roll_volatility":
                    values = roll_volatility(df, win, factor)
                    name = "Rolling Volatility"
                    label = '%'
                    
                if metrics[i] == "roll_sharpe": 
                    values = roll_sharpe_ratio(df, win, factor)
                    name = "Rolling Sharpe"
                    label = ''
                    
                if metrics[i] == "roll_sortino":
                    label = ''
                    raise "Not implemented"
                    
                if metrics[i] == "roll_downside":
                    label = ''
                    raise "Not implemented"
                
                if metrics[i] == "roll_excess": 
                    values = roll_delta_cum_returns (df, df2, win)
                    name = "Rolling Excess Return"
                    label = '%'

                if metrics[i] == "roll_tracking":
                    raise "Not implemented"

                if metrics[i] == "roll_correlation":
                    values = roll_correlation (df, df2, win)
                    name = "Rolling Correlation"
                    label = ''
                    
                if metrics[i] == "roll_alpha":
                    values = roll_alpha(df, df2, win)
                    name = "Rolling Alpha"
                    label = ''
                    

                if metrics[i] == "roll_beta":
                    values = roll_beta(df, df2, win)
                    name = "Rolling Beta"
                    label = ''
                    
                if metrics[i] == "roll_rsq":
                    raise "Not implemented"
                
                step_metrics = [
                    "roll_average", "roll_deviation", "roll_cumulative", "roll_skewness", 
                    "roll_kurtosis", "roll_annualised", "roll_volatility",  "roll_sharpe",  
                    "roll_sortino", "roll_downside", "roll_excess", "roll_tracking", "roll_correlation"   
                ]
                if metrics[i] in step_metrics:
                    values = values[::step]
                    
                if data_type == 'table':
                    list_values = to_list(values, False)
                    
                    for p, a in enumerate(list_values):
                        
                        try:
                            table[p]['date']
                        except:
                            table[p] = {}
                            
                        table[p]['date'] = a[0]
                        table[p]['metric_' + str(i + 1)] = a[1]
                        
                else:
                
                    values = to_list(values)
                
                    # create new previous dummy month
                    if isinstance(date_from, (str, unicode)):
                        date_from = datetime.strptime(date_from, '%Y-%m-%d')
                    new_date = datetime(date_from.year, date_from.month, 1) - timedelta(days=1)
                    new_date = datetime(new_date.year, new_date.month, 1)
                    values.insert(0, [
                        int(mktime(new_date.timetuple())) * 1000, 
                        0
                    ])
                    #assert False
                    
                    series.append({
                        'data': values,
                        'name': name,
                        'color': color,
                        'yAxis': i,
                        'xAxis': 0, #int(positions[i]) - 1,
                        'type': plots[i],
                        'zIndex': layers[i],
                        'label': label,
                    })
             
            if data_type == 'table':
                columns = ['metric_' + str(i + 1) for i, m in enumerate(metrics)]
                columns.insert(0, 'date')
                
                for i, dic in table.iteritems():
                    series.append(dic)   
                    
                return {
                    'rows': series,
                    'columns': super(FundReturnResource, self).set_columns(request, columns)
                }
                
            else:
                peer_colors = ['orange', 'red', 'brown', 'purple', 'yellow']
                for i, row in enumerate(series):
                    if row['color'] == 'peer':
                        row['color'] = peer_colors[randint(0, len(peer_colors) - 1)]
                        
                return series
        
    
        # Histogram
        if request.GET.get('histogram', False):
        
            lst = [row.data['fund_perf'] for row in data['objects']]
            
            if not date_from:
                date_from = start_date()
            
            dates = date_range(lst, date_from, freq)
            df = to_dataframe(lst, dates)
            
            #change to hist
            if lst:
                hist = histogram(df)
            else:
                hist = np.histogram(lst, bins=18, range=(-10,8), density=False)
            
            #assert False
            values = [int(row) for row in hist[0]]
            keys = [row for row in hist[1]]
                
            data = {
                'data': values,
                'columns': keys,
            }
            
            return data
            
            
        # W16 - cumulative return
        y1 = request.GET.get('y1', False)

        if y1 != False:

            name = data['objects'][0].data['fund__name']
            
            # create new previous dummy month
            first_date = data['objects'][0].data['value_date']
            new_date = datetime(first_date.year, first_date.month, 1) - timedelta(days=1)
            new_date = datetime(new_date.year, new_date.month, 1)
            
            new_data = {
                'fund_perf': decimal.Decimal('0'), 
                'value_date': new_date, 
                'bench_perf': decimal.Decimal('0')
            }
            new_obj = self.build_bundle(data = new_data)
            data['objects'].insert(0, new_obj)
            
            data = cumulative_return(data, perf_type = 'fund')
            data = cumulative_return(data, perf_type = 'bench')
            
            
            # delta
            if request.GET.get("graph_type", False) == 'bench' and widget == 'w16':
                for id, row in enumerate(data['objects']):
                    data['objects'][id].data['fund_perf'] = row.data['fund_perf'] - row.data['bench_perf']
                 
        # W152   
        # @TODO: this does not work with specified fields. 
        if widget == 'w152':
        
            try:
                name = data['objects'][0].data['fund__name']
            except:
                name = 'n/a'

            first = FundReturnMonthly.objects.order_by('value_date')[0]
            
            lst = [row.data['fund_perf'] for row in data['objects']]
            dates1 = date_range(lst, first.value_date)
            df1 = to_dataframe(lst, dates1)
            cum1 = cum_returns(df1, dates1)
            
            
            lst = [row.data['bench_perf'] for row in data['objects']]
            dates = date_range(lst, first.value_date)
            df = to_dataframe(lst, dates)
            cum2 = cum_returns(df, dates)
            delta1 = delta_cum_returns(df1, df, dates1, dates)
            
            lst = [row.data['sec_bench'] for row in data['objects']]
            dates = date_range(lst, first.value_date)
            df = to_dataframe(lst, dates)
            cum3 = cum_returns(df, dates)
            delta2 = delta_cum_returns(df1, df, dates1, dates)
            
            return [{
                'name': name,
                'data': to_list(cum1),
                'xAxis': 0,
                'yAxis': 0,
            },{
                'data': to_list(cum2),
                'name': 'Benchmark',
                'xAxis': 0,
                'yAxis': 0,
            },{
                'data': to_list(cum3),
                'name': 'Secondary Benchmark',
                'xAxis': 0,
                'yAxis': 0,
            },{
                'data': to_list(delta1),
                'name': 'Fund vs Benchmark',
                'xAxis': 0,
                'yAxis': 1,
            },{
                'data': to_list(delta2),
                'name': 'Fund vs Secondary Benchmark',
                'xAxis': 0,
                'yAxis': 1,
            }]

        return super(FundReturnResource, self) \
                .alter_list_data_to_serialize(request, data)

class FundReturnDailyResource(FundReturnResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnDaily.objects.all()
        
    def alter_detail_data_to_serialize(self, request, data): 
        if request.GET.get('has_data', False):
            return FundReturnDaily.objects.filter(fund=data.data['id']).count()
        
        return super(FundReturnDailyResource, self) \
                .alter_detail_data_to_serialize(request, data)        

class FundReturnDailyResource2(FundReturnResource):
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnDaily.objects.all()

class FundReturnMonthlyResource(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()
        ordering = ['value_date']


class FundReturnMonthlyResource2(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()


class FundReturnMonthlyResource3(FundReturnResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    class Meta(MainBaseResource.Meta):
        queryset = FundReturnMonthly.objects.all()

class HoldingResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Holding.objects.all()

class HoldingDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingDaily.objects.all()

class HoldingMonthlyResource(MainBaseResource):
    holding = fields.ForeignKey(HoldingResource, 'holding')
    class Meta(MainBaseResource.Meta):
        queryset = HoldingMonthly.objects.all()

class HoldingDepositResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingDeposit.objects.all()

class HoldingEtfResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingEtf.objects.all()

class HoldingEquityResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingEquity.objects.all()

class HoldingFixedIncomeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingFixedIncome.objects.all()

class HoldingForwardResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingForward.objects.all()

class HoldingFutureResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingFuture.objects.all()

class HoldingHedgeFundsResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingHedgeFund.objects.all()

class HoldingMutualFundResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingMutualFund.objects.all()

class HoldingOptionResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingOption.objects.all()

class HoldingWarrantResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingWarrant.objects.all()

class HoldingPositionDailyResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = HoldingPositionDaily.objects.all()

class PositionMonthlyResource(MainBaseResource):
    fund = fields.ForeignKey(FundResource, 'fund')
    
    class Meta(MainBaseResource.Meta):
        queryset = PositionMonthly.objects.all()
        ordering = ['weight']


    def alter_list_data_to_serialize(self, request, data):  
    
    
        fund = request.GET.get('fund', False)
        year = request.GET.get('value_date__year', False)
        month = request.GET.get('value_date__month', False)
        performance = request.GET.get('performance', False) 
        
        # W2 - Holding Performance Bar & W7 Holding NAV
        # Get performance from HoldingMonthly (only utilized in W2)
        # and the weight of the prior month to calculate the average weight
        if performance and year and month and fund:
        
            hm = HoldingMonthly.objects.filter(
                value_date__year=year, value_date__month=month). \
                select_related('holding').only('holding__name', 'performance')
                
            if int(month) == 1:
                prior_year = int(year) - 1
                prior_month = 12
            else:
                prior_year = year
                prior_month = int(month) - 1
                
            prior_pos = PositionMonthly.objects.filter(
                value_date__year=prior_year, value_date__month=prior_month,
                fund=fund). \
                select_related('holding').only('holding__name', 'weight')
                
            pos = data['objects']
            data['objects'] = [] # delete old data
            new_data = {}
            
            # set the average weight for the current month
            for i, p in enumerate(pos):
                for h in hm:
                    if p.data['holding__name'] == h.holding.name:
                        
                        name = h.holding.name
                        
                        average_weight = p.data['weight']
                            
                        if average_weight >= 0:
                        
                            new_data[name] = {
                                'weighted_perf': (p.data['weight'] * h.performance) / 100,
                                'average_weight': (average_weight) / 100, 
                                'performance': h.performance,
                                'holding__name': p.data['holding__name'],
                            }
                            
            # update the average weight for prior months (if exists)
            for i, p in enumerate(pos):
                for pp in prior_pos:
                    for h in hm:
                        if p.data['holding__name'] == h.holding.name and pp.holding.name == h.holding.name:
                        
                            name = h.holding.name
                            
                            if pp.weight > 0:
                                average_weight = (p.data['weight'] + pp.weight) / 2 / 100
                        
                                new_data[name]['average_weight'] = average_weight
                                
            # convert dictionary to a list of dictionaries
            sorted_data = []
            for i, new in new_data.iteritems():
                sorted_data.append(new)
             
            # sort by average weight
            new_data = sorted(sorted_data, key=itemgetter('average_weight')) 
            
            # insert new data
            for new in new_data:
                new_obj = self.build_bundle(data = new)
                data['objects'].insert(0, new_obj)
        
        return super(PositionMonthlyResource, self) \
                .alter_list_data_to_serialize(request, data)

class TradeResource(MainBaseResource):
    class Meta(MainBaseResource.Meta):
        queryset = Trade.objects.all()

