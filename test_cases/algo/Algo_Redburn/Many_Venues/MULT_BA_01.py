import os
import logging
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True

instrument = {
    'Symbol': 'IT0003497168-MTAA',
    'SecurityID': 'IT0003497168',
    'SecurityIDSource': '4',
    'SecurityExchange': 'MTAA'
}


def execute(report_id):
    try:
        new_order_single_params = {
            'Account': "REDBURN",
            'ClOrdID': (os.path.basename(__file__)[:-3]) + '_' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 5000000,
            'TimeInForce': 0,
            'OrdType': 1,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "EUR",
            'TargetStrategy': 1008,
            'ExDestination': 'MTAA',
            'Text': 'MULT_BA_01',
            'QuodFlatParameters': {
                'AllowMissingPrimary': True,
                "AvailableVenues": True
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
