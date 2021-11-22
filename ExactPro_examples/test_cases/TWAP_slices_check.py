import logging
import uuid
from copy import deepcopy
import time
from datetime import datetime, timedelta

from th2_grpc_act_gui_quod import order_book_service
from th2_grpc_act_gui_quod.order_book_pb2_grpc import OrderBookServiceStub
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs

from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction, ConnectionID

from custom.basic_custom_actions import create_event
from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from win_gui_modules.order_book_wrappers import OrderInfo, OrdersDetails, ExtractionDetail, ExtractionAction
from win_gui_modules.utils import call, get_base_request, set_session_id, prepare_fe, close_fe
from win_gui_modules.wrappers import verification, verify_ent, set_base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    act2 = Stubs.win_act_order_book
    simulator = Stubs.simulator

    case_name = "TWAP_slices_check"
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)
    rule_man = RuleManager()
    session_alias = 'fix-bs-eq-trqx'
    symbol_trqx = '3686'

    OCR = rule_man.add_OCR(session_alias)
    OCRR = rule_man.add_OCRR(session_alias)
    trade_rule = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=50,
        mask_as_connectivity="fix-fh-eq-trqx",
        md_entry_size={1000: 0},
        md_entry_px={10: 20},
        symbol={"TRQX": symbol_trqx}
    ))
    logger.info(f"Start rules with id's: \n {OCRR, OCR, trade_rule}")

    seconds, nanos = bca.timestamps()  # Store case start time
    now = datetime.today() - timedelta(hours=2)
    # Create sub-report for case
    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'CLIENT1',
        'Account2': 'TRQX_CLIENT1',
        'HandlInst': '2',
        'Side': '1',
        'OrderQty': 150,
        'OrdType': '2',
        'Price': '20',
        'TimeInForce': '0',
        'TargetStrategy': 1005,
        'Instrument': {
            'Symbol': 'CH0012268360_CHF',
            'SecurityID': 'CH0012268360',
            'SecurityIDSource': 4,
            'SecurityExchange': 'XSWX'
        },
    }

    reusable_order_params = {  # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'OrderQty': case_params['OrderQty'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'CHF',
        'Price': case_params['Price']
    }

    # Send new TWAP order

    new_order_params = {
        **reusable_order_params,
        'ClOrdID': bca.client_orderid(9),
        'TransactTime': datetime.utcnow().isoformat(),
        'Instrument': case_params['Instrument'],
        'ExDestination': 'TRQX',
        'TargetStrategy': case_params['TargetStrategy'],
        'NoStrategyParameters': [{'StrategyParameterName': 'StartDate',
                                  'StrategyParameterType': '19',
                                  'StrategyParameterValue': now.strftime("%Y%m%d-%H:%M:%S")},
                                 {'StrategyParameterName': 'EndDate',
                                  'StrategyParameterType': '19',
                                  'StrategyParameterValue': (now + timedelta(minutes=2)).strftime("%Y%m%d-%H:%M:%S")},
                                 {'StrategyParameterName': 'Aggressivity',
                                  'StrategyParameterType': '1', 'StrategyParameterValue': 1},
                                 {'StrategyParameterName': 'Waves',
                                  'StrategyParameterType': '1', 'StrategyParameterValue': 3},
                                 ],
        'NoParty': [{
            'PartyID': bca.client_orderid(12),
            'PartyIDSource': 'D',
            'PartyRole': '24'
        }],
    }

    new_twap_order = act.placeOrderFIX(
        bca.convert_to_request(
            'Send NewOrderSingle',
            case_params['TraderConnectivity'],
            case_id,
            bca.message_to_grpc('NewOrderSingle', new_order_params, case_params['TraderConnectivity'])
        ))
    rule_man.remove_rule(trade_rule)
    NOS = rule_man.add_NOS(session_alias, "TRQX_CLIENT1")

    checkpoint_1 = new_twap_order.checkpoint_id
    pending_er_params = {
        **reusable_order_params,
        'Account': '*',
        'ExecID': '*',
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': new_twap_order.response_messages_list[0].fields['OrderID'].simple_value,
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
        'Instrument': case_params['Instrument'],
        'NoParty': [
            {
                'PartyID': new_order_params['NoParty'][0]['PartyID'],
                'PartyIDSource': 'D',
                'PartyRole': '24'
            },
            {
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }
        ],
        'NoStrategyParameters': new_order_params['NoStrategyParameters']
    }
    pending_er_params['Instrument']['SecurityExchange'] = 'TRQX'
    verifier.submitCheckRule(
        bca.create_check_rule(
            "ER Pending NewOrderSingle Received",
            bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1, case_params['TraderConnectivity'], case_id
        )
    )

    new_er_params = {
        **reusable_order_params,
        'ExecID': '*',
        'ClOrdID': new_order_params['ClOrdID'],
        'OrderID': new_twap_order.response_messages_list[0].fields['OrderID'].simple_value,
        'TransactTime': '*',
        'CumQty': '0',
        'LastPx': '0',
        'LastQty': '0',
        'QtyType': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'OrdType': case_params['OrdType'],
        'ExecType': '0',
        'LeavesQty': new_order_params['OrderQty'],
        'TargetStrategy': new_order_params['TargetStrategy'],
        'Instrument': case_params['Instrument'],
        'NoParty': pending_er_params['NoParty'],
        'NoStrategyParameters': new_order_params['NoStrategyParameters'],
        'ExecRestatementReason': '4',
        'SettlDate': '*'
    }

    time.sleep(60)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    child_ord_id1 = None
    child_ord_id2 = None
    child_ord_id3 = None
    try:
        prepare_fe(case_id, session_id, work_dir, username, password)
        order_info_extraction = "getOrderInfo"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["Order ID", new_er_params['OrderID']])
        main_order_id = ExtractionDetail("order_id", "Order ID")

        main_order_extraction_action = ExtractionAction.create_extraction_action(
            extraction_details=[main_order_id])

        child1_id = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
        sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
            extraction_details=[child1_id])
        sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1])

        child2_id = ExtractionDetail("subOrder_lvl_2.id", "Order ID")
        sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(
            extraction_detail=child2_id)
        sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

        child3_id = ExtractionDetail("subOrder_lvl_3.id", "Order ID")
        sub_lvl1_3_ext_action = ExtractionAction.create_extraction_action(
            extraction_detail=child3_id)
        sub_lv1_3_info = OrderInfo.create(actions=[sub_lvl1_3_ext_action])

        sub_order_details = OrdersDetails.create(order_info_list=[sub_lv1_1_info, sub_lv1_2_info, sub_lv1_3_info])

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_details))
        request = call(act2.getOrdersDetails, main_order_details.request())

        child_id_list = ['child1: ' + request[child1_id.name], 'child2: ' + request[child2_id.name], 'child3: '
                         + request[child3_id.name]]
        child_ord_id1 = request[child3_id.name]
        child_ord_id2 = request[child2_id.name]
        child_ord_id3 = request[child1_id.name]
        print("\n".join(child_id_list))
    except Exception:
        logger.error("Error execution in GUI part", exc_info=True)
        for rule in [NOS, OCRR, OCR]:
            rule_man.remove_rule(rule)
        rule_man.print_active_rules()

    close_fe(case_id, session_id)

    instrument_bs = {
        'SecurityType': 'CS',
        'Symbol': 'KUD_VX',
        'SecurityID': case_params['Instrument']['SecurityID'],
        'SecurityIDSource': '4',
        'SecurityExchange': 'XSWX'
    }

    child_nos1 = {
        'Account': case_params['Account2'],
        'HandlInst': '1',
        'Side': case_params['Side'],
        'OrderQty': int(new_order_params['OrderQty'] / 3),
        'TimeInForce': case_params['TimeInForce'],
        'Price': case_params['Price'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'AlgoCst03': new_order_params['NoParty'][0]['PartyID'],
        'Currency': 'CHF',
        'ClOrdID': child_ord_id1,
        'ChildOrderID': '*',
        'SettlDate': '*',
        'TransactTime': '*',
        'Instrument': instrument_bs,
        'ExDestination': 'TRQX',
        'NoParty': [{
            'PartyID': new_order_params['NoParty'][0]['PartyID'],
            'PartyIDSource': 'D',
            'PartyRole': '24'
        },
            {
                'PartyID': 'KMEFIC',
                'PartyIDSource': 'D',
                'PartyRole': 3
            }
        ]

    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'NewOrderSingle transmitted >> PARIS',
            bca.filter_to_grpc('NewOrderSingle', child_nos1),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    child1_er_fill_params = {
        'Account': case_params['Account2'],
        'ClOrdID': child_nos1['ClOrdID'],
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': child_nos1['OrderQty'],
        'Currency': child_nos1['Currency'],
        'OrderQty': child_nos1['OrderQty'],
        'LastQty': child_nos1['OrderQty'],
        'TimeInForce': child_nos1['TimeInForce'],
        'OrderCapacity': child_nos1['OrderCapacity'],
        'OrdType': child_nos1['OrdType'],
        'Side': child_nos1['Side'],
        'Price': child_nos1['Price'],
        'LastPx': child_nos1['Price'],
        'AvgPx': child_nos1['Price'],
        'OrdStatus': '2',
        'ExecType': 'F',
        'LeavesQty': '0',
        'Text': 'Hello sim',
        'Instrument': instrument_bs,
        'NoParty': [{
            'PartyID': 'KEPLER',
            'PartyIDSource': 'D',
            'PartyRole': '1'
        },
            {
                'PartyID': 1,
                'PartyIDSource': 'D',
                'PartyRole': 2
            },
            {
                'PartyID': 2,
                'PartyIDSource': 'D',
                'PartyRole': 3
            }
        ]
    }

    logger.debug("Verify received Execution Report (OrdStatus = Filled)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER child filled transmitted << TRQX',
            bca.filter_to_grpc('ExecutionReport', child1_er_fill_params, ['ClOrdID', 'OrdStatus', 'ExecType']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )
    # time.sleep(60)
    child_nos2 = deepcopy(child_nos1)
    child_nos2['ClOrdID'] = child_ord_id2
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Child order_2 transmitted >> TRQX',
            bca.filter_to_grpc('NewOrderSingle', child_nos2, ["ClOrdID"]),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        )
    )
    child2_er_new_params = {
        'ClOrdID': child_nos2['ClOrdID'],
        'OrderID': '*',
        'ExecID': '*',
        'TransactTime': '*',
        'CumQty': 0,
        'OrderQty': child_nos1['OrderQty'],
        'OrdType': case_params['OrdType'],
        'Side': case_params['Side'],
        'Price': case_params['Price'],
        # 'LastPx': '0',
        'AvgPx': '0',
        'OrdStatus': '0',
        'ExecType': '0',
        'LeavesQty': '0',
        'Text': 'sim work'
    }
    logger.debug("Verify received Child order_1 Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER child_2 transmitted << TRQX',
            bca.filter_to_grpc('ExecutionReport', child2_er_new_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )

    # time.sleep(60)
    child2_cancel_replace_order_params = {
        'Account': case_params['Account2'],
        'Instrument': instrument_bs,
        'ClOrdID': '*',
        'OrderID': '*',
        'Side': case_params['Side'],
        'Price': child_nos1['Price'],
        'TransactTime': '*',
        'OrderQty': child_nos1['OrderQty'],
        'OrderCapacity': child_nos1['OrderCapacity'],
        'OrigClOrdID': child_nos2['ClOrdID'],
        'ChildOrderID': '*',
        'HandlInst': child_nos1['HandlInst'],
        'Currency': child_nos1['Currency'],
        'TimeInForce': 3,
        'AlgoCst03': child_nos1['AlgoCst03'],
        'OrdType': child_nos1['OrdType'],
        'ExDestination': child_nos1['ExDestination'],
        'NoParty': new_order_params['NoParty']
    }
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Check OrderCancelReplaceRequest for child_2 >> TRQX',
            bca.filter_to_grpc('OrderCancelReplaceRequest', child2_cancel_replace_order_params,
                               ['OrigClOrdID']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        )
    )

    child2_er_can_params = deepcopy(child2_er_new_params)
    child2_er_can_params['OrdStatus'] = child2_er_can_params['ExecType'] = '4'
    child2_er_can_params['TimeInForce'] = child2_cancel_replace_order_params['TimeInForce']
    child2_er_can_params['OrigClOrdID'] = child2_cancel_replace_order_params['OrigClOrdID']
    child2_er_can_params['ClOrdID'] = child2_cancel_replace_order_params['ClOrdID']

    logger.debug("Verify received Child order_2 Execution Report (OrdStatus = Cancelled)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER child_2 cancelled << TRQX',
            bca.filter_to_grpc('ExecutionReport', child2_er_can_params, ['OrigClOrdID', 'OrdStatus']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )
    child_nos3 = deepcopy(child_nos1)
    child_nos3['OrderQty'] = int(new_order_params['OrderQty'] - child_nos1['OrderQty'])
    child_nos3['ClOrdID'] = child_ord_id3
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Child order_3 transmitted >> TRQX',
            bca.filter_to_grpc('NewOrderSingle', child_nos3, ['ClOrdID']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        )
    )
    child3_er_new_params = deepcopy(child2_er_new_params)
    child3_er_new_params['OrderQty'] = child_nos3['OrderQty']
    child3_er_new_params['ClOrdID'] = child_nos3['ClOrdID']
    logger.debug("Verify received Child order_3 Execution Report (OrdStatus = New)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER child_3 transmitted << TRQX',
            bca.filter_to_grpc('ExecutionReport', child3_er_new_params, ['ClOrdID', 'OrdStatus']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )
    child3_cancel_replace_order_params = deepcopy(child2_cancel_replace_order_params)
    child3_cancel_replace_order_params['OrderQty'] = child_nos3['OrderQty']
    child3_cancel_replace_order_params['OrigClOrdID'] = child_nos3['ClOrdID']
    verifier.submitCheckRule(
        bca.create_check_rule(
            'Check OrderCancelReplaceRequest for child_3 >> TRQX',
            bca.filter_to_grpc('OrderCancelReplaceRequest', child3_cancel_replace_order_params,
                               ['OrigClOrdID']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id
        )
    )
    child3_er_can_params = deepcopy(child2_er_can_params)
    child3_er_can_params['OrderQty'] = child3_er_new_params['OrderQty']
    child3_er_can_params['ClOrdID'] = child3_cancel_replace_order_params['ClOrdID']
    child3_er_can_params['OrigClOrdID'] = child3_cancel_replace_order_params['OrigClOrdID']
    logger.debug("Verify received Child order_3 Execution Report (OrdStatus = Cancelled)")
    verifier.submitCheckRule(
        bca.create_check_rule(
            'ER child_3 cancelled << TRQX',
            bca.filter_to_grpc('ExecutionReport', child3_er_can_params, ['OrigClOrdID', 'OrdStatus']),
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )

    pre_filter_req_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'SenderCompID': case_params['SenderCompID2'],
            'TargetCompID': case_params['TargetCompID2']
        },
        'NoParty': [{
            'PartyID': new_order_params['NoParty'][0]['PartyID']
        }]
        # 'TestReqID': ('TEST', "NOT_EQUAL")
    }
    pre_filter_req = bca.prefilter_to_grpc(pre_filter_req_params)
    message_filters_req = [
        bca.filter_to_grpc('NewOrderSingle', child_nos1, keys=['NoParty']),
        bca.filter_to_grpc('NewOrderSingle', child_nos2),
        bca.filter_to_grpc('OrderCancelReplaceRequest', child2_cancel_replace_order_params),
        bca.filter_to_grpc('NewOrderSingle', child_nos3),
        bca.filter_to_grpc('OrderCancelReplaceRequest', child3_cancel_replace_order_params),
    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check child orders' NOS and OCRR messages in " + case_params['TraderConnectivity2'],
            # chain_id=chain_id,
            prefilter=pre_filter_req,
            msg_filters=message_filters_req,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_id,
            timeout=3000
        )
    )

    pre_filter_er_params = {
        'header': {
            'MsgType': ('0', "NOT_EQUAL"),
            'TargetCompID': case_params['SenderCompID2'],
            'SenderCompID': case_params['TargetCompID2']
        },
        # 'NoParty': [{
        #     'PartyID': new_order_params['NoParty'][0]['PartyID']
        # }]
        # 'TestReqID': ('TEST', "NOT_EQUAL")
    }
    pre_filter_req = bca.prefilter_to_grpc(pre_filter_er_params)
    message_filters_req = [
        bca.filter_to_grpc('ExecutionReport', child1_er_fill_params),
        bca.filter_to_grpc('ExecutionReport', child2_er_new_params),
        bca.filter_to_grpc('ExecutionReport', child2_er_can_params),
        bca.filter_to_grpc('ExecutionReport', child3_er_new_params),
        bca.filter_to_grpc('ExecutionReport', child3_er_can_params),

    ]
    verifier.submitCheckSequenceRule(
        bca.create_check_sequence_rule(
            description="Check child orders' ER messages in " + case_params['TraderConnectivity2'],
            # chain_id=chain_id,
            prefilter=pre_filter_req,
            msg_filters=message_filters_req,
            checkpoint=checkpoint_1,
            connectivity=case_params['TraderConnectivity2'],
            event_id=case_id,
            timeout=3000,
            direction=Direction.Value("SECOND"))
    )

    for rule in [NOS, OCRR, OCR]:
        rule_man.remove_rule(rule)
    rule_man.print_active_rules()
    # close_fe(case_id, session_id)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
