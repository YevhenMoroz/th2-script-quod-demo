from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_const_enum import FxInstruments, FxVenues, FxClients, FxAccounts, \
    FxWashbookAccounts, FxRecipients, DaysOfWeek


class FxDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = FxInstruments
    venues = FxVenues
    clients = FxClients
    accounts = FxAccounts
    washbook_accounts = FxWashbookAccounts
    recipients = FxRecipients
    days_of_week = DaysOfWeek

    def get_day_by_name(self, name: str):
        if hasattr(self.days_of_week, name):
            return getattr(self.days_of_week, name).value
        raise ValueError(f"{self.days_of_week} not found!")
