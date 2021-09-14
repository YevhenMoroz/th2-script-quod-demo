from stubs import Stubs
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request, \
    filter_to_grpc, create_check_sequence_rule, prefilter_to_grpc
from datetime import datetime, timedelta
from copy import deepcopy
from rule_management import RuleManager
from th2_grpc_common.common_pb2 import Direction
import time


def run_test_case():
    seconds, nanos = timestamps()
    case_name = "adil test"
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
            'PartyID': sell_side_conn,
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
    pre_filter_sim = prefilter_to_grpc(pre_filter_sim_params)

    # message filter list for 2 types of Execution Report
    message_filters_sell = [
        filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
        filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus'])
    ]

    # Creating request for verification to check1
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sell,
            checkpoint=checkpoint_1,
            connectivity=sell_side_conn,
            event_id=case_id,
        )
    )
    buy_side_instrument = {
        'SecurityType': 'CS',
        'Symbol': 'GARD',
        'SecurityID': 'FR0000065435',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    # new order single params for buy side
    order_params_buys_side = deepcopy(new_order_params)
    order_params_buys_side.pop("ClientAlgoPolicyID")
    order_params_buys_side.pop("ComplianceID")
    order_params_buys_side.pop("TargetStrategy")
    order_params_buys_side["ClOrdID"] = "*"
    order_params_buys_side["TransactTime"] = "*"
    order_params_buys_side["ChildOrderID"] = "*"
    order_params_buys_side["SettlDate"] = "*"
    order_params_buys_side["Instrument"] = buy_side_instrument
    order_params_buys_side["HandlInst"] = "1"
    order_params_buys_side["ExDestination"] = "XPAR"
    message_filters_nos_bs = [filter_to_grpc("NewOrderSingle", order_params_buys_side, ["SecurityID"])]

    # request for module check1, which compares NOS message from the buy side
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side NOS message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_nos_bs,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id
        )
    )

    # Execution report params for buy side
    er_params_buy_side = {
        "OrderID": "*",
        "ExecID": "*",
        "ExecType": "0",
        "OrdStatus": "0",
        "CumQty": "0",
        "AvgPx": "0",
        "Text": "sim work",
        "LeavesQty": "0",
        "TransactTime": "*",
        "OrderQty": new_order_params["OrderQty"],
        "OrdType": new_order_params["OrdType"],
        "ClOrdID": "*",
        "Side": new_order_params["Side"],
        "Price": new_order_params["Price"]
    }
    message_filters_er_bs = [filter_to_grpc("ExecutionReport", er_params_buy_side)]

    # request for module check1, which compares the NOS message from the buy side
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side ER message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_er_bs,
            checkpoint=checkpoint_1,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND")
        )
    )
    print("flag")
    time.sleep(5)

    amend_order_params = {
        "OrigClOrdID": new_order_params["ClOrdID"],
        "ClOrdID": new_order_params["ClOrdID"],
        "Account": new_order_params["Account"],
        "HandlInst": new_order_params["HandlInst"],
        "Side": new_order_params["Side"],
        "Instrument": new_order_params["Instrument"],
        "TransactTime": datetime.utcnow().isoformat(),
        "OrdType": "2",
        "OrderQty": "250"
    }
    rule_ocrr = rule_manager.add_OCRR(buy_side_conn)
    amend_order = Stubs.fix_act.placeOrderReplaceFIX(
        request=convert_to_request("Send cancel/replace order", sell_side_conn, case_id,
                                   wrap_message(amend_order_params, "OrderCancelReplaceRequest", sell_side_conn))
    )
    checkpoint_2 = amend_order.checkpoint_id

    ocrr_er_params = {
        "ExecID": "*",
        "OrderID": "*",
        "Side": new_order_params["Side"],
        "AvgPx": "0",
        "OrdStatus": "0",
        "ExecType": "5",
        "LeavesQty": amend_order_params["OrderQty"],
        "Instrument": new_order_params["Instrument"],
        "CumQty": "0",
        "OrdType": "2",
        "TransactTime": "*",
        "OrderQty": "250",
        "LastQty": "0",
        "SecondaryAlgoPolicyID": new_order_params['ClientAlgoPolicyID'],
        "SettlDate": new_er_params["SettlDate"],
        "Currency": new_order_params['Currency'],
        "TimeInForce": "0",
        "HandlInst": new_order_params['HandlInst'],
        "NoParty": pending_er_params['NoParty'],
        "LastPx": "0",
        "ClOrdID": new_order_params['ClOrdID'],
        "OrigClOrdID": new_order_params['ClOrdID'],
        "QtyType": "0",
        "ExecRestatementReason": "4",
        "Price": "20",
        "TargetStrategy": new_order_params['TargetStrategy']
    }

    message_filters_ocrr = [filter_to_grpc("ExecutionReport", ocrr_er_params)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_ocrr,
            checkpoint=checkpoint_2,
            connectivity=sell_side_conn,
            event_id=case_id
        )
    )

    ocrr_er_params_bs = {
        "ExecID": "*",
        "OrderID": "*",
        "Side": new_order_params["Side"],
        "AvgPx": "0",
        "OrdStatus": "0",
        "ExecType": "5",
        "LeavesQty": amend_order_params["OrderQty"],
        "CumQty": "0",
        "OrdType": "2",
        "TransactTime": "*",
        "OrderQty": amend_order_params["OrderQty"],
        "ClOrdID": "*",
        "OrigClOrdID": "*",
        "Text": "OCRRRule",
        "Price": "20",
        "TimeInForce": "0",
    }

    message_filters_ocrr_er_bs = [filter_to_grpc("ExecutionReport", ocrr_er_params_bs)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_ocrr_er_bs,
            checkpoint=checkpoint_2,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND")
        )
    )

    ocrr_params_bs = {
        "OrigClOrdID": "*",
        "ClOrdID": "*",
        "ChildOrderID": "*",
        "Account": new_order_params["Account"],
        "Side": new_order_params["Side"],
        "Instrument": buy_side_instrument,
        "TransactTime": "*",
        "OrdType": "2",
        "OrderQty": "250",
        "OrderCapacity": "A",
        "OrderID": "*",
        "Price": "20",
        "Currency": "EUR",
        "TimeInForce": "0",
        "HandlInst": "1",
        "ExDestination": "XPAR"
    }

    message_filters_ocrr_bs = [filter_to_grpc("OrderCancelReplaceRequest", ocrr_params_bs)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_ocrr_bs,
            checkpoint=checkpoint_2,
            connectivity=buy_side_conn,
            event_id=case_id,
        )
    )

    # Order cancel request params
    cancel_order_params = {
        "OrigClOrdID": new_order_params["ClOrdID"],
        "ClOrdID": new_order_params["ClOrdID"],
        "Instrument": new_order_params["Instrument"],
        "TransactTime": datetime.utcnow().isoformat(),
        "Side": new_order_params["Side"]
    }
    rule_ocr = rule_manager.add_OCR(buy_side_conn)
    cancel_order = Stubs.fix_act.placeOrderCancelFIX(
        request=convert_to_request("Send cancel order", sell_side_conn, case_id,
                                   wrap_message(cancel_order_params, "OrderCancelRequest", sell_side_conn))
    )
    checkpoint_3 = cancel_order.checkpoint_id

    # OCR execution report params
    ocr_er_params = {
        "OrigClOrdID": new_order_params["ClOrdID"],
        "SettlDate": new_er_params["SettlDate"],
        "SecondaryAlgoPolicyID": new_er_params["SecondaryAlgoPolicyID"],
        "ExecID": "*",
        "OrderQty": amend_order_params["OrderQty"],
        "LastQty": "0",
        "OrderID": "*",
        "TransactTime": "*",
        "Side": new_order_params["Side"],
        "AvgPx": "0",
        "OrdStatus": "4",
        "Currency": "EUR",
        "TimeInForce": "0",
        "ExecType": "4",
        "HandlInst": new_order_params["HandlInst"],
        "LeavesQty": "0",
        'NoParty': pending_er_params["NoParty"],
        "Instrument": new_order_params["Instrument"],
        "CumQty": "0",
        "LastPx": "0",
        "OrdType": "2",
        "ClOrdID": new_order_params["ClOrdID"],
        "QtyType": "0",
        "Price": "20",
        "TargetStrategy": new_order_params["TargetStrategy"],
        "ExecRestatementReason": "4"
    }

    message_filters_ocr = [filter_to_grpc("ExecutionReport", ocr_er_params)]

    # Creating request for verification to check1
    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_ocr,
            checkpoint=checkpoint_3,
            connectivity=sell_side_conn,
            event_id=case_id
        )
    )

    # Execution Report params from buy side
    ocr_er_params_bs = {
        "CumQty": "0",
        "ExecID": "*",
        "OrderQty": amend_order_params["OrderQty"],
        "ClOrdID": "*",
        "Text": "sim work",
        "OrderID": "*",
        "TransactTime": "*",
        "Side": ocr_er_params["Side"],
        "ExecType": ocr_er_params["ExecType"],
        "OrdStatus": ocr_er_params["ExecType"],
        "AvgPx": "0",
        "LeavesQty": "0",
        "OrigClOrdID": "*"
    }

    message_filter_ocr_er_bs = [filter_to_grpc('ExecutionReport', ocr_er_params_bs)]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filter_ocr_er_bs,
            checkpoint=checkpoint_3,
            connectivity=buy_side_conn,
            event_id=case_id,
            direction=Direction.Value("SECOND")
        )
    )

    # OCR message from buy side
    ocr_params_bs = {
        "Side": "2",
        "Account": "KEPLER",
        "OrderQty": amend_order_params["OrderQty"],
        "ClOrdID": "*",
        "Instrument": buy_side_instrument,
        "OrderID": "*",
        "ExDestination": "XPAR",
        "ChildOrderID": "*",
        "OrigClOrdID": "*",
        "TransactTime": "*"
    }

    message_filter_ocr_bs = [
        filter_to_grpc('OrderCancelRequest', ocr_params_bs)
    ]

    Stubs.verifier.submitCheckSequenceRule(
        create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=message_filter_ocr_bs,
            checkpoint=checkpoint_3,
            connectivity=buy_side_conn,
            event_id=case_id,
        )
    )

    rule_manager.remove_rule(rule)
    rule_manager.remove_rule(rule_ocrr)
    rule_manager.remove_rule(rule_ocr)


if __name__ == '__main__':
    run_test_case()
    Stubs.factory.close()
