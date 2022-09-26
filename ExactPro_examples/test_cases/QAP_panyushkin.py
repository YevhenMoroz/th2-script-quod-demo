from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_sequence_rule, prefilter_to_grpc
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager
from th2_grpc_common.common_pb2 import Direction


def run_test_case():
    seconds, nanos = timestamps()
    case_name = "panyushkin"
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
        'TargetStrategy': '1011'
    }

    rule = rule_manager.add_NOS(buy_side_conn, new_order_params['Account'])
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
        'NoParty': [{
            'PartyID': f'{sell_side_conn}',
            'PartyIDSource': 'D',
            'PartyRole': '36'}],
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': new_order_params['Instrument']
    }

    new_er_params = deepcopy(pending_er_params)
    new_er_params['Account'] = '#'
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'

    pre_filter_params = {'header': {'MsgType': ('0', "NOT_EQUAL")}}
    pre_filter = prefilter_to_grpc(pre_filter_params)
    message_filters_sell_side = [
        filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
        filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus'])]

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

    instrument_2 = {
        'SecurityType': 'CS',
        'Symbol': 'GARD',
        'SecurityID': 'FR0000065435',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    trailer_1 = {
        'CheckSum': '*'
    }

    order_params_buy_side = deepcopy(new_order_params)
    order_params_buy_side['ExDestination'] = '*'
    order_params_buy_side['ChildOrderID'] = '*'
    order_params_buy_side['HandlInst'] = '1'
    order_params_buy_side['ClOrdID'] = '*'
    order_params_buy_side['SettlDate'] = '*'
    order_params_buy_side['TransactTime'] = '*'
    order_params_buy_side['TimeInForce'] = '0'
    order_params_buy_side['OrderCapacity'] = 'A'
    order_params_buy_side['Currency'] = 'EUR'
    order_params_buy_side['trailer'] = trailer_1
    order_params_buy_side['Instrument'] = instrument_2
    order_params_buy_side.pop('ClientAlgoPolicyID')
    order_params_buy_side.pop('ComplianceID')
    order_params_buy_side.pop('TargetStrategy')

    message_filters_buy_side = [filter_to_grpc("NewOrderSingle", order_params_buy_side)]

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

    params_buy_side_er = {
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': new_order_params['OrderQty'],
        'OrdType': new_order_params['OrdType'],
        'ClOrdID': '*',
        'Text': "sim work",
        'TransactTime': '*',
        'Side': new_order_params['Side'],
        'OrderID': '*',
        'AvgPx': '0',
        'OrdStatus': '0',
        'Price': new_order_params['Price'],
        'ExecType': '0',
        'LeavesQty': '0'
    }

    message_filters_er = [filter_to_grpc("ExecutionReport", params_buy_side_er)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check ExecutionReport",
            prefilter=pre_filter,
            msg_filters=message_filters_er,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value('SECOND'),
            timeout=2000
        )
    )

    amend_params = {
        'Side': new_order_params['Side'],
        'Account': new_order_params['Account'],
        'OrderQty': 1500,
        'ClOrdID': new_order_params['ClOrdID'],
        'Instrument': new_order_params['Instrument'],
        'HandlInst': new_order_params['HandlInst'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrigClOrdID': new_order_params['ClOrdID'],
        'OrdType': '2'
    }

    rule_amend = rule_manager.add_OCRR(buy_side_conn)
    amend_order = Stubs.fix_act.placeOrderCancelFIX(
        request=convert_to_request("Send amend order", sell_side_conn, case_id,
                                   wrap_message(amend_params, "OrderCancelReplaceRequest", sell_side_conn)))

    checkpoint_3 = amend_order.checkpoint_id

    amend_er_params = {
        'ExecID': '*',
        'OrderQty': amend_params['OrderQty'],
        'LastQty': '0',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': new_order_params['Side'],
        'AvgPx': '0',
        'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
        'OrdStatus': '0',
        'SettlDate': new_er_params['SettlDate'],
        'Currency': 'EUR',
        'TimeInForce': '0',
        'ExecType': '5',
        'HandlInst': new_order_params['HandlInst'],
        'LeavesQty': amend_params['OrderQty'],
        'NoParty': pending_er_params['NoParty'],
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': '2',
        'ClOrdID': new_order_params['ClOrdID'],
        'QtyType': '0',
        'ExecRestatementReason': '4',
        'Price': '20',
        'TargetStrategy': new_order_params['TargetStrategy'],
        'Instrument': new_order_params['Instrument'],
        'OrigClOrdID': new_order_params['ClOrdID']

    }

    message_filters_amend_order = [
        filter_to_grpc("ExecutionReport", amend_er_params)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side",
            prefilter=pre_filter,
            msg_filters=message_filters_amend_order,
            checkpoint=checkpoint_3,
            connectivity=sell_side_conn,
            event_id=case_id,
            timeout=2000

        )
    )

    amend_params_buy = {
        'Side': '2',
        'Account': 'KEPLER',
        'OrderQty': amend_params['OrderQty'],
        'ClOrdID': '*',
        'Instrument': instrument_2,
        'OrderID': '*',
        'TransactTime': '*',
        'ExDestination': 'XPAR',
        'ChildOrderID': '*',
        'OrigClOrdID': '*',
        'OrdType': '2',
        'OrderCapacity': 'A',
        'Price': 20,
        'TimeInForce': '0',
        'HandlInst': '1',
        'Currency': 'EUR'
    }

    message_filters_amend_buy = [
        filter_to_grpc('OrderCancelReplaceRequest', amend_params_buy)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side",
            prefilter=pre_filter,
            msg_filters=message_filters_amend_buy,
            checkpoint=checkpoint_3,
            connectivity=buy_side_conn,
            event_id=case_id,
            timeout=2000

        )
    )

    amend_params_buy_er = {
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': amend_params['OrderQty'],
        'OrdType': '2',
        'ClOrdID': '*',
        'Text': "OCRRRule",
        'OrderID': '*',
        'TransactTime': '*',
        'Side': amend_er_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'Price': 20,
        'TimeInForce': '0',
        'ExecType': amend_er_params['ExecType'],
        'LeavesQty': amend_params['OrderQty'],
        'OrigClOrdID': '*'
    }

    message_filters_amend_buy_er = [
        filter_to_grpc('ExecutionReport', amend_params_buy_er)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check ExecutionReport",
            prefilter=pre_filter,
            msg_filters=message_filters_amend_buy_er,
            checkpoint=checkpoint_3,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND"),
            timeout=2000

        )
    )

    cancel_params = {
        'Side': new_order_params['Side'],
        'ClOrdID': new_order_params['ClOrdID'],
        'Instrument': new_order_params['Instrument'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrigClOrdID': new_order_params['ClOrdID']
    }

    rule_cancel = rule_manager.add_OCR(buy_side_conn)
    cancel_order = Stubs.fix_act.placeOrderCancelFIX(
        request=convert_to_request("Send cancel order", sell_side_conn, case_id,
                                   wrap_message(cancel_params, "OrderCancelRequest", sell_side_conn)))

    checkpoint_2 = cancel_order.checkpoint_id

    cancel_er_params = {
        'ExecID': '*',
        'OrderQty': amend_params['OrderQty'],
        'LastQty': '0',
        'OrderID': '*',
        'TransactTime': '*',
        'Side': new_order_params['Side'],
        'AvgPx': '0',
        'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
        'OrdStatus': '4',
        'SettlDate': new_er_params['SettlDate'],
        'Currency': 'EUR',
        'TimeInForce': '0',
        'ExecType': '4',
        'HandlInst': new_order_params['HandlInst'],
        'LeavesQty': '0',
        'NoParty': pending_er_params['NoParty'],
        'CumQty': '0',
        'LastPx': '0',
        'OrdType': '2',
        'ClOrdID': new_order_params['ClOrdID'],
        'QtyType': '0',
        'ExecRestatementReason': '4',
        'Price': '20',
        'TargetStrategy': new_order_params['TargetStrategy'],
        'Instrument': new_order_params['Instrument'],
        'OrigClOrdID': new_order_params['ClOrdID']
    }

    message_filters_cancel_order = [
        filter_to_grpc("ExecutionReport", cancel_er_params)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side",
            prefilter=pre_filter,
            msg_filters=message_filters_cancel_order,
            checkpoint=checkpoint_2,
            connectivity=sell_side_conn,
            event_id=case_id,
            timeout=2000

        )
    )

    cancel_params_buy = {
        'Side': '2',
        'Account': 'KEPLER',
        'OrderQty': amend_params['OrderQty'],
        'ClOrdID': '*',
        'Instrument': instrument_2,
        'OrderID': '*',
        'TransactTime': '*',
        'ExDestination': 'XPAR',
        'ChildOrderID': '*',
        'OrigClOrdID': '*'
    }

    message_filters_cancel_buy = [
        filter_to_grpc('OrderCancelRequest', cancel_params_buy)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side",
            prefilter=pre_filter,
            msg_filters=message_filters_cancel_buy,
            checkpoint=checkpoint_2,
            connectivity=buy_side_conn,
            event_id=case_id,
            timeout=2000

        )
    )

    cancel_params_buy_er = {
        'CumQty': '0',
        'ExecID': '*',
        'OrderQty': amend_params['OrderQty'],
        'ClOrdID': '*',
        'Text': "sim work",
        'OrderID': '*',
        'TransactTime': '*',
        'Side': cancel_er_params['Side'],
        'AvgPx': '0',
        'OrdStatus': cancel_er_params['ExecType'],
        'ExecType': cancel_er_params['ExecType'],
        'LeavesQty': '0',
        'OrigClOrdID': '*'
    }

    message_filters_cancel_buy_er = [
        filter_to_grpc('ExecutionReport', cancel_params_buy_er)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check ExecutionReport",
            prefilter=pre_filter,
            msg_filters=message_filters_cancel_buy_er,
            checkpoint=checkpoint_2,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND"),
            timeout=2000

        )
    )

    rule_manager.remove_rule(rule)
    print(f"Case {case_name} was executed")

    rule_manager.remove_rule(rule_amend)
    print(f"Case {case_name} was executed")

    rule_manager.remove_rule(rule_cancel)
    print(f"Case {case_name} was executed")


if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()
