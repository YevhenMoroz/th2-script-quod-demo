import logging
import time
from pathlib import Path
from random import randint

from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.dealer_intervention_wrappers import BaseTableDataRequest, ExtractionDetailsRequest, \
    ModificationRequest, RFQExtractionDetailsRequest
from win_gui_modules.order_book_wrappers import ExtractionDetail
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base
from th2_grpc_act_fix_quod.act_fix_pb2 import PlaceMessageRequest
from th2_grpc_common.common_pb2 import Message, ConnectionID, MessageMetadata, MessageID, Value
from datetime import datetime


def check_dealer_intervention(base_request, service, case_id, qty):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_filter_list(["Qty", qty])
    extraction_request = ExtractionDetailsRequest(base_data)
    extraction_id = bca.client_orderid(8)
    extraction_request.set_extraction_id(extraction_id)
    extraction_request.add_extraction_detail(ExtractionDetail("dealerIntervention.status", "Status"))

    response = call(service.getUnassignedRFQDetails, extraction_request.build())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check quote request in DI")
    verifier.compare_values("Status", "New", response["dealerIntervention.status"])


def assign_firs_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    call(service.assignToMe, base_data.build())


def estimate_first_request(base_request, service):
    base_data = BaseTableDataRequest(base=base_request)
    base_data.set_row_number(1)
    call(service.estimate, base_data.build())


def press_send(base_request, service):
    modify_request = ModificationRequest(base=base_request)
    modify_request.send()
    call(service.modifyAssignedRFQ, modify_request.build())


def close_dmi_window(base_request, dealer_interventions_service):
    call(dealer_interventions_service.closeWindow, base_request)


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    dealer_service = Stubs.win_act_dealer_intervention_service

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)

    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty = str(randint(17000000, 20000000))
    symbol = "GBP/USD"
    security_type_spo = "FXSPOT"
    settle_date = spo()
    settle_type = "SPO"
    currency = "GBP"

    try:
        # Step 1
        # params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
        #                            securitytype=security_type_spo, settldate=settle_date, settltype=settle_type,
        #                            currency=currency,
        #                            account=client_tier)
        # rfq = FixClientSellRfq(params)
        # rfq.send_request_for_quote_no_reply()
        # region Working ↓
        # quote_req_id = bca.client_orderid(8)
        # params = {
        #     'QuoteReqID': quote_req_id,
        #     'NoRelatedSymbols': [{
        #         'Account': "Iridium1",
        #         'Instrument': {
        #             'Symbol': "EUR/USD",
        #             'SecurityType': "FXSPOT"
        #         },
        #         'SettlDate': spo(),
        #         'SettlType': 0,
        #         'Currency': "EUR",
        #         'QuoteType': '1',
        #         'OrderQty': "25000000",
        #         'OrdType': 'D'
        #     }
        #     ]
        # }
        # act = Stubs.fix_act
        # response = act.sendQuoteViaWindow(
        #     request=bca.convert_to_request(
        #         "SendQuoteRequest",
        #         "fix-ss-rfq-314-luna-standard",
        #         case_id,
        #         bca.message_to_grpc("QuoteRequest", params, "fix-ss-rfq-314-luna-standard")
        #     )
        # )
        #
        # check_dealer_intervention(case_base_request, dealer_service, case_id, "25000000")
        # assign_firs_request(case_base_request, dealer_service)
        # estimate_first_request(case_base_request, dealer_service)
        # time.sleep(5)
        # press_send(case_base_request, dealer_service)
        # a = next(response)
        # quote_id = a.response_messages_list[0].fields['QuoteID'].simple_value
        # print(quote_id)
        # #
        # order_params = {
        #     'Account': "Iridium1",
        #     'HandlInst': "1",
        #     'Side': "1",
        #     'OrderQty': "25000000",
        #     'TimeInForce': "3",
        #     'Price': '1.187',
        #     'QuoteID': quote_id,
        #     'OrdType': "D",
        #     'ClOrdID': bca.client_orderid(8),
        #     'TransactTime': datetime.utcnow().isoformat(),
        #     'SettlType': "0",
        #     'SettlDate': spo(),
        #     'Instrument': {
        #         'Symbol': "EUR/USD",
        #         'SecurityType': "FXSPOT",
        #         'Product': 4,
        #     },
        #     'Currency': "EUR"
        # }
        # order = act.placeOrderFIX(
        #     request=bca.convert_to_request(
        #         'Send new order ', "fix-ss-rfq-314-luna-standard", case_id,
        #         bca.message_to_grpc('NewOrderSingle', order_params,
        #                             "fix-ss-rfq-314-luna-standard")
        #     ))
        # endregion
        params = CaseParamsSellRfq(client_tier, case_id, orderqty=qty, symbol=symbol,
                                   securitytype=security_type_spo, settldate=settle_date,
                                   settltype=settle_type, securityid=symbol,
                                   currency=currency, settlcurrency="USD",
                                   account=account)
        rfq = FixClientSellRfq(params)
        rfq.send_request_for_dmi()
        check_dealer_intervention(case_base_request, dealer_service, case_id, qty)
        assign_firs_request(case_base_request, dealer_service)
        estimate_first_request(case_base_request, dealer_service)
        time.sleep(3)
        press_send(case_base_request, dealer_service)
        a = next(rfq)
        quote_id = a.extract_filed('QuoteID')
        price = rfq.extract_filed("OfferPX")
        rfq.send_new_order_single(price, quote_id=quote_id)

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            close_dmi_window(case_base_request, dealer_service)
        except Exception:
            logging.error("Error execution", exc_info=True)
