import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import verifier_pb2, infra_pb2
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP-2702"
    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'Sender': '',
        'SenderCompID': 'QUOD3',
        'TargetCompID': 'QUODFX_UAT',
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': '2',
        'OrdType': '2',
        'Price': '1',
        'NewPrice': '2',
        'TimeInForce': '0',
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        },
        'TargetStrategy': 1011
    }
    
    reusable_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': case_params['TargetStrategy']
    }

    case_id = bca.create_event(case_name, report_id)

    new_order_single_params = {
        **reusable_params,
        'Instrument': case_params['Instrument'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['Price'],
        'ComplianceID': 'FX5',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'F_ShortCode': '17536',
        'StrategyName': 'SORPING',
        'IClOrdIdTO': '19864',
        'AlgoCst01': 'KEPLER06',
        'AlgoCst02': 'KEPLER07',
        'AlgoCst03': 'KEPLER10'
    }

    logger.debug(f"Send new order with ClOrdID = {new_order_single_params['ClOrdID']}")
    new_order_single = act.placeOrderFIX(
        bca.convert_to_request(
            "Send NewSingleOrder",
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', new_order_single_params)
        ))

    checkpoint = new_order_single.checkpoint_id

    execution_report_params_1 = {
        **reusable_params,
        'OrderQty': new_order_single_params['OrderQty'],
        'Price': new_order_single_params['Price'],
        'ClOrdID': new_order_single_params['ClOrdID'],
        # 'OrderID': new_order_single.response_message.fields['OrderID'].simple_value,
        'OrderID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_single_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        'NoParty': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = Pending)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_params_1, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    execution_report_params_2 = deepcopy(execution_report_params_1)
    execution_report_params_2['OrdStatus'] = execution_report_params_2['ExecType'] = '0'
    execution_report_params_2['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
    execution_report_params_2['ExecRestatementReason'] = '4'
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Verify received Execution Report (OrdStatus = New)",
            bca.filter_to_grpc("ExecutionReport", execution_report_params_2, ['ClOrdID', 'OrdStatus']),
            checkpoint,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    replace_order_params = {
        'OrigClOrdID': new_order_single_params['ClOrdID'],
        'ClOrdID': bca.client_orderid(9),
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Instrument': case_params['Instrument'],
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrdType': case_params['OrdType'],
        'OrderQty': case_params['OrderQty'],
        'Price': case_params['NewPrice'],
        'OrderCapacity': 'A'
    }

    logger.debug(f"Send replace order with ClOrdID = {replace_order_params['ClOrdID']}")
    replace_order = act.placeOrderReplaceFIX(
        bca.convert_to_request(
            'Send OrderCancelReplaceRequest',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params)
        ))

    execution_report_params_3 = {
        **reusable_params,
        'ClOrdID': replace_order_params['ClOrdID'],
        'OrderID': execution_report_params_1['OrderID'],
        'ExecID': '*',
        'CumQty': '*',
        'LastPx': '*',
        'LastQty': '*',
        'QtyType': '*',
        'AvgPx': '*',
        'OrdStatus': '*',
        'ExecType': '5',
        'LeavesQty': case_params['OrderQty'],
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        },
        'ExecRestatementReason': '4',
        'Price': case_params['NewPrice'],
        'OrderQty': case_params['OrderQty'],
        'NoParty': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport3',
            bca.filter_to_grpc('ExecutionReport', execution_report_params_3, ["ClOrdID", "OrdStatus"]),
            replace_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    cancel_order_params = {
        'OrigClOrdID': new_order_single_params['ClOrdID'],
        'ClOrdID': new_order_single_params['ClOrdID'],
        'Instrument': new_order_single_params['Instrument'],
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
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
        ))

    execution_report_params_4 = {
        **reusable_params,
        'Instrument': {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        },
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': execution_report_params_1['OrderID'],
        'OrderQty': replace_order_params['OrderQty'],
        'Price': replace_order_params['Price'],
        'TransactTime': '*',
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'ExecRestatementReason': '4',
        'NoParty': '*'
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive CancellationReport',
            bca.filter_to_grpc('ExecutionReport', execution_report_params_4, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        )
    )

    # ------------------------------------------------
    pre_filter = verifier_pb2.PreFilter(
        fields={
            'header': infra_pb2.ValueFilter(
                message_filter=infra_pb2.MessageFilter(
                    fields={
                        'MsgType': infra_pb2.ValueFilter(
                            simple_filter='0', operation=infra_pb2.FilterOperation.NOT_EQUAL
                        ),
                        'SenderCompID': infra_pb2.ValueFilter(simple_filter=case_params['TargetCompID']),
                        'TargetCompID': infra_pb2.ValueFilter(simple_filter=case_params['SenderCompID']),
                        'TestReqID': infra_pb2.ValueFilter(
                            simple_filter='TEST', operation=infra_pb2.FilterOperation.NOT_EQUAL
                        )
                    }
                )
            )
        }
    )

    message_filters = [
        bca.filter_to_grpc('ExecutionReport', execution_report_params_1, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report_params_2, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report_params_3, ["ClOrdID", "OrdStatus"]),
        bca.filter_to_grpc('ExecutionReport', execution_report_params_4, ["ClOrdID", "OrdStatus"])
    ]

    check_sequence_rule = verifier_pb2.CheckSequenceRuleRequest(
        pre_filter=pre_filter,
        message_filters=message_filters,
        checkpoint=new_order_single.checkpoint_id,
        timeout=1000,
        connectivity_id=infra_pb2.ConnectionID(session_alias=case_params['TraderConnectivity']),
        parent_event_id=case_id,
        description='Some description',
        check_order=True
    )
    logger.debug("Verify a sequence of Execution Report messages")
    verifier.submitCheckSequenceRule(check_sequence_rule)

    if timeouts:
        sleep(5)

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
