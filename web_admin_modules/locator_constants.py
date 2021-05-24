class SidebarTabTitle(str):
    GENERAL = 'General'
    SETTINGS = 'Settings'
    MD_ENTITLEMENTS = 'MDEntitlements'
    ADMIN_COMMAND = 'AdminCommand'

    USERS = 'Users'
    USER_SESSIONS = 'User Sessions'
    DESKS = 'User Desks'

    REFERENCE_DATA = 'Reference Data'
    VENUES = 'Venues'
    SUB_VENUES = 'SubVenues'
    LISTING_GROUPS = 'ListingGroups'
    LISTINGS = 'Listings'
    RECOVER_HISTORICAL_VOLUME = 'Recover Historical Volume'
    INSTR_SYMBOL_INFO = 'InstrSymbolInfo'
    INSTRUMENT_GROUP = 'Instrument Group'
    INSTRUMENT_LIST = 'Instrument List'

    CLIENT_AND_ACCOUNTS = 'Client/Accounts'
    ACCOUNTS = 'Accounts'
    WASH_BOOK = 'WashBook'
    WASH_BOOK_RULES = 'WashBook Rules'
    CLIENTS = 'Clients'
    CLIENT_GROUPS = 'ClientGroups'
    CLIENT_LIST = 'Client List'
    CASH_ACCOUNTS = 'CashAccounts'
    CLIENT_CLIENT_GROUPS = 'ClientClientGroups'

    ORDER_MANAGEMENT = 'Order Management'
    EXECUTION_STRATEGIES = 'Execution Strategies'
    ORDER_MANAGEMENT_RULES = 'Order Management Rules'

    MIDDLE_OFFICE = 'Middle Office'
    FEES = 'Fees'
    COMMISSIONS = 'Commissions'
    SETTLEMENT_MODEL = 'Settlement Model'
    FIX_MATCHING_PROFILE = 'FIX Matching Profile'

    FX_MARKET_MAKING = 'FX Market Making'
    QUOTING_SESSIONS = 'Quoting Sessions'
    CLIENT_TIER = 'Client Tier'
    AUTO_HEDGER = 'Auto Hedger'

    PRICE_CLEANSING = 'Price Cleansing'
    CROSSED_VENUE_RATES = 'Crossed Venue Rates'
    STALE_RATES = 'Stale Rates'
    RATES_FOLLOWING_TRADES = 'Rates Following Trades'
    UNBALANCED_RATES = 'Unbalanced Rates'

    RISK_LIMITS = 'Risk Limits'
    TRADING_LIMITS = 'TradingLimits'
    CUM_TRADING_LIMITS = 'CumTradingLimits'
    LISTING_CUM_TRD_LMT_COUNTER = 'Listing CumTrdLmt Counter'
    CUM_TRD_LMT_COUNTER = 'CumTrdLmt Counter'
    POSITION_LIMITS = 'PositionLimits'
    FX_POSITION_LIMITS = 'FX PositionLimits'
    PRICE_TOLERANCE_CONTROL = 'Price Tolerance Control'
    EXTERNAL_CHECK = 'External Check'

    POSITIONS = 'Positions'
    SECURITY_POSITIONS = 'Security Positions'
    FX_POSITIONS = 'FX Positions'

    OTHERS = 'Others'
    COUNTERPARTS = 'Counterparts'
    INSTITUTIONS = 'Institutions'
    MARKET_DATA_SOURCE = 'Market Data Source'
    ROUTES = 'Routes'
    USER_INSTR_SYMB_BLACK_OUT = 'User Instr Symb Black Out'


class InputText(str):
    NAME_REQ = 'Name *'
    VENUE_REQ = 'Venue *'
    SUB_VENUE_REQ = 'SubVenue *'


class ButtonText(str):
    NEW = 'New'
    OK = 'Ok'
    SAVE_CHANGES = 'Save Changes'
    CLEAR_CHANGES = 'Clear Changes'


class EventText(str):
    SUB_VENUE_CHANGES_SUCCESS = 'SubVenue changes saved'
    LISTING_GROUP_CHANGES_SUCCESS = 'ListingGroup changes saved'

    @staticmethod
    def sub_venue_deleted(sub_venue_name: str):
        return f'SubVenue {sub_venue_name} Deleted'

    @staticmethod
    def listing_group_deleted(listing_group_name: str):
        return f'Listing Group {listing_group_name} Deleted'


class FilterFieldName(str):
    NAME = 'Name'
    EXT_ID_VENUE = 'Ext ID Venue'
    VENUE = 'Venue'
    MARKET_DATA_SOURCE = 'Market Data Source'
    DEFAULT_SYMBOL = 'Default Symbol'
    NEWS = 'News'
    NEWS_SYMBOL = 'News Symbol'


class TooltipAction(str):
    EDIT = 'Edit'
    CLONE = 'Clone'
    DELETE = 'Delete'
    DOWNLOAD_PDF = 'Download PDF'


class CreationEntityHeaderText(str):
    SUB_COUNTERPARTS = 'Sub counterparts'
    PARTY_ROLES = 'Party roles'
