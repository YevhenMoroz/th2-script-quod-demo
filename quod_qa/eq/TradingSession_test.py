from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    params = {
        'TradingSessionID': '1',
        'TradSesStatus': '3',
        'MarketID': 'TRQX'
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send MarketDataSnapshotFullRefresh',
        "fix-fh-310-columbia",
        report_id,
        message_to_grpc('TradingSessionStatus', params, "fix-fh-310-columbia")
    ))
