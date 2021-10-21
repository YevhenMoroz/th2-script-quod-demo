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
    expire_date = "ExpireDate"
    owner = "Owner"
    client_id = "Client ID"
    client_name = "Client Name"


class QuoteBookColumns(Enum):
    pass


class QuoteRequestBookColumns(Enum):
    pass
