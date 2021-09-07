from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_rule
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager
import time


def run_test_case():
    seconds, nanos = timestamps()
    case_name = "test instance"
    sell_side_conn = "gtwquod3"
    rule_manager = RuleManager()

    # create event with name case_name and return case_id
    case_id = create_event(case_name)

    # new order params
    instrument_1 = {
        'Symbol': 'FR0000065435_EUR',
        'SecurityID': 'FR0000065435',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }
    new_order_params = {
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 150,
        'TimeInForce': '0',
        'Price': 20,
        'OrdType': '2',
        'ClOrdID': client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument_1,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': "1011"
    }
    #print(new_order_params['ClOrdID'])
    rule = rule_manager.add_NOS(sell_side_conn, new_order_params['Account'])
    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn))
    )
    checkpoint_1 = new_order.checkpoint_id

    # Execution report params with status pending
    pending_er_params = {
        'Account': new_order_params['Account'],
        'HandlInst': new_order_params['HandlInst'],
        'Side': new_order_params['Side'],
        'TimeInForce': new_order_params['TimeInForce'],
        'OrdType': new_order_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': new_order_params['TargetStrategy'],
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': "*",
        'ExecID': "*",
        'TransactTime': '*',
        'Price': new_order_params['Price'],
        'OrderQty': new_order_params['OrderQty'],
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': new_order_params['Instrument'],
        'NoParty': [{
            'PartyID': f'{sell_side_conn}',
            'PartyIDSource': 'D',
            'PartyRole': '36'
        }]
    }
    Stubs.verifier.submitCheckRule(
        request=create_check_rule(
            "Execution Report with OrdStatus = Pending",
            filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, sell_side_conn, case_id
        )
    )

    # Execution report params with status New
    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'
    new_er_params['Account'] = "#"

    Stubs.verifier.submitCheckRule(
        request=create_check_rule(
            "Execution Report with OrdStatus = New",
            filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, sell_side_conn, case_id
        )
    )
    # time.sleep(3)
    # amend_order_params = deepcopy(new_order_params)
    # amend_order_params['OrderQty'] = 200
    # amend_order_params['OrigClOrdID'] = new_order_params['ClOrdID']
    # amend_order_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    # amend_order_params['TransactTime'] = datetime.utcnow().isoformat()
    # amend_order = Stubs.fix_act.placeOrderReplaceFIX(
    #     request=convert_to_request("Send order Cancel and Replace", sell_side_conn, case_id,
    #                                wrap_message(amend_order_params, "OrderCancelReplaceRequest", sell_side_conn))
    # )
    #
    rule_manager.remove_rule(rule)


if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()
