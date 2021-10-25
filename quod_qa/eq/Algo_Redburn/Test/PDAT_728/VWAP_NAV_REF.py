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
            'ClOrdID': 'VWAP_NAV_05_01' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 2,
            'OrderQty': 500000,
            'TimeInForce': 0,
            'Price': 110,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "GBX",
            'TargetStrategy': 1,
            'ExDestination': 'XLON',
            'Text': 'VWAP-NAV_01',
            'QuodFlatParameters': {
                #'MaxPercentageVolume': '10',
                'NavigatorPercentage': '100',
                # 'NavigatorMaxTotalShares': '500000',
                'NavigatorExecution': '1',
                #'NavigatorInitialSweepTime': '10',
                'NavGuard': '0',
                #'NavigatorLimitPrice': '110',
                'NavigatorLimitPriceReference': 'LTP',
                #'NavigatorLimitPriceOffset': '100',
                # 'NavigatorMaxSliceSize': '10000',
                # 'NavigatorMinBookReloadSeconds': '10',
                #'NavigatorRebalanceTime': '10',
                'AllowedVenues': 'XLON',
                #'StartDate2': '20211021-15:29:00.000',
                'EndDate2': '20211022-12:08:00.000',
                # 'Waves': '4'
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
