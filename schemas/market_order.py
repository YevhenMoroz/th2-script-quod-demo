from __future__ import print_function

import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
timeouts = False


def execute(case_name, report_id, case_params):
    seconds, nanos = bca.timestamps()  # Store case start time

    # Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': 'KEPLER',
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': '0',
        'OrdType': '1',
        'OrderCapacity': 'A',
        'Currency': 'EUR',
    }
    specific_order_params = {   # There are reusable and specific for submition parameters
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': case_params['Instrument'],
        'ExDestination': 'QDL1',
        'ComplianceID': 'FX5',
        'Text': 'Big masrket order',
    }
    bca.act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', specific_order_params)
        ))

    if timeouts:
        time.sleep(5)

    bca.create_event(case_name, case_params['case_id'], report_id)  # Create sub-report for case
    print("Case " + case_name + " is executed in " + str(
        round(datetime.now().timestamp() - seconds)) + " sec.")
