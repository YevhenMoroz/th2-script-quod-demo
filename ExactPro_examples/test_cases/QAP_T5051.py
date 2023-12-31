import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction
# from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from stubs import Stubs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP_T5051"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'TraderConnectivity3': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'Account2': 'TRQX_KEPLER',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': '400',
        'OrdType': '2',
        'Price': '20',
        'TimeInForce': '0',
        'TargetStrategy': 1004,
        'Instrument': {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
            'SecurityIDSource': 4,
            'SecurityExchange': 'XPAR'
        }
    }

    instrument_2 = {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }

    reusable_order_params = {   # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'Price': case_params['Price'],
        'TargetStrategy': case_params['TargetStrategy']
    }

    check_params = {
        'IClOrdIdCO': 'OD_5fgfDXg-00',
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'misc3': 'test 5004',
        'AlgoCst01': 'test 5006',
        'AlgoCst02': 'test 5007',
        'AlgoCst03': 'test 5010'
    }

    # Send new Iceberg order

    new_order_params = {
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'OrderCapacity': 'A',
        'ExDestination': 'XPAR',
        'ComplianceID': 'FX5',
        'StrategyName': 'ICEBERG',
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        **check_params
    }
    # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))
    new_ib_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder Iceberg',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', new_order_params, case_params['TraderConnectivity'])
        ))
    checkpoint_1 = new_ib_order.checkpoint_id
    execution_report1_params = {
        **reusable_order_params,
        'ClOrdID': new_order_params['ClOrdID'],
        # 'OrderID': new_ib_order.response_messages_list[0].fields['OrderID'].simple_value,
        'OrderID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': case_params['Instrument'],
        **check_params
    }
    # print(bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']))
    verifier.submitCheckRule(
        request=bca.create_check_rule(
            "ER Pending Received",
            bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_id
        ), timeout=3000
    )

    execution_report2_params = deepcopy(execution_report1_params)
    execution_report2_params['OrdStatus'] = execution_report2_params['ExecType'] = '0'
    execution_report2_params['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
    verifier.submitCheckRule(
        request=bca.create_check_rule(
            "Receive Execution Report New",
            bca.filter_to_grpc("ExecutionReport", execution_report2_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_id
        ), timeout=3000
    )

    instrument_1_2 = case_params['Instrument']
    instrument_1_2['SecurityType'] = 'CS'
    instrument_1_2['Symbol'] = 'PAR'

    newordersingle_params = {
        'Account': case_params['Account'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': new_order_params['DisplayInstruction']['DisplayQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'Instrument': instrument_1_2,
        'ExDestination': 'XPAR',
        **check_params

    }
    verifier.submitCheckRule(
        request=bca.create_check_rule(
            'Transmitted NewOrderSingle',
            bca.filter_to_grpc('NewOrderSingle', newordersingle_params, ["ClOrdID"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        ), timeout=3000
    )

    er_sim_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'OrderQty': newordersingle_params['OrderQty'],
            'OrdType': case_params['OrdType'],
            'Side': case_params['Side'],
            # 'LastPx': '0',
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '0',
            'LeavesQty': '0',
            'Text': '*'
    }

    logger.debug("Verify received Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        request=bca.create_check_rule(
            'Receive ExecutionReport New Sim',
            bca.filter_to_grpc('ExecutionReport', er_sim_params, ["ClOrdID", "OrdStatus"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        ), timeout=3000
    )

    cancel_order_params = {
        'OrigClOrdID': new_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': (new_order_params['ClOrdID']),
        'Instrument': new_order_params['Instrument'],
        # 'ExDestination': 'QDL1',
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

    execution_report3_params = {
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
        'Instrument': instrument_2
    }
    verifier.submitCheckRule(
        request=bca.create_check_rule(
            'Receive CancellationReport',
            bca.filter_to_grpc('ExecutionReport', execution_report3_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_id
        ), timeout=3000
    )

    sim_cancel_order_params = {
        'Account': case_params['Account'],
        'Instrument': new_order_params['Instrument'],
        'ExDestination': 'XPAR',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': case_params['OrderQty']
    }

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['SenderCompID2'],
            'TargetCompID': case_params['TargetCompID2']
        },
        'TestReqID': ('TEST', "NOT_EQUAL")
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)
    message_filters_sim = [
        bca.filter_to_grpc('NewOrderSingle', newordersingle_params),
        bca.filter_to_grpc('OrderCancelRequest', sim_cancel_order_params),
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages ",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sim,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_id,
            timeout=2000
        )
    )

    if timeouts:
        time.sleep(5)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
