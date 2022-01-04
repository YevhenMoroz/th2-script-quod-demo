from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.ret_data_set.ret_const_enum import RetInstruments, RetVenues, RetClients, RetAccounts, \
    RetWashbookAccounts, RetRecipients


class RetDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = RetInstruments
    venues = RetVenues
    clients = RetClients
    accounts = RetAccounts
    washbook_accounts = RetWashbookAccounts
    recipients = RetRecipients
