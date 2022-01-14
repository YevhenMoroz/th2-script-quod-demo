class BaseDataSet:
    """
    Base class that describes the common attributes and methods for all product lines datasets.
    """
    instruments = None
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

    def get_instruments(self):
        if self.instruments:
            return self.instruments.__members__

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

    def get_instrument_by_name(self, name: str):
        if hasattr(self.instruments, name):
            return getattr(self.instruments, name).value
        raise ValueError(f"{self.instruments} not found!")

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
