import os
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_sim_fix_quod.sim_pb2 import RequestMDRefID, NoMDEntries
from th2_grpc_common.common_pb2 import ConnectionID
from test_framework.old_wrappers.fix_manager import FixManager
from test_framework.old_wrappers.fix_verifier import FixVerifier
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request

# venue param
ex_destination_1 = "XPAR"
client = "CLIENT2"
account = 'XPAR_CLIENT2'
currency = 'EUR'
s_par = '704'

case_name = os.path.basename(__file__)
connectivity_buy_side = "fix-buy-side-316-ganymede"
connectivity_sell_side = "fix-sell-side-316-ganymede"
connectivity_fh = 'fix-feed-handler-316-ganymede'

instrument = {
    'Symbol': 'FR0010436584_EUR',
    'SecurityID': 'FR0010436584',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XPAR'
}


def send_market_data(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntries': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataSnapshotFullRefresh',
                        md_params, connectivity_fh)
    ))


def send_market_dataT(symbol: str, case_id: str, market_data):
    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol=symbol,
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    md_params = {
        'MDReqID': MDRefID,
        'NoMDEntriesIR': market_data
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataIncrementalRefresh',
        connectivity_fh,
        case_id,
        message_to_grpc('MarketDataIncrementalRefresh',
                        md_params, connectivity_fh)
    ))


def execute(report_id):
    case_id = bca.create_event((os.path.basename(__file__)[:-3]), report_id)
    # Send_MarkerData
    case_id_0 = bca.create_event("Send Market Data", case_id)
    market_data1 = [
        {
            'MDEntryType': '0',
            'MDEntryPx': 20,
            'MDEntrySize': 1200,
            'MDEntryPositionNo': '1'
        },
        {
            'MDEntryType': '1',
            'MDEntryPx': 21,
            'MDEntrySize': 1200,
            'MDEntryPositionNo': '1'
        }
    ]
    #send_market_data(s_par, case_id_0, market_data1)

    market_data2 = [
        {
            'MDUpdateAction': '0',
            'MDEntryType': '2',
            'MDEntryPx': 20,
            'MDEntrySize': 2000,
            'MDEntryDate': datetime.utcnow().date().strftime("%Y%m%d"),
            'MDEntryTime': datetime.utcnow().time().strftime("%H:%M:%S")
        }
    ]
    send_market_dataT(s_par, case_id_0, market_data2)
