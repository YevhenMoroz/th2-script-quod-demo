import logging
import time
from datetime import datetime
from posixpath import expanduser
from custom import basic_custom_actions as bca
from custom.basic_custom_actions import message_to_grpc, convert_to_request
from rule_management import RuleManager
from stubs import Stubs

timeouts = True

instrument = {
            'Symbol': 'IT0001054904_EUR',
            'SecurityID': 'IT0001054904',
            'SecurityIDSource': '4',
            'SecurityExchange': 'MTAA'
        }


def execute(report_id):
    try:
        rule_manager = RuleManager()
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew("fix-buy-side-316-ganymede", "TRQX_CLIENT1", "TRQX", 15)

        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport("fix-buy-side-316-ganymede", False)

        new_order_single_params = {
            'Account': "CLIENT1",
            'ClOrdID': bca.client_orderid(9),
            'HandlInst': 1,
            'Side': 1,
            'OrderQty': 100,
            'TimeInForce': 0,
            'OrdType': 2,
            'Price': 15,
            'TransactTime': datetime.utcnow().isoformat(),
            'Instrument': instrument,
            'OrderCapacity': 'A',
            'Currency': "EUR",
        }

        Stubs.fix_act.placeOrderFIX(request=convert_to_request(
            'Send NewOrderSingle',
            "fix-sell-side-316-ganymede",
            report_id,
            message_to_grpc('NewOrderSingle', new_order_single_params,
                            "fix-sell-side-316-ganymede")
        ))

        time.sleep(2)
        rule_manager.remove_rule(nos_rule)
        rule_manager.remove_rule(ocrr_rule)
    except:
        logging.error("Error execution", exc_info=True)
