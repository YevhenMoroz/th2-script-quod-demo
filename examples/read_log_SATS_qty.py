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

    case_name = "Log_SATS_qty_example"

    NOS1 = rule_man.add_NOS('fix-bs-eq-paris')
    NOS2 = rule_man.add_NOS('fix-bs-eq-trqx', 'TRQX_CLIENT1')
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    OCRR1 = rule_man.add_OCRR('fix-bs-eq-paris')
    OCR2 = rule_man.add_OCR('fix-bs-eq-trqx')
    OCRR2 = rule_man.add_OCRR('fix-bs-eq-trqx')
    logger.info(f"Start rules with id's: \n {NOS1}, {NOS2}, {OCR1}, {OCR2}, {OCRR1}, {OCRR2}")
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

        del pending_er_params['Account']
        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['NoStrategyParameters'] = '*'
        new_er_params['ExecID'] = '*'
        new_er_params['ExecRestatementReason'] = '4'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['Instrument'] = case_params['Instrument']
        new_er_params['SettlDate'] = "*"
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint,
                case_params['TraderConnectivity'],
                case_id
            )
        )

        sleep(5)
        replace_order_params = {
            'OrigClOrdID': new_order_single_params['ClOrdID'],
            'ClOrdID': bca.client_orderid(9),
            'Account': case_params['Account'],
            'HandlInst': case_params['HandlInst'],
            'Instrument': case_params['Instrument'],
            'Side': case_params['Side'],
            'TransactTime': (datetime.utcnow().isoformat()),
            'OrdType': case_params['OrdType'],
            'OrderQty': 1,
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
        sleep(60)
        sats_qty_logs_params = {
            'MsgType': 'SATSAmendQty',
            'NewQty': replace_order_params['OrderQty'],
            'OldQty': new_order_single_params['OrderQty'],
            'OrderID': pending_er_params['OrderID']
        }
        verifier.submitCheckRule(
            bca.create_check_rule(
                "SATS Log Qty Msg Received",
                bca.filter_to_grpc("Csv_Message", sats_qty_logs_params, keys=["OrderID"]),
                checkpoint2, 'log305-sats-qty', case_id
            )
        )
        # print(bca.filter_to_grpc("Csv_Header/Csv_Message", sats_qty_logs_params))
        del new_er_params['Instrument']
        replacement_er_params = {
            **new_er_params,
            'ClOrdID': replace_order_params['ClOrdID'],
            'OrigClOrdID': new_order_single_params['ClOrdID'],
            'OrderID': pending_er_params['OrderID'],
            'ExecID': '*',
            'ExecType': '5',
            'Instrument': case_params['Instrument'],
            'ExecRestatementReason': '4',
            'Price': case_params['NewPrice'],
            'OrderQty': replace_order_params['OrderQty'],
            'LeavesQty': replace_order_params['OrderQty'],
            'TransactTime': '*',
            'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
            'NoStrategyParameters': new_er_params['NoStrategyParameters'],
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


    except Exception as e:
        logging.error("Error execution", exc_info=True)

    if timeouts:
        sleep(5)

    rule_man.remove_rule(NOS1)
    rule_man.remove_rule(NOS2)
    rule_man.remove_rule(OCR1)
    rule_man.remove_rule(OCR2)
    rule_man.remove_rule(OCRR1)
    rule_man.remove_rule(OCRR2)
    rule_man.print_active_rules()


    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
