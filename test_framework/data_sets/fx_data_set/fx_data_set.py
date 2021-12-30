from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_const_enum import FxInstruments, FxVenues, FxClients, FxAccounts, \
    FxSymbols, FxSecurityTypes, FxSettleTypes, FxSettleDates


class FxDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = FxInstruments
    venues = FxVenues
    clients = FxClients
    accounts = FxAccounts
    symbols = FxSymbols
    security_types = FxSecurityTypes
    settle_types = FxSettleTypes
    settle_dates = FxSettleDates

    def get_symbol_by_name(self, name: str):
        """
        get symbol from FxSymbols
        example ---> get_symbol_by_name("eur_usd"):
        """
        if hasattr(self.symbols, name):
            return getattr(self.symbols, name).value
        raise ValueError(f"{self.symbols} not found!")

    def get_security_type_by_name(self, name: str):
        """
        get security_type from FxSecurityTypes
        example ---> get_security_type_by_name("fxspot"):
        """
        if hasattr(self.security_types, name):
            return getattr(self.security_types, name).value
        raise ValueError(f"{self.security_types} not found!")

    def get_settle_type_by_name(self, name: str):
        """
        get settle type by name from FxSettleTypes
        example ---> get_security_type_by_name("fxspot"):
        """
        if hasattr(self.settle_types, name):
            return getattr(self.settle_types, name).value
        raise ValueError(f"{self.settle_types} not found!")

    def get_settle_date_by_name(self, name: str):
        """
        get settle type by name from FxSettleTypes
        example ---> get_settle_date_by_name("spot"):
        """
        if hasattr(self.settle_dates, name):
            return getattr(self.settle_dates, name).value
        raise ValueError(f"{self.settle_dates} not found!")