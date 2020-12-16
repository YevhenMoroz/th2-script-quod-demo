import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
from grpc_modules.act_fix_pb2_grpc import ActFixStub
from grpc_modules.event_store_pb2_grpc import EventStoreServiceStub
from grpc_modules.verifier_pb2_grpc import VerifierStub
from grpc_modules.quod_simulator_pb2_grpc import TemplateSimulatorServiceStub
from grpc_modules.simulator_pb2_grpc import ServiceSimulatorStub
from grpc_modules.infra_pb2 import Direction, ConnectionID
from grpc_modules.quod_simulator_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
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

    sim_rules = [
        # simulator.createQuodMDRRule(bca.create_sim_rule_mdr('fix-fh-eq-paris', "QUOD_UTP", {1000: 1000}, {40: 30})),
        # simulator.createQuodMDRRule(bca.create_sim_rule_mdr(
        #     session_alias="fix-fh-eq-trqx", sender="QUOD_UTP", md_entry_size={1000: 1000}, md_entry_px={40: 30}
        # )),
        # simulator.createQuodOCRRule(bca.create_sim_rule_ocr('fix-bs-eq-paris')),
        # simulator.createQuodOCRRule(bca.create_sim_rule_ocr(session_alias='fix-bs-eq-trqx')),
        # simulator.createQuodSingleExecRule(
        #     request=TemplateQuodSingleExecRule(
        #         connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
        #         no_party_ids=[
        #             TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
        #             TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
        #             TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        #         ],
        #         cum_qty=1000
        #     )
        # ),
        # simulator.createQuodSingleExecRule(
        #     request=TemplateQuodSingleExecRule(
        #         connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        #         no_party_ids=[
        #             TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
        #             TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
        #             TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        #         ],
        #         cum_qty=100
        #     )
        # )
    ]
    logger.info("Rules with the next IDs are running: " + " ".join(str(rule.id) for rule in sim_rules))

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    event_request_1 = bca.create_store_event_request(case_name, case_params['case_id'], report_id)
    event_store.StoreEvent(event_request_1)

    instrument_1 = case_params['Instrument']
    instrument_1['Symbol'] = instrument_1['Symbol'] + '_EUR'

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

    MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="1062",
        connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
    )).MDRefID
    MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        symbol="3503",
        connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
    )).MDRefID

    mdfr_params_1 = {
        'MDReportID': "1",
        'MDReqID': MDRefID_1,
        'Instrument': {
            'Symbol': "1062"
        },
        # 'LastUpdateTime': "",
        'NoMDEntries': [
            {
                'MDEntryType': '0',
                'MDEntryPx': '30',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
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
                'MDEntryPx': '30',
                'MDEntrySize': '1000',
                'MDEntryPositionNo': '1'
            },
            {
                'MDEntryType': '1',
                'MDEntryPx': '40',
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
    execution_report1_params = {
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
    newordersingle_1_params = {
        'Account': case_params['Account'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': 1000,
        'TimeInForce': '3',
        'Price': 40,
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
            bca.filter_to_grpc('NewOrderSingle', newordersingle_1_params),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_params['case_id']
        )
    )

    newordersingle_2_params = {
        'Account': case_params['Account2'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': 100,
        'TimeInForce': '3',
        'Price': 40,
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'ExDestination': 'TRQX',
        'Instrument': {
            'SecurityID': case_params['Instrument']['SecurityID'],
            'SecurityIDSource': case_params['Instrument']['SecurityIDSource']
        }
    }

    verifier.submitCheckRule(
        bca.create_check_rule(
            'Transmitted NewOrderSingle',
            bca.filter_to_grpc('NewOrderSingle', newordersingle_2_params),
            checkpoint_1,
            case_params['TraderConnectivity3'],
            case_params['case_id']
        )
    )

    execution_report3_params = {
        'Account': case_params['Account'],
        'Side': case_params['Side'],
        'OrderQty': 1000,
        'TimeInForce': '3',
        'Price': 40,
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'ClOrdID': '*',
        'OrderID': '*',
        'ChildOrderID': '*',
        'TransactTime': '*',
        'CumQty': 1000,
        'LastPx': 40,
        'LastQty': 1000,
        'AvgPx': 40,
        'OrdStatus': '2',
        'ExecType': 'F',
        'LeavesQty': 0,
        'Instrument': case_params['Instrument']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Filled for PARIS",
            bca.filter_to_grpc("ExecutionReport", execution_report3_params),
            checkpoint_1, case_params['TraderConnectivity2'], case_params['case_id'],
            direction=Direction.Value("SECOND")
        )
    )

    execution_report4_params = deepcopy(execution_report3_params)
    execution_report4_params['Account'] = 'TRQX_KEPLER'
    execution_report4_params['OrderQty'] = execution_report4_params['LastQty'] = \
        execution_report4_params['CumQty'] = 100

    verifier.submitCheckRule(
        bca.create_check_rule(
            "Receive Execution Report Filled for TRQX",
            bca.filter_to_grpc("ExecutionReport", execution_report4_params),
            checkpoint_1, case_params['TraderConnectivity3'], case_params['case_id'],
            direction=Direction.Value("SECOND")
        )
    )

    pre_filter_sim_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL")
            # 'SenderCompID': case_params['SenderCompID2'],
            # 'TargetCompID': case_params['TargetCompID2']
        }
    }
    pre_filter_sim = bca.prefilter_to_grpc(pre_filter_sim_params)
    message_filters_sim = [
        bca.filter_to_grpc('NewOrderSingle', newordersingle_1_params),
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

    message_filters_sim_2 = [
        bca.filter_to_grpc('NewOrderSingle', newordersingle_2_params),
    ]

    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_sim_2,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity3'],
            event_id=case_params['case_id'],
            timeout=2000

        )
    )
    message_filters_conn_1_to = [
        bca.filter_to_grpc('ExecutionReport', execution_report3_params)
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_conn_1_to,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_params['case_id'],
            timeout=2000,
            direction=Direction.Value("SECOND")

        )
    )
    message_filters_conn_2_to = [
        bca.filter_to_grpc('ExecutionReport', execution_report4_params)
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check buy side messages ",
            prefilter=pre_filter_sim,
            msg_filters=message_filters_conn_2_to,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity3'],
            event_id=case_params['case_id'],
            timeout=2000,
            direction=Direction.Value("SECOND")

        )
    )

    # stop all rules
    for rule in sim_rules:
        rules_killer.removeRule(rule)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
