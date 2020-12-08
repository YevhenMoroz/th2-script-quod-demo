import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules import infra_pb2
from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.infra_pb2 import Direction, ConnectionID
from grpc_modules.quod_simulator_pb2 import RequestMDRefID


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = True


def execute(case_name, report_id, case_params):
    act = ActFixStub(case_params['act'])
    event_store = EventStoreServiceStub(case_params['event-store'])
    verifier = VerifierStub(case_params['verifier'])
    simulator = TemplateSimulatorServiceStub(case_params['simulator'])
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
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': case_params['TargetStrategy']
    }

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
        'OrdSubStatus': 'SORPING',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': case_params['TargetStrategy'],
        'NoParty': [{
            'PartyID': 'TestCLIENTACCOUNT',
            'PartyIDSource': 'D',
            'PartyRole': '24'
        }]
    }
    # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))
    new_sor_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewSingleOrder',
            case_params['TraderConnectivity'],
            case_params['case_id'],
            bca.message_to_grpc('NewOrderSingle', sor_order_params)
        ))

    MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="596",
        connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
    )).MDRefID
    MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="3390",
        connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
    )).MDRefID

    mdfr_params_1 = {
        'MDReportID': "1",
        'MDReqID': MDRefID_1,
        'Instrument': {
            'Symbol': "3390"
        },
        # 'LastUpdateTime': "",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '10',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '30',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            }
        ]
    }
    mdfr_params_2 = {
        'MDReportID': "1",
        'MDReqID': MDRefID_2,
        'Instrument': {
            'Symbol': "3503"
        },
        # 'LastUpdateTime': "",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '10',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '30',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            }
        ]
    }
    act.sendMessage(
        request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh',
            "fix-fh-eq-paris",
            case_params['case_id'],
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1)
        )
    )
    act.sendMessage(
        request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh',
            "fix-fh-eq-trqx",
            case_params['case_id'],
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2)
        )
    )

    checkpoint_1 = new_sor_order.checkpoint_id
    pending_er_params = {
        **reusable_order_params,
        'ClOrdID': sor_order_params['ClOrdID'],
        'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': 'A',
        'ExecType': 'A',
        # 'TradingParty': sor_order_params['TradingParty'],
        'NoParty': [{
                'PartyID': 'TestCLIENTACCOUNT',
                'PartyIDSource': 'D',
                'PartyRole': '24'
            }],
        'LeavesQty': sor_order_params['OrderQty'],
        'Instrument': case_params['Instrument']
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
    new_er_params['Instrument'] = {
        'Symbol': case_params['Instrument']['Symbol'],
        'SecurityExchange': case_params['Instrument']['SecurityExchange']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ER New NewOrderSingle Received",
            bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_params['case_id']
        )
    )

    instrument_1_2 = case_params['Instrument']
    instrument_1_2['SecurityType'] = 'CS'
    instrument_1_2['Symbol'] = 'AN'

    newordersingle_params = {
        'Account': case_params['Account'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': sor_order_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'Instrument': instrument_1_2,
        'NoParty': sor_order_params['NoParty']
        # 'IClOrdIdCO': 'OD_5fgfDXg-00',
        # 'IClOrdIdAO': 'OD_5fgfDXg-00',
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'NewOrderSingle transmitted >> PARIS',
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
            'OrderQty': sor_order_params['OrderQty'],
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
            bca.filter_to_grpc('ExecutionReport', er_sim_params, ["ClOrdID", "OrdStatus"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_params['case_id'],
            infra_pb2.Direction.Value("SECOND")
        )
    )

    cancel_order_params = {
        'OrigClOrdID': sor_order_params['ClOrdID'],
        # 'OrderID': '',
        'ClOrdID': (sor_order_params['ClOrdID']),
        'Instrument': sor_order_params['Instrument'],
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
        'OrderID': pending_er_params['OrderID'],
        'ExecID': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '4',
        'ExecType': '4',
        'LeavesQty': '0',
        'Instrument': instrument_2,
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

    sim_cancel_order_params = {
        'Account': case_params['Account'],
        'Instrument': sor_order_params['Instrument'],
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
    for rule in sim_rules:
        rules_killer.removeRule(rule)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
