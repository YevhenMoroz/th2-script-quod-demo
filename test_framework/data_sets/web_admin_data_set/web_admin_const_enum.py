from enum import Enum


class WebAdminUsers(Enum):
    user_1 = "adm03"
    user_2 = "adm_loca"
    user_3 = "adm_desk"
    user_4 = "adm01"
    user_5 = "adm02"
    user_6 = "acameron"
    user_7 = "gbarrett"
    user_8 = "QA1"
    user_9 = "adm08"
    user_10 = "adm07"


class WebAdminPasswords(Enum):
    password_1 = "adm03"
    password_2 = "adm02"


# region WaGeneral
class WebAdminComponentId(Enum):
    component_id_1 = "SATS"


class WebAdminSystemCommands(Enum):
    system_command_1 = "ChangeLogLevel"


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
    client_2 = "CLIENT2"
    client_3 = "CLIENT3"
    client_4 = "BrokerACA"
    client_5 = "QAP5913"
    client_6 = "QAP6706"


class WebAdminClientType(Enum):
    client_type_1 = "Holder"


class WebAdminVenues(Enum):
    venue_1 = "AMEX"
    venue_2 = "ASE"
    venue_3 = "BRU"
    venue_4 = "AMSTERDAM"
    venue_5 = "BATS"
    venue_6 = "ADX"
    venue_7 = "Equiduct"
    venue_8 = "AMERICAN STOCK EXCHANGE"
    venue_9 = "EURONEXT AMSTERDAM"
    venue_10 = "BINANCE"
    venue_11 = "Dubai Financial Exchange"


class WebAdminEmail(Enum):
    email_1 = "test@test"


class WebAdminPermRole(Enum):
    perm_role_1 = "Permissions for FIX Clients"
    perm_role_2 = "Permissions for Head of Sale-Dealers role"


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
    instr_symbol_3 = "AUD/CAD"
    instr_symbol_4 = "AUD/HUF"


class WebAdminSymbol(Enum):
    symbol_1 = "EUR/USD"
    symbol_2 = "AUD/CAD"
    symbol_3 = "AUD/TRY"
    symbol_4 = "AUD/BRL"
    symbol_5 = "AUD/USD"
    symbol_6 = "EUR/PHP"


class WebAdminCurrency(Enum):
    currency_1 = "AFN"
    currency_2 = "AED"
    currency_3 = "EUR"


class WebAdminInstrType(Enum):
    instr_type_1 = "Bond"
    instr_type_2 = "FXNDF"
    instr_type_3 = "FXForward"
    instr_type_4 = "DepositLoanLeg"
    instr_type_5 = "Future"
    instr_type_6 = "Forward"
    instr_type_7 = "Option"
    instr_type_8 = "Certificate"
    instr_type_9 = "Equity"


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
    feed_source_3 = "InteraciveData"
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

# region WAClientAccounts

class WebAdminClientIdSource(Enum):
    client_id_source_1 = "BIC"
    client_id_source_2 = "Other"


class WebAdminRouteAccountName(Enum):
    route_account_name_1 = ""


class WebAdminRoute(Enum):
    route_1 = "JP Morgan"
    route_2 = "DB RFQ"


class WebAdminClearingAccountType(Enum):
    clearing_account_type_1 = "Institutional"
    clearing_account_type_2 = "Firm"
    clearing_account_type_3 = "Retail"


class WebAdminDiscloseExec(Enum):
    disclose_exec_1 = "Manual"


class WebAdminAccountIdSource(Enum):
    account_id_source_1 = "BIC"
    account_id_source_2 = "Other"


class WebAdminDefaultRoute(Enum):
    default_route_1 = "Direct"


class WebAdminDefaultExecutionStrategy(Enum):
    default_execution_strategy_1 = "Default"


class WebAdminTradConfirmGeneration(Enum):
    trade_confirm_generation_1 = "Automatic"


class WebAdminTradConfirmPreference(Enum):
    trade_confirm_preference_1 = "Excel"


class WebAdminNetGrossIndType(Enum):
    net_gross_ind_type_1 = "Net"


class WebAdminRecipientTypes(Enum):
    recipient_type_1 = "CC"


# endregion

# region WaOrderManagement
class WebAdminDefaultTif(Enum):
    default_tif_1 = "Day"


class WebAdminStrategyType(Enum):
    strategy_type_1 = "Quod MultiListing"
    strategy_type_2 = "External AMBUSH"
    strategy_type_3 = "Quod LitDark"
    strategy_type_4 = "External CUSTOM1"
    strategy_type_5 = "Quod DarkPool"
    strategy_type_6 = "Quod TWAP"
    strategy_type_7 = "Custom one"
    strategy_type_8 = "Quod Auction"
    strategy_type_9 = "Quod Synthetic OrdType"


class WebAdminExecPolicy(Enum):
    exec_policy_1 = "Care"
    exec_policy_2 = "DMA"
    exec_policy_3 = "ExternalCare"
    exec_policy_4 = "Algorithmic"
    exec_policy_5 = "SOR"
    exec_policy_6 = "ExternalAlgo"


# endregion

# region WaMiddleOffice

class WebAdminCommissionAmountType(Enum):
    commission_amount_type_1 = "Broker"


class WebAdminCommissionProfile(Enum):
    commission_profile_1 = "UK stamp"


class WebAdminSettlLocation(Enum):
    settl_location_1 = "CASH"
    settl_location_2 = "CAMBIUM"


class WebAdminCountryCode(Enum):
    country_code_1 = "ABW"
    country_code_2 = "AIA"


class WebAdminClientGroup(Enum):
    client_group_1 = "DEMO"
    client_group_2 = "Kepler"
    client_group_3 = "test"


class WebAdminInstrument(Enum):
    instrument_1 = "EUR"
    instrument_2 = "INSURANCE"


class WebAdminInstrumentGroup(Enum):
    instrument_group_1 = "TC Danish"
    instrument_group_2 = "TC Instr Grp"


class WebAdminClientList(Enum):
    client_list_1 = "WEILRG"
    client_list_2 = "test"


class WebAdminCommAlgorithm(Enum):
    comm_algorithm_1 = "Flat"
    comm_algorithm_2 = "SlidingScale"


class WebAdminCommType(Enum):
    comm_type_1 = "Percentage"
    comm_type_2 = "AbsoluteAmount"


class WebAdminTenor(Enum):
    tenor_1 = "Spot"
    tenor_2 = "1W"


class WebAdminCoreSpotPriceStrategy(Enum):
    core_spot_price_strategy_1 = "VWAPPriceOptimized"
    core_spot_price_strategy_2 = "VWAPSpeedOptimized"
    core_spot_price_strategy_3 = "Direct"


class WebAdminPartyRole(Enum):
    party_role_1 = "Exchange"
    party_role_2 = "GiveupClearingFirm"

# endregion
