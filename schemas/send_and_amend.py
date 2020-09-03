import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules import verifier_pb2
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
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': '1004'
    }
    specific_order_params = {   # There are reusable and specific for submition parameters
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
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', specific_order_params)
        ))

    # Prepare system output
    execution_report1_params = {
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
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'Price': case_params['Price'],
        'OrderQty': case_params['OrderQty'],
    }
    logger.debug("Verify received Execution Report (OrdStatus = Pending)")
    bca.verify_response(
        verifier,
        'Receive ExecutionReport1',
        bca.create_filter('ExecutionReport', execution_report1_params),
        enter_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
    bca.verify_response(
        verifier,
        'Receive ExecutionReport2',
        bca.create_filter('ExecutionReport', execution_report2_params),
        enter_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params)
        ))

    er3 = execution_report3_params = {
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
    bca.verify_response(
        verifier,
        'Receive ExecutionReport3',
        bca.create_filter('ExecutionReport', execution_report3_params),
        replace_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
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
    bca.verify_response(
        verifier,
        'Receive ExecutionReport3',
        bca.create_filter('ExecutionReport', execution_report4_params),
        cancel_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )
    if timeouts:
        time.sleep(5)

    # ------------------------------------------------
    pre_filter = verifier_pb2.PreFilter(
        fields={
            # 'Instrument': infra_pb2.ValueFilter(
            #     message_filter=infra_pb2.MessageFilter(
            #         fields={
            #             'Symbol': infra_pb2.ValueFilter(
            #                 simple_filter=execution_report1_params['Instrument']['Symbol']),
            #             'SecurityID': infra_pb2.ValueFilter(
            #                 simple_filter=execution_report1_params['Instrument']['SecurityID']),
            #             'SecurityIDSource': infra_pb2.ValueFilter(
            #                 simple_filter=execution_report1_params['Instrument']['SecurityIDSource']),
            #             'SecurityExchange': infra_pb2.ValueFilter(
            #                 simple_filter=execution_report1_params['Instrument']['SecurityExchange']),
            #         }
            #     )
            # ),
            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={
                        'MsgType': infra_pb2.ValueFilter(
                            simple_filter='0', operation=infra_pb2.FilterOperation.NOT_EQUAL
                        ),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID'])
                    }
                )
            ),
        }
    )

    message_filters = [
        bca.create_filter('ExecutionReport', execution_report1_params),
        bca.create_filter('ExecutionReport', execution_report2_params),
        bca.create_filter('ExecutionReport', execution_report3_params),
        bca.create_filter('ExecutionReport', execution_report4_params),
    ]

    checkpoint = enter_order.checkpoint_id

    check_sequence_rule = verifier_pb2.CheckSequenceRuleRequest(
        pre_filter=pre_filter,
        message_filters=message_filters,
        checkpoint=checkpoint,
        timeout=1000,
        connectivity_id=infra_pb2.ConnectionID(session_alias=case_params['TraderConnectivity']),
        parent_event_id=case_params['case_id'],
        description='Some description',
        check_order=True
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule)

    # cancel_order_params = {
    #     'OrigClOrdID': specific_order_params['ClOrdID'],
    #     # 'OrderID': '',
    #     'ClOrdID': str(int(specific_order_params['ClOrdID'])+1),
    #     'Instrument': specific_order_params['Instrument'],
    #     'ExDestination': 'QDL1',
    #     'Side': case_params['Side'],
    #     'TransactTime': (datetime.utcnow().isoformat()),
    #     'OrderQty': case_params['OrderQty'],
    #     'Text': 'Cancel order'
    # }
    # cancel_order = bca.send_message(
    #     'Send CancelOrderRequest',
    #     case_params['TraderConnectivity'],
    #     case_params['case_id'],
    #     bca.create_message('OrderCancelRequest', cancel_order_params),
    # )
    #
    # execution_report3_params = {
    #     **reusable_order_params,
    #     'ClOrdID': cancel_order_params['ClOrdID'],
    #     'OrderID': execution_report1_params['OrderID'],
    #     'CumQty': '0',
    #     'LastPx': '0',
    #     'LastQty': '0',
    #     'QtyType': '0',
    #     'AvgPx': '0',
    #     'OrdStatus': '4',
    #     'ExecType': '4',
    #     'LeavesQty': '0',
    #     'Instrument': {
    #         'Symbol': 'TESTQA00.EUR-[QDL1',
    #         'SecurityID': 'TESTQA00',
    #         'SecurityIDSource': '8',
    #         'SecurityExchange': 'QDL1',
    #         'CFICode': 'EMXXXB'
    #     },
    #     'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
    #     'NoStrategyParameters': execution_report2_params['NoStrategyParameters'],
    #     'ExecRestatementReason': '4'
    # }
    # bca.verify_response(
    #     'Receive ExecutionReport3',
    #     bca.create_filter('ExecutionReport', execution_report3_params),
    #     cancel_order,
    #     case_params['TraderConnectivity'],
    #     case_params['case_id']
    # )
    if timeouts:
        time.sleep(5)

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
    # print("Case " + case_name + " is executed in " + str(
    #     round(datetime.now().timestamp() - seconds)) + " sec.")
