from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_rule
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager
import time
import com.exactpro.th2.common.grpc.Direction


def run_test_case():
    seconds, nanos = timestamps() 
    case_name = "Example"
    sell_side_conn = "gtwquod3"
    buy_side_conn = "fix-bs-eq-paris"
    rule_manager = RuleManager()

    case_id = create_event(case_name)

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
        'OrderQty': 500,
        'TimeInForce': '1',
        'Price': 5000,
        'OrdType': '1',
        'ClOrdID': client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': instrument_1,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': "1011"
    }

    rule = rule_manager.add_NOS(sell_side_conn, new_order_params['Account'])
    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request("Send new order", sell_side_conn, case_id,
                                   wrap_message(new_order_params, "NewOrderSingle", sell_side_conn))
    )
    checkpoint_1 = new_order.checkpoint_id
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
        'OrderID': '*',
        'ExecID': '*',
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
        'Instrument': new_order_params['Instrument']
    }

    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'

    pre_filter_params = {'header': {'MsgType':('0',"Not_equal")}}
    pre_filter = prefilter_to_grpc(pre_filter_params)
    message_filters_sell_side = [
        filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID','OrdStatus']),
        filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID','OrdStatus']) ]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side",
            prefilter=pre_filter,
            msg_filters=message_filters_sell_side,
            checkpoint=checkpoint_1,
            connectivity=sell_side_conn,
            event_id=case_id,
            timeout=2000
            
        )
    )
    
    order_params_buy_side = deepcopy(new_order_params)
    order_params_buy_side['HandlInst'] = '2'
    order_params_buy_side['TimeInForce'] = '1'
    order_params_buy_side['OrderCapacity'] = "A"
    order_params_buy_side['Currency'] = 'EUR'
    order_params_buy_side['TargetStrategy'] = "1011"
    order_params_buy_side["Instrument"] = instrument_1
    
    message_filters_buy_side = [filter_to_grpc("NewOrderSingle",order_params_buy_side)]
        Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side",
            prefilter=pre_filter,
            msg_filters=message_filters_buy_side,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id,
            timeout=2000
            
        )
    )
        
    params_buy_side_er = 
    {
        'Side': new_order_params['Side'],
        'OrdType': new_order_params['OrdType'],
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': '*',
        'ExecID': '*',
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
    }
        
    message_filters_er = [filter_to_grpc("ExecutionReport", params_buy_side_er)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check ExecutionReport",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_er,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.SECOND
            timeout=2000
        )
    )

    rule_manager.remove_rule(rule)
    print(f"Case {case_name} was executed")

if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()
