from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.web_admin_data_set.web_admin_const_enum import WebAdminUsers, \
    WebAdminPasswords, WebAdminComponentId, WebAdminAdminCommands, WebAdminDesks, \
    WebAdminZones, WebAdminLocations, WebAdminInstitutions, WebAdminClients, WebAdminClientType, WebAdminVenues, \
    WebAdminEmail, WebAdminPermRole, WebAdminFirstUserName, WebAdminVenueId, WebAdminVenueType, WebAdminMic, \
    WebAdminCountry, WebAdminSubVenue, WebAdminTradingStatus, WebAdminTradingPhase, WebAdminPriceLimitProfile, \
    WebAdminTickSizeProfile, WebAdminTradingPhaseProfile, WebAdminTickSizeXaxisType, WebAdminInstrSymbol, \
    WebAdminSymbol, WebAdminCurrency, WebAdminInstrType, WebAdminPreferredVenue, WebAdminListingGroup, \
    WebAdminSettleType, WebAdminFeedSource, WebAdminNegativeRoutes, WebAdminPositiveRoutes


class WebAdminDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    user = WebAdminUsers
    password = WebAdminPasswords
    component_id = WebAdminComponentId
    admin_command = WebAdminAdminCommands
    desk = WebAdminDesks
    location = WebAdminLocations
    institution = WebAdminInstitutions
    zone = WebAdminZones
    client = WebAdminClients
    client_type = WebAdminClientType
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
    symbol = WebAdminSymbol
    currency = WebAdminCurrency
    instr_type = WebAdminInstrType
    preferred_venue = WebAdminPreferredVenue
    listing_group = WebAdminListingGroup
    settle_type = WebAdminSettleType
    feed_source = WebAdminFeedSource
    negative_route = WebAdminNegativeRoutes
    positive_route = WebAdminPositiveRoutes
