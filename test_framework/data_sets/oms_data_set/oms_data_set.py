from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.oms_data_set.oms_const_enum import OmsInstruments, OmsVenues, OmsClients, OmsAccounts, \
    OmsWashbookAccounts, OmsRecipients


class OmsDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = OmsInstruments
    venues = OmsVenues
    clients = OmsClients
    accounts = OmsAccounts
    washbook_accounts = OmsWashbookAccounts
    recipients = OmsRecipients
