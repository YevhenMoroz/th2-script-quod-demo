from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs
import os

timeouts = True


def execute(report_id):
    instrument = {
        'Symbol': 'GRS015003007-XATH',
        'SecurityID': 'GRS015003007',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XATH'
    }

    new_order_single_params = {
        'Account': "REDBURN",
        'ClOrdID': (os.path.basename(__file__)[:-3]) + '_' + bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 1,
        'OrderQty': 10000,
        'TimeInForce': 0,
        'Price': 3,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "EUR",
        'TargetStrategy': 1012, # MOO
        'ExDestination': 'XATH',
        'Text': 'MOO_AMS',
        'QuodFlatParameters': {
            'MaxParticipation': '10',
            'ExcludePricePoint2': '1',
            'AllowedVenues': 'XATH'
        }
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-redburn",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-redburn")
    ))
