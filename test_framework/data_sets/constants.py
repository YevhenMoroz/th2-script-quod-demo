from enum import Enum


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
    Ganymede_317_ja = '317_java_api'
    Ganymede_317_als_email_report = 'log317-als-email-report'


class FrontEnd(Enum):
    # 317 site
    USER_317 = ""
    PASSWORD_317 = ""
    PASSWORD_317_1 = ""
    PASSWORD_317_2 = ""
    FOLDER_317 = ""
    DESKS_317 = ('Desk of Order Book', 'Desk of Middle Office')
    MAIN_WIN_NAME_317 = "Quod Financial - 317 GANYMEDE"
    LOGIN_WIN_NAME_317 = "Login to Quod Financial (317 GANYMEDE) "
    # common values
    EXE_NAME = "QuodFrontEnd.exe"
    # target_server values
    TARGET_SERVER_WIN = None  # by default we can set up here value of Jenkins machine


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
    CancelRequest = "CancelReplace"
    Cancel = "Cancel"
    Eliminate = "Eliminate"
