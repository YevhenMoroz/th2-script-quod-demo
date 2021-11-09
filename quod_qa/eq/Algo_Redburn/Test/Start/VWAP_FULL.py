import logging
from datetime import datetime, timedelta
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
        now = datetime.today() - timedelta(hours=2)
        new_order_single_params = {
            'Account': "REDBURN",
            'ClOrdID': 'TestVWAP_' + bca.client_orderid(9),
            'HandlInst': 2,
            'Side': 1,
            'OrderQty': 10000,
            'TimeInForce': 0,
            'Price': 100,
            'OrdType': 2,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "GBX",
            'TargetStrategy': 1,
            'ExDestination': 'XLON',
            'Text': 'VWAP-AUC_01',
            'QuodFlatParameters': {
                'ParticipateInOpeningAuctions': 'Y',
                'ParticipateInClosingAuctions': 'Y',
                'MaxParticipationOpen': '10',
                'MaxParticipationClose': '10',
                'SaveForClosePercentage': '80',
                'SaveForCloseShares': '800',
                'AuctionInitalSliceMultiplier': '200',
                'WouldInAuction': '1',
                'AuctionWouldCap': '150',
                'StartDate2': '20210921-09:30:00.000',
                'AtLast': '0',
                'AllowedVenues': 'XLON'
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
