import logging
import os
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True

instrument = {
    'Symbol': 'NO0003054108-XOSL',
    'SecurityID': 'NO0003054108',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XOSL'
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
            'Price': 175,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "NOK",
            'TargetStrategy': 1,
            'ExDestination': 'XOSL',
            'Text': 'MMT_VWAP_AUC_LMT_XOSL',
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
