from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.algo_data_set.algo_const_enum import AlgoFixInstruments, AlgoVenues, AlgoClients, \
    AlgoAccounts, AlgoWashbookAccounts, AlgoRecipients, AlgoMic, AlgoListingId, AlgoCurrency


class AlgoDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    fix_instruments = AlgoFixInstruments
    venues = AlgoVenues
    clients = AlgoClients
    accounts = AlgoAccounts
    washbook_accounts = AlgoWashbookAccounts
    recipients = AlgoRecipients
    mic = AlgoMic
    listing_id = AlgoListingId
    currency = AlgoCurrency

