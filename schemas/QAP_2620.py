import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules.act_fix_pb2_grpc import ActStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.infra_pb2 import Direction, ConnectionID
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])
    rules_killer = ServiceSimulatorStub(case_params['simulator'])

    sim_rules = []
    logger.info("Rules with the next IDs are running: " + " ".join(str(rule.id) for rule in sim_rules))

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    event_store.StoreEvent(event_request_1)

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
        'IClOrdIdAO': 'OD_5fgfDXg-00'
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
        'StrategyName': 'InternalQuodQa_Iceberg',
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
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_params)
        ))
    checkpoint_1 = new_ib_order.checkpoint_id
    execution_report1_params = {
        **reusable_order_params,
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': new_ib_order.response_message.fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'Instrument': case_params['Instrument']
    }
    # print(bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']))
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
        bca.create_check_rule(
            'Transmitted NewOrderSingle',
            bca.filter_to_grpc('NewOrderSingle', newordersingle_params, ["ClOrdID"]),
            checkpoint_1,
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
        bca.create_check_rule(
            'Receive ExecutionReport New Sim',
            bca.filter_to_grpc('ExecutionReport', er_sim_params, ["ClOrdID", "OrdStatus"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_params['case_id'],
            infra_pb2.Direction.Value("SECOND")
        )
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
            case_params['case_id'],
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params),
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
        'Instrument': case_params['Instrument']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Receive CancellationReport',
            bca.filter_to_grpc('ExecutionReport', execution_report3_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
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
            event_id=case_params['case_id'],
            timeout=2000

        )
    )

    if timeouts:
        time.sleep(5)

    # stop all rules
    for rule in sim_rules:
        rules_killer.removeRule(rule)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
