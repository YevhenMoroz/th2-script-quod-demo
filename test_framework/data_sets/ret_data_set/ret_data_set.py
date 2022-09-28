from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.ret_data_set.ret_const_enum import RetTradingApiInstruments, RetInstruments,\
    RetInstrumentID, RetCurrency, RetSettlCurrency, RetVenues, RetClients, RetAccounts, RetWashbookAccounts,\
    RetRecipients,RetWashBookRules, RetCashAccounts, RetRiskLimitDimensions, RetCashAccountCounters,\
    RetWebAdminRestApiUsers, RetCashTransferTypes, RetFee, RetCommission, RetHierarchicalLevels


class RetDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    trading_api_instruments = RetTradingApiInstruments
    instruments = RetInstruments
    instrument_id = RetInstrumentID
    currency = RetCurrency
    settl_currency = RetSettlCurrency
    venues = RetVenues
    clients = RetClients
    accounts = RetAccounts
    cash_accounts = RetCashAccounts
    cash_account_counters = RetCashAccountCounters
    washbook_accounts = RetWashbookAccounts
    washbook_rules = RetWashBookRules
    recipients = RetRecipients
    web_admin_rest_api_users = RetWebAdminRestApiUsers
    risk_limit_dimensions = RetRiskLimitDimensions
    cash_transfer_types = RetCashTransferTypes
    fee = RetFee
    commission = RetCommission
    hierarchical_levels = RetHierarchicalLevels
