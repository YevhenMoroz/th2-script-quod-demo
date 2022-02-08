from enum import Enum

from aenum import NoAlias
from aenum import Enum as CustomEnum
from test_cases.fx.fx_wrapper.common_tools import hash_green, hash_yellow, hash_red


class OrderBookColumns(Enum):
    order_id = "Order ID"
    quote_id = "QuoteID"
    cl_ord_id = "ClOrdID"
    security_id = "Security Id"
    symbol = "Symbol"
    side = "Side"
    lookup = "Lookup"
    stop_price = "Stop Price"
    inst_type = "InstType"
    venue = "Venue"
    sts = "Sts"
    exec_progress = "ExecProgress"
    exec_sts = "ExecSts"
    cd_sts = "CDSts"
    qty = "Qty"
    display_qty = "DisplayQty"
    unmatched_qty = "UnmatchedQty"
    limit_price = "Limit Price"
    leaves_qty = "LeavesQty"
    cum_qty = "CumQty"
    avg_price = "AvgPrice"
    ord_type = "OrdType"
    tif = "TIF"
    orig = 'Orig'
    expire_date = "ExpireDate"
    owner = "Owner"
    suspend = 'Suspended'
    client_id = 'Client ID'
    client_name = "Client Name"
    free_notes = 'FreeNotes'
    instrument_type = 'InstrType'
    currency = 'Currency'
    venue_client_account = "Venue Client Account"
    account_id = 'Account ID'
    done_for_day = 'DoneForDay'
    # region Executions
    exec_price = 'ExecPrice'
    exec_id = 'ExecID'
    last_market = 'LastMkt'
    post_trade_status = 'PostTradeStatus'
    # endregion


class TimeInForce(Enum):
    FOK = 'FillOrKill'
    IOC = 'ImmediateOrCancel'
    GTC = 'GoodTillCancel'
    GTD = 'GoodTillDate'
    DAY = 'Day'


class OrderType(Enum):
    limit = "Limit"
    market = "Market"
    previously_quoted = "PreviouslyQuoted"


# TODO: Need to compare with actual version (v156)
class InstrType(Enum):
    spot = 'FXSpot'
    forward = 'FXForward'
    swap = 'FXSwap'
    ndf = 'NDF'
    nds = 'NDS'


class QuoteBookColumns(Enum):
    quote_id = 'Id'
    account_group = 'AccountGroup'
    security_id = 'SecurityID'
    owner = 'Owner'
    instrument_type = 'InstrType'
    originator = 'Originator'
    ord_qty = 'OrdQty'
    quote_status = 'QuoteStatus'
    bid_px = 'Bid Px'
    bid_size = 'BidSize'
    bid_spot = 'Bid Spot'
    offer_px = 'Offer PX'
    offer_size = 'OfferSize'
    offer_spot = 'Offer Spot'
    quote_type = 'QuoteType'


class TradeBookColumns(Enum):
    exec_id = 'ExecID'
    order_id = 'Order ID'
    contra_exec_id = 'ContraExecID'
    venue = 'Venue'
    qty = 'Qty'
    side = 'Side'
    exec_price = 'ExecPrice'
    last_market = 'LastMkt'
    instrument_type = 'InstrType'
    security_id = 'Security Id'
    symbol = 'Symbol'
    origin = 'Origin'
    owner = 'Owner'
    exec_fees = "Exec Fees"
    client_commission = "Client Commission"


class QuoteRequestBookColumns(Enum):
    quote_request_id = 'ID'
    instrument_symbol = 'InstrSymbol'
    instrument_type = 'InstrType'
    automatic_quoting = 'AutomaticQuoting'
    currency = 'Currency'
    venue = 'Venue'
    qty = 'Qty'
    user = 'User'
    status = 'Status'
    quote_status = 'QuoteStatus'
    rejection_reason = 'RejReason'
    free_notes = 'FreeNotes'
    client = 'Client'
    client_tier = 'ClientTier'
    tenor = 'Tenor'
    # region Quotes sub-level
    quote_id = 'ID'
    account_group = 'AccountGroup'
    security_id = 'SecurityID'
    owner = 'Owner'
    originator = 'Originator'
    ord_qty = 'OrdQty'
    bid_px = 'Bid Px'
    bid_size = 'BidSize'
    bid_spot = 'Bid Spot'
    offer_px = 'Offer PX'
    offer_size = 'OfferSize'
    offer_spot = 'Offer Spot'
    quote_type = 'QuoteType'
    # endregion


class ExecSts(Enum):
    filled = 'Filled'
    eliminated = 'Eliminated'
    rejected = 'Rejected'
    open = 'Open'
    cancelled = 'Cancelled'
    held = 'Held'
    partially_filled = 'PartiallyFilled'
    terminated = 'Terminated'


class Status(Enum):
    terminated = 'Terminated'
    expired = 'Expired'
    new = 'New'
    rejected = 'Rejected'
    frozen = 'Frozen'


class QuoteStatus(Enum):
    accepted = 'Accepted'
    terminated = 'Terminated'
    expired = 'Expired'
    canceled = 'Canceled'
    filled = 'Filled'
    removed = 'RemovedFromMarket'


class Side(Enum):
    sell = "Sell"
    buy = "Buy"


class ClientPrisingTileAction(Enum):
    widen_spread = "Widen Spread"
    narrow_spread = "Narrow Spread"
    increase_ask = "Increase Ask"
    decrease_ask = "Decrease Ask"
    increase_bid = "Increase Bid"
    decrease_bid = "Decrease Bid"
    skew_towards_bid = "Skew Towards Bid"
    skew_towards_ask = "Skew Towards ask"


class PriceNaming(Enum):
    ask_large = "ask_large"
    ask_pips = "ask_pips"
    bid_large = "bid_large"
    bid_pips = "bid_pips"
    spread = "spread"


class AutoHedgerID(Enum):
    osmium = {'OsmiumAH': '400000018'}


class RatesColumnNames(CustomEnum):
    _settings_ = NoAlias
    ask_effective = "-"
    ask_base = "Base"
    ask_band = "Band"
    ask_pub = "Pub"
    ask_pts = "Pts"
    ask_spot = "Spot"
    ask_px = "Px"
    bid_effective = "-"
    bid_base = "Base"
    bid_band = "Band"
    bid_pub = "Pub"
    bid_pts = "bid_pts.Pts"
    bid_spot = "Spot"
    bid_px = "Px"


class PricingButtonColor(Enum):
    green_button = hash_green
    yellow_button = hash_yellow
    red_button = hash_red


class MiddleOfficeColumns(Enum):
    qty = "Qty"
    price = "AvgPx"
    client_id = "Client ID"
    client_comm = "Client Comm"
    total_fees = "Total Fees"
    sts = 'Status'
    match_status = 'Match Status'
    summary_status = 'Summary Status'
    order_id = 'Order ID'
    block_id = 'Block ID'
    conf_service = "Conf Service"
    side = 'Side'


class AllocationsColumns(Enum):
    client_comm = "Client Comm"
    alloc_qty = "Alloc Qty"
    total_fees = "Total Fees"
    alt_account = "Alt Account"
    account_id = "Account ID"
    security_acc = "Security Account"
    sts = 'Status'
    match_status = 'Match Status'
    alloc_id = 'Allocation ID'
    avg_px = 'Avg Px'


class SecondLevelTabs(Enum):
    child_tab = 'Child Orders'
