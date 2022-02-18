import logging
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True

instrument = {
    'Symbol': 'GB00BH4HKS39-XLON',
    'SecurityID': 'GB00BH4HKS39',
    'SecurityIDSource': '4',
    'SecurityExchange': 'XLON'
}


def execute(report_id):
    try:
        new_order_single_params = {
            'Account': "REDBURN",
            'ClOrdID': 'POV_BA_01 ' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 10000000,
            'TimeInForce': 0,
            'OrdType': 1,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "GBX",
            'TargetStrategy': 1008,
            'ExDestination': 'XLON',
            'Text': 'POV_BA_01',
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
