from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator

    MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="953",
        connection_id=ConnectionID(session_alias="fix-feed-handler-316-ganymede")
    )).MDRefID
    mdir_params_bid = {
        'MDReqID': MDRefID,
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '19',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '19.99',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            }
        ]
    }

    # mdir_params_bid = {
    #     'MDReqID': MDRefID,
    #     'NoMDEntries':{
    #         'NoMDEntries':
    #             [
    #                 {
    #                     'MDEntryType': '0',
    #                     'MDEntryPx': '30',
    #                     'MDEntrySize': '100000',
    #                     'MDEntryPositionNo': '1'
    #                 },
    #                 {
    #                     'MDEntryType': '1',
    #                     'MDEntryPx': '40',
    #                     'MDEntrySize': '100000',
    #                     'MDEntryPositionNo': '1'
    #                 }
    #             ]
    #     }
    # }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        "fix-feed-handler-316-ganymede",
        report_id,
        message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, "fix-feed-handler-316-ganymede")
    ))
    # MDRefID = Stubs.simulator.getMDRefIDForConnection(request=RequestMDRefID(
    #     symbol="3416",
    #     connection_id=ConnectionID(session_alias="fix-fh-310-columbia")
    # )).MDRefID
    # mdir_params_bid = {
    #     'MDReqID': MDRefID,
    #     'NoMDEntries': [
    #         {
    #             'MDEntryType': '0',
    #             'MDEntryPx': '30',
    #             'MDEntrySize': '100000',
    #             'MDEntryPositionNo': '1'
    #         },
    #         {
    #             'MDEntryType': '1',
    #             'MDEntryPx': '40',
    #             'MDEntrySize': '100000',
    #             'MDEntryPositionNo': '1'
    #         }
    #     ]
    # }
    #
    # Stubs.fix_act.sendMessage(request=convert_to_request(
    #     'Send MarketDataSnapshotFullRefresh',
    #     "fix-fh-310-columbia",
    #     report_id,
    #     message_to_grpc('MarketDataSnapshotFullRefresh', mdir_params_bid, "fix-fh-310-columbia")
    # ))
