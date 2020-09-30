import logging
import time
from grpc_modules import verifier_pb2
from grpc_modules import infra_pb2
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules.act_fix_pb2_grpc import ActStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])

    seconds, nanos = bca.timestamps()  # Store case start time

    # Prepare user input
    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': '1004'
    }
    specific_order_params = {   # There are reusable and specific for submission parameters
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'ExDestination': case_params['ExDestination'],
        'ComplianceID': 'FX5',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'StrategyName': 'ICEBERG'
    }
    logger.debug("Send new order with ClOrdID = {}".format(specific_order_params['ClOrdID']))
    enter_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewOrderSingle',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', specific_order_params)
        ))

    # Prepare system output
    er_pending_params = {
        **reusable_order_params,
        'ClOrdID': specific_order_params['ClOrdID'],
        'OrderID': enter_order.response_message.fields['OrderID'].simple_value,
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
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty']
    }
    logger.debug("Verify received Execution Report (OrdStatus = Pending)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport Pending',
            bca.filter_to_grpc('ExecutionReport', er_pending_params, ["ClOrdID", "OrdStatus"]),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    er_new_params = {
        **reusable_order_params,
        'ClOrdID': specific_order_params['ClOrdID'],
        'OrderID': er_pending_params['OrderID'],
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
        'ExecRestatementReason': '4',
        'NoStrategyParameters': [
            {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}]
    }
    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport New',
            bca.filter_to_grpc('ExecutionReport', er_new_params, ["ClOrdID", "OrdStatus"]),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    instrument_3_2 = {
        'SecurityType': 'CS',
        'Symbol': 'PAR',
        'SecurityID': 'FR0010263202',
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    newordersingle_params = {
        'Account': case_params['Account'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': specific_order_params['DisplayInstruction']['DisplayQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'Instrument': instrument_3_2,
        'ExDestination': case_params['ExDestination'],
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Transmitted NewOrderSingle',
            bca.filter_to_grpc('NewOrderSingle', newordersingle_params),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )
    er_sim_params = {
        'ClOrdID': '*',
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'OrderQty': specific_order_params['DisplayInstruction']['DisplayQty'],
        'OrdType': case_params['OrdType'],
        'Side': case_params['Side'],
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': '0',
        'Text': '*',
    }

    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport New Sim',
            bca.filter_to_grpc("ExecutionReport", er_sim_params, ['text', 'OrdStatus']),
            enter_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_params['case_id'],
            infra_pb2.Direction.Value("SECOND")
        )
    )
    cancel_order_params = {
        'OrigClOrdID': specific_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': specific_order_params['ClOrdID'],
        # 'ClOrdID': str(int(specific_order_params['ClOrdID'])+0),
        'Instrument': specific_order_params['Instrument'],
        'ExDestination': case_params['ExDestination'],
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
    }
    logger.debug("Cancel order with ClOrdID = {}".format(specific_order_params['ClOrdID']))
    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
        ))

    cancel_order_params2 = {
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': specific_order_params['DisplayInstruction']['DisplayQty'],
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'Account': case_params['Account'],
        'ChildOrderID': '*',
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Transmitted OrderCancelRequest',
            bca.filter_to_grpc('OrderCancelRequest', cancel_order_params2, ["ClOrdID"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )

    er_cancel_params = {
        **reusable_order_params,
        'ClOrdID': specific_order_params['ClOrdID'],
        'OrderID': er_pending_params['OrderID'],
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': case_params['Instrument'],
        'NoStrategyParameters': er_new_params['NoStrategyParameters'],
        'ExecRestatementReason': '4',
        'ExecID': '*',
        'TransactTime': '*',
        'CxlQty': case_params['OrderQty'],
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'LastMkt': case_params['ExDestination'],
        'Text': '*',

    }
    logger.debug("Verify received Execution Report (OrdStatus = Cancelled)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport Cancel',
            bca.filter_to_grpc('ExecutionReport', er_cancel_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )
    er_sim_cancel_params = {
        'ClOrdID': '*',
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'OrderQty': specific_order_params['DisplayInstruction']['DisplayQty'],
        # 'OrdType': case_params['OrdType'],
        'Side': case_params['Side'],
        # 'LastPx': '0',
        # 'LastQty': '0',
        # 'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Text': '*',
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport Cancel Sim',
            bca.filter_to_grpc('ExecutionReport', er_sim_cancel_params, ["ClOrdID"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_params['case_id'],
            infra_pb2.Direction.Value("SECOND")
        )
    )

    pre_filter_params = {
        'header': {
            'MsgType': '8',
            'SenderCompID': case_params['SenderCompID'],
            'TargetCompID': case_params['TargetCompID']
        }
    }
    pre_filter = bca.prefilter_to_grpc(pre_filter_params)

    pre_filter2_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['SenderCompID2'],
            'TargetCompID': case_params['TargetCompID2'],
            'DeliverToCompID': case_params['DeliverToCompID']
        }
    }
    pre_filter2 = bca.prefilter_to_grpc(pre_filter2_params)

    pre_filter3_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['TargetCompID2'],
            'TargetCompID': case_params['SenderCompID2']
        }
    }
    pre_filter3 = bca.prefilter_to_grpc(pre_filter3_params)

    message_filters = [
        bca.filter_to_grpc('ExecutionReport', er_pending_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', er_new_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', er_cancel_params, ["ClOrdID", "OrdStatus"])
    ]
    message_filters2 = [
        bca.filter_to_grpc('NewOrderSingle', newordersingle_params, ["ClOrdID"]),
        bca.filter_to_grpc('OrderCancelRequest', cancel_order_params2, ["ClOrdID"])
    ]
    message_filters3 = [
        bca.filter_to_grpc('ExecutionReport', er_sim_params, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', er_sim_cancel_params, ["ClOrdID", "OrdStatus"])
    ]
    checkpoint = enter_order.checkpoint_id

    check_sequence_rule = verifier_pb2.CheckSequenceRuleRequest(
        pre_filter=pre_filter,
        message_filters=message_filters,
        checkpoint=checkpoint,
        timeout=1000,
        connectivity_id=infra_pb2.ConnectionID(session_alias=case_params['TraderConnectivity']),
        parent_event_id=case_params['case_id'],
        description='',
        check_order=True
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule)

    check_sequence_rule2 = verifier_pb2.CheckSequenceRuleRequest(
        pre_filter=pre_filter2,
        message_filters=message_filters2,
        checkpoint=checkpoint,
        timeout=1000,
        connectivity_id=infra_pb2.ConnectionID(session_alias=case_params['TraderConnectivity2']),
        parent_event_id=case_params['case_id'],
        description='',
        check_order=True
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule2)

    check_sequence_rule3 = verifier_pb2.CheckSequenceRuleRequest(
        pre_filter=pre_filter3,
        message_filters=message_filters3,
        checkpoint=checkpoint,
        timeout=1000,
        connectivity_id=infra_pb2.ConnectionID(session_alias=case_params['TraderConnectivity2']),
        parent_event_id=case_params['case_id'],
        description='from Sim',
        check_order=True,
        direction=infra_pb2.Direction.values()[1],
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule3)

    if timeouts:
        time.sleep(5)

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))

