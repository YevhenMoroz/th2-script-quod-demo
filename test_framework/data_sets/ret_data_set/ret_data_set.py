from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.ret_data_set.ret_const_enum import RetTradingApiInstruments, RetInstruments, RetInstrumentID, RetCurrency, RetVenues, RetClients, RetAccounts, \
    RetWashbookAccounts, RetRecipients, RetWashBookRules


class RetDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    trading_api_instruments = RetTradingApiInstruments
    instruments = RetInstruments
    instrument_id = RetInstrumentID
    currency = RetCurrency
    venues = RetVenues
    clients = RetClients
    accounts = RetAccounts
    washbook_accounts = RetWashbookAccounts
    washbook_rules = RetWashBookRules
    recipients = RetRecipients
