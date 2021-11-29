import logging
import time
from copy import deepcopy
from datetime import datetime, timedelta

from th2_grpc_common.common_pb2 import Direction

from custom import basic_custom_actions as bca
from custom.basic_custom_actions import create_event, timestamps, client_orderid, wrap_message, convert_to_request
from rule_management import RuleManager
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def my_test_case():
    rule_manager = RuleManager()
    nos_rule = rule_manager.add_NOS("fix-bs-eq-paris", 'KEPLER')
    ocr_rule = rule_manager.add_OCR("fix-bs-eq-paris")
    ocrr_rule = rule_manager.add_OCRR("fix-bs-eq-paris")
    case_name = "Example_mg"
    verifier = Stubs.verifier

    # connection box - gtwquod3 always uses Account Kepler
    sell_side_conn = "gtwquod3"

    case_id = create_event(case_name)
    instrument_1 = {
        'Symbol': 'FR0010380626_EUR',
        'SecurityID': 'FR0010380626',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    # new_order_params -> set the order fields
    new_order_params = {
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 100,
        'TimeInForce': '0',
        'Price': 15,
        'OrdType': '2',  # Limit
        'ClOrdID': client_orderid(9),
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': instrument_1,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': "1011"
    }

    new_order = Stubs.fix_act.placeOrderFIX(
        request=convert_to_request(
            "Send new Order", sell_side_conn, case_id,
            wrap_message(new_order_params, "NewOrderSingle", sell_side_conn)))

    pending_er_params = {
        'Account': 'KEPLER',
        'HandlInst': new_order_params['HandlInst'],
        'Side': new_order_params['Side'],
        'TimeInForce': new_order_params['TimeInForce'],
        'OrdType': new_order_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': new_order_params['TargetStrategy'],
        'ClOrdID': '*',
        'OrderID': '*',
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
        'NoParty': [{
            'PartyID': 'gtwquod3',
            'PartyIDSource': 'D',
            'PartyRole': '36'
        }],
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': new_order_params['Instrument']
    }
    checkpoint_1 = new_order.checkpoint_id

    new_er_params = deepcopy(pending_er_params)
    del new_er_params['Account']
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = new_order_params['ClientAlgoPolicyID']
    new_er_params['SettlDate'] = (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d")
    new_er_params['ExecRestatementReason'] = '4'

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL")
        }
    }

    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)

    msg_filter_sell = [
        bca.filter_to_grpc('ExecutionReport', pending_er_params),
        bca.filter_to_grpc('ExecutionReport', new_er_params)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_sell,
            checkpoint=checkpoint_1,
            connectivity='gtwquod3',
            event_id=case_id,
            timeout=5000
        )
    )

    instrument_2 = {
        'Symbol': 'PROL',
        'SecurityType': 'CS',
        'SecurityID': 'FR0010380626',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    #  NOS parameters in case of buy side
    nos_params_bs = {
        'ClOrdID': '*',
        'Account': 'KEPLER',
        'SettlDate': '*',
        'HandlInst': '1',
        'ExDestination': 'XPAR',
        'Instrument': instrument_2,
        'Side': '2',
        'TransactTime': '*',
        'OrderQty': new_order_params['OrderQty'],
        'OrdType': '2',
        'Price': new_order_params['Price'],
        'Currency': 'EUR',
        'TimeInForce': '0',
        'OrderCapacity': 'A',
        'ChildOrderID': '*'
    }

    msg_filter_nos = [
        bca.filter_to_grpc('NewOrderSingle', nos_params_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_nos,
            checkpoint=checkpoint_1,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=5000
        )
    )

    #  executable parameters for NOS buy side
    nos_exec_bs = {
        'OrderID': '*',
        'ClOrdID': '*',
        'ExecID': '*',
        'ExecType': '0',
        'OrdStatus': '0',
        'Side': nos_params_bs['Side'],
        'OrderQty': '*',
        'OrdType': nos_params_bs['OrdType'],
        'Price': '*',
        'LeavesQty': '*',
        'CumQty': '0',
        'AvgPx': '0',
        'TransactTime': '*',
        'Text': 'sim work'

    }

    msg_filter_nos_exec = [
        bca.filter_to_grpc('ExecutionReport', nos_exec_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_nos_exec,
            checkpoint=checkpoint_1,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=5000,
            direction=Direction.Value("SECOND")
        )
    )

    # following part is responsible for Amending
    time.sleep(4)

    replace_order_params = {
        'OrigClOrdID': new_order_params['ClOrdID'],
        'ClOrdID': new_order_params['ClOrdID'],
        'SettlDate': (datetime.utcnow() + timedelta(days=2)).strftime("%Y%m%d"),
        'HandlInst': pending_er_params['HandlInst'],
        'Instrument': pending_er_params['Instrument'],
        'Side': pending_er_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': 110,
        'OrdType': pending_er_params['OrdType'],
        'Price': pending_er_params['Price'],
        'TargetStrategy': pending_er_params['TargetStrategy'],
        'Currency': pending_er_params['Currency'],
        'TimeInForce': pending_er_params['TimeInForce'],
        'OrderCapacity': pending_er_params['OrderCapacity']

    }
    logger.debug("Amend order with ClOrdID = {}".format(pending_er_params['ClOrdID']))
    replace_order = Stubs.fix_act.placeOrderReplaceFIX(
        request=convert_to_request(
            'Send OrderCancelReplaceRequest',
            sell_side_conn, case_id,
            wrap_message(replace_order_params, "OrderCancelReplaceRequest", sell_side_conn)))

    exec_replace_ord = {
        'ClOrdID': '*',
        'Instrument': pending_er_params['Instrument'],
        'OrderQty': 110,
        'Price': pending_er_params['Price'],
        'TargetStrategy': pending_er_params['TargetStrategy'],
        'ExecID': "*",
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '5',
        'LeavesQty': replace_order_params['OrderQty'],
        'NoParty': pending_er_params['NoParty'],
        'OrigClOrdID': replace_order_params['OrigClOrdID'],
        'OrderID': '*',
        'SettlDate': replace_order_params['SettlDate'],
        'HandlInst': "*",
        'Side': pending_er_params['Side'],
        'TransactTime': '*',
        'OrdType': replace_order_params['OrdType'],
        'OrderCapacity': replace_order_params['OrderCapacity'],
        'TimeInForce': pending_er_params['TimeInForce'],
        'Currency': replace_order_params['Currency'],
        'SecondaryAlgoPolicyID': new_order_params['ClientAlgoPolicyID'],
        'ExecRestatementReason': "*"
    }
    checkpoint_2 = replace_order.checkpoint_id

    msg_filter_replace = [
        bca.filter_to_grpc('ExecutionReport', exec_replace_ord)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_replace,
            checkpoint=checkpoint_2,
            connectivity='gtwquod3',
            event_id=case_id,
            timeout=5000
        )
    )

    # parameters for amendment in case of BuySide(BS)
    replace_params_bs = {
        'OrderID': '*',
        'OrigClOrdID': '*',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'Account': 'KEPLER',
        'HandlInst': '1',
        'ExDestination': 'XPAR',
        'Instrument': instrument_2,
        'Side': '2',
        'TransactTime': '*',
        'OrderQty': 110,
        'OrdType': '2',
        'Price': new_order_params['Price'],
        'Currency': 'EUR',
        'TimeInForce': '0',
        'OrderCapacity': 'A'

    }
    exec_replace_bs = {
        'ClOrdID': '*',
        'OrderQty': 110,
        'Price': pending_er_params['Price'],
        'ExecID': "*",
        'CumQty': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '5',
        'LeavesQty': replace_order_params['OrderQty'],
        'OrigClOrdID': '*',
        'OrderID': '*',
        'Side': pending_er_params['Side'],
        'TransactTime': '*',
        'OrdType': replace_order_params['OrdType'],
        'TimeInForce': pending_er_params['TimeInForce'],
        'Text': "OCRRRule"
    }

    msg_filter_replace_bs = [
        bca.filter_to_grpc('OrderCancelReplaceRequest', replace_params_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_replace_bs,
            checkpoint=checkpoint_2,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=5000
        )
    )

    msg_filter_replace_exec = [
        bca.filter_to_grpc('ExecutionReport', exec_replace_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_replace_exec,
            checkpoint=checkpoint_2,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=7000,
            direction=Direction.Value('SECOND')
        )
    )

    # cancel previously Amended order
    cancel_order_params = {
        'OrigClOrdID': replace_order_params['ClOrdID'],
        'ClOrdID': replace_order_params['ClOrdID'],
        'Instrument': replace_order_params['Instrument'],
        'Side': replace_order_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': replace_order_params['OrderQty'],
    }

    cancel_order = Stubs.fix_act.placeOrderCancelFIX(
        request=convert_to_request(
            'Send CancelOrderRequest',
            sell_side_conn,
            case_id,
            wrap_message(cancel_order_params, 'OrderCancelRequest', sell_side_conn)
        ))

    execute_cancel_ord = {
        'OrigClOrdID': cancel_order_params['OrigClOrdID'],
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': '*',
        'Instrument': cancel_order_params['Instrument'],
        'Side': new_order_params['Side'],
        'TransactTime': '*',
        'OrderQty': cancel_order_params['OrderQty'],
        'TargetStrategy': new_order_params['TargetStrategy'],
        'TimeInForce': new_order_params['TimeInForce'],
        'ExecID': "*",
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'NoParty': pending_er_params['NoParty'],
        'ExecRestatementReason': "*",
        'SecondaryAlgoPolicyID': new_order_params['ClientAlgoPolicyID'],
        'SettlDate': replace_order_params['SettlDate'],
        'Currency': 'EUR',
        'HandlInst': '2',
        'OrdType': '2',
        'OrderCapacity': 'A',
        'Price': new_order_params['Price']
    }
    checkpoint_3 = cancel_order.checkpoint_id
    msg_filter_cancel = [
        bca.filter_to_grpc('ExecutionReport', execute_cancel_ord)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check sell side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_cancel,
            checkpoint=checkpoint_3,
            connectivity='gtwquod3',
            event_id=case_id,
            timeout=5000
        )
    )

    # Cancel order params BS
    cancel_params_bs = {
        'OrigClOrdID': '*',
        'OrderID': '*',
        'ClOrdID': '*',
        'Account': 'KEPLER',
        'Instrument': instrument_2,
        'ExDestination': 'XPAR',
        'Side': '2',
        'TransactTime': '*',
        'OrderQty': replace_params_bs['OrderQty'],
        'ChildOrderID': '*'
    }

    exec_cancel_bs = {
        'OrderID': '*',
        'ExecID': "*",
        'ExecType': '4',
        'OrdStatus': '4',
        'CumQty': '0',
        'AvgPx': '0',
        'Text': 'sim work',
        'LeavesQty': '0',
        'TransactTime': '*',
        'Side': cancel_params_bs['Side'],
        'ClOrdID': '*',
        'OrderQty': cancel_params_bs['OrderQty'],
        'OrigClOrdID': '*'

    }

    msg_filter_cancel_bs = [
        bca.filter_to_grpc('OrderCancelRequest', cancel_params_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_cancel_bs,
            checkpoint=checkpoint_3,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=4000

        )
    )

    msg_filter_cancel_exec = [
        bca.filter_to_grpc('ExecutionReport', exec_cancel_bs)
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side message from Paris",
            prefilter=pre_filter_sim,
            msg_filters=msg_filter_cancel_exec,
            checkpoint=checkpoint_3,
            connectivity='fix-bs-eq-paris',
            event_id=case_id,
            timeout=4000,
            direction=Direction.Value('SECOND')
        )
    )

    rule_manager.remove_rule(nos_rule)
    rule_manager.remove_rule(ocr_rule)
    rule_manager.remove_rule(ocrr_rule)


if __name__ == '__main__':
    my_test_case()
    Stubs.factory.close()
