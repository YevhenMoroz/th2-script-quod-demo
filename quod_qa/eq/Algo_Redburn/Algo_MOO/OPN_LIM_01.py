from datetime import datetime
from custom import basic_custom_actions as bca
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
        'Account': "REDBURN",
        'ClOrdID': bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 1,
        'OrderQty': 100,
        'TimeInForce': 0,
        'Price': 20,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "EUR",
        'TargetStrategy': 1012, # MOO
        'ExDestination': 'XPAR',
        'Text': 'OPN_LIM_01',
        'QuodFlatParameters': {
            'MaxParticipation': '10',
            'LimitPriceReference': 'LTP',
            'LimitPriceOffset': '2',
            'ExcludePricePoint2': '1'
        }
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-redburn",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-redburn")
    ))
