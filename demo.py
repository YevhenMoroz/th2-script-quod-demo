from __future__ import print_function

import logging
from datetime import datetime
from custom import basic_custom_actions as bca
from schemas import *

timeouts = False


def test_run():
    # Generation id and time for test run
    report_id = bca.create_event_id()
    bca.create_event(
        'quod_demo_1 ' + datetime.now().strftime('%Y%m%d-%H:%M:%S'),
        report_id,
        None
    )

    # Reference data for test cases
    instrument = {
        'Symbol': 'QUODTESTQA00',
        'SecurityID': 'TESTQA00',
        'SecurityIDSource': '8',
        'SecurityExchange': 'QDL1'
    }

    # Specific data for test case test
    send_and_cancel_suit = {
        'QAP-2462': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '2',
            'OrderQty': '50000000',
            'OrdType': '2',
            'Price': '19',
            'TimeInForce': '0',
            'Instrument': instrument
        },
        'QAP-2422': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '500000000',
            'OrdType': '2',
            'Price': '19',
            'TimeInForce': '0',
            'Instrument': instrument
        },
    }
    send_and_amend_suit = {
        'QAP-AMEND': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'newOrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'newPrice': '19',
            'TimeInForce': '0',
            'Instrument': instrument
        },
    }
    trade_example_suit = {
        'QAP-AMEND': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Account': 'KEPLER',
            'HandlInst': '2',
            'Side': '1',
            'OrderQty': '400',
            'newOrderQty': '500',
            'OrdType': '2',
            'Price': '20',
            'newPrice': '19',
            'TimeInForce': '0',
            'Instrument': instrument
        },
    }
    market_order_suit = {
        'Big market order SELL': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Side': '1',
            'Instrument': instrument
        },
        'Big market order BUY': {
            'case_id': bca.create_event_id(),
            'TraderConnectivity': 'gtwquod3',
            'Side': '1',
            'Instrument': instrument
        },
    }
    # Run all test cases

    for case in send_and_cancel_suit:
        send_and_cancel.execute(case, report_id, send_and_cancel_suit[case])

    for case in send_and_amend_suit:
        send_and_amend.execute(case, report_id, send_and_amend_suit[case])

    # for case in trade_example_suit:
    #     send_and_amend.execute(case, report_id, trade_example_suit[case])

    # for case in market_order_suit:
    #     market_order.execute(case, report_id, market_order_suit[case])


if __name__ == '__main__':
    logging.basicConfig()
    test_run()
