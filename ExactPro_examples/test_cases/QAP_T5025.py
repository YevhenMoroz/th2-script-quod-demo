import logging
from copy import deepcopy
import time
from datetime import datetime

from th2_grpc_act_gui_quod import order_book_service
from th2_grpc_act_gui_quod.order_book_pb2_grpc import OrderBookServiceStub

from custom import basic_custom_actions as bca
from th2_grpc_common.common_pb2 import Direction

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

    rule_man = RuleManager()
    NOS1 = rule_man.add_NOS('fix-bs-eq-paris')
    NOS2 = rule_man.add_NOS('fix-bs-eq-trqx')
    OCR1 = rule_man.add_OCR('fix-bs-eq-paris')
    OCR2 = rule_man.add_OCR('fix-bs-eq-trqx')
    logger.info(f"Start rules with id's: \n {NOS1}, {NOS2}, {OCR1}, {OCR2}")

    seconds, nanos = bca.timestamps()  # Store case start time

    # Create sub-report for case
    case_name = "QAP_T5025"
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    # common_act = HandWinActStub(Channels.ui_act_channel)
    common_act = Stubs.win_act
    act2 = Stubs.win_act_order_book

    # act2 = OrderBookServiceStub(Channels.ui_act_channel)
    # call = self.call
    #
    # set_base(self._session_id, self._event_id)

    # common_act = self._services.main_win_service
    # order_book_act = order_book_service

    order_info_extraction = "getOrderInfo"
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
        'OrderQty': '400',
        'OrdType': '2',
        'Price': '20',
        'TimeInForce': '0',
        'TargetStrategy': 1004,
        'Instrument': {
            'Symbol': 'FR0010263202_EUR',
            'SecurityID': 'FR0010263202',
            'SecurityIDSource': 4,
            'SecurityExchange': 'XPAR'
        }
    }

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
        'IClOrdIdAO': 'test tag 5005'
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
            case_id,
            bca.message_to_grpc('NewOrderSingle', new_order_params, case_params['TraderConnectivity'])
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
        # 'TargetStrategy': new_order_params['TargetStrategy'],
        'MaxFloor': new_order_params['DisplayInstruction']['DisplayQty'],
        'Instrument': case_params['Instrument'],
        'NoParty': '*',
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
    # new_er_params['SecondaryAlgoPolicyID'] = 'ICEBERG'
    new_er_params['NoStrategyParameters'] = [
        {'StrategyParameterName': 'ReleasedNbr', 'StrategyParameterType': '1', 'StrategyParameterValue': '1'},
        {'StrategyParameterName': 'ReleasedQty', 'StrategyParameterType': '6', 'StrategyParameterValue': '400'}]
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
            checkpoint_1, case_params['TraderConnectivity'], case_id
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
            checkpoint_1,
            case_params['TraderConnectivity2'],
            case_id,
            Direction.Value("SECOND")
        )
    )

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']

    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["FO field 4", "test tag 5005"])

        main_order_qty = ExtractionDetail("order.Qty", "Qty")
        main_order_field4 = ExtractionDetail("order.FOfield4", "FO field 4")
        main_order_price = ExtractionDetail("order.Price", "LmtPrice")
        main_order_exec_pcy = ExtractionDetail("order.ExecPcy", "ExecPcy")
        main_order_display_qty = ExtractionDetail("order.DisplayQty", "DisplQty")
        main_order_order_id = ExtractionDetail("order.Id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_qty,
                                                                                                     main_order_price,
                                                                                                     main_order_field4,
                                                                                                     main_order_exec_pcy,
                                                                                                     main_order_display_qty,
                                                                                                     main_order_order_id])

        sub_order_id_dt = ExtractionDetail("subOrder_lvl_1.id", "Order ID")

        lvl1_info = OrderInfo.create(action=ExtractionAction.create_extraction_action(sub_order_id_dt))
        lvl1_details = OrdersDetails.create(info=lvl1_info)

        main_order_details.add_single_order_info(
            OrderInfo.create(action=main_order_extraction_action, sub_order_details=lvl1_details))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                     [verify_ent("Order ExecPcy", main_order_exec_pcy.name,
                                                                 "Synth (Quod Split Manager)"),
                                                      verify_ent("Order Price", main_order_price.name, "20"),
                                                      verify_ent("Order Qty", main_order_qty.name, "400"),
                                                      verify_ent("FO field 4", main_order_field4.name,
                                                                 "test tag 5005"),
                                                      verify_ent("Order Display Qty", main_order_display_qty.name,
                                                                 "50")]))

        # check child orders

        sub_order_id = request[sub_order_id_dt.name]
        if not sub_order_id:
            raise Exception("Sub order id is not returned")
        print("Sub order id " + sub_order_id)

        lvl2_length = "subOrders_lv2.length"
        algo_split_man_extr_id = "order.algo_split_man"
        sub_order_lvl2_exec_pcy = ExtractionDetail("subOrder_1_lv2.ExecPcy", "ExecPcy")
        sub_order_lvl2_field4 = ExtractionDetail("subOrder_1_lv2.FOfield4", "FO field 4")

        lvl2_details = OrdersDetails()
        lvl2_details.set_default_params(base_request)
        lvl2_details.set_extraction_id(algo_split_man_extr_id)
        lvl2_details.set_filter(["ParentOrdID", sub_order_id])
        lvl2_details.add_single_order_info(OrderInfo.create(
            action=ExtractionAction.create_extraction_action(extraction_details=[sub_order_lvl2_exec_pcy,
                                                                                 sub_order_lvl2_field4])
        ))
        lvl2_details.extract_length(lvl2_length)

        call(act2.getChildOrdersDetails, lvl2_details.request())

        call(common_act.verifyEntities, verification(algo_split_man_extr_id, "checking order",
                                                     [verify_ent("Sub 1 Lvl 2 FO field 4", sub_order_lvl2_field4.name,
                                                                 "test tag 5005"),
                                                      verify_ent("Sub 1 Lvl 2 ExecPcy", sub_order_lvl2_exec_pcy.name,
                                                                 "DMA"),
                                                      verify_ent("Sub order Lvl 2 count", lvl2_length, "1")
                                                      ]))

    except Exception as e:
        logging.error("Error execution", exc_info=True)

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
            case_id,
            bca.message_to_grpc('OrderCancelRequest', cancel_order_params, case_params['TraderConnectivity']),
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
        # 'SecondaryAlgoPolicyID': new_er_params['SecondaryAlgoPolicyID'],
        # 'TargetStrategy': new_er_params['TargetStrategy'],
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
            case_id
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
        'OrigClOrdID': '*',
        'ChildOrderID': '*',
        'ExDestination': new_order_params['ExDestination'],
        **check_params
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
            event_id=case_id,
            timeout=2000

        )
    )

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
    close_fe(case_id, session_id)

    logger.info("Case {} was executed in {} sec.".format(
        case_name, str(round(datetime.now().timestamp() - seconds))))
