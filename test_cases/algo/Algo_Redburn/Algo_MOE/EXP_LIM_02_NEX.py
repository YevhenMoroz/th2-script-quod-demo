from datetime import datetime
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from stubs import Stubs

timeouts = True


def execute(report_id):
    instrument = {
        'Symbol': 'GB00BZ4BQC70-XLON',
        'SecurityID': 'GB00BZ4BQC70',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XLON'
    }

    new_order_single_params = {
        'Account': "REDBURN",
        'ClOrdID': 'EXP_LIM_02_NEX ' + bca.client_orderid(9),
        'HandlInst': 2,
        'Side': 1,
        'OrderQty': 10000000,
        'TimeInForce': 0,
        'Price': 117,
        'OrdType': 2,
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument,
        'OrderCapacity': 'A',
        'Currency': "GBX",
        'TargetStrategy': 1014, # Expiry
        'ExDestination': 'XLON',
        # 'Text': 'CLO_LIM_01',
        'QuodFlatParameters': {
            'MaxParticipation': '10',
            'LimitPriceReference': 'LTP',
            'LimitPriceOffset': '2',
            'ExcludePricePoint2': '1'
        }
    }

    Stubs.fix_act.sendMessage(request=convert_to_request(
        'Send NewOrderSingle',
        "fix-sell-side-redburn",
        report_id,
        message_to_grpc('NewOrderSingle', new_order_single_params, "fix-sell-side-redburn")
    ))
