from enum import Enum
from xml.etree import ElementTree

from stubs import ROOT_DIR


def find_target_server():
    tree = ElementTree.parse(f"{ROOT_DIR}/regression_run_config.xml")
    root = tree.getroot()
    target_server = root.find(f".//target_server_win").text
    return target_server


class Connectivity(Enum):
    Ganymede_316_Feed_Handler = 'fix-feed-handler-316-ganymede'
    Ganymede_316_Sell_Side = 'fix-sell-side-316-ganymede'
    Ganymede_316_Buy_Side = 'fix-buy-side-316-ganymede'
    Ganymede_316_Buy_Side_Redburn = 'fix-buy-side-316-ganymede-redburn'
    Ganymede_316_Sell_Side_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_316_web_admin_site = 'rest_wa316ganymede'
    Ganymede_317_ss = 'fix-sell-317-standard-test'
    Ganymede_317_bs = 'fix-buy-317-standard-test'
    Ganymede_317_dc = 'fix-sell-317-backoffice'
    Ganymede_317_wa = "rest_wa317ganymede"
    Luna_314_ss_rfq = 'fix-ss-rfq-314-luna-standard'
    Luna_314_bs_md = 'fix-sell-md-t-314-stand'
    Luna_314_bs_rfq = 'fix-bs-rfq-314-luna-standard'
    Luna_314_ss_esp = 'fix-sell-esp-m-314luna-stand'
    Luna_314_Feed_Handler = 'fix-fh-314-luna'
    Luna_314_Feed_Handler_Q = 'fix-fh-q-314-luna'
    Luna_314_ss_esp_t = 'fix-sell-esp-t-314-stand'
    Luna_314_dc = 'fix-sell-m-314luna-drop'
    Luna_314_cnx = 'fix-sell-rfq-m-314-cnx'
    Luna_314_wa = "rest_wa314luna"
    Luna_314_ja = "314_java_api"
    Luna_314_ev = "fix-buy-extern-314-stand"
    Luna_315_web_admin = 'rest_wa315luna'
    Luna_315_web_admin_site = 'rest_wa315luna_site_admin'
    Luna_315_desktop_trading_http = 'rest_trading_desktop315luna'
    Luna_315_desktop_trading_web_socket = 'api_session_desktop315luna'
    Luna_315_web_trading_http = 'rest_wt315luna'
    Luna_315_web_trading_web_socket = 'api_session_315luna'
    Ganymede_317_ja = '317_java_api'
    Ganymede_317_als_email_report = 'log317-als-email-report'
    Ganymede_317_ors_report = "log317-ors-report"
    Columbia_310_Feed_Handler = 'fix-fh-310-columbia'
    Columbia_310_Sell_Side = 'fix-ss-310-columbia-standart'
    Columbia_310_Buy_Side = 'fix-bs-310-columbia'
    Kuiper_320_web_admin = 'rest_wa320kuiper'
    Kuiper_320_web_admin_site = 'rest_wa320kuiper_site_admin'
    Kuiper_320_web_trading_http = 'rest_wt320kuiper'
    Kuiper_320_web_trading_web_socket = 'api_session_320kuiper'
    Kepler_319_Sell_Side = 'fix-sell-side-319-kepler'
    Kepler_319_Buy_Side = 'fix-buy-side-319-kepler'
    Kuiper_319_Feed_Handler = 'fix-feed-handler-319-kuiper'
    Kuiper_319_web_admin_site = 'rest_wa319kuiper'
    Kratos_309_ss_rfq = 'fix-sell-rfq-m-309kratos-stand'
    Kratos_309_ss_esp = 'fix-sell-esp-m-309kratos-stand'
    Kratos_309_Feed_Handler = 'fix-fh-309-kratos'



class FrontEnd(Enum):
    # 317 site
    USERS_317 = [""]
    PASSWORDS_317 = [""]
    FOLDER_317 = ""
    DESKS_317 = ["Desk of Order Book", "Desk of Middle Office"]
    DESKS_ID_317 = [9, 10]
    MAIN_WIN_NAME_317 = "Quod Financial - 317 GANYMEDE"
    LOGIN_WIN_NAME_317 = "Login to Quod Financial (317 GANYMEDE) "
    # common values
    EXE_NAME = "QuodFrontEnd.exe"
    # target_server values
    TARGET_SERVER_WIN = find_target_server()

    # region quod314
    USERS_314 = ["QA1"]
    PASSWORDS_314 = ["QA1"]
    FOLDER_314 = ""
    DESKS_314 = ["Q"]
    MAIN_WIN_NAME_314 = "Quod Financial - Quod site 314"
    LOGIN_WIN_NAME_314 = "Login to Quod Financial (Quod site 314)"
    # common values
    # target_server values
    TARGET_SERVER_WIN_OSTRONOV = "quod_11q"
    # endregion

    # region quod310
    USERS_310 = ["HD5"]
    PASSWORDS_310 = ["HD5"]
    FOLDER_310 = ""
    DESKS_310 = ["Q"]
    MAIN_WIN_NAME_310 = "Quod Financial - Quod site"
    LOGIN_WIN_NAME_310 = "Login to Quod Financial (Quod site)"
    # endregion

class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class GatewaySide(Enum):
    Sell = "Sell"
    Buy = "Buy"
    RBSell = "RBSell"

class Aggressivity(Enum):
    Passive = '1'
    Neutral = '2'
    Aggressive = '3'

class MessageType(Enum):
    NewOrderSingle = "NewOrderSingle"
    NewOrderMultiLeg = "NewOrderMultileg"
    ExecutionReport = "ExecutionReport"
    OrderCancelReplaceRequest = "OrderCancelReplaceRequest"
    OrderCancelRequest = "OrderCancelRequest"
    MarketDataRequest = "MarketDataRequest"
    MarketDataIncrementalRefresh = "MarketDataIncrementalRefresh"
    MarketDataSnapshotFullRefresh = "MarketDataSnapshotFullRefresh"
    NewOrderList = "NewOrderList"
    ListStatus = "ListStatus"
    QuoteRequest = "QuoteRequest"
    Quote = "Quote"
    Confirmation = "Confirmation"
    AllocationInstruction = "AllocationInstruction"
    QuoteCancel = "QuoteCancel"


class Status(Enum):
    Pending = "Pending"
    New = "New"
    Fill = "Fill"
    PartialFill = "PartialFill"
    Reject = "Reject"
    CancelReplace = "CancelReplace"
    Cancel = "Cancel"
    Eliminate = "Eliminate"


class OrdStatus(Enum):
    PendingNew = "A"
    New = "0"
    PartiallyFilled = "1"
    Fill = "2"
    CanceledOrEliminated = "4"
    Rejected = "8"


class Reference(Enum):
    LastTradePrice = 'LTP'
    Primary = 'PRM'
    Market = 'MKT'
    Mid = 'MID'
    Open = 'OPN'
    Close = 'CLO'
    DayHight = 'DHI'
    DayLow = 'DLO'
    Manual = 'MAN'
    Limit = 'LMT'


class TimeInForce(Enum):
    Day = 0
    GoodTillCancel = 1
    AtTheOpening = 2
    ImmediateOrCancel = 3
    FillOrKill = 4
    GoodTillCrossing = 5
    GoodTillDate = 6
    AtTheClose = 7
    ValidForAuction = 100


class ClientAlgoPolicy(Enum):
    qa_mpdark = "QA_Auto_MPDark"
    qa_mpdark_2 = "QA_Auto_MPDark2"
    qa_mpdark_3 = "QA_Auto_MPDark3"
    qa_mpdark_4 = "QA_Auto_MPDark4"
    qa_mpdark_5 = "QA_Auto_MPDark5"
    qa_mpdark_6 = "QA_Auto_MPDark6"
    qa_mpdark_7 = "QA_Auto_MPDark7"
    qa_mpdark_8 = "QA_Auto_MPDark8"
    qa_mpdark_11 = "QA_Auto_MPDark11"
    qa_mpdark_12 = "QA_Auto_MPDark12"
    qa_sorping = "QA_SORPING"
    qa_sorping_1 = "QA_Auto_SORPING_1"
    qa_sorping_2 = "QA_Auto_SORPING_2"
    qa_sorping_3 = "QA_Auto_SORPING_3"
    qa_sorping_4 = "QA_Auto_SORPING_4"
    qa_sorping_5 = "QA_Auto_SORPING_5"
    qa_sorping_6 = "QA_Auto_SORPING_6"
    qa_sorping_7 = "QA_Auto_SORPING_7"
    qa_sorping_8 = "QA_Auto_SORPING_8"
    qa_sorping_9 = "QA_Auto_SORPING_9"
    qa_sorping_10 = "QA_Auto_SORPING_10"
    qa_sorping_11 = "QA_Auto_SORPING_11"
    qa_sorping_12 = "QA_Auto_SORPING_12"
    qa_sorping_13 = "QA_Auto_SORPING_13"
    qa_multiple_y = 'QA_Auto_SORPING_ME_Y'
    qa_multiple_n = 'QA_Auto_SORPING_ME_N'
    qa_iceberg = 'QA_Auto_ICEBERG'


class OrderType(Enum):
    Market = 1
    Limit = 2
    Stop = 3
    StopLimit = 4
    PreviouslyQuoted = "D"


class TargetStrategy(Enum):
    VWAP = '1'
    Participate = '2'
    SynthStop = '1001'
    SynthTIF = '1003'
    Iceberg = '1004'
    TWAP = '1005'
    Multilisted = '1008'
    SynthPeg = '1009'
    DarkPool = '1010'
    LitDark = '1011'
    SynthBlock = '1019'


class Custom(Enum):
    Passive = 'Passive'

class OrderSide(Enum):
    Buy = 1
    Sell = 2


class AlgoCurrencyRate(Enum):
    eur_to_sek = "9.960000000"


class Venues(Enum):
    chixlis = "CHIXLIS"
    paris = "Euronext Paris"


class PartyID(Enum):
    party_id_1 = "TestCLIENTACCOUNT"
    party_id_2 = "TestClientAccount"
    party_id_3 = "TestEXTERNAL-UTI"
    party_id_4 = "TestINITIATOR-UTI"
    party_id_5 = "12345678"
    party_id_6 = "18831"
    party_id_7 = "10000"
    party_id_8 = "TestClientID"
    party_id_9 = "TestTraderID"
    party_id_10 = "TestTraderName"



class PartyIDSource(Enum):
    party_id_source_1 = "D"
    party_id_source_2 = "P"


class PartyRole(Enum):
    party_role_3 = "3"
    party_role_11 = "11"
    party_role_12 = "12"
    party_role_24 = "24"
    party_role_58 = "58"
    party_role_55 = "55"


class MiscNumber(Enum):
    ordr_misc_0 = "OrdrMisc0"
    ordr_misc_1 = "OrdrMisc1"
    ordr_misc_2 = "OrdrMisc2"
    ordr_misc_3 = "OrdrMisc3"
    ordr_misc_5 = "OrdrMisc5"
    ordr_misc_6 = "OrdrMisc6"
    ordr_misc_7 = "OrdrMisc7"
    ordr_misc_8 = "OrdrMisc8"


class Symbol(Enum):
    symbol_1 = 'DE0005489561'
    symbol_2 = 'BE0020575115'


class SecurityID(Enum):
    security_id_1 = 'DE0005489561'
    security_id_2 = '2681'
    security_id_3 = 'BE0020575115'


class SecurityIDSource(Enum):
    sids_4 = 4
    sids_8 = 8


class SecurityType(Enum):
    cs = 'CS'


class TransactionStatus(Enum):
    new = "New"
    open = "Open"
    canceled = "Cancelled"


class ReadLogVerifiers(Enum):
    log_319_updating_status = "log319-updating-status"
    log_319_cancel_child = "log319-cancel-child"
    log_319_check_primary_listing = "log319-check-primary-listing"
    log_319_check_party_info = "log319-check-party-info"
    log_319_check_party_info_v2 = "log319-check-party-info-v2"
    log_319_check_tags_5052_and_207_mapping = "log319-check-tags-5052-and-207-mapping"
    log_319_check_that_venue_was_suspended = "log319-check-that-venue-was-suspended"
    log_319_check_that_lis_phase_is_skipping = "log319-check-that-lis-phase-is-skipping"
    log_319_check_the_currency_rate = "log319-check-the-currency-rate"
    log_319_check_the_lis_amount = "log319-check-the-lis-amount"
    log319_check_party_info_more_than_one_group = "log319-check-party-info-more-than-one-group"
    log319_check_party_info_for_three_groups_sell_side = "log319-check-party-info-for-three-groups-sell-side"
    log319_check_party_info_for_three_groups_buy_side = "log319-check-party-info-for-three-groups-buy-side"
    log319_check_party_info_for_the_one_group_sell_side = "log319-check-party-info-for-the-one-group-sell-side"
    log319_check_party_info_for_the_one_group_buy_side = "log319-check-party-info-for-the-one-group-buy-side"
    log319_check_tag_5047 = "log319-check-tag-5047"
    log319_check_tag_5048 = "log319-check-tag-5048"
    log319_check_tag_1 = "log319-check-tag-1"
    log_319_check_that_is_no_suitablle_liquidity = "log319-check-that-is-no-suitable-liquidity"
    log_319_check_transact_time_for_child = "log319-check-transact-time-for-child"
    log_319_check_settl_date_part_1 = "log319-check-settl-date-part-1"
    log_319_check_settl_date_part_2 = "log319-check-settl-date-part-2"
    log_319_check_settl_date_part_3 = "log319-check-settl-date-part-3"
    log_319_check_party_info_sell_side = "log319-check-party-info-sell-side"
    log_319_check_party_info_buy_side = "log319-check-party-info-buy-side"
    log_319_check_not_crossing_mid_price = "log319-check-not-crossing-mid-price"
    log_319_check_starting_mid_price_monitoring = "log319-check-starting-mid-price-monitoring"
    log_319_check_market_event_for_venue = "log319-check-market-event-for-venue"


class WebAdminURL(Enum):
    saturn_306 = "http://10.0.22.38:3480/adm/saturn/#/auth/login"


class WebBrowser(Enum):
    chrome = "chrome"
    firefox = "firefox"


class WebTradingURL(Enum):
    luna_315 = "http://10.0.22.38:6680/quodtrading/qakharkiv315Trading/#/signin"
    kuiper_320 = "http://10.0.22.38:6780/quodtrading/qakharkiv320Trading/#/signin"


class SshClientEnv(Enum):
    HOST_317 = "10.0.22.35"
    PORT_317 = 22
    USER_317 = ""
    PASSWORD_317 = ""
    SU_USER_317 = "quod317"
    SU_PASSWORD_317 = "quod317"


class FreeNotesReject(Enum):
    MissWouldPriceReference = "missing WouldPriceReference"
    MissLimitPriceReference = "missing LimitPriceReference"
    MissNavigatorLimitPriceReference = "missing NavigatorLimitPriceReference"
    MissNavigatorLimitPrice = "missing Limit price for Navigator"
    InvalidMaxParticipation = "invalid value for MaxParticipation"
    InvalidPercentageOfVolume = "invalid value for percentage of volume"
    InvalidPricePoint1Participation = "invalid value for PricePoint1Participation"
    InvalidPricePoint2Participation = "invalid value for PricePoint2Participation"
    ReachedMaximumNumberOfAllowedChildOrders = "reached maximum number of allowed child orders"

class TradingPhases(Enum):
    Auction = "AUC"
    Closed = "CLO"
    Open = "OPN"
    PreClosed = "PCL"
    PreOpen = "POP"
    Expiry = "EXA"
    AtLast = "TAL"
