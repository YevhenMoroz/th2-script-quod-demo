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
            'header': {
                'OnBehalfOfCompID': 'kames_ul_DCOI'
            },
            'Account': "REDBURN",
            'ClOrdID': 'QA_TWAP_NAV_WW_MAXShares ' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 1000000,
            'TimeInForce': 0,
            'Price': 111,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "GBX",
            'TargetStrategy': 1005,
            'ExDestination': 'XLON',
            'Text': 'QA_TWAP_NAV_WW_MAXShares',
            'QuodFlatParameters': {
                'NavigatorPercentage': '100',
                'NavigatorExecution': '1',
                'NavigatorInitialSweepTime': '5',
                'AllowedVenues': 'XLON',
                'TriggerPriceRed': '110.04',
                'MaxWouldShares': '109.6',
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
