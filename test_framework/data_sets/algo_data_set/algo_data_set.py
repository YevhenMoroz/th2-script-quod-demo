from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.algo_data_set.algo_const_enum import AlgoInstruments, AlgoVenues, AlgoClients, \
    AlgoAccounts, AlgoWashbookAccounts, AlgoRecipients


class AlgoDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = AlgoInstruments
    venues = AlgoVenues
    clients = AlgoClients
    accounts = AlgoAccounts
    washbook_accounts = AlgoWashbookAccounts
    recipients = AlgoRecipients
