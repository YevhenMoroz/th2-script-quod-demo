from enum import Enum

from test_framework.data_sets.fx_data_set.fx_const_enum import FxSymbols, FxSecurityTypes, FxSettleTypes, FxSettleDates


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
    listing_id = None
    instrument_id = None
    mic = None  # Market Identifier Code
    currency = None
    venue_client_names = None
    symbols = None
    security_types = None
    settle_types = None
    settle_dates = None
    routes = None
    lookups = None
    commission_profiles = None
    misc_fee_type = None
    fee_exec_scope: Enum = None
    fee = None
    commission = None
    client_tiers = None
    client_tiers_id = None
    days_of_week = None
    tenors = None
    symbols = FxSymbols
    security_types = FxSecurityTypes
    settle_types = FxSettleTypes
    settle_dates = FxSettleDates
    auto_hedgers = None
    auto_hedgers_id = None
    algo_policies = None
    algo_policies_id = None
    counterparts = None
    qty_types = None

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

    def get_listing_id_by_name(self, name: str):
        if hasattr(self.listing_id, name):
            return getattr(self.listing_id, name).value
        raise ValueError(f"{self.listing_id} not found!")

    def get_instrument_id_by_name(self, name: str):
        if hasattr(self.instrument_id, name):
            return getattr(self.instrument_id, name).value
        raise ValueError(f"{self.instrument_id} not found!")

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
        example ---> get_symbol_by_name("symbol_1"):
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
        get settle date by name from FxSettleDates
        example ---> get_settle_date_by_name("spot"):
        """
        if hasattr(self.settle_dates, name):
            return getattr(self.settle_dates, name).value
        raise ValueError(f"{self.settle_dates} not found!")

    def get_route(self, name:str):
        if hasattr(self.routes, name):
            return getattr(self.routes, name).value
        raise ValueError(f"{self.routes} not found!")

    def get_client_tier_by_name(self, name: str):
        """
        get client tier by name from FxClientTiers
        example ---> get_client_tier_by_name("client_tier_1"):
        """
        if hasattr(self.client_tiers, name):
            return getattr(self.client_tiers, name).value
        raise ValueError(f"{self.client_tiers} not found!")

    def get_client_tier_id_by_name(self, name: str):
        """
        get client tier ID by name from FxClientTiersID
        example ---> get_client_tier_id_by_name("client_tier_id_1"):
        """
        if hasattr(self.client_tiers_id, name):
            return getattr(self.client_tiers_id, name).value
        raise ValueError(f"{self.client_tiers_id} not found!")

    def get_day_of_week_by_name(self, name: str):
        """
        get day of week by name from DaysOfWeek
        example ---> get_day_of_week_by_name("monday"):
        """
        if hasattr(self.days_of_week, name):
            return getattr(self.days_of_week, name).value
        raise ValueError(f"{self.days_of_week} not found!")

    def get_tenor_by_name(self, name: str):
        """
        get tenor by name from FxTenors
        example ---> get_tenor_by_name("tenor_spot"):
        """
        if hasattr(self.tenors, name):
            return getattr(self.tenors, name).value
        raise ValueError(f"{self.tenors} not found!")

    def get_auto_hedger_by_name(self, name: str):
        """
        get auto hedger by name from FXAutoHedgers
        example ---> get_client_tier_by_name("auto_hedger_1"):
        """
        if hasattr(self.auto_hedgers, name):
            return getattr(self.auto_hedgers, name).value
        raise ValueError(f"{self.auto_hedgers} not found!")

    def get_auto_hedger_id_by_name(self, name: str):
        """
        get auto hedger ID by name from FXAutoHedgersID
        example ---> get_client_tier_id_by_name("auto_hedger_id_1"):
        """
        if hasattr(self.auto_hedgers_id, name):
            return getattr(self.auto_hedgers_id, name).value
        raise ValueError(f"{self.auto_hedgers_id} not found!")

    def get_algo_policy_by_name(self, name: str):
        """
        get algo policy by name from FXAlgoPolicies
        example ---> get_client_tier_by_name("algo_policy_1"):
        """
        if hasattr(self.algo_policies, name):
            return getattr(self.algo_policies, name).value
        raise ValueError(f"{self.algo_policies} not found!")

    def get_algo_policy_id_by_name(self, name: str):
        """
        get algo policy ID by name from FXAlgoPoliciesID
        example ---> get_client_tier_id_by_name("algo_policy_id_1"):
        """
        if hasattr(self.algo_policies_id, name):
            return getattr(self.algo_policies_id, name).value
        raise ValueError(f"{self.algo_policies_id} not found!")
    # endregion

    def get_lookup_by_name(self, name: str):
        if hasattr(self.lookups, name):
            return getattr(self.lookups, name).value
        return ValueError(f"{self.lookups} not found!")

    def get_comm_profile_by_name(self, name: str):
        if hasattr(self.commission_profiles, name):
            return getattr(self.commission_profiles, name).value
        return ValueError(f"{self.commission_profiles} not found!")

    def get_misc_fee_type_by_name(self, name: str):
        if hasattr(self.misc_fee_type, name):
            return getattr(self.misc_fee_type, name).value
        return ValueError(f"{self.misc_fee_type} not found!")
    def get_counterpart(self, name: str):
        if hasattr(self.counterparts, name):
            return getattr(self.counterparts, name).value
        return ValueError(f"{self.counterparts} not found!")


    def get_fee_exec_scope_by_name(self, name: str):
        if hasattr(self.fee_exec_scope, name):
            return getattr(self.fee_exec_scope, name).value
        return ValueError(f"{self.fee_exec_scope} not found!")

    def get_fee_by_name(self, name: str):
        if hasattr(self.fee, name):
            return getattr(self.fee, name)
        return ValueError(f"{self.fee} not found!")

    def get_fees(self):
        if self.fee:
            return self.fee

    def get_commission_by_name(self, name: str):
        if hasattr(self.commission, name):
            return getattr(self.commission, name)
        return ValueError(f"{self.commission} not found!")

    def get_commissions(self):
        if self.commission:
            return self.commission

    def get_qty_type(self, name: str):
        if hasattr(self.qty_types, name):
            return getattr(self.qty_types, name).value
        return ValueError(f"{self.qty_types} not found!")
