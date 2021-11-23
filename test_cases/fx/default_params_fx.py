from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID

from custom import tenor_settlement_date as tsd
from stubs import Stubs

simulator = Stubs.simulator

defauot_quote_params = {
    'Side': 1,
    'Instrument': {
        'Symbol': 'EUR/USD',
        'SecurityType': 'FXSPOT'
        },
    'SettlDate': tsd.spo(),
    'SettlType': '0',
    'OrderQty': 1000000
    }
text_messages = {
    'erPending': 'Receive ExecutionReport (pending)',
    'sendQR': 'Send QuoteRequest',
    'recQ': 'Receive Quote message',
    'sendNOS': 'Send NewOrderSingle',
    'recQC': 'Receive CQuoteCancel message',
    'recQRR': 'Receive QuoteRequestReject message',
    'sendNOwithID': 'Send new order with ClOrdID = {}'
    }
band1fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18192,
    "MDEntrySize": 1000000,
    "MDEntryPositionNo": 1,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0002,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band2fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18120,
    "MDEntrySize": 1000000,
    "MDEntryPositionNo": 2,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0003,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band3fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18180,
    "MDEntrySize": 5000000,
    "MDEntryPositionNo": 3,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0004,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band4fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18140,
    "MDEntrySize": 5000000,
    "MDEntryPositionNo": 4,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0005,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band5fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18170,
    "MDEntrySize": 10000000,
    "MDEntryPositionNo": 5,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0006,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band6fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18160,
    "MDEntrySize": 10000000,
    "MDEntryPositionNo": 6,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0002,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
# mdu_params_fwd = {
#     "MDReqID": simulator.getMDRefIDForConnection303(
#             request=RequestMDRefID(
#                     symbol="EUR/USD:FXF:WK1:HSBC",
#                     connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
#     # "MDReportID": "1",
#     # "MDTime": "TBU",
#     # "MDArrivalTime": "TBU",
#     # "OrigMDTime": "TBU",
#     # "OrigMDArrivalTime": "TBU",
#     # "ReplyReceivedTime": "TBU",
#     'Instrument': {
#         'Symbol': 'EUR/USD',
#         'SecurityType': 'FXFWD'
#         },
#     # "LastUpdateTime": "TBU",
#     "NoMDEntries": [
#         band1fwd,
#         band2fwd,
#         band3fwd,
#         band4fwd,
#         band5fwd,
#         band6fwd
#         ]
#     }
band1fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18192,
    "MDEntrySize": 1000000,
    "MDEntryPositionNo": 1,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0002,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band2fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18120,
    "MDEntrySize": 1000000,
    "MDEntryPositionNo": 2,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0003,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band3fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18180,
    "MDEntrySize": 5000000,
    "MDEntryPositionNo": 3,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0004,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band4fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18140,
    "MDEntrySize": 5000000,
    "MDEntryPositionNo": 4,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0005,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band5fwd = {
    "MDEntryType": "0",
    "MDEntryPx": 1.18170,
    "MDEntrySize": 10000000,
    "MDEntryPositionNo": 5,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0006,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
band6fwd = {
    "MDEntryType": "1",
    "MDEntryPx": 1.18160,
    "MDEntrySize": 10000000,
    "MDEntryPositionNo": 6,
    "MDEntrySpotRate": 1.1819,
    "MDEntryForwardPoints": 0.0002,
    'SettlDate': tsd.wk1(),
    "MDEntryDate": datetime.utcnow().strftime('%Y%m%d'),
    "MDEntryTime": datetime.utcnow().strftime('%H:%M:%S'),
    }
# mdu_params_fwd = {
#     "MDReqID": simulator.getMDRefIDForConnection303(
#             request=RequestMDRefID(
#                     symbol="EUR/USD:FXF:WK1:HSBC",
#                     connection_id=ConnectionID(session_alias="fix-fh-fx-esp"))).MDRefID,
#     # "MDReportID": "1",
#     # "MDTime": "TBU",
#     # "MDArrivalTime": "TBU",
#     # "OrigMDTime": "TBU",
#     # "OrigMDArrivalTime": "TBU",
#     # "ReplyReceivedTime": "TBU",
#     'Instrument': {
#         'Symbol': 'EUR/USD',
#         'SecurityType': 'FXFWD'
#         },
#     # "LastUpdateTime": "TBU",
#     "NoMDEntries": [
#         band1fwd,
#         band2fwd,
#         band3fwd,
#         band4fwd,
#         band5fwd,
#         band6fwd
#         ]
#     }
