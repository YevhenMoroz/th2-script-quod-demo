class BaseDataSet:
    """
    Base class that describes the common attributes and methods for all product lines datasets.
    """
    trading_api_instruments = None
    fix_instruments = None
    instruments = None
    instrument_id = None
    venues = None
    clients = None
    accounts = None
    cash_accounts = None
    cash_account_counters = None
    washbook_accounts = None
    washbook_rules = None
    counterpart_id_fix = None
    recipients = None
    web_admin_rest_api_users = None
    risk_limit_dimensions = None
    cash_transfer_types = None
    listing_id = None
    counterpart_id_java_api = None
    mic = None  # Market Identifier Code
    currency = None
    settl_currency = None
    venue_client_names = None
    symbols = None
    security_types = None
    settle_types = None
    settle_dates = None
    routes = None
    route_id = None
    lookups = None
    commission_profiles = None
    misc_fee_type = None
    fee_exec_scope = None
    fee = None
    commission = None
    client_tiers = None
    client_tiers_id = None
    days_of_week = None
    tenors = None
    auto_hedgers = None
    auto_hedgers_id = None
    algo_policies = None
    algo_policies_id = None
    counterpart = None
    qty_types = None
    venue_client_accounts = None
    verifier_key_parameters = None
    fee_order_scope = None
    pset = None
    basket_templates = None
    give_up_brokers = None
    fee_type_in_booking_ticket = None
    client_desks = None
    middle_office_status = None
    middle_office_match_status = None
    capacity = None
    scenario = None
    strategy = None
    market_ids = None
    contra_firm = None
    all_venue_sec_account_names_of_acc = None
    venue_list = None
    isin_security_alt_ids = None
    security_id_source = None
    hierarchical_levels = None
    # region fields added by Web Admin team
    user = None
    password = None
    component_id = None
    system_command = None
    desk = None
    location = None
    institution = None
    zone = None
    client = None
    client_type = None
    email = None
    perm_role = None
    first_user_name = None
    venue_id = None
    venue_type = None
    country = None
    sub_venue = None
    trading_status = None
    trading_phase = None
    price_limit_profile = None
    tick_size_profile = None
    trading_phase_profile = None
    tick_size_xaxis_type = None
    instr_symbol = None
    symbol = None
    instr_type = None
    fx_istr_type_wa = None
    preferred_venue = None
    listing_group = None
    settle_type = None
    feed_source = None
    negative_route = None
    positive_route = None
    client_id_source = None
    route_account_name = None
    route = None
    clearing_account_type = None
    disclose_exec = None
    account_id_source = None
    default_route = None
    default_execution_strategy = None
    trade_confirm_generation = None
    trade_confirm_preference = None
    net_gross_ind_type = None
    recipient_type = None
    default_tif = None
    strategy_type = None
    exec_policy = None
    commission_amount_type = None
    settl_location = None
    country_code = None
    client_group = None
    instrument = None
    instrument_group = None
    client_list = None
    comm_algorithm = None
    comm_type = None
    core_spot_price_strategy = None
    party_role = None
    counterpart_id = None
    cl_list_id = None
    pre_filter = None
    reference_price = None
    java_api_instruments = None
    # endregion

    # region fields added by Web Trading team
    order_type = None
    time_in_force = None
    commission_basis = None

    # endregion

    def get_instruments(self):
        if self.fix_instruments:
            return self.fix_instruments.__members__

    def get_instrument_id(self):
        if self.instruments:
            return self.instrument_id.__members__

    def get_currency(self):
        if self.currency:
            return self.currency.__members__

    def get_settl_currency(self):
        if self.settl_currency:
            return self.settl_currency.__members__

    def get_venues(self):
        if self.venues:
            return self.venues.__members__

    def get_clients(self):
        if self.clients:
            return self.clients.__members__

    def get_accounts(self):
        if self.accounts:
            return self.accounts.__members__

    def get_cash_accounts(self):
        if self.cash_accounts:
            return self.cash_accounts.__members__

    def get_cash_account_counters(self):
        if self.cash_account_counters:
            return self.cash_account_counters.__members__

    def get_washbook_accounts(self):
        if self.washbook_accounts:
            return self.washbook_accounts.__members__

    def get_washbook_rule(self):
        if self.washbook_rules:
            return self.washbook_rules.__members__

    def get_recipients(self):
        if self.recipients:
            return self.recipients.__members__

    def get_web_admin_rest_api_users(self):
        if self.web_admin_rest_api_users:
            return self.web_admin_rest_api_users.__members__

    def get_risk_limit_dimensions(self):
        if self.accounts:
            return self.accounts.__members__

    def get_cash_transfer_types(self):
        if self.cash_transfer_types:
            return self.cash_account_counters.__members__

    def get_trading_api_instrument_by_name(self, name: str):
        if hasattr(self.trading_api_instruments, name):
            return getattr(self.trading_api_instruments, name).value
        raise ValueError(f"{self.trading_api_instruments} not found!")

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

    def get_cash_account_by_name(self, name: str):
        if hasattr(self.cash_accounts, name):
            return getattr(self.cash_accounts, name).value
        raise ValueError(f"{self.cash_accounts} not found!")

    def get_cash_account_counters_by_name(self, name: str):
        if hasattr(self.cash_account_counters, name):
            return getattr(self.cash_account_counters, name).value
        raise ValueError(f"{self.cash_account_counters} not found!")

    def get_washbook_account_by_name(self, name: str):
        if hasattr(self.washbook_accounts, name):
            return getattr(self.washbook_accounts, name).value
        raise ValueError(f"{self.washbook_accounts} not found!")

    def get_washbook_rule_by_name(self, name: str):
        if hasattr(self.washbook_rules, name):
            return getattr(self.washbook_rules, name).value
        raise ValueError(f"{self.washbook_rules} not found!")

    def get_recipient_by_name(self, name: str):
        if hasattr(self.recipients, name):
            return getattr(self.recipients, name).value
        raise ValueError(f"{self.recipients} not found!")

    def get_web_admin_rest_api_users_by_name(self, name: str):
        if hasattr(self.web_admin_rest_api_users, name):
            return getattr(self.web_admin_rest_api_users, name).value
        raise ValueError(f"{self.web_admin_rest_api_users} not found!")

    def get_risk_limit_dimension_by_name(self, name: str):
        if hasattr(self.risk_limit_dimensions, name):
            return getattr(self.risk_limit_dimensions, name).value
        raise ValueError(f"{self.risk_limit_dimensions} not found!")

    def get_cash_transfer_types_by_name(self, name: str):
        if hasattr(self.cash_transfer_types, name):
            return getattr(self.cash_transfer_types, name).value
        raise ValueError(f"{self.cash_transfer_types} not found!")

    def get_listing_id_by_name(self, name: str):
        if hasattr(self.listing_id, name):
            return getattr(self.listing_id, name).value
        raise ValueError(f"{self.listing_id} not found!")

    def get_instrument_id_by_name(self, name: str):
        if hasattr(self.instrument_id, name):
            return getattr(self.instrument_id, name).value
        raise ValueError(f"{self.instrument_id} not found!")

    def get_fx_instr_type_wa(self, name: str):
        if hasattr(self.fx_istr_type_wa, name):
            return getattr(self.fx_istr_type_wa, name).value
        return ValueError(f"{self.fx_istr_type_wa} not found!")

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

    def get_counterpart_id_fix(self, name: str):
        if hasattr(self.counterpart_id_fix, name):
            return getattr(self.counterpart_id_fix, name).value
        raise ValueError(f"{self.counterpart_id_fix} not found!")

    def get_counterpart_id_java_api(self, name: str):
        if hasattr(self.counterpart_id_java_api, name):
            return getattr(self.counterpart_id_java_api, name).value
        raise ValueError(f"{self.counterpart_id_java_api} not found!")

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

    def get_route(self, name: str):
        if hasattr(self.routes, name):
            return getattr(self.routes, name).value
        raise ValueError(f"{self.routes} not found!")

    def get_route_id_by_name(self, name: str):
        if hasattr(self.route_id, name):
            return getattr(self.route_id, name).value
        raise ValueError(f"{self.route_id} not found!")

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

    def get_market_id_by_name(self, name: str):
        """
        get Market ID by name from FxMarketIDs
        example ---> get_market_id_by_name("market_1"):
        """
        if hasattr(self.market_ids, name):
            return getattr(self.market_ids, name).value
        raise ValueError(f"{self.market_ids} not found!")

    # endregion

    def get_lookup_by_name(self, name: str):
        if hasattr(self.lookups, name):
            return getattr(self.lookups, name).value
        raise ValueError(f"{self.lookups} not found!")

    def get_verifier_key_parameters_by_name(self, name: str):
        if hasattr(self.verifier_key_parameters, name):
            return getattr(self.verifier_key_parameters, name).value
        raise ValueError(f"{self.verifier_key_parameters} not found!")

    def get_venue_client_account(self, name: str):
        if hasattr(self.venue_client_accounts, name):
            return getattr(self.venue_client_accounts, name).value
        raise ValueError(f"{self.venue_client_accounts} not found!")

    def get_comm_profile_by_name(self, name: str):
        if hasattr(self.commission_profiles, name):
            return getattr(self.commission_profiles, name).value
        raise ValueError(f"{self.commission_profiles} not found!")

    def get_misc_fee_type_by_name(self, name: str):
        if hasattr(self.misc_fee_type, name):
            return getattr(self.misc_fee_type, name).value
        raise ValueError(f"{self.misc_fee_type} not found!")

    def get_fee_exec_scope_by_name(self, name: str):
        if hasattr(self.fee_exec_scope, name):
            return getattr(self.fee_exec_scope, name).value
        raise ValueError(f"{self.fee_exec_scope} not found!")

    def get_fee_order_scope_by_name(self, name: str):
        if hasattr(self.fee_order_scope, name):
            return getattr(self.fee_order_scope, name).value
        raise ValueError(f"{self.fee_order_scope} not found!")

    def get_fee_by_name(self, name: str):
        if hasattr(self.fee, name):
            return getattr(self.fee, name)
        raise ValueError(f"{self.fee} not found!")

    def get_fees(self):
        if self.fee:
            return self.fee

    def get_commission_by_name(self, name: str):
        if hasattr(self.commission, name):
            return getattr(self.commission, name)
        raise ValueError(f"{self.commission} not found!")

    def get_commissions(self):
        if self.commission:
            return self.commission

    def get_pset(self, name: str):
        """
        @param name: name_of_pset
        @return: value_of_pset
        """
        if hasattr(self.pset, name):
            return getattr(self.pset, name).value
        raise ValueError(f"{self.pset} not found")

    def get_qty_type(self, name: str):
        if hasattr(self.qty_types, name):
            return getattr(self.qty_types, name).value
        raise ValueError(f"{self.qty_types} not found!")

    def get_give_up_broker(self, name: str):
        if hasattr(self.give_up_brokers, name):
            return getattr(self.give_up_brokers, name).value
        raise ValueError(f"{self.give_up_brokers} not found!")

    def get_client_desk(self, name: str):
        if hasattr(self.client_desks, name):
            return getattr(self.client_desks, name).value
        raise ValueError(f"{self.client_desks} not found!")

    def get_fee_type_from_booking_ticket(self, name: str):
        if hasattr(self.fee_type_in_booking_ticket, name):
            return getattr(self.fee_type_in_booking_ticket, name).value
        raise ValueError(f"{self.fee_type_in_booking_ticket} not found!")

    def get_middle_office_status(self, name: str):
        if hasattr(self.middle_office_status, name):
            return getattr(self.middle_office_status, name).value
        raise ValueError(f"{self.middle_office_status} not found!")

    def get_middle_office_match_status(self, name: str):
        if hasattr(self.middle_office_match_status, name):
            return getattr(self.middle_office_match_status, name).value
        raise ValueError(f"{self.middle_office_match_status} not found!")

    def get_strategy(self, name: str):
        if hasattr(self.strategy, name):
            return getattr(self.strategy, name).value
        raise ValueError(f"{self.strategy} not found!")

    def get_scenario(self, name: str):
        if hasattr(self.scenario, name):
            return getattr(self.scenario, name).value
        raise ValueError(f"{self.scenario} not found!")

    # region WebAdmin getters

    def get_user(self, name: str):
        if hasattr(self.user, name):
            return getattr(self.user, name).value
        return ValueError(f"{self.user} not found!")

    def get_password(self, name: str):
        if hasattr(self.password, name):
            return getattr(self.password, name).value
        return ValueError(f"{self.password} not found!")

    def get_component_id(self, name: str):
        if hasattr(self.component_id, name):
            return getattr(self.component_id, name).value
        return ValueError(f"{self.component_id} not found!")

    def get_system_command(self, name: str):
        if hasattr(self.system_command, name):
            return getattr(self.system_command, name).value
        return ValueError(f"{self.system_command} not found!")

    def get_desk(self, name: str):
        if hasattr(self.desk, name):
            return getattr(self.desk, name).value
        return ValueError(f"{self.desk} not found!")

    def get_location(self, name: str):
        if hasattr(self.location, name):
            return getattr(self.location, name).value
        return ValueError(f"{self.location} not found!")

    def get_institution(self, name: str):
        if hasattr(self.institution, name):
            return getattr(self.institution, name).value
        return ValueError(f"{self.institution} not found!")

    def get_zone(self, name: str):
        if hasattr(self.zone, name):
            return getattr(self.zone, name).value
        return ValueError(f"{self.zone} not found!")

    def get_client(self, name: str):
        if hasattr(self.clients, name):
            return getattr(self.clients, name).value
        return ValueError(f"{self.clients} not found!")

    def get_client_type(self, name: str):
        if hasattr(self.client_type, name):
            return getattr(self.client_type, name).value
        return ValueError(f"{self.client_type} not found!")

    def get_email(self, name: str):
        if hasattr(self.email, name):
            return getattr(self.email, name).value
        return ValueError(f"{self.email} not found!")

    def get_perm_role(self, name: str):
        if hasattr(self.perm_role, name):
            return getattr(self.perm_role, name).value
        return ValueError(f"{self.perm_role} not found!")

    def get_first_user_name(self, name: str):
        if hasattr(self.first_user_name, name):
            return getattr(self.first_user_name, name).value
        return ValueError(f"{self.first_user_name} not found!")

    def get_venue_id(self, name: str):
        if hasattr(self.venue_id, name):
            return getattr(self.venue_id, name).value
        return ValueError(f"{self.venue_id} not found!")

    def get_venue_type(self, name: str):
        if hasattr(self.venue_type, name):
            return getattr(self.venue_type, name).value
        return ValueError(f"{self.venue_type} not found!")

    def get_country(self, name: str):
        if hasattr(self.country, name):
            return getattr(self.country, name).value
        return ValueError(f"{self.country} not found!")

    def get_sub_venue(self, name: str):
        if hasattr(self.sub_venue, name):
            return getattr(self.sub_venue, name).value
        return ValueError(f"{self.sub_venue} not found!")

    def get_trading_status(self, name: str):
        if hasattr(self.trading_status, name):
            return getattr(self.trading_status, name).value
        return ValueError(f"{self.trading_status} not found!")

    def get_trading_phase(self, name: str):
        if hasattr(self.trading_phase, name):
            return getattr(self.trading_phase, name).value
        return ValueError(f"{self.trading_phase} not found!")

    def get_price_limit_profile(self, name: str):
        if hasattr(self.price_limit_profile, name):
            return getattr(self.price_limit_profile, name).value
        return ValueError(f"{self.price_limit_profile} not found!")

    def get_tick_size_profile(self, name: str):
        if hasattr(self.tick_size_profile, name):
            return getattr(self.tick_size_profile, name).value
        return ValueError(f"{self.tick_size_profile} not found!")

    def get_trading_phase_profile(self, name: str):
        if hasattr(self.trading_phase_profile, name):
            return getattr(self.trading_phase_profile, name).value
        return ValueError(f"{self.trading_phase_profile} not found!")

    def get_tick_size_xaxis_type(self, name: str):
        if hasattr(self.tick_size_xaxis_type, name):
            return getattr(self.tick_size_xaxis_type, name).value
        return ValueError(f"{self.tick_size_xaxis_type} not found!")

    def get_instr_symbol(self, name: str):
        if hasattr(self.instr_symbol, name):
            return getattr(self.instr_symbol, name).value
        return ValueError(f"{self.instr_symbol} not found!")

    def get_instr_type(self, name: str):
        if hasattr(self.instr_type, name):
            return getattr(self.instr_type, name).value
        return ValueError(f"{self.instr_type} not found!")

    def get_preferred_venue(self, name: str):
        if hasattr(self.preferred_venue, name):
            return getattr(self.preferred_venue, name).value
        return ValueError(f"{self.preferred_venue} not found!")

    def get_listing_group(self, name: str):
        if hasattr(self.listing_group, name):
            return getattr(self.listing_group, name).value
        return ValueError(f"{self.listing_group} not found!")

    def get_feed_source(self, name: str):
        if hasattr(self.feed_source, name):
            return getattr(self.feed_source, name).value
        return ValueError(f"{self.feed_source} not found!")

    def get_negative_route(self, name: str):
        if hasattr(self.negative_route, name):
            return getattr(self.negative_route, name).value
        return ValueError(f"{self.negative_route} not found!")

    def get_positive_route(self, name: str):
        if hasattr(self.positive_route, name):
            return getattr(self.positive_route, name).value
        return ValueError(f"{self.positive_route} not found!")

    def get_client_id_source(self, name: str):
        if hasattr(self.client_id_source, name):
            return getattr(self.client_id_source, name).value
        return ValueError(f"{self.client_id_source} not found!")

    def get_route_account_name(self, name: str):
        if hasattr(self.route_account_name, name):
            return getattr(self.route_account_name, name).value
        return ValueError(f"{self.route_account_name} not found!")

    def get_clearing_account_type(self, name: str):
        if hasattr(self.clearing_account_type, name):
            return getattr(self.clearing_account_type, name).value
        return ValueError(f"{self.clearing_account_type} not found!")

    def get_disclose_exec(self, name: str):
        if hasattr(self.disclose_exec, name):
            return getattr(self.disclose_exec, name).value
        return ValueError(f"{self.disclose_exec} not found!")

    def get_account_id_source(self, name: str):
        if hasattr(self.account_id_source, name):
            return getattr(self.account_id_source, name).value
        return ValueError(f"{self.account_id_source} not found!")

    def get_default_route(self, name: str):
        if hasattr(self.default_route, name):
            return getattr(self.default_route, name).value
        return ValueError(f"{self.default_route} not found!")

    def get_default_execution_strategy(self, name: str):
        if hasattr(self.default_execution_strategy, name):
            return getattr(self.default_execution_strategy, name).value
        return ValueError(f"{self.default_execution_strategy} not found!")

    def get_trade_confirm_generation(self, name: str):
        if hasattr(self.trade_confirm_generation, name):
            return getattr(self.trade_confirm_generation, name).value
        return ValueError(f"{self.trade_confirm_generation} not found!")

    def get_trade_confirm_preference(self, name: str):
        if hasattr(self.trade_confirm_preference, name):
            return getattr(self.trade_confirm_preference, name).value
        return ValueError(f"{self.trade_confirm_preference} not found!")

    def get_net_gross_ind_type(self, name: str):
        if hasattr(self.net_gross_ind_type, name):
            return getattr(self.net_gross_ind_type, name).value
        return ValueError(f"{self.net_gross_ind_type} not found!")

    def get_recipient_type(self, name: str):
        if hasattr(self.recipient_type, name):
            return getattr(self.recipient_type, name).value
        return ValueError(f"{self.recipient_type} not found!")

    def get_default_tif(self, name: str):
        if hasattr(self.default_tif, name):
            return getattr(self.default_tif, name).value
        return ValueError(f"{self.default_tif} not found!")

    def get_strategy_type(self, name: str):
        if hasattr(self.strategy_type, name):
            return getattr(self.strategy_type, name).value
        return ValueError(f"{self.strategy_type} not found!")

    def get_exec_policy(self, name: str):
        if hasattr(self.exec_policy, name):
            return getattr(self.exec_policy, name).value
        return ValueError(f"{self.exec_policy} not found!")

    def get_basket_template(self, name: str):
        if hasattr(self.basket_templates, name):
            return getattr(self.basket_templates, name).value
        return ValueError(f"{self.basket_templates} not found!")

    def get_commission_amount_type(self, name: str):
        if hasattr(self.commission_amount_type, name):
            return getattr(self.commission_amount_type, name).value
        return ValueError(f"{self.commission_amount_type,} not found!")

    def get_settl_location(self, name: str):
        if hasattr(self.settl_location, name):
            return getattr(self.settl_location, name).value
        return ValueError(f"{self.settl_location,} not found!")

    def get_country_code(self, name: str):
        if hasattr(self.country_code, name):
            return getattr(self.country_code, name).value
        return ValueError(f"{self.country_code,} not found!")

    def get_client_group(self, name: str):
        if hasattr(self.client_group, name):
            return getattr(self.client_group, name).value
        return ValueError(f"{self.client_group,} not found!")

    def get_instrument(self, name: str):
        if hasattr(self.instrument, name):
            return getattr(self.instrument, name).value
        return ValueError(f"{self.instrument,} not found!")

    def get_instrument_group(self, name: str):
        if hasattr(self.instrument_group, name):
            return getattr(self.instrument_group, name).value
        return ValueError(f"{self.instrument_group,} not found!")

    def get_client_list(self, name: str):
        if hasattr(self.client_list, name):
            return getattr(self.client_list, name).value
        return ValueError(f"{self.client_list,} not found!")

    def get_comm_algorithm(self, name: str):
        if hasattr(self.comm_algorithm, name):
            return getattr(self.comm_algorithm, name).value
        return ValueError(f"{self.comm_algorithm,} not found!")

    def get_comm_type(self, name: str):
        if hasattr(self.comm_type, name):
            return getattr(self.comm_type, name).value
        return ValueError(f"{self.comm_type,} not found!")

    def get_core_spot_price_strategy(self, name: str):
        if hasattr(self.core_spot_price_strategy, name):
            return getattr(self.core_spot_price_strategy, name).value
        return ValueError(f"{self.core_spot_price_strategy,} not found!")

    def get_party_role(self, name: str):
        if hasattr(self.party_role, name):
            return getattr(self.party_role, name).value
        return ValueError(f"{self.party_role,} not found!")

    def get_pre_filter(self, name: str):
        if hasattr(self.pre_filter, name):
            return getattr(self.pre_filter, name).value
        return ValueError(f"{self.pre_filter,} not found!")

    # endregion

    # region WebTrading getters
    def get_order_type(self, name: str):
        if hasattr(self.order_type, name):
            return getattr(self.order_type, name).value
        return ValueError(f"{self.order_type,} not found!")

    def get_time_in_force(self, name: str):
        if hasattr(self.time_in_force, name):
            return getattr(self.time_in_force, name).value
        return ValueError(f"{self.time_in_force,} not found!")

    def get_commission_basis(self, name: str):
        if hasattr(self.commission_basis, name):
            return getattr(self.commission_basis, name).value
        return ValueError(f"{self.commission_basis} not found!")

    def get_capacity(self, name: str):
        if hasattr(self.capacity, name):
            return getattr(self.capacity, name).value
        return ValueError(f"{self.capacity} not found!")

    def get_counterpart_id(self, name: str):
        if hasattr(self.counterpart_id, name):
            return getattr(self.counterpart_id, name).value
        return ValueError(f"{self.counterpart_id} not found!")

    def get_counterpart(self, name: str):
        if hasattr(self.counterpart, name):
            return getattr(self.counterpart, name).value
        return ValueError(f"{self.counterpart} not found!")

    def get_cl_list_id(self, name: str):
        if hasattr(self.cl_list_id, name):
            return getattr(self.cl_list_id, name).value
        return ValueError(f"{self.cl_list_id} not found!")

    def get_ref_price(self, name: str):
        if hasattr(self.reference_price, name):
            return getattr(self.reference_price, name).value
        return ValueError(f"{self.reference_price} not found!")

    def get_venue_list(self, name: str):
        if hasattr(self.venue_list, name):
            return getattr(self.venue_list, name).value
        return ValueError(f"{self.venue_list} not found!")

    def get_java_api_instrument(self, name: str):
        if hasattr(self.java_api_instruments, name):
            return getattr(self.java_api_instruments, name).value
        return ValueError(f"{self.java_api_instruments} not found!")

    def get_contra_firm(self, name: str):
        if hasattr(self.contra_firm, name):
            return getattr(self.contra_firm, name).value
        return ValueError(f"{self.contra_firm} not found!")
    # endregion
