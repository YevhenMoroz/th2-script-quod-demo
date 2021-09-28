from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    instrument = {
        'Symbol': 'GB00BH4HKS39-XLON',
        'SecurityID': 'GB00BH4HKS39',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XLON'
    }

    new_order_single_params = {
        'Account': "REDBURN",
        'ClOrdID': 'CLO_VO_01' + bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 2,
        'OrderQty': 10000000,
        'TimeInForce': 0,
        'Price': 100,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "GBX",
        'TargetStrategy': 1015, # MOC
        'ExDestination': 'XLON',
        'Text': 'CLO_VO_01',
        'QuodFlatParameters': {
            'MaxParticipation': '10',
            'PricePoint1Price': '102',
            'PricePoint1Participation': '20',
            'PricePoint2Price': '104',
            'PricePoint2Participation': '40',
            'AllowedVenues': 'XLON'
        }
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-redburn",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-redburn")
    ))
