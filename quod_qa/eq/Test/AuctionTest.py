from datetime import datetime

from custom import basic_custom_actions as bca
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodOCRRule, TemplateQuodOCRRRule, TemplateQuodNOSRule
from th2_grpc_common.common_pb2 import ConnectionID, Direction

from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    instrument = {
        'Symbol': 'FR0000121121_EUR',
        'SecurityID': 'FR0000121121',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    new_order_single_params = {
        'Account': "CLIENT1",
        'ClOrdID': bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 1,
        'OrderQty': 100,
        'TimeInForce': 2,
        'Price': 20,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "EUR",
        'TargetStrategy': 1012,
        'ExDestination': 'XPAR',
        'NoStrategyParameters': [
            {
                'StrategyParameterName': 'MaxParticipation',
                'StrategyParameterType': '6',
                'StrategyParameterValue': '10'
            },
            {
                'StrategyParameterName': 'PercentageForClose',
                'StrategyParameterType': '6',
                'StrategyParameterValue': '10'
            }
        ]
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-316-ganymede",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-316-ganymede")
    ))
