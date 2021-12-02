from enum import Enum


class OrderBookColumns(Enum):
    order_id = "Order ID"
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
    client_id = "Client ID"
    client_name = "Client Name"
    free_notes = 'FreeNotes'
    instrument_type = 'InstrType'
    # region Executions
    exec_price = 'ExecPrice'
    exec_id = 'ExecID'
    last_market = 'LastMkt'
    # endregion


class TimeInForce(Enum):
    FOK = 'FillOrKill'
    IOC = 'ImmediateOrCancel'
    GTC = 'GoodTillCancel'
    GTD = 'GoodTillDate'
    DAY = 'Day'


# TODO: Need to compare with actual version (v156)
class InstrType(Enum):
    spot = 'Spot'
    forward = 'FXForward'
    swap = 'FXSwap'
    ndf = 'NDF'
    nds = 'NDS'


class QuoteBookColumns(Enum):
    quote_id = 'ID'
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


class Side(Enum):
    sell = "Sell"
    buy = "Buy"
