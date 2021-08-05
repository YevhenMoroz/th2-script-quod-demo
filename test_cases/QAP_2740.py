import logging
from copy import deepcopy
from datetime import datetime

from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import RequestMDRefID, TemplateQuodSingleExecRule, TemplateNoPartyIDs

from custom.verifier import Verifier
from rule_management import RuleManager
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.order_book_wrappers import OrdersDetails, ExtractionDetail, ExtractionAction, \
    OrderInfo, OrderAnalysisAction, CalcDataContentsRowSelector
from win_gui_modules.utils import call, get_base_request, prepare_fe, set_session_id, close_fe_2, close_fe
from win_gui_modules.wrappers import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
timeouts = False


def execute(report_id):
    case_name = "QAP-2740 [SORPING] Send SORPING algo order to check PriceCost criteria in Aggressive phase"
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    base_request = get_base_request(session_id, case_id)

    act = Stubs.fix_act
    common_act = Stubs.win_act
    act2 = Stubs.win_act_order_book
    verifier = Stubs.verifier
    verifier2 = Verifier(case_id)
    simulator = Stubs.simulator
    sim = Stubs.core

    seconds, nanos = bca.timestamps()  # Store case start time

    rule_man = RuleManager()
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    OCR2 = rule_man.add_OCR('fix-bs-eq-trqx')
    logger.info(f"Start rules with id's: \n  {OCR1}, {OCR2}")

    set_base(session_id, case_id)

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
        'OrderQty': 100,
        'OrdType': '2',
        'Price': 25,
        'TimeInForce': '0',
        'TargetStrategy': 1011,
        'Instrument': {
            'Symbol': 'FR0000125460_EUR',
            'SecurityID': 'FR0000125460',
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
    symbol_paris = "596"
    symbol_trqx = "3390"
    trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=case_params['OrderQty'],
        mask_as_connectivity="fix-fh-eq-paris",
        md_entry_size={50: 0},
        md_entry_px={40: 30},
        symbol={"XPAR": symbol_paris}
    ))
    trade_rule_2 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=case_params['OrderQty'],
        mask_as_connectivity="fix-fh-eq-trqx",
        md_entry_size={50: 0},
        md_entry_px={40: 30},
        symbol={"TRQX": symbol_trqx}
    ))
    try:
        # Send MarketDataSnapshotFullRefresh message

        MDRefID_1 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_paris,
            connection_id=ConnectionID(session_alias="fix-fh-eq-paris")
        )).MDRefID
        MDRefID_2 = simulator.getMDRefIDForConnection(request=RequestMDRefID(
            symbol=symbol_trqx,
            connection_id=ConnectionID(session_alias="fix-fh-eq-trqx")
        )).MDRefID
        mdfr_params_1 = {
            'MDReportID': "1",
            'MDReqID': MDRefID_1,
            'Instrument': {
                'Symbol': symbol_paris
            },
            'NoMDEntries': [
                {
                    'MDEntryType': '0',
                    'MDEntryPx': '30',
                    'MDEntrySize': '100',
                    'MDEntryPositionNo': '1'
                },
                {
                    'MDEntryType': '1',
                    'MDEntryPx': '40',
                    'MDEntrySize': '100',
                    'MDEntryPositionNo': '1'
                }
            ]
        }
        mdfr_params_2 = deepcopy(mdfr_params_1)
        mdfr_params_2['MDReqID'] = MDRefID_2
        mdfr_params_2['Instrument'] = {
            'Symbol': symbol_trqx
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
            'Currency': 'EUR',
            'ComplianceID': 'FX5',
            'ClientAlgoPolicyID': 'QA_SORPING',
            'TargetStrategy': case_params['TargetStrategy'],
            'Text': 'QAP-2740'
        }
        new_sor_order = act.placeOrderFIX(
            bca.convert_to_request(
                'Send NewSingleOrder',
                case_params['TraderConnectivity'],
                case_id,
                bca.message_to_grpc('NewOrderSingle', sor_order_params, case_params['TraderConnectivity'])
            ))
        checkpoint_1 = new_sor_order.checkpoint_id
        pending_er_params = {
            **reusable_order_params,
            'ClOrdID': sor_order_params['ClOrdID'],
            'OrderID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'ExecID': new_sor_order.response_messages_list[0].fields['OrderID'].simple_value,
            'TransactTime': '*',
            'CumQty': '0',
            'LastPx': '0',
            'OrderQty': case_params['OrderQty'],
            'Price': case_params['Price'],
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
            bca.create_check_rule(
                "ER Pending NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", pending_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )

        del pending_er_params['Account']
        new_er_params = deepcopy(pending_er_params)
        new_er_params['OrdStatus'] = new_er_params['ExecType'] = '0'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['ExecID'] = '*'
        new_er_params['ExecRestatementReason'] = '4'
        new_er_params['SecondaryAlgoPolicyID'] = 'QA_SORPING'
        new_er_params['Instrument'] = case_params['Instrument']
        new_er_params['SettlDate'] = "*"
        verifier.submitCheckRule(
            bca.create_check_rule(
                "ER New NewOrderSingle Received",
                bca.filter_to_grpc("ExecutionReport", new_er_params, ['ClOrdID', 'OrdStatus']),
                checkpoint_1, case_params['TraderConnectivity'], case_id
            )
        )

        work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
        username = Stubs.custom_config['qf_trading_fe_user_305']
        password = Stubs.custom_config['qf_trading_fe_password_305']
        if not Stubs.frontend_is_open:
            prepare_fe(case_id, session_id, work_dir, username, password)

        try:
            order_info_extraction = "getOrderInfo"

            main_order_details = OrdersDetails()
            main_order_details.set_default_params(base_request)
            main_order_details.set_extraction_id(order_info_extraction)
            main_order_details.set_filter(["ClOrdID", sor_order_params['ClOrdID']])

            main_order_exec_pcy = ExtractionDetail("order_exec_pcy", "ExecPcy")
            main_order_lmt_price = ExtractionDetail("order_lmt_price", "LmtPrice")
            main_order_sts = ExtractionDetail("order_sts", "ExecSts")
            main_order_id = ExtractionDetail("order_id", "Order ID")

            main_order_extraction_action = ExtractionAction.create_extraction_action(
                extraction_details=[main_order_exec_pcy,
                                    main_order_lmt_price,
                                    main_order_sts,
                                    main_order_id])

            sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "Order ID")
            sub_lvl1_1_exec_pcy = ExtractionDetail("subOrder_lv1.ExecPcy", "ExecPcy")
            sub_lvl1_1_venue = ExtractionDetail("subOrder_lv1.Venue", "Venue")
            sub_lvl1_1_venue_OA = ExtractionDetail("subOrder_lv1_OA.Venues", "Venues")
            sub_lvl1_1_ext_action1 = ExtractionAction.create_extraction_action(
                extraction_details=[sub_order_id_dt, sub_lvl1_1_exec_pcy, sub_lvl1_1_venue])
            row_selector = CalcDataContentsRowSelector()
            row_selector.set_column_name("PriceCost")
            row_selector.minimize()
            sub_lvl1_1_ext_action2 = OrderAnalysisAction.create_extract_calc_data_contents(event_number=1,
                                                                                           row_selector=row_selector,
                                                                                           detail=sub_lvl1_1_venue_OA)

            sub_lv1_1_info = OrderInfo.create(actions=[sub_lvl1_1_ext_action1, sub_lvl1_1_ext_action2])
            sub_lvl1_2_exec_pcy = ExtractionDetail("subOrder_lv1_2.ExecPcy", "ExecPcy")
            sub_lvl1_2_ext_action = ExtractionAction.create_extraction_action(
                extraction_detail=sub_lvl1_2_exec_pcy)
            sub_lv1_2_info = OrderInfo.create(actions=[sub_lvl1_2_ext_action])

            sub_order_det_both = OrdersDetails.create(order_info_list=[sub_lv1_1_info, sub_lv1_2_info])

            main_order_details.add_single_order_info(
                OrderInfo.create(action=main_order_extraction_action, sub_order_details=sub_order_det_both))
            request = call(act2.getOrdersDetails, main_order_details.request())

            venue = request[sub_lvl1_1_venue_OA.name]
            logger.info(venue)
            call(common_act.verifyEntities, verification(order_info_extraction, "Checking main order",
                                                         [verify_ent("Order ExecPcy", main_order_exec_pcy.name,
                                                                     "Synth (Quod LitDark)"),
                                                          verify_ent("Order LmtPrice", main_order_lmt_price.name, "25"),
                                                          verify_ent("Order Status", main_order_sts.name, "Filled")]))
            call(common_act.verifyEntities, verification(order_info_extraction, "Checking Lvl_2 orders",
                                                         [verify_ent("Sub Order 1 Lvl 1 ExecPcy",
                                                                     sub_lvl1_1_exec_pcy.name,
                                                                     "Synth (Quod MultiListing)"),
                                                          verify_ent("Sub Order 2 Lvl 1 ExecPcy",
                                                                     sub_lvl1_2_exec_pcy.name,
                                                                     "Synth (Quod DarkPool)")
                                                          ]))

            # check child orders
            sub_order_id = request[sub_order_id_dt.name]
            if not sub_order_id:
                raise Exception("Sub order id is not returned")
            print("Sub order id " + sub_order_id)
            #
            lvl2_length = "subOrders_lv2.length"
            sub_lvl2_1_ext_action = "order.sublvl2_1"
            sub_lv2_1_venue = ExtractionDetail("subOrder_1_lv2.Venue", "Venue")
            sub_lv2_1_qty = ExtractionDetail("subOrder_1_lv2.Qty", "Qty")
            sub_lv2_1_lmt_price = ExtractionDetail("subOrder_1_lv2.LmtPrice", "LmtPrice")

            lvl2_details = OrdersDetails()
            lvl2_details.set_default_params(base_request)
            lvl2_details.set_extraction_id(sub_lvl2_1_ext_action)
            lvl2_details.set_filter(["ParentOrdID", sub_order_id])
            lvl2_details.add_single_order_info(OrderInfo.create(
                action=ExtractionAction.create_extraction_action(extraction_details=[sub_lv2_1_venue,
                                                                                     sub_lv2_1_qty,
                                                                                     sub_lv2_1_lmt_price])))
            lvl2_details.extract_length(lvl2_length)

            request2 = call(act2.getChildOrdersDetails, lvl2_details.request())

            verifier2.set_event_name("Checking Lvl_3 order")
            verifier2.compare_values("Sub 1 Lvl 2 Venue", request2[sub_lv2_1_venue.name], "TRQX")
            verifier2.compare_values("Sub 1 Lvl 2 Qty", request2[sub_lv2_1_qty.name], "100")
            verifier2.compare_values("Sub 1 Lvl 2 Price", request2[sub_lv2_1_lmt_price.name], "30")
            verifier2.compare_values("OA Minimum PriceCost Venue Sub Order 1 Lvl 1", request[sub_lvl1_1_venue_OA.name], "TRQX")
            verifier2.compare_values("Compare venues", request2[sub_lv2_1_venue.name], request[sub_lvl1_1_venue_OA.name])
            verifier2.compare_values("Sub order Lvl 2 count", request2[lvl2_length], "1")
            verifier2.verify()

        except Exception:
            logger.error("Error execution in GUI part", exc_info=True)

        close_fe(case_id, session_id)

    except Exception as e:
        logging.error("Error execution in FIX part", exc_info=True)

    sim.removeRule(trade_rule_1)
    sim.removeRule(trade_rule_2)
    rule_man.remove_rule(OCR1)
    rule_man.remove_rule(OCR2)
    rule_man.print_active_rules()

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
