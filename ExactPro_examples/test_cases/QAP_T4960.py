import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID
from th2_grpc_common.common_pb2 import ConnectionID, Direction
from win_gui_modules.utils import set_session_id, prepare_fe, close_fe, get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo, ExtractionDetail, ExtractionAction, \
    OrderAnalysisAction

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    sim = Stubs.core

    seconds, nanos = bca.timestamps()  # Store case start time
    case_name = "QAP_T4960"

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'TraderConnectivity3': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'HandlInst': '2',
        'Side': '2',
        'OrderQty': 1000,
        'OrdType': '2',
        'Price': 25,
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            'Symbol': 'FR0010542647_EUR',
            'SecurityID': 'FR0010542647',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XPAR'
        }
    }
    reusable_order_params = {  # This parameters can be used for ExecutionReport message
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'EUR',
        'TargetStrategy': case_params['TargetStrategy']
    }
    symbol_1 = "1062"
    symbol_2 = "3503"

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)

    trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=int(case_params['OrderQty'] / 2),
        mask_as_connectivity="fix-fh-eq-paris",
        md_entry_size={500: 0},
        md_entry_px={30: 25},
        symbol={"XPAR": symbol_1}
    ))
    trade_rule_2 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=int(case_params['OrderQty'] / 2),
        mask_as_connectivity="fix-fh-eq-trqx",
        md_entry_size={500: 0},
        md_entry_px={30: 25},
        symbol={"TRQX": symbol_2}
    ))
    try:
        # Send MarketDataSnapshotFullRefresh messages

        MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_1,
            connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        )).MDRefID
        MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_2,
            connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
        )).MDRefID
        mdfr_params_1 = {
            'MDReportID': "1",
            'MDReqID': MDRefID_1,
            'Instrument': {
                'Symbol': symbol_1
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '25',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '30',
                    'MDEntrySize': '500',
                    'MDEntryPositionNo': '1'
                }
            ]
        }
        mdfr_params_2 = deepcopy(mdfr_params_1)
        mdfr_params_2['MDReqID'] = MDRefID_2
        mdfr_params_2['Instrument'] = {
                'Symbol': symbol_2
        }
        act.sendMessage(request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-paris", case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_1, "fix-fh-eq-paris")
        ))
        act.sendMessage(request=bca.convert_to_request(
            'Send MarketDataSnapshotFullRefresh', "fix-fh-eq-trqx", case_id,
            bca.message_to_grpc('MarketDataSnapshotFullRefresh', mdfr_params_2, "fix-fh-eq-trqx")
        ))

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
            'Text': 'QAP_T4960'
        }
        new_sor_order = act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new sorping order", "gtwquod3", case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, "gtwquod3")
            ))
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
            'NoParty': [{
                'PartyID': 'gtwquod3',
                'PartyIDSource': 'D',
                'PartyRole': '36'
            }],
            'LeavesQty': sor_order_params['OrderQty'],
            'Instrument': case_params['Instrument']
        }
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = Pending",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            ),
            timeout=3000
        )

        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['Instrument'] = {
            'Symbol': case_params['Instrument']['Symbol'],
            'SecurityExchange': case_params['Instrument']['SecurityExchange']
        }
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = New",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            ),
            timeout=3000
        )
        new_order_single_to_paris = {
            'HandlInst': '1',
            'Side': case_params['Side'],
            'OrderQty': 500,
            'TimeInForce': '3',
            'Price': 25,
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
            request=bca.create_check_rule(
                "NewOrderSingle >> PARIS",
                bca.filter_to_grpc("NewOrderSingle", new_order_single_to_paris),
                checkpoint_1, case_params['TraderConnectivity2'], case_id
            ),
            timeout=3000
        )

        er_filled_from_paris_params = {
            'ClOrdID': '*',
            'OrderID': '*',
            'ExecID': '*',
            'TransactTime': '*',
            'CumQty': new_order_single_to_paris['OrderQty'],
            'OrderQty': new_order_single_to_paris['OrderQty'],
            'OrdType': case_params['OrdType'],
            'Side': new_order_single_to_paris['Side'],
            'LastPx': new_order_single_to_paris['Price'],
            'AvgPx': new_order_single_to_paris['Price'],
            'OrdStatus': '2',
            'ExecType': 'F',
            'LeavesQty': '0',
            'Text': '*'
        }
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = Filled << PARIS",
                bca.filter_to_grpc("ExecutionReport", er_filled_from_paris_params),
                checkpoint_1, case_params['TraderConnectivity2'], case_id,
                direction=Direction.Value("SECOND")
            ),
            timeout=3000
        )
        new_order_single_to_trqx = deepcopy(new_order_single_to_paris)
        new_order_single_to_trqx['ExDestination'] = 'TRQX'
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "NewOrderSingle >> TRQX",
                bca.filter_to_grpc("NewOrderSingle", new_order_single_to_trqx),
                checkpoint_1, case_params['TraderConnectivity3'], case_id
            ),
            timeout=3000
        )
        er_filled_from_trqx_params = deepcopy(er_filled_from_paris_params)
        verifier.submitCheckRule(
            request=bca.create_check_rule(
                "Execution Report with OrdStatus = Filled << TRQX",
                bca.filter_to_grpc("ExecutionReport", er_filled_from_trqx_params),
                checkpoint_1, case_params['TraderConnectivity3'], case_id,
                direction=Direction.Value("SECOND")
            ),
            timeout=3000
        )

        order_info_extraction = "getOrderInfo"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["ClOrdID", sor_order_params['ClOrdID']])

        main_order_qty = ExtractionDetail("order_qty", "Qty")
        main_order_exec_pcy = ExtractionDetail("order_exec_pcy", "ExecPcy")
        main_order_extraction_action = ExtractionAction.create_extraction_action(
                extraction_details=[main_order_qty, main_order_exec_pcy])

        sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
        lvl1_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(sub_order_id_dt))
        lvl1_details = OrdersDetails.create(info=lvl1_info)

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=lvl1_details))

        request = call(Stubs.win_act_order_book.getOrdersDetails, main_order_details.request())
        Stubs.win_act.verifyEntities(verification(
            order_info_extraction, "checking order", [
                verify_ent("Order ExecPcy", main_order_exec_pcy.name, "Synth (Quod LitDark)"),
                verify_ent("Order Qty", main_order_qty.name, "1,000")
            ]))

        # check child orders
        sub_order_id = request[sub_order_id_dt.name]
        if not sub_order_id:
            raise Exception("Sub order id is not returned")
        logger.debug("Sub order id " + sub_order_id)

        extraction_id = "child_orders"

        child_order_lvl1_details = OrdersDetails()
        child_order_lvl1_details.set_default_params(base_request)
        child_order_lvl1_details.set_extraction_id(extraction_id)
        child_order_lvl1_details.set_filter(["Order ID", sub_order_id])
        child_order_lvl1_exec_pcy = ExtractionDetail("child_order_lvl1.ExecPcy", "ExecPcy")
        child_order_lvl1_ext_action1 = ExtractionAction.create_extraction_action(
            extraction_detail=child_order_lvl1_exec_pcy)
        child_order_lvl1_ext_action2 = OrderAnalysisAction.create_extract_event_rows(event_number=1)

        child_order_lvl2_1_exec_pcy = ExtractionDetail("child_order_lvl2_1.ExecPcy", "ExecPcy")
        child_order_lvl2_1_misc9 = ExtractionDetail("child_order_lvl2_1.Misc9", "FO field 9")
        child_order_lvl2_1_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[child_order_lvl2_1_exec_pcy, child_order_lvl2_1_misc9]
            ))
        child_order_lvl2_2_exec_pcy = ExtractionDetail("child_order_lvl2_2.ExecPcy", "ExecPcy")
        child_order_lvl2_2_misc9 = ExtractionDetail("child_order_lvl2_2.Misc9", "FO field 9")
        child_order_lvl2_2_info = OrderInfo.create(
            action=ExtractionAction.create_extraction_action(
                extraction_details=[child_order_lvl2_2_exec_pcy, child_order_lvl2_2_misc9]
            ))
        child_orders_lvl2_details = OrdersDetails.create(
            order_info_list=[child_order_lvl2_1_info, child_order_lvl2_2_info])
        length_name = "child_orders_lvl2.length"
        child_orders_lvl2_details.extract_length(length_name)

        child_order_lvl1_details.add_single_order_info(
            OrderInfo.create(
                actions=[child_order_lvl1_ext_action1, child_order_lvl1_ext_action2],
                sub_order_details=child_orders_lvl2_details
            ))
        data = call(Stubs.win_act_order_book.getChildOrdersDetails, child_order_lvl1_details.request())
        event1_id = data['event1.id']
        logger.debug(f"Event ID = {event1_id}")
        Stubs.win_act.verifyEntities(
            verification(extraction_id, "Checking child orders", [
                verify_ent("Child order Lvl 1 ExecPcy", child_order_lvl1_exec_pcy.name, "Synth (Quod MultiListing)"),
                verify_ent("Child order 1 Lvl 2 ExecPcy", child_order_lvl2_1_exec_pcy.name, "DMA"),
                verify_ent("Child order 1 Lvl 2 Misc9", child_order_lvl2_1_misc9.name, event1_id),
                verify_ent("Child order 2 Lvl 2 ExecPcy", child_order_lvl2_2_exec_pcy.name, "DMA"),
                verify_ent("Child order 2 Lvl 2 Misc9", child_order_lvl2_2_misc9.name, event1_id),
                verify_ent("Child orders Lvl 2 count", length_name, "2")
            ]))

    except Exception as e:
        logging.error("Error execution", exc_info=True)
    sim.removeRule(trade_rule_1)
    sim.removeRule(trade_rule_2)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
