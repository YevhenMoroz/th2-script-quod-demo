from __future__ import print_function

import logging
import time
from datetime import datetime
from custom import basic_custom_actions as bca
timeouts = False


def execute(case_name, report_id, case_params):
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
        'TransactTime': (datetime.utcnow().isoformat()),
        'Instrument': case_params['Instrument'],
        'ExDestination': 'QDL1',
        'ComplianceID': 'FX5',
        'Text': '-204',
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        'StrategyName': 'ICEBERG'
    }
    enter_order = bca.act.placeOrderFIX(
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
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty']
    }
    bca.verify_response(
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
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'NoStrategyParameters': [
            {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}]
    }
    bca.verify_response(
        'Receive ExecutionReport2',
        bca.create_filter('ExecutionReport', execution_report2_params),
        enter_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )

    cancel_order_params = {
        'OrigClOrdID': specific_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': bca.client_orderid(9),
        'Instrument': specific_order_params['Instrument'],
        'ExDestination': 'QDL1',
        'Side': case_params['Side'],
        'TransactTime': (datetime.utcnow().isoformat()),
        'OrderQty': case_params['OrderQty'],
        'Text': 'Cancel order'
    }
    cancel_order = bca.act.placeOrderCancelFIX(
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
        'Instrument': {
            'Symbol': 'TESTQA00.EUR-[QDL1',
            'SecurityID': 'TESTQA00',
            'SecurityIDSource': '8',
            'SecurityExchange': 'QDL1',
            'CFICode': 'EMXXXB'
        },
        'MaxFloor': specific_order_params['DisplayInstruction']['DisplayQty'],
        'NoStrategyParameters': execution_report2_params['NoStrategyParameters'],
        'ExecRestatementReason': '4'
    }
    bca.verify_response(
        'Receive ExecutionReport3',
        bca.create_filter('ExecutionReport', execution_report3_params),
        cancel_order,
        case_params['TraderConnectivity'],
        case_params['case_id']
    )
    if timeouts:
        time.sleep(5)

    bca.create_event(case_name, case_params['case_id'], report_id)  # Create sub-report for case
    print("Case " + case_name + " is executed in " + str(
        round(datetime.now().timestamp() - seconds)) + " sec.")
