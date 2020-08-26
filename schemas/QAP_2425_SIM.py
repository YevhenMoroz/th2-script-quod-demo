import copy
import logging
import time
from grpc_modules import verifier_pb2
from grpc_modules import infra_pb2
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import quod_simulator_pb2, simulator_pb2_grpc
from grpc_modules import quod_simulator_pb2_grpc, infra_pb2
from grpc_modules import simulator_pb2
import grpc

#start rule
channel = grpc.insecure_channel('localhost:8081')
simulator = quod_simulator_pb2_grpc.TemplateSimulatorServiceStub(channel)
DemoRule = simulator.createTemplateQuodDemoRule(
    request=quod_simulator_pb2.TemplateQuodDemoRule(
        connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child'),
        demo_field1=123,
        demo_field2='KCH_QA_RET_CHILD'))

OCR = simulator.createQuodOCRRule(request=quod_simulator_pb2.TemplateQuodOCRRule(connection_id=infra_pb2.ConnectionID(session_alias='kch-qa-ret-child')))
print(f"{DemoRule}, {OCR}")

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
    bca.verify_response(
        verifier,
        'Receive ExecutionReport Pending',
        bca.create_filter('ExecutionReport', er_pending_params),
        enter_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
    bca.verify_response(
        verifier,
        'Receive ExecutionReport New',
        bca.create_filter('ExecutionReport', er_new_params),
        enter_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
        'ChildOrderID' : '*',
        'TransactTime': '*',
        'Instrument': instrument_3_2,
        'ExDestination': case_params['ExDestination'],
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
    }

    bca.verify_response(
        verifier,
        'Transmitted NewOrderSingle',
        bca.create_filter('NewOrderSingle', newordersingle_params),
        enter_order,
        case_params['TraderConnectivity2'],
        case_params['case_id']
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
        # 'LastPx': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': '0',
        'Text': '*',
        # 'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        # 'NoStrategyParameters': [
        #     {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}]
    }

    logger.debug("Verify received Execution Report (OrdStatus = New)")
    bca.verify_response(
        verifier,
        'Receive ExecutionReport New Sim',
        bca.create_filter('ExecutionReport', er_sim_params),
        enter_order,
        case_params['TraderConnectivity2'],
        case_params['case_id'],
        infra_pb2.Direction.values()[1]
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

    bca.verify_response(
        verifier,
        'Transmitted OrderCancelRequest',
        bca.create_filter('OrderCancelRequest', cancel_order_params2),
        cancel_order,
        case_params['TraderConnectivity2'],
        case_params['case_id']
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
        'Text': 'sim work',

    }
    logger.debug("Verify received Execution Report (OrdStatus = Cancelled)")
    bca.verify_response(
        verifier,
        'Receive ExecutionReport Cancel',
        bca.create_filter('ExecutionReport', er_cancel_params),
        cancel_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
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
        'Text': 'sim work',
    }

    bca.verify_response(
        verifier,
        'Receive ExecutionReport Cancel Sim',
        bca.create_filter('ExecutionReport', er_sim_cancel_params),
        cancel_order,
        case_params['TraderConnectivity2'],
        case_params['case_id'],
        infra_pb2.Direction.values()[1]
    )

    pre_filter = verifier_pb2.PreFilter(
        fields={

            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={'MsgType': infra_pb2.ValueFilter(
                        simple_filter='8', operation=infra_pb2.FilterOperation.EQUAL),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID'])

                    })),

        })
    pre_filter2 = verifier_pb2.PreFilter(
        fields={

            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={'MsgType': infra_pb2.ValueFilter(
                        simple_filter='0', operation=infra_pb2.FilterOperation.NOT_EQUAL),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID2']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID2']),
                        'DeliverToCompID': infra_pb2.ValueFilter(simple_filter=case_params['DeliverToCompID']),
                    }

                )),
            # 'IClOrdIdCO': infra_pb2.ValueFilter(simple_filter=specific_order_params['IClOrdIdCO']),
            # 'IClOrdIdAO': infra_pb2.ValueFilter(simple_filter=specific_order_params['IClOrdIdAO'])

        })

    pre_filter3 = verifier_pb2.PreFilter(
        fields={
            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={'MsgType': infra_pb2.ValueFilter(
                        simple_filter='0', operation=infra_pb2.FilterOperation.NOT_EQUAL),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID2']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID2']),
                    }

                ))

    })

    message_filters = [
        bca.create_filter('ExecutionReport', er_pending_params),
        bca.create_filter('ExecutionReport', er_new_params),
        bca.create_filter('ExecutionReport', er_cancel_params)
    ]
    message_filters2 = [
        bca.create_filter('NewOrderSingle', newordersingle_params),
        # bca.create_filter('ExecutionReport', er_sim_params),
        bca.create_filter('OrderCancelRequest', cancel_order_params2),
        # bca.create_filter('ExecutionReport', er_sim_cancel_params),
    ]

    message_filters3 = [
        bca.create_filter('ExecutionReport', er_sim_params),
        bca.create_filter('ExecutionReport', er_sim_cancel_params),
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
        description='Received from Sim',
        check_order=True,
        direction=infra_pb2.Direction.values()[1]
    )

    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule3)

    if timeouts:
        time.sleep(5)

    bca.create_event(event_store, case_name, case_params['case_id'], report_id)  # Create sub-report for case
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))

    #stop rule
    core = simulator_pb2_grpc.ServiceSimulatorStub(channel)
    core.removeRule(DemoRule)
    core.removeRule(OCR)
    channel.close()
