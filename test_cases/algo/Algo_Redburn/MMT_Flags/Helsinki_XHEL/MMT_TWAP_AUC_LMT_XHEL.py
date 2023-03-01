import logging
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs
import os

timeouts = True

instrument = {
    'Symbol': 'FI0009000681-XHEL',
    'SecurityID': 'FI0009000681',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XHEL'
}


def execute(report_id):
    try:
        new_order_single_params = {
            'Account': "REDBURN",
            'ClOrdID': (os.path.basename(__file__)[:-3]) + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 10000000,
            'TimeInForce': 0,
            'OrdType': 2,
            'Price': 4.4,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "EUR",
            'TargetStrategy': 1005,
            'ExDestination': 'XHEL',
            'Text': 'MMT_TWAP_AUC_LMT_XHEL',
            'QuodFlatParameters': {
                'ParticipateInOpeningAuctions': 'Y',
                'ParticipateInClosingAuctions': 'Y',
                'MaxParticipationOpen': '10',
                'MaxParticipationClose': '10',
            }
        }

        Stubs.fix_act.sendMessage(request=convert_to_request(
            'Send NewOrderSingle',
            "fix-sell-side-redburn",
            report_id,
            message_to_grpc('NewOrderSingle', new_order_single_params,
                            "fix-sell-side-redburn")
        ))
    except:
        logging.error("Error execution", exc_info=True)
