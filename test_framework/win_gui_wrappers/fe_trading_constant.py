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
    tenor = "Tenor"
    near_leg = 'Near Leg Tenor'
    far_leg = 'Far Leg Tenor'
    beneficiary = 'Beneficiary'
    # region Executions
    exec_price = 'ExecPrice'
    exec_id = 'ExecID'
    last_market = 'LastMkt'
    post_trade_status = 'PostTradeStatus'
    disclose_exec = "DiscloseExec"
    exec_fees = "Exec Fees"
    washbook = 'Wash Book'
    capacity = 'Capacity'
    near_tenor = 'NearTenor'
    near_qty = 'NearQty'
    near_fwd_pts = 'NearFwdPts'
    near_px = 'NearPx'
    near_settl_date = 'NearSettlDate'
    far_tenor = 'FarTenor'
    far_qty = 'FarQty'
    far_fwd_pts = 'FarFwdPts'
    far_px = 'FarPx'
    far_settl_date = 'FarSettlDate'
    last_spot_rate = 'LastSpotRate'
    settle_date = 'Settle Date'
    day_cum_qty = 'DayCumQty'
    day_cum_amt = 'DayCumAmt'
    # endregion


class PositionBookColumns(Enum):
    symbol = "Symbol"
    account = "Account"
    position = "Position"
    quote_position = "Quote Position"
    position_usd = "Position (USD)"
    quote_position_usd = "Quote Position (USD)"


class TimeInForce(Enum):
    FOK = 'FillOrKill'
    IOC = 'ImmediateOrCancel'
    GTC = 'GoodTillCancel'
    GTD = 'GoodTillDate'
    DAY = 'Day'
    ATC = "AtTheClose"


class TriggerType(Enum):
    last_trade = "LastTrade"
    market_best_bid_offer = "MarketBestBidOffer"
    primary_best_bid_offer = "PrimaryBestBidOffer"


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


class ExecType(Enum):
    trade = "Trade"
    calculated = "Calculated"


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
    near_tenor = 'Near Leg Tenor'
    near_qty = 'NearQty'
    near_fwd_pts = 'NearFwdPts'
    near_px = 'NearPx'
    near_settl_date = 'Near Leg Settle Date'
    far_tenor = 'Far Leg Tenor'
    far_qty = 'FarQty'
    far_fwd_pts = 'FarFwdPts'
    far_px = 'FarPx'
    far_settl_date = 'Far Leg Settle Date'
    last_spot_rate = 'LastSpotRate'
    exec_type = 'ExecType'


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


class BasketBookColumns(Enum):
    id = "Id"
    exec_policy = "ExecPolicy"
    status = "Status"
    basket_name = "Basket Name"
    cl_basket_id = "Client Basket ID"
    """Waves Tab"""
    percent_qty_to_release = "Percent Qty To Release"
    percent_profile = "Percentage Profile"
    client_basket_id = 'Client Basket ID'


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
    ttl = "ttl"


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
    bid_pts = "Pts"
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
    pset = 'PSET'
    pset_bic = 'PSET BIC'
    settltype = 'SettlType'


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
    pset = 'PSET'
    pset_bic = 'PSET BIC'


class SecondLevelTabs(Enum):
    child_tab = 'Child Orders'
    executions = 'Executions'


class PostTradeStatuses(Enum):
    ready_to_book = "ReadyToBook"
    booked = "Booked"


class RFQPanelValues(Enum):
    button_text = "button_text"
    is_bid_price_pips_enabled = "is_bid_price_pips_enabled"
    is_ask_price_pips_enabled = "is_ask_price_pips_enabled"
    is_near_leg_quantity_enabled = "is_near_leg_quantity_enabled"
    is_far_leg_quantity_enabled = "is_far_leg_quantity_enabled"
    is_price_spread_enabled = "is_price_spread_enabled"
    is_bid_price_large_enabled = "is_bid_price_large_enabled"
    is_ask_price_large_enabled = "is_ask_price_large_enabled"


class RFQPanelPtsAndPx(Enum):
    bid_near_points_value_label = "bid_near_points_value_label"
    bid_far_points_value_label = "bid_far_points_value_label"
    bid_near_price_value_label = "bid_near_price_value_label"
    bid_far_price_value_label = "bid_far_price_value_label"
    bid_value_label = "bid_value_label"
    ask_value_label = "ask_value_label"
    ask_near_points_value_label = "ask_near_points_value_label"
    ask_far_points_value_label = "ask_far_points_value_label"
    ask_near_price_value_label = "ask_near_price_value_label"
    ask_far_price_value_label = "ask_far_price_value_label"


class RFQPanelQty(Enum):
    near_leg_quantity = "near_leg_quantity"
    far_leg_quantity = "far_leg_quantity"
    opposite_near_bid_qty_value_label = "opposite_near_bid_qty_value_label"
    opposite_near_ask_qty_value_label = "opposite_near_ask_qty_value_label"
    opposite_far_bid_qty_value_label = "opposite_far_bid_qty_value_label"
    opposite_far_ask_qty_value_label = "opposite_far_ask_qty_value_label"


class RFQPanelHeaderValues(Enum):
    request_state = "request_state"
    request_side = "request_side"
    instrument_label_control = "instrument_label_control"
    currency_value_label_control = "currency_value_label_control"
    near_tenor_label = "near_tenor_label"
    far_tenor_label = "far_tenor_label"
    near_settl_date_label = "near_settl_date_label"
    far_settl_date_label = "far_settl_date_label"
    party_value_label_control = "party_value_label_control"
    case_state_value_label_control = "case_state_value_label_control"
    quote_state_value_label_control = "quote_state_value_label_control"
    fill_side_value_label_control = "fill_side_value_label_control"
    request_side_value_label_control = "request_side_value_label_control"
    creation_value_label_control = "creation_value_label_control"


class PanicValues(Enum):
    executable = "executable"
    pricing = "pricing"
    hedge_orders = "hedge_orders"


class DiscloseExec(Enum):
    manual = 'M'
    real_time = 'R'


class PercentageProfile(Enum):
    remaining_qty = "RemainingQty"
    initial_qty = "InitialQty"
    target_basket_qty = "TargetBasketQty"


class Capacity(Enum):
    agency = 'Agency'


class OrderBagColumn(Enum):
    unmatched_qty = 'UnmatchedQty'
    order_bag_qty = 'OrderBagQty'
    ord_bag_name = 'OrdBagName'
    id = 'Id'
    leaves_qty = 'LeavesQty'


class BasketSecondTabName(Enum):
    orders = 'Orders'


class MatchWindowsColumns(Enum):
    order_id = 'OrderId'


class OrderBookColumnName(Enum):
    id = 'Id'
    order_bag_id = 'OrderBagID'


class MenuItemFromOrderBook(Enum):
    split_bag_by_qty_priority = 'Split Bag By Qty Priority'
    split_bag_by_avg_px_priority = 'Split Bag By Avg Px Priority'
    bag_by_avg_px_priority = 'Bag By Avg Px Priority'
    group_into_a_bag_for_grouping = 'Group into a bag for grouping'


class ClientInboxColumns(Enum):
    order_id = "Order ID"
