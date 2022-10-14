from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_const_enum import FxInstruments, FxVenues, FxClients, FxAccounts, \
    FxClientTiers, FxSymbols, DaysOfWeek, FxCurrencies, FxTenors, FxClientTiersID, FXAutoHedgers, FXAutoHedgersID, \
    FXAlgoPolicies, FXAlgoPoliciesID, FxSecurityTypes, FxSettleTypes, FxSettleDates, FxInstrTypeWA, FxMarketIDs, \
    FxTenorsJavaApi, FxInstrTypeJavaAPi, FxSettleTypesJavaAPi


class FxDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = FxInstruments
    venues = FxVenues
    clients = FxClients
    accounts = FxAccounts
    client_tiers = FxClientTiers
    client_tiers_id = FxClientTiersID
    symbols = FxSymbols
    days_of_week = DaysOfWeek
    currency = FxCurrencies
    tenors = FxTenors
    tenors_java_api = FxTenorsJavaApi
    auto_hedgers = FXAutoHedgers
    auto_hedgers_id = FXAutoHedgersID
    algo_policies = FXAlgoPolicies
    algo_policies_id = FXAlgoPoliciesID
    security_types = FxSecurityTypes
    settle_types = FxSettleTypes
    settle_types_ja = FxSettleTypesJavaAPi
    settle_dates = FxSettleDates
    fx_istr_type_wa = FxInstrTypeWA
    fx_istr_type_ja = FxInstrTypeJavaAPi
    market_ids = FxMarketIDs

