from custom.verifier import Verifier
from win_gui_modules.order_book_wrappers import ModifyOrderDetails, OrderInfo, OrdersDetails, ExtractionDetail, \
    CancelOrderDetails, ExtractionAction
from stubs import Stubs
from win_gui_modules.wrappers import *
from win_gui_modules.order_ticket_wrappers import OrderTicketDetails, NewOrderDetails
from custom.basic_custom_actions import timestamps, create_event
from win_gui_modules.utils import set_session_id, get_base_request, call, prepare_fe, close_fe
import logging
from rule_management import RuleManager
from datetime import datetime
from th2_grpc_common.common_pb2 import ConnectionID
from th2_grpc_sim_quod.sim_pb2 import TemplateQuodSingleExecRule, TemplateNoPartyIDs, RequestMDRefID
from custom import basic_custom_actions as bca
from win_gui_modules.middle_office_wrappers import ModifyTicketDetails, ExtractMiddleOfficeBlotterValuesRequest

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def execute(report_id):
    fix_act = Stubs.fix_act
    act = Stubs.win_act_order_ticket
    act2 = Stubs.win_act_order_book
    common_act = Stubs.win_act
    simulator = Stubs.simulator

    bs_paris = 'fix-bs-eq-paris'
    bs_trqx = 'fix-bs-eq-trqx'

    seconds, nanos = timestamps()  # Store case start time
    case_name = "QAP-3349"

    # Create sub-report for case
    case_id = create_event(case_name, report_id)

    session_id = set_session_id()
    set_base(session_id, case_id)
    base_request = get_base_request(session_id, case_id)

    work_dir = Stubs.custom_config['qf_trading_fe_folder_305']
    username = Stubs.custom_config['qf_trading_fe_user_305']
    password = Stubs.custom_config['qf_trading_fe_password_305']
    if not Stubs.frontend_is_open:
        prepare_fe(case_id, session_id, work_dir, username, password)
    try:

        case_params = {
            'TraderConnectivity': 'gtwquod3',
            'TraderConnectivity2': 'fix-bs-eq-paris',
            'SenderCompID': 'QUODFX_UAT',
            'TargetCompID': 'QUOD3',
            'SenderCompID2': 'KCH_QA_RET_CHILD',
            'TargetCompID2': 'QUOD_QA_RET_CHILD',
            'Account': 'MOClient',
            'HandlInst': '1',
            'Side': '2',
            'OrderQty': '100',
            'OrdType': '2',
            'Price': '100',
            'TimeInForce': '0',
            'DeliverToCompID': 'PARIS',
            'Instrument': {
                'Symbol': 'FR0004186856_EUR',
                'SecurityID': 'FR0004186856',
                'SecurityIDSource': 4,
                'SecurityExchange': 'XPAR'
            }
        }

        trade_rule_1 = simulator.createQuodSingleExecRule(request=TemplateQuodSingleExecRule(
            connection_id=ConnectionID(session_alias="fix-bs-eq-paris"),
            no_party_ids=[
                TemplateNoPartyIDs(party_id="KEPLER", party_id_source="D", party_role="1"),
                TemplateNoPartyIDs(party_id="1", party_id_source="D", party_role="2"),
                TemplateNoPartyIDs(party_id="2", party_id_source="D", party_role="3")
            ],
            cum_qty=100,
            mask_as_connectivity="fix-fh-eq-paris",
            md_entry_size={500: 0},
            md_entry_px={30: 25},
            symbol={"XPAR": '1224'}))

        dma_order_params = {
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
            'Currency': 'EUR'
        }
        new_dma_order = fix_act.placeOrderFIX(
            request=bca.convert_to_request(
                "Send new sorping order", "gtwquod5", case_id,
                bca.message_to_grpc('NewOrderSingle', dma_order_params, "gtwquod5")
            ))

        Stubs.core.removeRule(trade_rule_1)

        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)
        modify_request.set_filter(["ClOrdID", dma_order_params['ClOrdID'], "Symbol", "VETO"])

        settlement_details = modify_request.add_settlement_details()
        settlement_details.set_settlement_type("Regular")
        settlement_details.set_settlement_currency("AED")
        settlement_details.set_exchange_rate("10")
        settlement_details.set_exchange_rate_calc("Multiply")
        # settlement_details.set_settlement_date("3/27/2021")
        settlement_details.set_pset("EURO_CLEAR")

        # extraction_details = modify_request.add_extraction_details()
        # extraction_details.set_extraction_id("BookExtractionId")
        # extraction_details.extract_agreed_price("book.agreedPrice")
        # extraction_details.extract_gross_amount("book.grossAmount")
        # extraction_details.extract_total_comm("book.totalComm")
        # extraction_details.extract_total_fees("book.totalFees")
        # extraction_details.extract_net_price("book.netPrice")
        # extraction_details.extract_net_amount("book.netAmount")
        # extraction_details.extract_pset_bic("book.psetBic")
        # extraction_details.extract_exchange_rate("book.exchangeRate")

        call(middle_office_service.bookOrder, modify_request.build())

        extraction_id = "main_order"
        main_order_details = OrdersDetails()
        main_order_details.set_default_params(base_request)
        main_order_details.set_extraction_id(extraction_id)
        main_order_details.set_filter(["ClOrdID", dma_order_params['ClOrdID'], "Symbol", "VETO"])

        main_order_post_trade_status = ExtractionDetail("post_trade_status", "PostTradeStatus")
        main_order_id = ExtractionDetail("main_order_id", "Order ID")
        main_order_extraction_action = ExtractionAction.create_extraction_action(extraction_details=[main_order_post_trade_status, main_order_id])
        main_order_details.add_single_order_info(OrderInfo.create(action=main_order_extraction_action))

        request = call(act2.getOrdersDetails, main_order_details.request())
        call(common_act.verifyEntities, verification(extraction_id, "checking order",
                                                     [verify_ent("Order PostTradeStatus", main_order_post_trade_status.name, "Booked")]))

        block_order_id = request[main_order_id.name]
        if not block_order_id:
            raise Exception("Block order id is not returned")
        print("Block order id " + block_order_id)

        # Step 2 check columns in MO

        ext_id = "MiddleOfficeExtractionId"
        middle_office_service = Stubs.win_act_middle_office_service
        extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        extract_request.set_extraction_id(ext_id)
        extract_request.set_filter(["Order ID", block_order_id])
        block_order_id = ExtractionDetail("middleOffice.blockId", "Order ID")
        block_id = ExtractionDetail("middleOffice.blockId", "Block ID")
        block_order_status = ExtractionDetail("middleOffice.status", "Status")
        block_order_match_status = ExtractionDetail("middleOffice.matchStatus", "Match Status")
        block_order_summary_status = ExtractionDetail("middleOffice.summaryStatus", "Summary Status")
        block_order_settl_type = ExtractionDetail("middleOffice.settlType", "SettlType")
        block_order_settl_currency = ExtractionDetail("middleOffice.settlCurrency", "SettlCurrency")
        block_order_exchange_rate = ExtractionDetail("middleOffice.exchangeRate", "ExchangeRate")
        block_order_settl_curr_fx_rate_calc = ExtractionDetail("middleOffice.settlCurrFxRateCalc", "SettlCurrFxRateCalc")
        block_order_settl_date = ExtractionDetail("middleOffice.settlDate", "SettlDate")
        block_order_pset = ExtractionDetail("middleOffice.pset", "PSET")
        block_order_pset_bic = ExtractionDetail("middleOffice.psetbic", "PSET BIC")
        block_order_root_commission = ExtractionDetail("middleOffice.rootCommission", "RootCommission")
        block_order_net_amt = ExtractionDetail("middleOffice.netAmt", "Net Amt")
        block_order_net_price = ExtractionDetail("middleOffice.netPrice", "Net Price")
        extract_request.add_extraction_details(
            [block_order_id, block_id, block_order_status, block_order_match_status, block_order_summary_status,
             block_order_settl_type, block_order_settl_currency, block_order_exchange_rate, block_order_settl_curr_fx_rate_calc,
             block_order_settl_date, block_order_pset, block_order_pset_bic, block_order_root_commission, block_order_net_amt, block_order_net_price])
        request = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())

        verifier2 = Verifier(case_id)

        verifier2.set_event_name("Checking block order")
        verifier2.compare_values("Order Status", request[block_order_status.name], "ApprovalPending")
        verifier2.compare_values("Order Match Status", request[block_order_match_status.name], "Unmatched")
        verifier2.compare_values("Order Summary Status", request[block_order_summary_status.name], "")
        verifier2.compare_values("Order SettlType", request[block_order_settl_type.name], "")
        verifier2.compare_values("Order SettlCurrency", request[block_order_settl_currency.name], "")
        verifier2.compare_values("Order ExchangeRate", request[block_order_exchange_rate.name], "")
        verifier2.compare_values("Order SettlCurrFxRateCalc", request[block_order_settl_curr_fx_rate_calc.name], "")
        verifier2.compare_values("Order SettlDate", request[block_order_settl_date.name], "")
        verifier2.compare_values("Order PSET", request[block_order_pset.name], "")
        verifier2.compare_values("Order PSET BIC", request[block_order_pset_bic.name], "")
        verifier2.compare_values("Order RootCommission", request[block_order_root_commission.name], "")
        verifier2.compare_values("Order Net Amt", request[block_order_net_amt.name], "")
        verifier2.compare_values("Order Net Price", request[block_order_net_price.name], "")
        verifier2.verify()

        # Step 3 Approve

        modify_request = ModifyTicketDetails(base=base_request)
        call(middle_office_service.approveMiddleOfficeTicket, modify_request.build())

        ext_id_approve = "MiddleOfficeExtractionId2"
        middle_office_service_approve = Stubs.win_act_middle_office_service
        extract_request_approve = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        extract_request_approve.set_extraction_id(ext_id_approve)
        block_order_id = ExtractionDetail("middleOffice.blockId", "Order ID")
        block_id = ExtractionDetail("middleOffice.blockId", "Block ID")
        block_order_status = ExtractionDetail("middleOffice.status", "Status")
        block_order_match_status = ExtractionDetail("middleOffice.matchStatus", "Match Status")
        block_order_summary_status = ExtractionDetail("middleOffice.summaryStatus", "Summary Status")
        extract_request_approve.add_extraction_details(
            [block_order_id, block_id, block_order_status, block_order_match_status, block_order_summary_status])
        request_approve = call(middle_office_service_approve.extractMiddleOfficeBlotterValues, extract_request.build())

        verifier2 = Verifier(case_id)

        verifier2.set_event_name("Checking block order")
        verifier2.compare_values("Order Status", request_approve[block_order_status.name], "Accepted")
        verifier2.compare_values("Order Match Status", request_approve[block_order_match_status.name], "Matched")
        verifier2.compare_values("Order Summary Status", request_approve[block_order_summary_status.name], "")
        verifier2.verify()

        # Step 4 Allocate

        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)

        allocations_details = modify_request.add_allocations_details()
        allocations_details.add_allocation_param({"Account": "MOClientSA1", "Alloc Qty": "100"})
        call(middle_office_service.allocateMiddleOfficeTicket, modify_request.build())

        # Step 5 Amend

        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)

        settlement_details = modify_request.add_settlement_details()
        settlement_details.set_settlement_currency("EUR")

        call(middle_office_service.amendMiddleOfficeTicket, modify_request.build())

        # Step 6 Amend

        middle_office_service = Stubs.win_act_middle_office_service

        modify_request = ModifyTicketDetails(base=base_request)

        settlement_details = modify_request.add_settlement_details()
        settlement_details.set_settlement_currency("EUR")

        call(middle_office_service.amendMiddleOfficeTicket, modify_request.build())

        # middle_office_service = Stubs.win_act_middle_office_service
        # extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        # extract_request.set_extraction_id("MiddleOfficeExtractionId")
        # extract_request.set_filter(["Order ID", main_order_id])
        # extract_request.add_extraction_details([ExtractionDetail("middleOffice.blockId", "Block ID"),
        #                                         ExtractionDetail("middleOffice.status", "Status"),
        #                                         ExtractionDetail("middleOffice.matchStatus", "Match Status"),
        #                                         ExtractionDetail("middleOffice.summaryStatus", "Summary Status"),
        #                                         ExtractionDetail("middleOffice.settlType", "SettlType"),
        #                                         ExtractionDetail("middleOffice.settlCurrency", "SettlCurrency"),
        #                                         ExtractionDetail("middleOffice.exchangeRate", "ExchangeRate"),
        #                                         ExtractionDetail("middleOffice.settlDate", "SettlDate"),
        #                                         ExtractionDetail("middleOffice.PSET", "PSET"),
        #                                         ExtractionDetail("middleOffice.PSETBIC", "PSET BIC"),
        #                                         ExtractionDetail("middleOffice.rootCommission", "RootCommission"),
        #                                         ExtractionDetail("middleOffice.netAmt", "Net Amt"),
        #                                         ExtractionDetail("middleOffice.netPrice", "Net Price")])
        #
        # response = call(middle_office_service.extractMiddleOfficeBlotterValues, extract_request.build())
        # call(common_act.verifyEntities, verification(extraction_id, "checking order",
        #                                              [verify_ent("Order PostTradeStatus",
        #                                                          main_order_post_trade_status.name, "Booked")]))
        #
        # # Step 3 Approve  block
        #
        # call(middle_office_service.approveMiddleOfficeTicket, modify_request.build())
        #
        # extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        # extract_request.set_extraction_id("MiddleOfficeExtractionId")
        # extract_request.set_filter(["Order ID", main_order_id])
        # extract_request.add_extraction_details([ExtractionDetail("middleOffice.blockId", "Block ID"),
        #                                         ExtractionDetail("middleOffice.status", "Status"),
        #                                         ExtractionDetail("middleOffice.matchStatus", "Match Status"),
        #                                         ExtractionDetail("middleOffice.summaryStatus", "Summary Status")])
        #
        # # Step 4 Allocate
        #
        # modify_request = ModifyTicketDetails(base=base_request)
        #
        # allocations_details = modify_request.add_allocations_details()
        # allocations_details.add_allocation_param({"Account": "MOClientSA1", "BO Field 2": "123"})
        # allocations_details.add_allocation_param({"Account": "MOClientSA2", "BO Field 3": "123"})
        #
        # extraction_details = modify_request.add_extraction_details()
        # extraction_details.set_extraction_id("BookExtractionId")
        # extraction_details.extract_net_price("book.netPrice")
        # extraction_details.extract_net_amount("book.netAmount")
        # extraction_details.extract_total_comm("book.totalComm")
        # extraction_details.extract_gross_amount("book.grossAmount")
        # extraction_details.extract_total_fees("book.totalFees")
        # extraction_details.extract_agreed_price("book.agreedPrice")
        #
        # response = call(middle_office_service.allocateMiddleOfficeTicket, modify_request.build())
        #
        # extract_request = ExtractMiddleOfficeBlotterValuesRequest(base=base_request)
        # extract_request.set_extraction_id("MiddleOfficeExtractionId")
        # extract_request.set_filter(["Order ID", main_order_id])
        # extract_request.add_extraction_details([ExtractionDetail("middleOffice.blockId", "Block ID"),
        #                                         ExtractionDetail("middleOffice.status", "Status"),
        #                                         ExtractionDetail("middleOffice.matchStatus", "Match Status"),
        #                                         ExtractionDetail("middleOffice.summaryStatus", "Summary Status")])

        # Step 5 Amend Allocate


    except Exception as e:
        logging.error("Error execution", exc_info=True)
    close_fe(case_id, session_id)
    logger.info(f"Case {case_name} was executed in {str(round(datetime.now().timestamp() - seconds))} sec.")