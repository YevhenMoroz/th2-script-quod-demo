from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.web_admin_data_set.web_admin_const_enum import WebAdminUsers, \
    WebAdminPasswords, WebAdminComponentId, WebAdminSystemCommands, WebAdminDesks, \
    WebAdminZones, WebAdminLocations, WebAdminInstitutions, WebAdminClients, WebAdminClientType, WebAdminVenues, \
    WebAdminEmail, WebAdminPermRole, WebAdminFirstUserName, WebAdminVenueId, WebAdminVenueType, WebAdminMic, \
    WebAdminCountry, WebAdminSubVenue, WebAdminTradingStatus, WebAdminTradingPhase, WebAdminPriceLimitProfile, \
    WebAdminTickSizeProfile, WebAdminTradingPhaseProfile, WebAdminTickSizeXaxisType, WebAdminInstrSymbol, \
    WebAdminSymbol, WebAdminCurrency, WebAdminInstrType, WebAdminPreferredVenue, WebAdminListingGroup, \
    WebAdminSettleType, WebAdminFeedSource, WebAdminNegativeRoutes, WebAdminPositiveRoutes, WebAdminClientIdSource, \
    WebAdminRouteAccountName, WebAdminRoute, WebAdminClearingAccountType, WebAdminDiscloseExec, WebAdminAccountIdSource, \
    WebAdminDefaultRoute, WebAdminDefaultExecutionStrategy, WebAdminTradConfirmGeneration, \
    WebAdminTradConfirmPreference, WebAdminNetGrossIndType, WebAdminRecipientTypes, WebAdminDefaultTif, \
    WebAdminStrategyType, WebAdminExecPolicy, WebAdminCommissionAmountType, WebAdminCommissionProfile, \
    WebAdminSettlLocation, WebAdminCountryCode, WebAdminClientGroup, WebAdminInstrument, WebAdminInstrumentGroup, \
    WebAdminCommAlgorithm, WebAdminCommType, WebAdminTenor, WebAdminCoreSpotPriceStrategy, WebAdminPartyRole, \
    WebAdminClientList, WebAdminCounterpart


class WebAdminDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    user = WebAdminUsers
    password = WebAdminPasswords
    component_id = WebAdminComponentId
    system_command = WebAdminSystemCommands
    desk = WebAdminDesks
    location = WebAdminLocations
    institution = WebAdminInstitutions
    zone = WebAdminZones
    clients = WebAdminClients
    client_type = WebAdminClientType
    client_list = WebAdminClientList
    venues = WebAdminVenues
    email = WebAdminEmail
    perm_role = WebAdminPermRole
    first_user_name = WebAdminFirstUserName
    venue_id = WebAdminVenueId
    venue_type = WebAdminVenueType
    mic = WebAdminMic
    country = WebAdminCountry
    sub_venue = WebAdminSubVenue
    trading_status = WebAdminTradingStatus
    trading_phase = WebAdminTradingPhase
    price_limit_profile = WebAdminPriceLimitProfile
    tick_size_profile = WebAdminTickSizeProfile
    trading_phase_profile = WebAdminTradingPhaseProfile
    tick_size_xaxis_type = WebAdminTickSizeXaxisType
    instr_symbol = WebAdminInstrSymbol
    symbols = WebAdminSymbol
    currency = WebAdminCurrency
    instr_type = WebAdminInstrType
    preferred_venue = WebAdminPreferredVenue
    listing_group = WebAdminListingGroup
    settle_types = WebAdminSettleType
    feed_source = WebAdminFeedSource
    negative_route = WebAdminNegativeRoutes
    positive_route = WebAdminPositiveRoutes
    client_id_source = WebAdminClientIdSource
    route_account_name = WebAdminRouteAccountName
    routes = WebAdminRoute
    clearing_account_type = WebAdminClearingAccountType
    disclose_exec = WebAdminDiscloseExec
    account_id_source = WebAdminAccountIdSource
    default_route = WebAdminDefaultRoute
    default_execution_strategy = WebAdminDefaultExecutionStrategy
    trade_confirm_generation = WebAdminTradConfirmGeneration
    trade_confirm_preference = WebAdminTradConfirmPreference
    net_gross_ind_type = WebAdminNetGrossIndType
    recipient_type = WebAdminRecipientTypes
    default_tif = WebAdminDefaultTif
    strategy_type = WebAdminStrategyType
    exec_policy = WebAdminExecPolicy
    commission_amount_type = WebAdminCommissionAmountType
    commission_profiles = WebAdminCommissionProfile
    settl_location = WebAdminSettlLocation
    country_code = WebAdminCountryCode
    client_group = WebAdminClientGroup
    instrument = WebAdminInstrument
    instrument_group = WebAdminInstrumentGroup
    comm_algorithm = WebAdminCommAlgorithm
    comm_type = WebAdminCommType
    tenors = WebAdminTenor
    core_spot_price_strategy = WebAdminCoreSpotPriceStrategy
    party_role = WebAdminPartyRole
    counterpart = WebAdminCounterpart
