import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules.act_fix_pb2_grpc import ActFixStub
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
    act = ActFixStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])
    # rules_killer = ServiceSimulatorStub(case_params['simulator'])

    # sim_rules = []
    # logger.info("Rules with the next IDs are running: " + " ".join(str(rule.id) for rule in sim_rules))

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    bca.create_event(EventStoreServiceStub(case_params['event-store']), case_name, case_params['case_id'], report_id)
    # event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    # event_store.StoreEvent(event_request_1)

    reusable_order_params = {  # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'Price': case_params['Price']
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
        'StrategyName': 'ICEBERG',
        'TargetStrategy': case_params['TargetStrategy'],
        'DisplayInstruction': {
            'DisplayQty': '50'
        },
        **check_params
    }
    # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))

    new_ib_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewOrderSingle',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', new_order_params)
        ))
    checkpoint_1 = new_ib_order.checkpoint_id
    # logger.info(new_ib_order)
    pending_er_params = {
        **reusable_order_params,
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': new_ib_order.response_messages_list[0].fields['OrderID'].simple_value,
        'ExecID': new_ib_order.response_messages_list[0].fields['ExecID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        'LeavesQty': new_order_params['OrderQty'],
        'TargetStrategy': new_order_params['TargetStrategy'],
        'MaxFloor': new_order_params['DisplayInstruction']['DisplayQty'],
        'Instrument': case_params['Instrument'],
        'NoParty': '*',
    }
    # print(bca.filter_to_grpc("ExecutionReport", execution_report1_params, ['ClOrdID', 'OrdStatus']))
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ER Pending NewOrderSingle Received",
            bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    new_er_params = deepcopy(pending_er_params)
    new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
    new_er_params['SecondaryAlgoPolicyID'] = 'ICEBERG'
    new_er_params['NoStrategyParameters'] = [
        {'StrategyParameterName': 'LowLiquidity', 'StrategyParameterType': '13', 'StrategyParameterValue': 'Y'}]
    new_er_params['ExecID'] = '*'
    # new_er_params['Instrument'] = {
    #     'Symbol': case_params['Instrument']['Symbol'],
    #     'SecurityExchange': case_params['Instrument']['SecurityExchange']
    # }
    new_er_params['ExecRestatementReason'] = '4'
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ER New NewOrderSingle Received",
            bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    instrument_bs = {
        'SecurityType': 'CS',
        'Symbol': 'PAR',
        'SecurityID': case_params['Instrument']['SecurityID'],
        'SecurityIDSource': '4',
        'SecurityExchange': 'XPAR'
    }

    nos_bs_params = {
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
        'Instrument': instrument_bs,
        'ExDestination': 'XPAR',
        **check_params

    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'NewOrderSingle transmitted >> PARIS',
            bca.filter_to_grpc('NewOrderSingle', nos_bs_params, ["ClOrdID"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )

    er_bs_params = {
        'ClOrdID': '*',
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': '0',
        'OrderQty': nos_bs_params['OrderQty'],
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
            'ER NewOrderSingle transmitted << PARIS',
            bca.filter_to_grpc('ExecutionReport', er_bs_params, ["ClOrdID", "OrdStatus"]),
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

    cancellation_er_params = {
        **reusable_order_params,
        'ClOrdID': cancel_order_params['ClOrdID'],
        'OrderID': new_er_params['OrderID'],
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
        'MaxFloor': new_er_params['MaxFloor'],
        'ExecRestatementReason': new_er_params['ExecRestatementReason'],
        'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
        'TargetStrategy': new_er_params['TargetStrategy'],
        'OrigClOrdID': new_order_params['ClOrdID'],
        'Instrument': new_er_params['Instrument'],
        'NoStrategyParameters': new_er_params['NoStrategyParameters']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Cancellation ER Received',
            bca.filter_to_grpc('ExecutionReport', cancellation_er_params, ["ClOrdID", "OrdStatus"]),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity'],
            case_params['case_id']
        )
    )

    bs_cancel_order_params = {
        'Account': case_params['Account'],
        'Instrument': instrument_bs,
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'TransactTime': '*',
        'OrderQty': new_order_params['DisplayInstruction']['DisplayQty'],
        'IClOrdIdAO': 'OD_5fgfDXg-00',
        'OrigClOrdID': '*',
        'ChildOrderID': '*',
        'ExDestination': new_order_params['ExDestination']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Check OrderCancelRequest >> PARIS',
            bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
            cancel_order.checkpoint_id,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )
    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['SenderCompID2'],
            'TargetCompID': case_params['TargetCompID2']
        },
        # 'TestReqID': ('TEST', "NOT_EQUAL")
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)
    message_filters_sim = [
        bca.filter_to_grpc('NewOrderSingle', nos_bs_params),
        bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages from Paris",
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
    # for rule in sim_rules:
    #     rules_killer.removeRule(rule)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
