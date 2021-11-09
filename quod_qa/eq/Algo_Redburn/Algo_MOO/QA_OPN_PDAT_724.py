from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    instrument = {
        'Symbol': 'GB0008706128-XLON',
        'SecurityID': 'GB0008706128',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XLON'
    }

    new_order_single_params = {
        'Account': "REDBURN",
        'ClOrdID': 'OPN_VO_01 ' + bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 1,
        'OrderQty': 10000000,
        'TimeInForce': 0,
        'Price': 47,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "GBX",
        'TargetStrategy': 1012, # MOO
        'ExDestination': 'XLON',
        'Text': 'OPN_VO_01',
        'QuodFlatParameters': {
            'MaxParticipation': '10',
            'ExcludePricePoint2': '1',
            'TriggerPriceRed': '45',
            'WouldInAuction': '1',
        }
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-redburn",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-redburn")
    ))
