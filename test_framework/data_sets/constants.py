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
    Ganymede_316_Redburn = 'fix-sell-side-316-gnmd-rb'
    Ganymede_317_ss = 'fix-sell-317-standard-test'
    Ganymede_317_bs = 'fix-buy-317-standard-test'
    Ganymede_317_dc = 'fix-sell-317-backoffice'
    Ganymede_317_wa = "rest_wa317ganymede"
    Luna_314_ss_rfq = 'fix-ss-rfq-314-luna-standard'
    Luna_314_bs_rfq = 'fix-bs-rfq-314-luna-standard'
    Luna_314_ss_esp = 'fix-sell-esp-m-314luna-stand'
    Luna_314_Feed_Handler = 'fix-fh-314-luna'
    Luna_314_Feed_Handler_Q = 'fix-fh-q-314-luna'
    Luna_314_ss_esp_t = 'fix-sell-esp-t-314-stand'
    Luna_314_dc = 'fix-sell-m-314luna-drop'
    Luna_314_wa = "rest_wa314luna"
    Luna_315_web_admin = 'rest_wa315luna'
    Luna_315_desktop_trading_http = 'rest_trading_desktop315luna'
    Luna_315_desktop_trading_web_socket = 'api_session_desktop315luna'
    Ganymede_317_ja = '317_java_api'
    Ganymede_317_als_email_report = 'log317-als-email-report'
    Columbia_310_Feed_Handler = 'fix-fh-310-columbia'
    Columbia_310_Sell_Side = 'fix-ss-310-columbia-standart'
    Columbia_310_Buy_Side = 'fix-bs-310-columbia'
    Kuiper_320_web_admin = 'rest_wa320kuiper'
    Kuiper_320_web_trading_http = 'rest_wt320kuiper'
    Kuiper_320_web_trading_web_socket = 'api_session_320kuiper'
    Kuiper_319_Sell_Side = 'fix-sell-side-319-kepler'
    Kuiper_319_Buy_Side = 'fix-buy-side-319-kepler'
    Kuiper_319_Feed_Handler = 'fix-feed-handler-319-kuiper'


class FrontEnd(Enum):
    # 317 site
    USERS_317 = [""]
    PASSWORDS_317 = [""]
    FOLDER_317 = ""
    DESKS_317 = ["Desk of Order Book", "Desk of Middle Office"]
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


class DirectionEnum(Enum):
    FromQuod = "FIRST"
    ToQuod = "SECOND"


class GatewaySide(Enum):
    Sell = "Sell"
    Buy = "Buy"


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


class WebAdminURL(Enum):
    saturn_306 = "http://10.0.22.38:3480/quodadmin/saturn/#/auth/login"


class WebBrowser(Enum):
    chrome = "chrome"
    firefox = "firefox"

class WebTradingURL(Enum):
    luna_315 = "http://10.0.22.38:6680/quodtrading/qakharkiv315Trading/#/signin"
    kuiper_320 = "http://10.0.22.38:6780/quodtrading/qakharkiv320Trading/#/signin"