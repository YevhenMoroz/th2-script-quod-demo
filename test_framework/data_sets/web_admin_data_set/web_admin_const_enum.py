from enum import Enum


class WebAdminUsers(Enum):
    user_1 = "adm03"
    user_2 = "adm_loca"
    user_3 = "adm_desk"
    user_4 = "adm01"
    user_5 = "adm02"
    user_6 = "acameron"
    user_7 = "gbarett"


class WebAdminPasswords(Enum):
    password_1 = "adm03"
    password_2 = "adm02"


# region WaGeneral
class WebAdminComponentId(Enum):
    component_id_1 = "SATS"


class WebAdminAdminCommands(Enum):
    admin_command_1 = "ChangeLogLevel"


# endregion

# region WaSite
class WebAdminInstitutions(Enum):
    institution_1 = "QUOD FINANCIAL"
    institution_2 = "LOAD"


class WebAdminDesks(Enum):
    desk_1 = "DESK A"
    desk_2 = "DESK-C"
    desk_3 = "Quod Desk"


class WebAdminLocations(Enum):
    location_1 = "EAST-LOCATION-B"
    location_2 = "WEST-LOCATION-B"
    location_3 = "EAST-LOCATION-A"


class WebAdminZones(Enum):
    zone_1 = "WEST-ZONE"
    zone_2 = "EAST-ZONE"


# endregion

# region WaUsers
class WebAdminClients(Enum):
    client_1 = "CLIENT1"


class WebAdminClientType(Enum):
    client_type_1 = "Holder"


class WebAdminVenues(Enum):
    venue_1 = "AMEX"
    venue_2 = "ASE"
    venue_3 = "BRU"
    venue_4 = "AMSTERDAM"
    venue_5 = "BATS"


class WebAdminEmail(Enum):
    email_1 = "test"


class WebAdminPermRole(Enum):
    perm_role_1 = "Permissions for FIX Clients"


class WebAdminFirstUserName(Enum):
    first_user_name_1 = "George"


# endregion


# region WAReferenceData
class WebAdminVenueId(Enum):
    venue_id_1 = "15"


class WebAdminVenueType(Enum):
    venue_type_1 = "DarkPool"


class WebAdminMic(Enum):
    mic_1 = "ALTX"
    mic_2 = "ALXA"
    mic_3 = "ALXP"


class WebAdminCountry(Enum):
    country_1 = "Albania"
    country_2 = "Angola"



class WebAdminSubVenue(Enum):
    sub_venue_1 = "Forward"


class WebAdminTradingStatus(Enum):
    trading_status_1 = "Suspended"


class WebAdminTradingPhase(Enum):
    trading_phase_1 = "201"
    trading_phase_2 = "Regular"
    trading_phase_3 = "Auction"


class WebAdminTradingPhaseProfile(Enum):
    trading_phase_profile_1 = "JSE"


class WebAdminPriceLimitProfile(Enum):
    price_limit_profile_1 = "test"


class WebAdminTickSizeProfile(Enum):
    tick_size_profile_1 = "0.000000010"


class WebAdminTickSizeXaxisType(Enum):
    tick_size_xaxis_type_1 = "Price"


class WebAdminInstrSymbol(Enum):
    instr_symbol_1 = "AUD/DKK"
    instr_symbol_2 = "EUR/USD"

class WebAdminSymbol(Enum):
    symbol_1 = "EUR/USD"

class WebAdminCurrency(Enum):
    currency_1 = "AFN"
    currency_2 = "AED"

class WebAdminInstrType(Enum):
    instr_type_1 = "Bond"
    instr_type_2 = "FXNDF"
    instr_type_3 = "FXForward"
    instr_type_4 = "DepositLoanLeg"
    instr_type_5 = "Future"
    instr_type_6 = "Forward"
    instr_type_7 = "Option"

class WebAdminPreferredVenue(Enum):
    preferred_venue_1 = "AMEX"
    preferred_venue_2 = "ADX"
    preferred_venue_3 = "BAueTS"

class WebAdminListingGroup(Enum):
    listing_group_1 = "test"

class WebAdminSettleType(Enum):
    settle_type_1 = "BrokenDate"

class WebAdminFeedSource(Enum):
    feed_source_1 = "ActivFinancial"
    feed_source_2 = "FeedOS"
    feed_source_3 = "Inte raciveData"
    feed_source_4 = "MarketPrizm"
    feed_source_5 = "Native Market"
    feed_source_6 = "Quod simulator"
    feed_source_7 = "RMDS"
    feed_source_8 = "ADX"

class WebAdminNegativeRoutes(Enum):
    negative_route_1 = "Direct"
    negative_route_2 = "Fixed income Route"

class WebAdminPositiveRoutes(Enum):
    positive_route_1 = "Credit Suisse"
    positive_route_2 = "JP Morgan"
# endregion
