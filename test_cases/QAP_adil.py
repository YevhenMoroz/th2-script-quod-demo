from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_sequence_rule, prefilter_to_grpc
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager



def run_test_case():
    seconds, nanos = timestamps()
    case_name = "test instance"
    sell_side_conn = "gtwquod3"
    buy_side_conn = "fix-bs-eq-paris"
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

    # print(new_order_params['ClOrdID'])
    rule = rule_manager.add_NOS(buy_side_conn, new_order_params['Account'])
    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn))
    )

    # set a checkpoint in order to start searching messages from a specific time
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

    # Execution report params with status New
    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'
    new_er_params['Account'] = "#"

    # Attributes by which messages will be filtered
    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL")
        }
    }

    # Making an example PreFilter class
    pre_filter_sim = prefilter_to_grpc(pre_filter_sim_params)

    # List of filters of messages
    message_filters_sim = [
        filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
        filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus'])
    ]

    # Creating request for verification to check1
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sim,
            checkpoint=checkpoint_1,
            connectivity=sell_side_conn,
            event_id=case_id,
        )
    )
    rule_manager.remove_rule(rule)


if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()
