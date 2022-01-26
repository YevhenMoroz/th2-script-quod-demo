class BaseDataSet:
    """
    Base class that describes the common attributes and methods for all product lines datasets.
    """
    fix_instruments = None
    venues = None
    clients = None
    accounts = None
    washbook_accounts = None
    recipients = None
    db_listing = None
    db_instrument = None
    mic = None  # Market Identifier Code
    currency = None
    venue_client_names = None
    symbols = None
    security_types = None
    settle_types = None
    settle_dates = None
    lookups = None

    def get_instruments(self):
        if self.fix_instruments:
            return self.fix_instruments.__members__

    def get_venues(self):
        if self.venues:
            return self.venues.__members__

    def get_clients(self):
        if self.clients:
            return self.clients.__members__

    def get_accounts(self):
        if self.accounts:
            return self.accounts.__members__

    def get_washbook_accounts(self):
        if self.washbook_accounts:
            return self.washbook_accounts.__members__

    def get_recipients(self):
        if self.recipients:
            return self.recipients.__members__

    def get_fix_instrument_by_name(self, name: str):
        if hasattr(self.fix_instruments, name):
            return getattr(self.fix_instruments, name).value
        raise ValueError(f"{self.fix_instruments} not found!")

    def get_venue_by_name(self, name: str):
        if hasattr(self.venues, name):
            return getattr(self.venues, name).value
        raise ValueError(f"{self.venues} not found!")

    def get_client_by_name(self, name: str):
        if hasattr(self.clients, name):
            return getattr(self.clients, name).value
        raise ValueError(f"{self.clients} not found!")

    def get_account_by_name(self, name: str):
        if hasattr(self.accounts, name):
            return getattr(self.accounts, name).value
        raise ValueError(f"{self.accounts} not found!")

    def get_washbook_account_by_name(self, name: str):
        if hasattr(self.washbook_accounts, name):
            return getattr(self.washbook_accounts, name).value
        raise ValueError(f"{self.washbook_accounts} not found!")

    def get_recipient_by_name(self, name: str):
        if hasattr(self.recipients, name):
            return getattr(self.recipients, name).value
        raise ValueError(f"{self.recipients} not found!")

    def get_db_listing_by_name(self, name: str):
        if hasattr(self.db_listing, name):
            return getattr(self.db_listing, name).value
        raise ValueError(f"{self.db_listing} not found!")

    def get_db_instrument_by_name(self, name: str):
        if hasattr(self.db_instrument, name):
            return getattr(self.db_instrument, name).value
        raise ValueError(f"{self.db_instrument} not found!")

    def get_mic_by_name(self, name: str):
        if hasattr(self.mic, name):
            return getattr(self.mic, name).value
        raise ValueError(f"{self.mic} not found!")

    def get_currency_by_name(self, name: str):
        if hasattr(self.currency, name):
            return getattr(self.currency, name).value
        raise ValueError(f"{self.currency} not found!")

    def get_venue_client_names_by_name(self, name: str):
        if hasattr(self.venue_client_names, name):
            return getattr(self.venue_client_names, name).value
        raise ValueError(f"{self.venue_client_names} not found!")

    # region FX getters
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
    # endregion

    def get_lookup_by_name(self, name: str):
        if hasattr(self.lookups, name):
            return getattr(self.lookups, name).value
        return ValueError(f"{self.lookups} not found!")
