import logging
from copy import deepcopy
from datetime import datetime
from custom import basic_custom_actions as bca
from stubs import Stubs

from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodNOSRule, TemplateQuodOCRRRule, TemplateQuodOCRRule

from win_gui_modules.order_ticket import OrderTicketDetails
from win_gui_modules.order_ticket_wrappers import NewOrderDetails
from win_gui_modules.utils import set_session_id, prepare_fe_2, close_fe_2, get_base_request, call
from win_gui_modules.wrappers import set_base, verification, verify_ent, order_analysis_algo_parameters_request, \
    create_order_analysis_events_request, create_verification_request, check_value
from win_gui_modules.order_book_wrappers import OrdersDetails, OrderInfo,\
    ExtractionDetail, ExtractionAction, ModifyOrderDetails, CancelOrderDetails
from th2_grpc_act_gui_quod.act_ui_win_pb2 import VerificationDetails


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    act = Stubs.fix_act
    verifier = Stubs.verifier
    simulator = Stubs.simulator
    core = Stubs.core

    conn = ConnectionID(session_alias='fix-bs-eq-trqx')

    # Rules
    NOS = simulator.createQuodNOSRule(request=TemplateQuodNOSRule(connection_id=conn))
    OCRR = simulator.createQuodOCRRRule(request=TemplateQuodOCRRRule(connection_id=conn))
    OCR = simulator.createQuodOCRRule(request=TemplateQuodOCRRule(connection_id=conn))

    # Store case start time
    seconds, nanos = bca.timestamps()
    case_name = "QAP-2838"
    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    if not Stubs.frontend_is_open:
        prepare_fe_2(case_id, session_id)

    # Preconditions
    symbol_trqx = "3631"
    trade_rule = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
        connection_id=ConnectionID(session_alias="fix-bs-eq-trqx"),
        no_party_ids=[
            TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
            TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
            TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
        ],
        cum_qty=100,
        mask_as_connectivity="fix-bs-eq-trqx",
        md_entry_size={100: 100},
        md_entry_px={100: 100},
        symbol={"TRQX": symbol_trqx}
    ))

    # Sending DMA order

    case_params = {
        'TraderConnectivity': 'gtwquod3',
        'TraderConnectivity2': 'fix-bs-eq-paris',
        'TraderConnectivity3': 'fix-bs-eq-trqx',
        'SenderCompID': 'QUODFX_UAT',
        'TargetCompID': 'QUOD3',
        'SenderCompID2': 'KCH_QA_RET_CHILD',
        'TargetCompID2': 'QUOD_QA_RET_CHILD',
        'Account': 'KEPLER',
        'HandlInst': '1',
        'Side': '1',
        'OrderQty': 100,
        'OrdType': '2',
        'Price': 100,
        'TimeInForce': '0',
        'Instrument': {
            'Symbol': 'SE0000818569_SEK',
            'SecurityID': 'SE0000818569',
            'SecurityIDSource': '4',
            'SecurityExchange': 'XSTO'
        }
    }

    # This parameters can be used for ExecutionReport message
    reusable_order_params = {
        'Account': case_params['Account'],
        'HandlInst': case_params['HandlInst'],
        'Side': case_params['Side'],
        'TimeInForce': case_params['TimeInForce'],
        'OrdType': case_params['OrdType'],
        'OrderCapacity': 'A',
        'Currency': 'SEK'
    }

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
        'Currency': 'SEK',
        'ComplianceID': 'FX5',
        'ClientAlgoPolicyID': 'QA_SORPING',
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
            checkpoint_1, case_params['TraderConnectivity'], case_id
        )
    )
    core.removeRule(trade_rule)

    try:
        # Step 1 - create algo order
        qty = "1000"
        limit = "1"
        lookup = "PAR_ST"

        act_order_ticket = Stubs.win_act_order_ticket
        config_vars = Stubs.custom_config
        act_order_book = Stubs.win_act_order_book
        common_win_act = Stubs.win_act

        order_ticket = OrderTicketDetails()
        order_ticket.set_quantity(qty)
        order_ticket.set_limit(limit)

        quod_participant_strategy = order_ticket.add_quod_participation_strategy("Quod Participation")
        quod_participant_strategy.set_start_date("Now")
        quod_participant_strategy.set_end_date("Now", "0.9")
        quod_participant_strategy.set_percentage_volume('30')
        quod_participant_strategy.set_aggressivity("Neutral")

        new_order_details = NewOrderDetails()
        new_order_details.set_lookup_instr(lookup)
        new_order_details.set_order_details(order_ticket)
        new_order_details.set_default_params(base_request)
        call(act_order_ticket.placeOrder, new_order_details.build())

        order_info_extraction = "getOrderInfo_1"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction)
        main_order_details.set_filter(["Owner", config_vars["qf_trading_fe_user"]])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_id = ExtractionDetail("order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                     main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act_order_book.getOrdersDetails, main_order_details.request())
        call(common_win_act.verifyEntities, verification(order_info_extraction, "checking order",
                                                         [verify_ent("Order Status", main_order_status.name, "Open")]))

        order_id = request[main_order_id.name]
        if not order_id:
            raise Exception("Order id is not returned")

        # Step 2 amend algo order

        act_order_book = Stubs.win_act_order_book

        order_amend = OrderTicketDetails()
        quod_participant_strategy_2 = order_amend.add_quod_participation_strategy("Quod Participation")
        quod_participant_strategy_2.set_percentage_volume('40')

        amend_order_details = ModifyOrderDetails()
        amend_order_details.set_default_params(base_request)
        amend_order_details.set_filter(["Order ID", order_id])
        amend_order_details.set_order_details(order_amend)

        call(act_order_book.amendOrder, amend_order_details.build())

        extraction_id = "getOrderAnalysisAlgoParameters"

        call(common_win_act.getOrderAnalysisAlgoParameters,
             order_analysis_algo_parameters_request(extraction_id, ["PercentageVolume"], {"Order ID": order_id}))
        call(common_win_act.verifyEntities, verification(extraction_id, "checking algo parameters",
                                                         [verify_ent("PercentageVolume", "PercentageVolume", "40.0")]))

        # Step 3 cancel algo order
        cancel_order_details = CancelOrderDetails()
        cancel_order_details.set_default_params(base_request)
        cancel_order_details.set_filter(["Order ID", order_id])
        cancel_order_details.set_comment("Order cancelled by script")
        cancel_order_details.set_cancel_children(True)

        call(act_order_book.cancelOrder, cancel_order_details.build())

        # Checking cancelled order status
        order_info_extraction_cancel = "getOrderInfo_cancelled"

        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(order_info_extraction_cancel)
        main_order_details.set_filter(["Order ID", order_id])

        main_order_status = ExtractionDetail("order_status", "Sts")
        main_order_id = ExtractionDetail("order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_status,
                                                                                                     main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        call(act_order_book.getOrdersDetails, main_order_details.request())
        call(common_win_act.verifyEntities, verification(order_info_extraction_cancel, "checking order",
                                                     [verify_ent("Order Status", main_order_status.name, "Cancelled")]))

        # step 4 check Audit for algo
        extraction_id = "getOrderAnalysisEvents"
        call(common_win_act.getOrderAnalysisEvents,
             create_order_analysis_events_request(extraction_id, {"Order ID": order_id}))

        vr = create_verification_request("checking order events", extraction_id, extraction_id)

        check_value(vr, "Event 1 Description contains", "event1.desc", "New User's Synthetic Order Received",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 2 Description contains", "event2.desc", "last trade is 100@1",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 3 Description contains", "event3.desc",
                    "User's Modification Received on the Synthetic Order",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Event 4 Description contains", "event4.desc",
                    "User's Cancellation Received on the Synthetic Order",
                    VerificationDetails.VerificationMethod.CONTAINS)

        check_value(vr, "Events Count", "events.count", "4")
        call(common_win_act.verifyEntities, vr)

    except Exception as e:
        logging.error("Error execution", exc_info=True)

    for rule in [NOS, OCRR, OCR]:
        core.removeRule(rule)
    close_fe_2(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")
