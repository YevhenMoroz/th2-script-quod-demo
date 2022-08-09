import logging
from copy import deepcopy
import time
from datetime import datetime
from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction, ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID

from rule_management import RuleManager
from stubs import Stubs


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    rule_man = RuleManager()

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP_T4996"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    NOS1 = rule_man.add_NOS('fix-bs-eq-paris')
    NOS2 = rule_man.add_NOS('fix-bs-eq-trqx')
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    OCR2 = rule_man.add_OCR('fix-bs-eq-trqx')
    logger.info(f"Start rules with id's: \n {NOS1}, {NOS2}, {OCR1}, {OCR2}")

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
        'OrderQty': '1000',
        'OrdType': '2',
        'Price': '20',
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
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
        # 'OrdSubStatus': 'SORPING',
        'Currency': 'EUR',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
        'TargetStrategy': case_params['TargetStrategy'],
        'NoParty': [{
            'PartyID': 'TestCLIENTACCOUNT',
            'PartyIDSource': 'D',
            'PartyRole': '24'
        }],
        'Text': case_name
    }

    try:
        # print(bca.message_to_grpc('NewOrderSingle', sor_order_params))
        new_sor_order = act.placeOrderFIX(
            bca.convert_to_request(
                'Send NewSingleOrder',
                case_params['TraderConnectivity'],
                case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, case_params['TraderConnectivity'])
            ))
        #
        # MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol="1062",
        #     connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        # )).MDRefID
        # MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
        #     symbol="3503",
        #     connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
        # )).MDRefID
        #
        # mdfr_params_1 = {
        #     'MDReportID': "1",
        #     'MDReqID': MDRefID_1,
        #     'Instrument': {
        #         'Symbol': "1062"
        #     },
        #     # 'LastUpdateTime': "",
        #     'NoMDEntries': [
        #         {
        #             'MDEntryType': '0',
        #             'MDEntryPx': '10',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         },
        #         {
        #             'MDEntryType': '1',
        #             'MDEntryPx': '30',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         }
        #     ]
        # }
        # mdfr_params_2 = {
        #     'MDReportID': "1",
        #     'MDReqID': MDRefID_2,
        #     'Instrument': {
        #         'Symbol': "3503"
        #     },
        #     # 'LastUpdateTime': "",
        #     'NoMDEntries': [
        #         {
        #             'MDEntryType': '0',
        #             'MDEntryPx': '10',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         },
        #         {
        #             'MDEntryType': '1',
        #             'MDEntryPx': '30',
        #             'MDEntrySize': '1000',
        #             'MDEntryPositionNo': '1'
        #         }
        #     ]
        # }
        # act.sendMessage(
        #     request=bca.convert_to_request(
        #         'Send MarketDataSnapshotFullRefresh',
        #         "fix-fh-eq-paris",
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1, "fix-fh-eq-paris")
        #     )
        # )
        # act.sendMessage(
        #     request=bca.convert_to_request(
        #         'Send MarketDataSnapshotFullRefresh',
        #         "fix-fh-eq-trqx",
        #         case_id,
        #         bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2, "fix-fh-eq-trqx")
        #     )
        # )

        checkpoint_1 = new_sor_order.checkpoint_id
        pending_er_params = {
            **reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'ExecID': new_sor_order.response_messages_list[0].fields['ExecID'].simple_value,
            'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'OrderQty': case_params['OrderQty'],
            'Price': case_params['Price'],
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
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['ExecID'] = '*'
        new_er_params['ExecRestatementReason'] = '4'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['Instrument'] = {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )

        instrument_1_2 = case_params['Instrument']
        instrument_1_2['SecurityType'] = 'CS'
        instrument_1_2['Symbol'] = 'RSC'

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
            'NoParty': sor_order_params['NoParty'],
            'AlgoCst03': sor_order_params['NoParty'][0]['PartyID'],
            'ExDestination': 'XPAR',
            # 'IClOrdIdCO': 'OD_5fgfDXg-00',
            # 'IClOrdIdAO': 'OD_5fgfDXg-00',
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'NewOrderSingle transmitted >> PARIS',
                bca.filter_to_grpc('NewOrderSingle', newordersingle_params, ["ClOrdID"]),
                checkpoint_1,
                case_params['TraderConnectivity2'],
                case_id
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
                case_id,
                Direction.Value("SECOND")
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
                case_id,
                bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
            ))

        cancellation_er_params = {
            **new_er_params,
            'ClOrdID': cancel_order_params['ClOrdID'],
            'OrigClOrdID': pending_er_params['ClOrdID'],
            'ExecID': '*',
            'NoParty': '*',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0'
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Cancellation ER Received',
                bca.filter_to_grpc('ExecutionReport', cancellation_er_params, ["ClOrdID", "OrdStatus"]),
                cancel_order.checkpoint_id,
                case_params['TraderConnectivity'],
                case_id
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
            # 'TestReqID': ('TEST', "NOT_EQUAL")
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
                event_id=case_id,
                timeout=2000

            )
        )
    except Exception:
        logger.error("Error execution", exc_info=True)

    if timeouts:
        time.sleep(5)

    # stop all rules
    # for rule in sim_rules:
    #     rules_killer.removeRule(rule)
    rule_man.remove_rule(NOS1)
    rule_man.remove_rule(NOS2)
    rule_man.remove_rule(OCR1)
    rule_man.remove_rule(OCR2)
    rule_man.print_active_rules()
    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
