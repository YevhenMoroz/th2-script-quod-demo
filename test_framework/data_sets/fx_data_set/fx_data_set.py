from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_const_enum import FxInstruments, FxVenues, FxClients, FxAccounts


class FxDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = FxInstruments
    venues = FxVenues
    clients = FxClients
    accounts = FxAccounts


    def get_security_type_by_name(self, name: str):
        """
        get security_type from FxSecurityTypes
        example ---> get_security_type_by_name("fxspot"):
        """
        if hasattr(self.security_types, name):
            return getattr(self.security_types, name).value
        raise ValueError(f"{self.security_types} not found!")
