import logging
from copy import deepcopy
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

    # Create sub-report for case
    event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    event_store.StoreEvent(event_request_1)

    instrument_1 = case_params['Instrument']
    instrument_1['Symbol'] = instrument_1['Symbol'] + '_EUR'

    instrument_2 = {
        'Symbol': instrument_1['Symbol'],
        'SecurityID': instrument_1['SecurityID']
    }

    bbo_params = {
        'Account': case_params['Account'],
        'HandlInst': 2,
        # 'OrderQty': 1000,
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'EUR'
    }

    # Send orders to 1st venue

    new_order_bbo1_params = {
        **bbo_params,
        'ClOrdID': bca.client_orderid(9),
        'Side': '2',
        'Price': 36,
        'OrderQty': 1000,
        'ExDestination': 'TRQX',
        'TransactTime': datetime.utcnow().isoformat()
    }
    new_order_bbo1 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_bbo1_params)
        ))
    checkpoint_bbo1 = new_order_bbo1.checkpoint_id
    execution_report_bbo1_1_params = {
        'ClOrdID': new_order_bbo1_params['ClOrdID'],
        'OrderID': new_order_bbo1.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_bbo1_params['OrderQty'],
        'Instrument': instrument_1
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo1_1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report_bbo1_2_params = deepcopy(execution_report_bbo1_1_params)
    execution_report_bbo1_2_params['OrdStatus'] = execution_report_bbo1_2_params['ExecType'] = '0'
    execution_report_bbo1_2_params['Instrument'] = instrument_2
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo1_2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    new_order_bbo2_params = {
        **bbo_params,
        'ClOrdID': bca.client_orderid(9),
        'Side': '1',
        'Price': 34,
        'OrderQty': 1000,
        'ExDestination': 'TRQX',
        'TransactTime': datetime.utcnow().isoformat()
    }
    new_order_bbo2 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_bbo2_params)
        ))
    checkpoint_bbo2 = new_order_bbo2.checkpoint_id
    execution_report_bbo2_1_params = {
        'ClOrdID': new_order_bbo2_params['ClOrdID'],
        'OrderID': new_order_bbo2.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_bbo2_params['OrderQty'],
        'Instrument': instrument_1
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo2_1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo2, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report_bbo2_2_params = deepcopy(execution_report_bbo2_1_params)
    execution_report_bbo2_2_params['OrdStatus'] = execution_report_bbo2_2_params['ExecType'] = '0'
    execution_report_bbo2_2_params['Instrument'] = instrument_2
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo2_2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo2, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    # Send orders to 2nd venue

    new_order_bbo3_params = {
        **bbo_params,
        'ClOrdID': bca.client_orderid(9),
        'Side': '2',
        'Price': 37,
        'OrderQty': 2000,
        'ExDestination': 'XPAR',
        'TransactTime': datetime.utcnow().isoformat()
    }
    new_order_bbo3 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_bbo3_params)
        ))
    checkpoint_bbo3 = new_order_bbo3.checkpoint_id
    execution_report_bbo3_1_params = {
        'ClOrdID': new_order_bbo3_params['ClOrdID'],
        'OrderID': new_order_bbo3.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_bbo3_params['OrderQty'],
        'Instrument': instrument_1
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo3_1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo3, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report_bbo3_2_params = deepcopy(execution_report_bbo3_1_params)
    execution_report_bbo3_2_params['OrdStatus'] = execution_report_bbo3_2_params['ExecType'] = '0'
    execution_report_bbo3_2_params['Instrument'] = instrument_2
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo3_2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo3, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    new_order_bbo4_params = {
        **bbo_params,
        'ClOrdID': bca.client_orderid(9),
        'Side': '1',
        'Price': 33,
        'OrderQty': 1000,
        'ExDestination': 'XPAR',
        'TransactTime': datetime.utcnow().isoformat()
    }
    new_order_bbo4 = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_bbo4_params)
        ))
    checkpoint_bbo4 = new_order_bbo4.checkpoint_id
    execution_report_bbo4_1_params = {
        'ClOrdID': new_order_bbo4_params['ClOrdID'],
        'OrderID': new_order_bbo4.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_bbo4_params['OrderQty'],
        'Instrument': instrument_1
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo4_1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo4, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report_bbo4_2_params = deepcopy(execution_report_bbo4_1_params)
    execution_report_bbo4_2_params['OrdStatus'] = execution_report_bbo4_2_params['ExecType'] = '0'
    execution_report_bbo4_2_params['Instrument'] = instrument_2
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report_bbo4_2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_bbo4, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    # Send sorping order

    sor_order_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'TargetStrategy': 1011,
        'ClientAlgoPolicyID': 'QA_SORPING'
    }
    new_sor_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', sor_order_params)
        ))
    checkpoint_1 = new_sor_order.checkpoint_id
    execution_report1_params = {
        'ClOrdID': sor_order_params['ClOrdID'],
        'OrderID': new_sor_order.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': sor_order_params['OrderQty'],
        'Instrument': case_params['Instrument']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Pending",
            bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    execution_report2_params = deepcopy(execution_report1_params)
    execution_report2_params['OrdStatus'] = execution_report2_params['ExecType'] = '0'
    execution_report2_params['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )
    newordersingle_params = {
        'Account': case_params['Account'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': 1500,
        'TimeInForce': '3',
        'Price': 37,
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'ExDestination': 'XPAR',
        'Instrument': {
            'SecurityID': case_params['Instrument']['SecurityID'],
            'SecurityIDSource': case_params['Instrument']['SecurityIDSource']
        }
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Transmitted NewOrderSingle',
            bca.filter_to_grpc('NewOrderSingle', newordersingle_params),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL")
            # 'SenderCompID': case_params['TargetCompID2'],
            # 'TargetCompID': case_params['SenderCompID2']
        }
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)
    message_filters_sim = [
        bca.filter_to_grpc('NewOrderSingle', newordersingle_params),
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sim,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_params['case_id'],
            timeout=5000

        )
    )

    # Cancel all rest orders

    cancel_order_1_params = {
        'OrigClOrdID': new_order_bbo2_params['ClOrdID'],
        'ClOrdID': bca.client_orderid(9),
        'Instrument': new_order_bbo2_params['Instrument'],
        'Side': new_order_bbo2_params['Side'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': new_order_bbo2_params['OrderQty'],
        'Text': 'Cancel order'
    }
    cancel_order_1 = act.placeOrderCancelFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_1_params),
        ))

    checkpoint_cancel_1 = cancel_order_1.checkpoint_id
    execution_report_cancelled_1_params = {
        'ClOrdID': cancel_order_1_params['ClOrdID'],
        'OrderID': '*',
        'ExecID': '*',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': case_params['Instrument']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport with OrdStatus = Cancelled',
            bca.filter_to_grpc('ExecutionReport', execution_report_cancelled_1_params, ["ClOrdID", "OrdStatus"]),
            checkpoint_cancel_1,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    cancel_order_2_params = {
        'OrigClOrdID': new_order_bbo4_params['ClOrdID'],
        'ClOrdID': bca.client_orderid(9),
        'Instrument': new_order_bbo4_params['Instrument'],
        'Side': new_order_bbo4_params['Side'],
        'TransactTime': datetime.utcnow().isoformat(),
        'OrderQty': new_order_bbo4_params['OrderQty'],
        'Text': 'Cancel order'
    }
    cancel_order_2 = act.placeOrderCancelFIX(
        bca.convert_to_request(
            'Send CancelOrderRequest',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_2_params),
        ))

    checkpoint_cancel_2 = cancel_order_2.checkpoint_id
    execution_report_cancelled_2_params = {
        'ClOrdID': cancel_order_2_params['ClOrdID'],
        'OrderID': '*',
        'ExecID': '*',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': cancel_order_2_params['Instrument']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive ExecutionReport with OrdStatus = Cancelled',
            bca.filter_to_grpc('ExecutionReport', execution_report_cancelled_2_params, ["ClOrdID", "OrdStatus"]),
            checkpoint_cancel_2,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
