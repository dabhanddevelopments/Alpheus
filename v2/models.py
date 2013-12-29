from __future__ import unicode_literals
from django.db import models

class Administrator(models.Model):
    id = models.AutoField(primary_key=True, db_column='AdministratorID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    #contact_name = models.CharField(max_length=200, db_column='ContactName', blank=True, null=True)
    #contact_number = models.CharField(max_length=200, db_column='ContactNumber', blank=True, null=True)
    #address_1 = models.CharField(max_length=200, db_column='AddressLine1', blank=True, null=True)
    #address_2 = models.CharField(max_length=200, db_column='AddressLine2', blank=True, null=True)
    #address_3 = models.CharField(max_length=200, db_column='AddressLine3', blank=True, null=True)
    #address_4 = models.CharField(max_length=200, db_column='AddressLine4', blank=True, null=True)
    #address_5 = models.CharField(max_length=200, db_column='AddressLine5', blank=True, null=True)
    #postcode = models.CharField(max_length=200, db_column='PostCode', blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_App_Administrators'

    def __unicode__(self):
        return self.name

#class AlarmType(models.Model):
#    id = models.AutoField(primary_key=True, db_column='AlarmTypeID')
#    name = models.CharField(max_length=200, db_column='Name', blank=True)
#    class Meta:
#        db_table = 'ALP_App_AlarmTypes'


#@TODO: Table missing PK
class Alarm(models.Model):
    id = models.AutoField(primary_key=True, db_column='AlarmID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    #alarm_type = models.ForeignKey(AlarmType, blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_App_Alarms'

    def __unicode__(self):
        return self.name

class AlpheusGroup(models.Model):
    id = models.AutoField(primary_key=True, db_column='AlpheusGroupID')
    name = models.CharField(max_length=50, db_column='Name', blank=True)
    short_name = models.CharField(max_length=50, db_column='ShortName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_AlpheusGroups'

    def __unicode__(self):
        return self.name

class InvestmentCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column='InvestmentCategoryID')
    name = models.CharField(max_length=200, db_column='Name')
    description = models.CharField(max_length=200, db_column='Description', blank=True, null=True)
    
    #sn = models.CharField(max_length=10, db_column='SN')
    class Meta:
        db_table = 'ALP_App_InvestmentCategory'

    def __unicode__(self):
        return self.name

class AssetClassRisk(models.Model):
    id = models.AutoField(primary_key=True, db_column='AssetClassRiskID')
    name = models.CharField(max_length=200, db_column='Name')
    description = models.CharField(max_length=200, db_column='Description', blank=True, null=True)
    #sn = models.CharField(max_length=10, db_column='SN')
    
    class Meta:
        db_table = 'ALP_App_AssetClassRisk'

    def __unicode__(self):
        return self.name

class AssetType(models.Model):
    id = models.AutoField(primary_key=True, db_column='AssetTypeID')
    name = models.CharField(max_length=200, db_column='Name')
    description = models.CharField(max_length=200, db_column='Description', blank=True, null=True)
    #sn = models.CharField(max_length=10, db_column='SN')
    
    class Meta:
        db_table = 'ALP_App_AssetType'

    def __unicode__(self):
        return self.name
        
        
class AssetClass(models.Model):
    HOLDING_TYPES = (
        ('CASH', 'Cash'),
    )
    id = models.AutoField(primary_key=True, db_column='AssetClassID')
    investment_category = models.ForeignKey(InvestmentCategory)
    asset_type = models.ForeignKey(AssetType)
    asset_class_risk = models.ForeignKey(AssetClassRisk)
    holding_type = models.CharField(max_length=5, choices=HOLDING_TYPES)
    
    class Meta:
        db_table = 'ALP_App_AssetClass'
        verbose_name_plural = "Asset Classes"


class Auditor(models.Model):
    id = models.AutoField(primary_key=True, db_column='AuditorID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    #contact_name = models.CharField(max_length=200, db_column='ContactName', blank=True, null=True)
    #contact_number = models.CharField(max_length=200, db_column='ContactNumber', blank=True, null=True)
    #address_1 = models.CharField(max_length=200, db_column='AddressLine1', blank=True, null=True)
    #address_2 = models.CharField(max_length=200, db_column='AddressLine2', blank=True, null=True)
    #address_3 = models.CharField(max_length=200, db_column='AddressLine3', blank=True, null=True)
    #address_4 = models.CharField(max_length=200, db_column='AddressLine4', blank=True, null=True)
    #address_5 = models.CharField(max_length=200, db_column='AddressLine5', blank=True, null=True)
    #postcode = models.CharField(max_length=200, db_column='PostCode', blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_App_Auditors'

    def __unicode__(self):
        return self.name
        
        
#@TODO: Table missing PK
class Currency(models.Model):
    id = models.AutoField(primary_key=True, db_column='CurrencyID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    short_name = models.CharField(max_length=3, db_column='ShortName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_Currencies'
        verbose_name_plural = "Currencies"

    def __unicode__(self):
        return self.name
        

class BenchPeer(models.Model):
    id = models.AutoField(primary_key=True, db_column='CompositeID')
    holding = models.ForeignKey('Holding')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    currency_rate = models.ForeignKey('CurrencyRate', related_name='benchpeer_currencyrate', null=True, db_column='CurrencyRateID', blank=True)
    type = models.CharField(max_length=1, db_column='Type')
    description = models.CharField(max_length=200, db_column='Description', blank=True, null=True)
    formula = models.CharField(max_length=200, db_column='Formula', blank=True)

    class Meta:
        db_table = 'ALP_App_BenchPeers'

    def __unicode__(self):
        return self.name
        

#@TODO: this table is missing FKs on table
#@TODO: Table missing PK
class BenchComponent(models.Model):
    id = models.AutoField(primary_key=True, db_column='BenchComponentID')
    bench_peer = models.ForeignKey(BenchPeer)
    holding = models.ForeignKey('Holding')
    currency = models.ForeignKey(Currency)
    weight = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Weight', blank=True)
    start_date = models.DateTimeField()
    
    class Meta:
        db_table = 'ALP_App_BenchComponents'


class Broker(models.Model):
    id = models.AutoField(primary_key=True, db_column='BrokedID') #@TODO: Should this column not be named BrokerID?
    name = models.CharField(max_length=100, db_column='Name', blank=True)
    short_name = models.CharField(max_length=50, db_column='ShortName', blank=True)
    class Meta:
        db_table = 'ALP_App_Brokers'
 
    def __unicode__(self):
        return self.name       

class CounterParty(models.Model):
    id = models.AutoField(primary_key=True, db_column='CounterpartyID')
    name = models.CharField(max_length=100, db_column='Name', blank=True)
    short_name = models.CharField(max_length=50, db_column='ShortName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_Counterparties'
        verbose_name_plural = "Counter Parties"

    def __unicode__(self):
        return self.name

class Country(models.Model):
    id = models.AutoField(primary_key=True, db_column='CountryID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    short_name = models.CharField(max_length=20, db_column='ShortName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_Countries'
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

        
class CurrencyRate(models.Model):
    holding = models.ForeignKey('Holding', db_column='HoldingID')
    currency_from = models.IntegerField(null=True, db_column='CurrencyFrom', blank=True)
    currency_to = models.IntegerField(null=True, db_column='CurrencyTo', blank=True)
    
    class Meta:
        db_table = 'ALP_App_CurrencyRates'


class Custodian(models.Model):
    id = models.AutoField(primary_key=True, db_column='CustodianID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    #contact_name = models.CharField(max_length=200, db_column='ContactName', blank=True, null=True)
    #contact_number = models.CharField(max_length=200, db_column='ContactNumber', blank=True, null=True)
    #address_1 = models.CharField(max_length=200, db_column='AddressLine1', blank=True, null=True)
    #address_2 = models.CharField(max_length=200, db_column='AddressLine2', blank=True, null=True)
    #address_3 = models.CharField(max_length=200, db_column='AddressLine3', blank=True, null=True)
    #address_4 = models.CharField(max_length=200, db_column='AddressLine4', blank=True, null=True)
    #address_5 = models.CharField(max_length=200, db_column='AddressLine5', blank=True, null=True)
    #postcode = models.CharField(max_length=200, db_column='PostCode', blank=True, null=True)

    class Meta:
        db_table = 'ALP_App_Custodians'

    def __unicode__(self):
        return self.name

#@TODO: Table does not exist
#class CategoryFee(models.Model):
#    FEE_TYPE = (
#        ('inc', 'Income'),
#        ('exp', 'Expense'),
#    )
#    id = models.AutoField(primary_key=True, db_column='FeeCategoryID')
#    fee_type = models.CharField(max_length=3, db_column='FeeType', choices=FEE_TYPE)
#    name = models.CharField(max_length=200, db_column='Name', blank=True)
#    short_name = models.CharField(max_length=20, db_column='ShortName', blank=True)

#    class Meta:
#        db_table = 'ALP_App_FeeCategory'
#


#@TODO: Table does not exist
#class SubCategoryFee(models.Model):
#    id = models.AutoField(primary_key=True, db_column='FeeSubCategoryID')
#    category_fee = models.ForeignKey(CategoryFee)
#    name = models.CharField(max_length=200, db_column='Name', blank=True)
#    short_name = models.CharField(max_length=20, db_column='ShortName', blank=True)

#    class Meta:
#        db_table = 'ALP_App_FeeSubCategory'



class Fee(models.Model):
    id = models.AutoField(primary_key=True, db_column='FeeID')
    #subcategory_fee = models.ForeignKey(SubCategoryFee, db_column='FeeSubCategoryID', blank=True, null=True)
    #custodian = models.ForeignKey(Custodian, db_column='CustodianID', blank=True, null=True)
    #admin = models.ForeignKey(Administrator, db_column='AdministratorID', blank=True, null=True)
    #manager = models.ForeignKey('Manager', db_column='ManagerID', blank=True, null=True)
    #auditor = models.ForeignKey(Auditor, db_column='AuditorID', blank=True, null=True)
    #broker = models.ForeignKey(Broker, db_column='BrokedID', blank=True, null=True)
    #counterparty = models.ForeignKey(CounterParty, db_column='CounterpartyID', blank=True, null=True)
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    fee_type = models.CharField(max_length=200, db_column='Type', blank=True)
    parameter_1 = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='Parameter1', blank=True)
    parameter_2 = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='Parameter2', blank=True)
    parameter_3 = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='Parameter3', blank=True)
    formula = models.CharField(max_length=200, db_column='Formula', blank=True)
    #custodian_identifier = models.CharField(max_length=50, db_column='CustodianIdentifier', blank=True, null=True)
    #administrator_identifier = models.CharField(max_length=50, db_column='AdministratorIdentifier', blank=True, null=True)
    #manager_identifier = models.CharField(max_length=50, db_column='ManagerIdentifier', blank=True, null=True)
    #auditor_identifier = models.CharField(max_length=50, db_column='AuditorIdentifier', blank=True, null=True)
    #broker_identifier = models.CharField(max_length=50, db_column='BrokerIdentifier', blank=True, null=True)
    #counterparty_identifier = models.CharField(max_length=50, db_column='CounterpartyIdentifier', blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_App_Fees'
        verbose_name_plural = "Fees"

    def __unicode__(self):
        return self.name

class FundStyle(models.Model):
    id = models.AutoField(primary_key=True, db_column='StyleID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    
    class Meta:
        db_table = 'ALP_App_FundStyles'

    def __unicode__(self):
        return self.name

class GicsCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column='GICSCategoryID')
    name = models.CharField(max_length=500, db_column='Name', blank=True)
    gics_subindustry_code = models.CharField(max_length=20, db_column='GICSSubIndustryCode', blank=True)
    sub_industry_name = models.CharField(max_length=100, db_column='SubIndustryName', blank=True)
    gics_industry_code = models.CharField(max_length=20, db_column='GICSIndustryCode', blank=True)
    industry_name = models.CharField(max_length=100, db_column='IndustryName', blank=True)
    gics_industry_group_code = models.CharField(max_length=20, db_column='GICSIndustryGroupCode', blank=True)
    industry_group_name = models.CharField(max_length=100, db_column='IndustryGroupName', blank=True)
    gics_sector_code = models.CharField(max_length=20, db_column='GICSSectorCode', blank=True)
    sector_name = models.CharField(max_length=100, db_column='SectorName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_GICSCategory'
        verbose_name = 'GICS Category'
        verbose_name_plural = 'GICS Categories'

    def __unicode__(self):
        return self.name

class Hf(models.Model):
    id = models.AutoField(primary_key=True, db_column='HFID')
    hf_sector = models.ForeignKey('HfSector', null=True, db_column='HFSectorID', blank=True)
    hf_strategy = models.ForeignKey('HfStrategy', null=True, db_column='HFStrategyID', blank=True)
    hf_risk = models.ForeignKey('HfRisk', null=True, db_column='HFRiskID', blank=True)
    
    class Meta:
        db_table = 'ALP_App_HF'


class HfRisk(models.Model):
    id = models.AutoField(primary_key=True, db_column='HFRiskID')
    description = models.CharField(max_length=200, db_column='Description', blank=True)
    
    class Meta:
        db_table = 'ALP_App_HFRisk'
        
        
class HfSector(models.Model):
    id = models.AutoField(primary_key=True, db_column='HFSectorID')
    hf_sector = models.CharField(max_length=50, db_column='HFSector', blank=True)
    hf_strategy = models.CharField(max_length=50, db_column='HFStrategy', blank=True)
    hf_risk = models.CharField(max_length=50, db_column='HFRisk', blank=True)
    
    class Meta:
        db_table = 'ALP_App_HFSector'
        verbose_name = 'HF sector'
        verbose_name_plural = 'HF Sectors'
        
        
class HfStrategy(models.Model):
    id = models.AutoField(primary_key=True, db_column='HFStrategyID')
    description = models.CharField(max_length=200, db_column='Description', blank=True)
    
    class Meta:
        db_table = 'ALP_App_HFStrategy'


class IcbCategory(models.Model):
    id = models.AutoField(primary_key=True, db_column='ICBCategoryID')
    name = models.CharField(max_length=500, db_column='Name', blank=True)
    icb_subsector_code = models.CharField(max_length=20, db_column='ICBSubSectorCode', blank=True)
    subsector_name = models.CharField(max_length=100, db_column='SubSectorName', blank=True)
    icb_sector_code = models.CharField(max_length=20, db_column='ICBSectorCode')
    sector_name = models.CharField(max_length=100, db_column='SectorName', blank=True)
    icb_super_sector_code = models.CharField(max_length=20, db_column='ICBSuperSectorCode')
    super_sectorn_ame = models.CharField(max_length=100, db_column='SuperSectorName', blank=True)
    icb_industry_code = models.CharField(max_length=20, db_column='ICBIndustryCode')
    industry_name = models.CharField(max_length=100, db_column='IndustryName', blank=True)
    
    class Meta:
        db_table = 'ALP_App_ICBCategory'
        verbose_name_plural = 'Icb Categories'
 
    def __unicode__(self):
        return self.name       

class IndustryGroup(models.Model):
    id = models.AutoField(primary_key=True, db_column='IndustryGroupID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    class Meta:
        db_table = 'ALP_App_IndustryGroup'

class IndustrySector(models.Model):
    id = models.AutoField(primary_key=True, db_column='IndustrySectorID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    
    class Meta:
        db_table = 'ALP_App_IndustrySector'

    def __unicode__(self):
        return self.name      

class IndustrySubGroup(models.Model):
    id = models.AutoField(primary_key=True, db_column='IndustrySubgroupID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    
    class Meta:
        db_table = 'ALP_App_IndustrySubgroup'

    def __unicode__(self):
        return self.name

class IssuerIndustry(models.Model):
    id = models.AutoField(primary_key=True, db_column='IssuerIndustryID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    
    class Meta:
        db_table = 'ALP_App_IssuerIndustry'

    def __unicode__(self):
        return self.name

class Manager(models.Model):
    id = models.AutoField(primary_key=True, db_column='ManagerID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    #contact_name = models.CharField(max_length=200, db_column='ContactName', blank=True, null=True)
    #contact_number = models.CharField(max_length=200, db_column='ContactNumber', blank=True, null=True)
    #address_1 = models.CharField(max_length=200, db_column='AddressLine1', blank=True, null=True)
    #address_2 = models.CharField(max_length=200, db_column='AddressLine2', blank=True, null=True)
    #address_3 = models.CharField(max_length=200, db_column='AddressLine3', blank=True, null=True)
    #address_4 = models.CharField(max_length=200, db_column='AddressLine4', blank=True, null=True)
    #address_5 = models.CharField(max_length=200, db_column='AddressLine5', blank=True, null=True)
    #postcode = models.CharField(max_length=200, db_column='PostCode', blank=True, null=True)

    class Meta:
        db_table = 'ALP_App_Managers'

    def __unicode__(self):
        return self.name

class Region(models.Model):
    #@TODO: need list of actual region types
    REGION_TYPE = (
        ('US', 'US'),
        ('EURO', 'Euro'),
    )
    id = models.AutoField(primary_key=True, db_column='RegionID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    short_name = models.CharField(max_length=20, db_column='ShortName', blank=True)
    region_type = models.CharField(max_length=5, db_column='RegionType', choices=REGION_TYPE)

    class Meta:
        db_table = 'ALP_App_Regions'

    def __unicode__(self):
        return self.name

#@TODO: Table missing PK
class ClientFilename(models.Model):
    #id = models.AutoField(primary_key=True, db_column='ClientFilenameID')
    client = models.ForeignKey('Client', db_column='ClientID')
    fund = models.ForeignKey('Fund', db_column='FundID')
    filename = models.CharField(max_length=50, db_column='FileName', blank=True, null=True)
    #file_identifier = models.CharField(max_length=50, db_column='FileIdentifier', blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_ClientFileNames'

    def __unicode__(self):
        return self.filename

#@TODO: Table missing PK
class ClientPositionAudit(models.Model):
    #id = models.AutoField(primary_key=True, db_column='ClientPositions_TSID')
    #custodian = models.ForeignKey(Custodian, blank=True, null=True)
    client = models.ForeignKey('Client', db_column='ClientID')
    value_date = models.DateTimeField(db_column='value_date')
    fund = models.ForeignKey('Fund', db_column='FundID')
    holding = models.ForeignKey('Holding', db_column='HoldingID')
    size = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Size', blank=True)
    market_value = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValue', blank=True)
    avg_cost_price = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='AvgCostPrice', blank=True)
    holding_return = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='HoldingReturn', blank=True)
    #weight = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_ClientPositions_TS'


class Client(models.Model):
    id = models.AutoField(primary_key=True, db_column='ClientID')
    name = models.CharField(max_length=50, db_column='Name', blank=True)
    #custodian = models.ForeignKey(Custodian, blank=True)
    #first_name = models.CharField(max_length=50, db_column='FirstName', blank=True)
    #last_name = models.CharField(max_length=50, db_column='LastName', blank=True)
    cs_account = models.CharField(max_length=50, db_column='CSAccount', blank=True)
    hsbc_account = models.CharField(max_length=50, db_column='HSBCAccount', blank=True)
    internal_id = models.IntegerField(null=True, db_column='InternalID', blank=True)
    #account_number = models.CharField(max_length=50, db_column='AccountNumber')
    
    class Meta:
        db_table = 'ALP_Clients'

    def __unicode__(self):
        return self.name

#@TODO: Table have IntegerFields instead of FKs
class ClientTransaction(models.Model):
    id = models.AutoField(primary_key=True, db_column='TransactionID')
    client = models.ForeignKey(Client, db_column='ClientID')
    value_date = models.DateTimeField(db_column='ValueDate')
    fund = models.ForeignKey('Fund', null=True, db_column='FundID', blank=True)
    holding = models.IntegerField(null=True, db_column='HoldingID', blank=True)
    confirm_flag = models.CharField(max_length=1, db_column='ConfirmFlag')
    buy_sell = models.CharField(max_length=1, db_column='BuySell')
    dealing_date = models.DateTimeField(db_column='DealingDate', null=True, blank=True)
    shares = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Shares', blank=True)
    nav_per_share = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='NAVPerShare', blank=True)
    nav = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='NAV', blank=True)
    fxrate = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FXRate', blank=True)
    amount_requested = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='AmountRequested', blank=True)
    #trade_date = models.DateTimeField(db_column='TradeDate', null=True, blank=True)
    #settlement_date = models.DateTimeField(db_column='SettlementDate',null=True, blank=True)

    class Meta:
        db_table = 'ALP_ClientsTransactions'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class ClientValAudit(models.Model):
    client = models.ForeignKey(Client, db_column='ClientID')
    value_date = models.DateTimeField(db_column='value_date')
    #fund = models.ForeignKey('Fund', db_column='FundID')
    #holding = models.IntegerField(db_column='HoldingID')
    nav = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='NAV', blank=True)
    inflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Inflows', blank=True)
    outflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Outflows', blank=True)
    client_return = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='ClientReturn', blank=True)
    
    class Meta:
        db_table = 'ALP_ClientsVals_TS'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundFee(models.Model):
    fund = models.ForeignKey('Fund', db_column='FundID')
    fee = models.ForeignKey(Fee, db_column='FeeID')
    start_date = models.DateTimeField(db_column='StartDate')
    end_date = models.DateTimeField(null=True, db_column='EndDate', blank=True)
    
    class Meta:
        db_table = 'ALP_FundFees'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundFeeAudit(models.Model):
    fund = models.ForeignKey('Fund', db_column='FundID')
    fee = models.ForeignKey(Fee, db_column='FeeID')
    value_date = models.DateTimeField(db_column='value_date')
    amount = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Amount', blank=True)
    
    class Meta:
        db_table = 'ALP_FundFees_TS'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundPeer(models.Model):
    user = models.IntegerField(db_column='UserID')
    fund = models.ForeignKey('Fund', db_column='FundID')
    benchpeer = models.ForeignKey(BenchPeer, db_column='BenchPeerID')
    
    class Meta:
        db_table = 'ALP_FundPeers'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundPositionAudit(models.Model):
    fund = models.ForeignKey('Fund', db_column='FundID')
    holding = models.ForeignKey('Holding', db_column='HoldingID')
    value_date = models.DateTimeField(db_column='value_date')
    size = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Size', blank=True)
    marketprice_lcl = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceLcl', blank=True)
    marketprice_fundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceFundCur', blank=True)
    marketvalue_lcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueLcl', blank=True)
    marketvalue_fundcur = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueFundCur', blank=True)
    costprice_lcl = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceLcl', blank=True)
    costprice_fundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceFundCur', blank=True)
    marketcost_lcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostLcl', blank=True)
    marketcost_fundcur = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostFundCur', blank=True)
    
    class Meta:
        db_table = 'ALP_FundPositions_TS'


#@TODO: Table has self referencing association to itself instead of PK
class Fund(models.Model):
    id = models.AutoField(primary_key=True, db_column='FundID')
    name = models.CharField(max_length=50, db_column='Name', blank=True)
    description = models.CharField(max_length=200, db_column='Description', blank=True)
    alpheusgroupid0 = models.ForeignKey(AlpheusGroup, null=True, db_column='AlpheusGroupID0', blank=True)
    currency = models.ForeignKey(Currency, related_name='fund_currency', null=True, db_column='CurrencyID', blank=True)
    assetclass = models.ForeignKey(AssetClass, null=True, db_column='AssetClassID', blank=True)
    countryi = models.ForeignKey(Country, related_name='country_i', null=True, db_column='CountryIID', blank=True)
    countryr = models.IntegerField(null=True, db_column='CountryRID', blank=True)
    region1 = models.ForeignKey(Region, related_name='fund_region1', null=True, db_column='Region1ID', blank=True)
    region2 = models.ForeignKey(Region, related_name='fund_region2', null=True, db_column='Region2ID', blank=True)
    region3 = models.ForeignKey(Region, related_name='fund_region3', null=True, db_column='Region3ID', blank=True)
    benchpeer = models.ForeignKey(BenchPeer, null=True, db_column='BenchPeerID', blank=True)
    admin = models.ForeignKey(Administrator, null=True, db_column='AdminID', blank=True)
    manager = models.ForeignKey(Manager, null=True, db_column='ManagerID', blank=True)
    custodian = models.ForeignKey(Custodian, null=True, db_column='CustodianID', blank=True)
    auditor = models.ForeignKey(Auditor, null=True, db_column='AuditorID', blank=True)
    alarm = models.ForeignKey(Alarm, null=True, db_column='AlarmID', blank=True)
    active = models.CharField(max_length=1, db_column='Active', blank=True)
    
    class Meta:
        db_table = 'ALP_Funds'

    def __unicode__(self):
        return self.name


#@TODO: Table missing PK
class FundCharAudit(models.Model):
    fund = models.ForeignKey(Fund, db_column='FundID')
    start_date = models.DateTimeField(db_column='StartDate')
    end_date = models.DateTimeField(null=True, db_column='EndDate', blank=True)
    currency = models.ForeignKey(Currency, related_name='fund_char_currency', null=True, db_column='CurrencyID', blank=True)
    assetclass = models.ForeignKey(AssetClass, null=True, db_column='AssetClassID', blank=True)
    countryi = models.ForeignKey(Country, related_name='country_char_i', null=True, db_column='CountryIID', blank=True)
    countryr = models.ForeignKey(Country, related_name='country_char_r', null=True, db_column='CountryRID', blank=True)
    region1 = models.ForeignKey(Region, related_name='fund_char_region1', null=True, db_column='Region1ID', blank=True)
    region2 = models.ForeignKey(Region, related_name='fund_char_region2', null=True, db_column='Region2ID', blank=True)
    region3 = models.ForeignKey(Region, related_name='fund_char_region3', null=True, db_column='Region3ID', blank=True)
    benchpeer = models.ForeignKey(BenchPeer, null=True, db_column='BenchPeerID', blank=True)
    admin = models.ForeignKey(Administrator, null=True, db_column='AdminID', blank=True)
    manager = models.ForeignKey(Manager, null=True, db_column='ManagerID', blank=True)
    custodian = models.ForeignKey(Custodian, null=True, db_column='CustodianID', blank=True)
    auditor = models.ForeignKey(Auditor, null=True, db_column='AuditorID', blank=True)
    alarm = models.ForeignKey(Alarm, null=True, db_column='AlarmID', blank=True)
    active = models.CharField(max_length=1, db_column='Active', blank=True)
    
    class Meta:
        db_table = 'ALP_FundsChars_TS'


#@TODO: Table missing PK
class FundReturnDaily(models.Model):
    fund = models.IntegerField(db_column='FundID')
    value_date = models.DateTimeField(db_column='ValueDate')
    nav = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='NAV', blank=True)
    shares = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Shares', blank=True)
    nav_per_share = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='NAVPerShare', blank=True)
    inflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Inflows', blank=True)
    outflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Outflows', blank=True)
    fund_perf = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FundDailyReturn', blank=True)
    fund_mtd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FundMTDReturn', blank=True)
    ytd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FundYTDReturn', blank=True)
    bench_perf = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='BenchDailyReturn', blank=True)
    bench_mtd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='BenchMTDReturn', blank=True)
    bench_ytd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='BenchYTDReturn', blank=True)
    flag = models.CharField(max_length=1, db_column='Flag', blank=True, null=True)
    
    class Meta:
        db_table = 'ALP_FundsDailyVals_TS'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundEstimate(models.Model):
    fund = models.ForeignKey(Fund, db_column='FundID')
    value_date = models.DateTimeField(db_column='value_date')
    manager = models.ForeignKey(Manager, null=True, db_column='ManagerID', blank=True)
    estimate = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Estimate', blank=True)
    
    class Meta:
        db_table = 'ALP_FundsEstimates'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class FundReturnMonthly(models.Model):
    fund = models.ForeignKey(Fund, db_column='FundID')
    value_date = models.DateTimeField(db_column='value_date')
    nav = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='NAV', blank=True)
    shares = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Shares', blank=True)
    nav_per_share = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='NAVPerShare', blank=True)
    inflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Inflows', blank=True)
    outflows = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Outflows', blank=True)
    fund_perf = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FundMonthlyReturn', blank=True)
    ytd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='FundYTDReturn', blank=True)
    bench_perf = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='BenchMonthlyReturn', blank=True)
    bench_ytd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='BenchYTDReturn', blank=True)
    flag = models.CharField(max_length=1, db_column='Flag', blank=True, null=True)
    sec_bench = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='SecBenchMonthlyReturn', blank=True)
    sec_bench_ytd = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='SecBenchYTDReturn', blank=True)

    class Meta:
        db_table = 'ALP_FundsMonthlyVals_TS'


class Holding(models.Model):
    holding = models.AutoField(primary_key=True, db_column='HoldingID')
    name = models.CharField(max_length=200, db_column='Name', blank=True)
    bloomberg_name = models.CharField(max_length=200, db_column='BloombergName', blank=True)
    description = models.CharField(max_length=500, db_column='Description', blank=True)
    underlying = models.CharField(max_length=50, db_column='Underlying', blank=True)
    currency = models.ForeignKey(Currency, related_name='holding_currency', null=True, db_column='CurrencyID', blank=True)
    otc = models.IntegerField(null=True, db_column='OTC', blank=True)
    counterparty = models.CharField(max_length=50, db_column='Counterparty', blank=True) #@TODO: Should be FK?
    exchangename = models.CharField(max_length=50, db_column='ExchangeName', blank=True)
    parentcompanyname = models.CharField(max_length=50, db_column='ParentCompanyName', blank=True)
    assetclass = models.IntegerField(null=True, db_column='AssetClassID', blank=True)
    country_ins = models.ForeignKey(Country, related_name='country_ins', null=True, db_column='CountryInsID', blank=True)
    country_risk = models.ForeignKey(Country, related_name='country_risk', null=True, db_column='CountryRiskID', blank=True)
    industry_sector = models.ForeignKey(IndustrySector, null=True, db_column='IndustrySectorID', blank=True)
    industry_group = models.ForeignKey(IndustryGroup, null=True, db_column='IndustryGroupID', blank=True)
    industry_subgroup = models.ForeignKey(IndustrySubGroup, null=True, db_column='IndustrySubGroupID', blank=True)
    issuer_industry = models.ForeignKey(IssuerIndustry, null=True, db_column='IssuerIndustryID', blank=True)
    idisin = models.CharField(max_length=20, db_column='IDIsin', blank=True)
    idcusip = models.CharField(max_length=20, db_column='IDCusip', blank=True)
    idbloombergticker = models.CharField(max_length=20, db_column='IDBloombergTicker', blank=True)
    idsedol = models.CharField(max_length=20, db_column='IDSedol', blank=True)
    idvaloren = models.CharField(max_length=20, db_column='IDValoren', blank=True)
    idother = models.CharField(max_length=20, db_column='IDOther', blank=True)
    region1 = models.ForeignKey(Region, related_name='holding_region1', null=True, db_column='Region1ID', blank=True)
    region2 = models.ForeignKey(Region, related_name='holding_region2', null=True, db_column='Region2ID', blank=True)
    region3 = models.ForeignKey(Region, related_name='holding_region3', null=True, db_column='Region3ID', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings'

    def __unicode__(self):
        return self.name

#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingDaily(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    value_date = models.DateTimeField(db_column='value_date')
    closing_price = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='ClosingPrice', blank=True)
    closing_bid = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='ClosingBid', blank=True)
    closing_ask = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='ClosingAsk', blank=True)
    daily_return = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='DailyReturn', blank=True)
    mtd = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MTDReturn', blank=True)
    ytd = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='YTDReturn', blank=True)
    
    class Meta:
        db_table = 'ALP_HoldingsDaily_TS'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingMonthly(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    value_date = models.DateTimeField(db_column='value_date')
    closingprice = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='ClosingPrice', blank=True)
    monthlyreturn = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MonthlyReturn', blank=True)
    ytd = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='YTDReturn', blank=True)
    
    class Meta:
        db_table = 'ALP_HoldingsMonthly_TS'


#@TODO: Table missing PK
class HoldingDeposit(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    start_date = models.DateTimeField(null=True, db_column='StartDate', blank=True)
    end_date = models.DateTimeField(null=True, db_column='EndDate', blank=True)
    rate = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='Rate', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Deposits'


#@TODO: Table missing PK
class HoldingEtf(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    benchmark = models.IntegerField(null=True, db_column='BenchmarkID', blank=True)
    eft_type = models.CharField(max_length=50, db_column='Type', blank=True)
    management_fees = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ManagementFees', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_ETF'
        verbose_name = 'Holding ETF'
        verbose_name_plural = 'Holding ETFs'


#@TODO: Table missing PK
class HoldingEquity(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    primary_exchange = models.CharField(max_length=20, db_column='PrimaryExchange', blank=True)
    gics_category = models.ForeignKey(GicsCategory, null=True, db_column='GICSCategoryID', blank=True)
    icb_category = models.ForeignKey(IcbCategory, null=True, db_column='ICBCategoryID', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Equities'
        verbose_name_plural = "Holding Equities"
        

#@TODO: Table missing PK
class HoldingFixedIncome(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    subordinated = models.CharField(max_length=1, db_column='SubOrdinated', blank=True)
    rank = models.CharField(max_length=50, db_column='Rank', blank=True)
    coupon = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Coupon', blank=True)
    couponfreq = models.CharField(max_length=50, db_column='CouponFreq', blank=True)
    coupontype = models.CharField(max_length=50, db_column='CouponType', blank=True)
    coupontypesecific = models.CharField(max_length=50, db_column='CouponTypeSecific', blank=True)
    structured = models.CharField(max_length=1, db_column='Structured', blank=True)
    convertible = models.CharField(max_length=1, db_column='Convertible', blank=True)
    collateral_type = models.CharField(max_length=50, db_column='CollateralType', blank=True)
    maturity = models.DateTimeField(null=True, db_column='Maturity', blank=True)
    maturity_type = models.CharField(max_length=50, db_column='MaturityType', blank=True)
    first_coupon_date = models.DateTimeField(null=True, db_column='FirstCouponDate', blank=True)
    moodys_rating = models.CharField(max_length=50, db_column='MoodysRating', blank=True)
    snp_rating = models.CharField(max_length=50, db_column='SnPRating', blank=True)
    fitch_rating = models.CharField(max_length=50, db_column='FitchRating', blank=True)
    dbrs_rating = models.CharField(max_length=50, db_column='DBRSRating', blank=True)
    date_rating_retrieval = models.DateTimeField(null=True, db_column='DateRatingRetrieval', blank=True)
    amt_issued = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='AmtIssued', blank=True)
    put_table = models.CharField(max_length=1, db_column='Puttable', blank=True)
    callable = models.CharField(max_length=1, db_column='Callable', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_FixedIncome'


#@TODO: Table missing PK
class HoldingForward(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    type_underlying = models.CharField(max_length=50, db_column='TypeUnderlying', blank=True)
    maturity = models.DateTimeField(null=True, db_column='Maturity', blank=True)
    contract_size = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ContractSize', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Forwards'


#@TODO: Table missing PK
class HoldingFuture(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    typeunderlying = models.CharField(max_length=50, db_column='TypeUnderlying', blank=True)
    maturity = models.DateTimeField(null=True, db_column='Maturity', blank=True)
    contractsize = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ContractSize', blank=True)
    value1pt = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Value1pt', blank=True)
    ticksize = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='TickSize', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Futures'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingHedgeFund(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    management_fees = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ManagementFees', blank=True)
    performance_fees = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='PerformanceFees', blank=True)
    admin = models.IntegerField(null=True, db_column='AdminID', blank=True)
    custodian = models.IntegerField(null=True, db_column='CustodianID', blank=True)
    auditor = models.IntegerField(null=True, db_column='AuditorID', blank=True)
    hfsector = models.ForeignKey(HfSector, null=True, db_column='HFSectorID', blank=True)
    softlock = models.CharField(max_length=10, db_column='SoftLock', blank=True)
    gate = models.CharField(max_length=10, db_column='Gate', blank=True)
    redemption_freq = models.CharField(max_length=1, db_column='RedemptionFreq', blank=True)
    redemption_noticecaldays = models.IntegerField(null=True, db_column='RedemptionNoticeCalDays', blank=True)
    redemption_noticebdays = models.IntegerField(null=True, db_column='RedemptionNoticeBDays', blank=True)
    redemption_fee12 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='RedemptionFee12', blank=True)
    redemption_fee24 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='RedemptionFee24', blank=True)
    redemption_fee36 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='RedemptionFee36', blank=True)
    parent_fundname = models.CharField(max_length=100, db_column='ParentFundName', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_HedgeFunds'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingMutualFund(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    benchmark = models.IntegerField(null=True, db_column='BenchmarkID', blank=True)
    subscription_fee = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='SubscriptionFee', blank=True)
    redemption_fee = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='RedemptionFee', blank=True)
    exchange_fee = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ExchangeFee', blank=True)
    distribution_fee = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='DistributionFee', blank=True)
    other_expenses = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='OtherExpenses', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_MutualFund'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingOption(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    call_put = models.CharField(max_length=4, db_column='CallPut', blank=True)
    type_undrlying = models.CharField(max_length=50, db_column='TypeUndrlying', blank=True)
    type_exercise = models.CharField(max_length=50, db_column='TypeExercise', blank=True)
    strike = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Strike', blank=True)
    maturity = models.DateTimeField(null=True, db_column='Maturity', blank=True)
    contract_size = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='ContractSize', blank=True)
    value_1pt = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Value1pt', blank=True)
    tick_size = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='TickSize', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Options'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class HoldingWarrant(models.Model):
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    type_exercise = models.CharField(max_length=10, db_column='TypeExercise', blank=True)
    strike = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Strike', blank=True)
    maturity = models.DateTimeField(null=True, db_column='Maturity', blank=True)
    
    class Meta:
        db_table = 'ALP_Holdings_Warrant'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class PositionDaily(models.Model):
    fund = models.ForeignKey(Fund, db_column='FundID')
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    value_date = models.DateTimeField(db_column='value_date')
    size = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Size', blank=True)
    marketpricelcl = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceLcl', blank=True)
    marketpricefundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceFundCur', blank=True)
    marketvaluelcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueLcl', blank=True)
    marketvaluefundcur = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueFundCur', blank=True)
    costpricelcl = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceLcl', blank=True)
    costpricefundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceFundCur', blank=True)
    marketcostlcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostLcl', blank=True)
    marketcostfundcur = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostFundCur', blank=True)
    
    class Meta:
        db_table = 'ALP_PositionsDaily'
        verbose_name_plural = 'Position Daily'


#@TODO: Table missing PK
#@TODO: Table have IntegerFields instead of FKs
class PositionMonthly(models.Model):
    fund = models.ForeignKey(Fund, db_column='FundID')
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    value_date = models.DateTimeField(db_column='value_date')
    size1 = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='Size1', blank=True)
    marketpricelcl1 = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceLcl1', blank=True)
    marketpricefundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='MarketPriceFundCur', blank=True)
    marketvaluelcl1 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueLcl1', blank=True)
    marketvaluefundcur1 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketValueFundCur1', blank=True)
    costpricelcl = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceLcl', blank=True)
    costpricefundcur = models.DecimalField(decimal_places=6, null=True, max_digits=18, db_column='CostPriceFundCur', blank=True)
    marketcostlcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostLcl', blank=True)
    marketcostfundcur = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='MarketCostFundCur', blank=True)
    
    class Meta:
        db_table = 'ALP_PositionsMonthly'
        verbose_name_plural = 'Position Monthly'


#@TODO: Table have IntegerFields instead of FKs
class Trade(models.Model):
    trade = models.AutoField(primary_key=True, db_column='TradeID')
    trade_date = models.DateTimeField(db_column='TradeDate')
    fund = models.ForeignKey(Fund, db_column='FundID')
    holding = models.ForeignKey(Holding, db_column='HoldingID')
    settlement_date = models.DateTimeField(null=True, db_column='SettlementDate', blank=True)
    confirm_flag = models.CharField(max_length=1, db_column='ConfirmFlag')
    buy_sell = models.CharField(max_length=1, db_column='BuySell')
    size = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='Size', blank=True)
    price_lcl = models.DecimalField(decimal_places=4, null=True, max_digits=18, db_column='PriceLcl', blank=True)
    amount_lcl = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='AmountLcl', blank=True)
    amount_lcl_requested = models.DecimalField(decimal_places=2, max_digits=18, db_column='AmountLclRequested')
    broker = models.ForeignKey(Broker, db_column='BrokerID')
    counterparty = models.ForeignKey(CounterParty, null=True, db_column='CounterpartyID', blank=True)
    feeid1 = models.IntegerField(null=True, db_column='FeeID1', blank=True)
    feevalue1 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='FeeValue1', blank=True)
    feeid2 = models.IntegerField(null=True, db_column='FeeID2', blank=True)
    feevalue2 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='FeeValue2', blank=True)
    feeid3 = models.IntegerField(null=True, db_column='FeeID3', blank=True)
    feevalue3 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='FeeValue3', blank=True)
    feeid4 = models.IntegerField(null=True, db_column='FeeID4', blank=True)
    feevalue4 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='FeeValue4', blank=True)
    feeid5 = models.IntegerField(null=True, db_column='FeeID5', blank=True)
    feevalue5 = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='FeeValue5', blank=True)
    totalfees = models.DecimalField(decimal_places=2, null=True, max_digits=18, db_column='TotalFees', blank=True)
    
    class Meta:
        db_table = 'ALP_Trades'
        
        
        
