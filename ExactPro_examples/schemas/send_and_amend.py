import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import ValueFilter, MessageFilter, FilterOperation, ConnectionID
from th2_grpc_check1.check1_pb2 import PreFilter, CheckSequenceRuleRequest
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time

    case_id = bca.create_event(case_name, report_id)  # Create sub-report for case

    # Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': '1004'
    }
    specific_order_params = {   # There are reusable and specific for submission parameters
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': case_params['Instrument'],
        # 'ExDestination': 'QDL1',
        'ExDestination': 'XPAR',
        'ComplianceID': 'FX5',
        'Text': '-204',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'StrategyName': 'ICEBERG',
        'Price': case_params['Price'],
        'OrderQty': case_params['OrderQty'],
    }
    logger.debug("Send new order with ClOrdID = {}".format(specific_order_params['ClOrdID']))
    enter_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', specific_order_params, case_params['TraderConnectivity'])
        )
    )

    # Prepare system output
    execution_report1_params = {
        **reusable_order_params,
        'ClOrdID': specific_order_params['ClOrdID'],
        'OrderID': '*',
        # 'OrderID': enter_order[0].response_message.fields['OrderID'].simple_value,
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': case_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'Price': case_params['Price'],
        'OrderQty': case_params['OrderQty'],
    }
    logger.debug("Verify received Execution Report (OrdStatus = Pending)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport1',
            bca.filter_to_grpc('ExecutionReport', execution_report1_params, ["ClOrdID", "OrdStatus"]),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    execution_report2_params = {
        **reusable_order_params,
        'ClOrdID': specific_order_params['ClOrdID'],
        'OrderID': execution_report1_params['OrderID'],
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': case_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'NoStrategyParameters': [
            {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}],
        'Price': case_params['Price'],
        'OrderQty': case_params['OrderQty'],
    }
    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport2',
            bca.filter_to_grpc('ExecutionReport', execution_report2_params, ["ClOrdID", "OrdStatus"]),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )
    replace_order_params = {
        'OrigClOrdID': specific_order_params['ClOrdID'],
        # 'ClOrdID': str(int(specific_order_params['ClOrdID']) + 1),
        'ClOrdID': bca.client_orderid(9),
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Instrument': case_params['Instrument'],
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrdType': case_params['OrdType'],
        'OrderQty': case_params['newOrderQty'],
        'Price': case_params['newPrice'],
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'OrderCapacity': 'A',
    }
    logger.debug("Amend order with ClOrdID = {}".format(specific_order_params['ClOrdID']))
    replace_order = act.placeOrderReplaceFIX(
        bca.convert_to_request(
            'Send OrderCancelReplaceRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params, case_params['TraderConnectivity'])
        ))

    execution_report3_params = {
        **reusable_order_params,
        'ClOrdID': replace_order_params['ClOrdID'],
        'OrderID': execution_report1_params['OrderID'],
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '5',
        'LeavesQty': case_params['newOrderQty'],
        'Instrument': case_params['Instrument'],
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'NoStrategyParameters': execution_report2_params['NoStrategyParameters'],
        # 'NoStrategyParameters': [
        #     {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}],
        'ExecRestatementReason': '4',
        'Price': case_params['newPrice'],
        'OrderQty': case_params['newOrderQty'],
    }
    logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport3',
            bca.filter_to_grpc('ExecutionReport', execution_report3_params, ["ClOrdID", "OrdStatus"]),
            replace_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )
    cancel_order_params = {
        'OrigClOrdID': specific_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': (specific_order_params['ClOrdID']),
        'Instrument': specific_order_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Text': 'Cancel order'
    }
    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
        ))

    execution_report4_params = {
        **reusable_order_params,
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': execution_report1_params['OrderID'],
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': case_params['Instrument'],
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'NoStrategyParameters': execution_report2_params['NoStrategyParameters'],
        'ExecRestatementReason': '4'
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport3',
            bca.filter_to_grpc('ExecutionReport', execution_report4_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )
    if timeouts:
        time.sleep(5)

    # ------------------------------------------------
    pre_filter = PreFilter(
        fields={
            'header': ValueFilter(
                message_filter=MessageFilter(
                    fields={
                        'MsgType': ValueFilter(
                            simple_filter='0', operation=FilterOperation.NOT_EQUAL
                        ),
                        'SenderCompID': ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': ValueFilter(simple_filter=case_params['TargetCompID'])
                    }
                )
            )
        }
    )

    message_filters = [
        bca.filter_to_grpc('ExecutionReport', execution_report1_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report2_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report3_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report4_params, ["ClOrdID", "OrdStatus"])
    ]

    checkpoint = enter_order.checkpoint_id

    check_sequence_rule = CheckSequenceRuleRequest(
        pre_filter=pre_filter,
        message_filters=message_filters,
        checkpoint=checkpoint,
        timeout=1000,
        connectivity_id=ConnectionID(session_alias=case_params['TraderConnectivity']),
        parent_event_id=case_id,
        description='Some description',
        check_order=True
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule)

    if timeouts:
        time.sleep(5)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
