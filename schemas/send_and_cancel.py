import logging
import time
from grpc_modules import verifier_pb2
from grpc_modules import infra_pb2
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import quod_simulator_pb2
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2
import grpc

# simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(grpc.insecure_channel('localhost:8081'))
# print(simulator.createQuodNOSRule(request=quod_simulator_pb2.TemplateQuodNOSRule(connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child'))))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = case_params['act_box']
    event_store = case_params['event_store_box']
    verifier = case_params['verifier_box']

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
    specific_order_params = {   # There are reusable and specific for submition parameters
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'ExDestination': 'XPAR',
        'ComplianceID': 'FX5',
        'Text': '-204',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'StrategyName': 'ICEBERG'
        # 'StrategyName': "InternalQuodQa_Iceberg"
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
        # 'ExecID': enter_order.response_message.fields['ExecID'].simple_value,
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
        # 'ExecID': execution_report1_params['ExecID'],
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
            {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}]
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

    cancel_order_params = {
        'OrigClOrdID': specific_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': str(int(specific_order_params['ClOrdID'])+1),
        'Instrument': specific_order_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Text': 'Cancel order'
    }
    logger.debug("Cancel order with ClOrdID = {}".format(specific_order_params['ClOrdID']))
    cancel_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
        ))

    execution_report3_params = {
        **reusable_order_params,
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': execution_report1_params['OrderID'],
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
    logger.debug("Verify received Execution Report (OrdStatus = Cancelled)")
    bca.verify_response(
        verifier,
        'Receive ExecutionReport3',
        bca.create_filter('ExecutionReport', execution_report3_params),
        cancel_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )

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
                    fields={'MsgType': infra_pb2.ValueFilter(
                        simple_filter='0', operation=infra_pb2.FilterOperation.NOT_EQUAL),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID'])
                    }))

        })

    message_filters = [
        bca.create_filter('ExecutionReport', execution_report1_params),
        bca.create_filter('ExecutionReport', execution_report2_params),
        bca.create_filter('ExecutionReport', execution_report3_params)
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

    if timeouts:
        time.sleep(5)

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
    # print("Case " + case_name + " is executed in " + str(
    #     round(datetime.now().timestamp() - seconds)) + " sec.")
