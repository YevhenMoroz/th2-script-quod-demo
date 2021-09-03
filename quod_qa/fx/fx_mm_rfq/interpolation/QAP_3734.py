from custom.tenor_settlement_date import wk1, wk2, spo, broken_2, wk3, broken_w1w2
from quod_qa.common_tools import random_qty
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
import logging
import random
from datetime import datetime
from pathlib import Path
from th2_grpc_act_gui_quod.common_pb2 import BaseTileData
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from stubs import Stubs
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.order_book_wrappers import (OrdersDetails, ExtractionDetail,
                                                 ExtractionAction, OrderInfo, FXOrdersDetails, FXOrderInfo)
from win_gui_modules.quote_wrappers import QuoteDetailsRequest
from win_gui_modules.utils import get_base_request, call
from win_gui_modules.wrappers import set_base

client = 'Argentina1'
account = 'Argentina1_1'
client_tier = 'Argentina'
symbol = "GBP/USD"
security_type_fwd = "FXFWD"
settle_date_br = broken_w1w2()
settle_type_broken = "B"
currency = "GBP"
settle_currency = "USD"
venue_citir = 'CITIR'
venue_quodfx = ''
side = "1"
qty_1 = random_qty(1, 3, 7)
qty_2 = random_qty(1, 3, 7)


def send_rfq_and_filled_order_broken(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_fwd, settldate=settle_date_br,
                                    settltype=settle_type_broken,
                                    currency=currency, side=side,
                                    account=account, securityid=symbol)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    price = rfq.extract_filed("OfferPx")
    rfq.send_new_order_single(price)
    rfq.verify_order_pending().verify_order_filled_fwd()


def send_rfq_and_reject_broken(case_id, qty_1):
    params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_1, symbol=symbol,
                                    securitytype=security_type_fwd, settldate=settle_date_br,
                                    settltype=settle_type_broken,
                                    currency=currency, side=side,
                                    account=client, securityid=symbol)
    rfq = FixClientSellRfq(params_spot)
    rfq.send_request_for_quote()
    rfq.verify_quote_pending()
    return rfq


def check_quote_request_b(base_request, service, case_id, qty, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    if venue == 'CITIR':
        qrb.set_filter(['Qty', qty, 'Venue', venue])
    if venue == '':
        qrb.set_filter(['Qty', qty, 'ClientTier', client_tier])
    qrb_tenor = ExtractionDetail('quoteRequestBook.Tenor', 'Tenor')
    qrb_quote_status = ExtractionDetail('quoteRequestBook.QuoteSts', 'QuoteStatus')
    qrb.add_extraction_details([qrb_tenor, qrb_quote_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book")
    if venue == 'CITIR':
        verifier.compare_values(f'Quote request book QuoteStatus for {venue}', '', response[qrb_quote_status.name])
    if venue == '':
        verifier.compare_values(f'Quote request book QuoteStatus for 2nd quote', 'Accepted',
                                response[qrb_quote_status.name])
    verifier.compare_values('Tenor', 'Broken', response[qrb_tenor.name])
    verifier.verify()


def check_quote_request_b_after_reject(base_request, service, case_id, qty, venue):
    qrb = QuoteDetailsRequest(base=base_request)
    if venue == 'CITIR':
        qrb.set_filter(['Qty', qty, 'Venue', venue])
    if venue == '':
        qrb.set_filter(['Qty', qty, 'ClientTier', client_tier])
    qrb_tenor = ExtractionDetail('quoteRequestBook.Tenor', 'Tenor')
    qrb_quote_status = ExtractionDetail('quoteRequestBook.QuoteSts', 'QuoteStatus')
    qrb_status = ExtractionDetail('quoteRequestBook.Sts', 'Status')
    qrb.add_extraction_details([qrb_tenor, qrb_quote_status, qrb_status])
    response = call(service.getQuoteRequestBookDetails, qrb.request())
    verifier = Verifier(case_id)
    verifier.set_event_name("Check QuoteRequest book after cancel")
    if venue == 'CITIR':
        verifier.compare_values(f'Quote request book QuoteStatus for {venue}', '', response[qrb_quote_status.name])
        verifier.compare_values(f'Quote request book Status for {venue}', 'New', response[qrb_status.name])
    if venue == '':
        verifier.compare_values(f'Quote request book QuoteStatus for 2nd quote', 'Canceled',
                                response[qrb_quote_status.name])
        verifier.compare_values(f'Quote request book Status for 2nd quote', 'Terminated', response[qrb_status.name])
    verifier.compare_values('Tenor', 'Broken', response[qrb_tenor.name])
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]

    # Create sub-report for case
    case_id = bca.create_event(case_name, report_id)
    print(f'{case_name} started {datetime.now()}')

    set_base(session_id, case_id)
    case_base_request = get_base_request(session_id, case_id)
    base_tile_data = BaseTileData(base=case_base_request)
    base_tile_details = BaseTileDetails(base=case_base_request)

    ar_service = Stubs.win_act_aggregated_rates_service
    ob_fx_act = Stubs.win_act_order_book_fx
    ob_act = Stubs.win_act_order_book
    cp_service = Stubs.win_act_cp_service
    try:
        rfq = send_rfq_and_reject_broken(case_id, qty_1)
        # send_rfq_and_filled_order_broken(case_id, qty_1)
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, venue_quodfx)
        check_quote_request_b(case_base_request, ar_service, case_id, qty_1, venue_citir)
        rfq.send_quote_cancel()
        check_quote_request_b_after_reject(case_base_request, ar_service, case_id, qty_1, venue_quodfx)
        check_quote_request_b_after_reject(case_base_request, ar_service, case_id, qty_1, venue_citir)
        send_rfq_and_filled_order_broken(case_id, qty_1)
    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
