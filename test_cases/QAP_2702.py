import logging
from copy import deepcopy
from time import sleep
from datetime import datetime
from custom import basic_custom_actions as bca
# from grpc_modules import quod_simulator_pb2
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

    case_name = "QAP-2702"

    NOS1 = rule_man.add_NOS('fix-bs-eq-paris')
    NOS2 = rule_man.add_NOS('fix-bs-eq-trqx', 'TRQX_CLIENT1')
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    OCR2 = rule_man.add_OCR('fix-bs-eq-trqx')
    logger.info(f"Start rules with id's: \n {NOS1}, {NOS2}, {OCR1}, {OCR2}")
    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'Sender': '',
        'SenderCompID': 'QUOD3',
        'TargetCompID': 'QUODFX_UAT',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
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
    }

    case_id = bca.create_event(case_name, report_id)
    try:
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
            'ShortCode': '17536',
            'StrategyName': 'SORPING',
            'IClOrdIdTO': '19864',
            'AlgoCst01': 'KEPLER06',
            'AlgoCst02': 'KEPLER07',
            'AlgoCst03': 'KEPLER10',
            'TargetStrategy': case_params['TargetStrategy']
        }

        logger.debug(f"Send new order with ClOrdID = {new_order_single_params['ClOrdID']}")
        new_order_single = act.placeOrderFIX(
            bca.convert_to_request(
                "Send NewSingleOrder",
                case_params['TraderConnectivity'],
                case_id,
                bca.message_to_grpc('NewOrderSingle', new_order_single_params, case_params['TraderConnectivity'])
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
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1, "fix-fh-eq-paris")
            )
        )
        act.sendMessage(
            request=bca.convert_to_request(
                'Send MarketDataSnapshotFullRefresh',
                "fix-fh-eq-trqx",
                case_id,
                bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2, "fix-fh-eq-trqx")
            )
        )

        checkpoint = new_order_single.checkpoint_id

        pending_er_params = {
            **reusable_params,
            'OrderQty': new_order_single_params['OrderQty'],
            'Price': new_order_single_params['Price'],
            'ClOrdID': new_order_single_params['ClOrdID'],
            'OrderID': new_order_single.response_messages_list[0].fields['OrderID'].simple_value,
            'ExecID': new_order_single.response_messages_list[0].fields['ExecID'].simple_value,
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
            'NoParty': '*',
            'TargetStrategy': case_params['TargetStrategy']
        }

        logger.debug("Verify received Execution Report (OrdStatus = Pending)")
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER Pending NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint,
                case_params['TraderConnectivity'],
                case_id
            )
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['NoStrategyParameters'] = '*'
        new_er_params['ExecID'] = '*'
        new_er_params['Instrument'] = {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }
        new_er_params['ExecRestatementReason'] = '4'
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint,
                case_params['TraderConnectivity'],
                case_id
            )
        )

        instrument_bs = {
            'SecurityType': 'CS',
            'Symbol': 'RSC',
            'SecurityID': case_params['Instrument']['SecurityID'],
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }

        nos_bs_params = {
            'Account': case_params['Account'],
            'HandlInst': '1',
            'Side': case_params['Side'],
            'TimeInForce': case_params['TimeInForce'],
            'OrdType': case_params['OrdType'],
            'OrderCapacity': 'A',
            'Currency': 'EUR',
            'OrderQty': case_params['OrderQty'],
            'Price': case_params['Price'],
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'IClOrdIdCO': new_order_single_params['IClOrdIdCO'],
            'IClOrdIdAO': new_order_single_params['IClOrdIdAO'],
            'IClOrdIdTO': new_order_single_params['IClOrdIdTO'],
            'Instrument': instrument_bs,
            'ExDestination': 'XPAR'

        }

        verifier.submitCheckRule(
            bca.create_check_rule(
                'NewOrderSingle transmitted >> PARIS',
                bca.filter_to_grpc('NewOrderSingle', nos_bs_params, ["ClOrdID"]),
                checkpoint,
                case_params['TraderConnectivity2'],
                case_id
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
                checkpoint,
                case_params['TraderConnectivity2'],
                case_id,
                Direction.Value("SECOND")
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
                bca.message_to_grpc('OrderCancelReplaceRequest', replace_order_params, case_params['TraderConnectivity'])
            ))
        checkpoint2 = replace_order.checkpoint_id
        replacement_er_params = {
            **reusable_params,
            'ClOrdID': replace_order_params['ClOrdID'],
            'OrigClOrdID': new_order_single_params['ClOrdID'],
            'OrderID': pending_er_params['OrderID'],
            'ExecID': '*',
            'CumQty': '0',
            'LastPx': '0',
            'LastQty': '0',
            'QtyType': '0',
            'AvgPx': '0',
            'OrdStatus': '0',
            'ExecType': '5',
            'LeavesQty': case_params['OrderQty'],
            'Instrument': {
                'Symbol': case_params['Instrument']['Symbol'],
                'SecurityExchange': case_params['Instrument']['SecurityExchange']
            },
            'ExecRestatementReason': '4',
            'Price': case_params['NewPrice'],
            'OrderQty': case_params['OrderQty'],
            'NoParty': '*',
            'TransactTime': '*',
            'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
            'NoStrategyParameters': new_er_params['NoStrategyParameters'],
            'TargetStrategy': case_params['TargetStrategy']
        }

        logger.debug("Verify received Execution Report (OrdStatus = New, ExecType = Replaced)")
        verifier.submitCheckRule(
            bca.create_check_rule(
                'OrderReplace ER Received',
                bca.filter_to_grpc('ExecutionReport', replacement_er_params, ["ClOrdID", "OrdStatus"]),
                replace_order.checkpoint_id,
                case_params['TraderConnectivity'],
                case_id
            )
        )
        bs_cancel_replace_order_params = {
            'Account': case_params['Account'],
            'Instrument': instrument_bs,
            'ClOrdID': '*',
            'OrderID': '*',
            'Side': case_params['Side'],
            'TransactTime': '*',
            'OrderQty': replace_order_params['OrderQty'],
            'IClOrdIdCO': nos_bs_params['IClOrdIdCO'],
            'IClOrdIdAO': nos_bs_params['IClOrdIdAO'],
            'IClOrdIdTO': nos_bs_params['IClOrdIdTO'],
            'OrigClOrdID': '*',
            'ChildOrderID': '*',
            'ExDestination': nos_bs_params['ExDestination']
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Check OrderCancelRequest for Replacement >> PARIS',
                bca.filter_to_grpc('OrderCancelRequest', bs_cancel_replace_order_params),
                checkpoint2,
                case_params['TraderConnectivity2'],
                case_id
            )
        )

        cancel_replace_er_bs_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'OrderQty': nos_bs_params['OrderQty'],
            'Side': case_params['Side'],
            # 'LastPx': '0',
            'AvgPx': '0',
            'OrdStatus': '4',
            'ExecType': '4',
            'LeavesQty': '0',
            'Text': '*',
            'OrigClOrdID': '*'
        }

        logger.debug("Verify received Execution Report (OrdStatus = Cancelled)")
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Replacement Cancellation ER transmitted << PARIS',
                bca.filter_to_grpc('ExecutionReport', cancel_replace_er_bs_params, ["ClOrdID", "OrdStatus"]),
                checkpoint2,
                case_params['TraderConnectivity2'],
                case_id,
                Direction.Value("SECOND")
            )
        )

        replace_nos_bs_params = {
            **reusable_params,
            'HandlInst': '1',
            'OrderQty': replace_order_params['OrderQty'],
            'Price': replace_order_params['Price'],
            'ClOrdID': '*',
            'ChildOrderID': '*',
            'TransactTime': '*',
            'IClOrdIdAO': nos_bs_params['IClOrdIdAO'],
            'Instrument': instrument_bs,
            'ExDestination': 'XPAR'

        }

        verifier.submitCheckRule(
            bca.create_check_rule(
                'Replacement NOS transmitted >> PARIS',
                bca.filter_to_grpc('NewOrderSingle', replace_nos_bs_params, ["ClOrdID"]),
                checkpoint2,
                case_params['TraderConnectivity2'],
                case_id
            )
        )

        replace_er_bs_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': '0',
            'OrderQty': replace_nos_bs_params['OrderQty'],
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
                'Replacement ER transmitted << PARIS',
                bca.filter_to_grpc('ExecutionReport', replace_er_bs_params, ["ClOrdID", "OrdStatus"]),
                checkpoint2,
                case_params['TraderConnectivity2'],
                case_id,
                Direction.Value("SECOND")
            )
        )

        cancel_order_params = {
            'OrigClOrdID': new_order_single_params['ClOrdID'],
            'ClOrdID': (new_order_single_params['ClOrdID']),
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
                bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
            ))

        cancellation_er_params = {
            **reusable_params,
            'Instrument': {
                'Symbol': case_params['Instrument']['Symbol'],
                'SecurityExchange': case_params['Instrument']['SecurityExchange']
            },
            'ClOrdID': cancel_order_params['ClOrdID'],
            'OrderID': pending_er_params['OrderID'],
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
            'NoParty': '*',
            'NoStrategyParameters': new_er_params['NoStrategyParameters'],
            'TargetStrategy': case_params['TargetStrategy'],
            'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID']
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

        bs_cancel_order_params = {
            'Account': case_params['Account'],
            'Instrument': instrument_bs,
            'ClOrdID': '*',
            'IClOrdIdCO': new_order_single_params['IClOrdIdCO'],
            'IClOrdIdAO': new_order_single_params['IClOrdIdAO'],
            'IClOrdIdTO': new_order_single_params['IClOrdIdTO'],
            'OrderID': '*',
            'Side': case_params['Side'],
            'TransactTime': '*',
            'OrderQty': replace_order_params['OrderQty'],
            'ChildOrderID': '*',
            # 'ExDestination': new_order_single_params['ExDestination']
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                'Check OrderCancelRequest >> PARIS',
                bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
                cancel_order.checkpoint_id,
                case_params['TraderConnectivity2'],
                case_id
            )
        )

        verifier.submitCheckRule(
            bca.create_check_rule(
                'Cancellation ER Received',
                bca.filter_to_grpc('ExecutionReport', cancellation_er_params, ["ClOrdID", "OrdStatus"]),
                cancel_order.checkpoint_id,
                case_params['TraderConnectivity'],
                case_id
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
            bca.filter_to_grpc('OrderCancelRequest', bs_cancel_replace_order_params),
            bca.filter_to_grpc('NewOrderSingle', replace_nos_bs_params),
            bca.filter_to_grpc('OrderCancelRequest', bs_cancel_order_params),
        ]
        verifier.submitCheckSequenceRule(
            bca.create_check_sequence_rule(
                description="Check buy side messages from Paris",
                prefilter=pre_filter_sim,
                msg_filters=message_filters_sim,
                checkpoint=checkpoint,
                connectivity=case_params['TraderConnectivity2'],
                event_id=case_id,
                timeout=2000
            )
        )
    except Exception as e:
        logging.error("Error execution", exc_info=True)

    if timeouts:
        sleep(5)

    rule_man.remove_rule(NOS1)
    rule_man.remove_rule(NOS2)
    rule_man.remove_rule(OCR1)
    rule_man.remove_rule(OCR2)
    rule_man.print_active_rules()

    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
