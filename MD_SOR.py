from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID
from stubs import Stubs
from custom.basic_custom_actions import message_to_grpc, convert_to_request


def md(report_id):
    connectivity_fh = 'fix-fh-310-columbia'
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="734",
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '10000000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '0',
                'MDEntryPx': '40',
                'MDEntrySize': '10000000',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        report_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))

    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="3416",
        connection_id=ConnectionID(session_alias=connectivity_fh)
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '0',
                'MDEntrySize': '0',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        connectivity_fh,
        report_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, connectivity_fh)
    ))