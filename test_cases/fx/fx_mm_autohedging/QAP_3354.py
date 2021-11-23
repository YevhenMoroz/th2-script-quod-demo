import logging
from pathlib import Path
import time
from test_cases.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from test_cases.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from custom.tenor_settlement_date import spo
from custom.verifier import Verifier, VerificationMethod
from test_framework.win_gui_wrappers.forex.fx_order_book import FXOrderBook
from stubs import Stubs
from custom import basic_custom_actions as bca
from win_gui_modules.dealing_positions_wrappers import GetOrdersDetailsRequest, ExtractionPositionsFieldsDetails, \
    ExtractionPositionsAction, PositionsInfo
from win_gui_modules.utils import get_base_request, call

client = "AURUM1"
account_client = "AURUM1_1"
account_quod = "QUOD4_1"
symbol = "NOK/SEK"
security_type_spo = "FXSPOT"
settle_date_spo = spo()
settle_type_spo = "0"
qty = "1000000"
qty_2 = "2000000"
qty_3 = "3000000"
currency = "NOK"
settle_currency = "SEK"
side = "1"


def get_dealing_positions_details(del_act, base_request, symbol, account):
    dealing_positions_details = GetOrdersDetailsRequest()
    dealing_positions_details.set_default_params(base_request)
    extraction_id = bca.client_orderid(4)
    dealing_positions_details.set_extraction_id(extraction_id)
    dealing_positions_details.set_filter(["Symbol", symbol, "Account", account])
    position = ExtractionPositionsFieldsDetails("dealingpositions.position", 'Position')
    dealing_positions_details.add_single_positions_info(
        PositionsInfo.create(
            action=ExtractionPositionsAction.create_extraction_action(extraction_details=[position])))

    response = call(del_act.getFxDealingPositionsDetails, dealing_positions_details.request())
    time.sleep(0.5)
    return float(response["dealingpositions.position"].replace(",", ""))


def compare_position(even_name, case_id, expected_pos, actual_pos, method = VerificationMethod.EQUALS):
    verifier = Verifier(case_id)
    verifier.set_event_name(even_name)
    verifier.compare_values("Quote position", str(float(expected_pos)), str(actual_pos), method)
    verifier.verify()


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)
    pos_service = Stubs.act_fx_dealing_positions
    case_base_request = get_base_request(session_id, case_id)
    ob_act = Stubs.win_act_order_book
    try:
        initial_pos_eur_usd = get_dealing_positions_details(pos_service, case_base_request, "EUR/USD", account_quod)
        # Step 2
        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

        FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "AO", "Orig", "AutoHedger", "Lookup", "USD/SEK-SPO.SPO", "Client ID", "QUOD4"]). \
            check_order_fields_list({"Sts": "Terminated", "Side": "Buy"},
                                    "Checking placed order AO USD/SEK")
        FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "AO", "Orig", "AutoHedger", "Lookup", "EUR/NOK-SPO.SPO", "Client ID", "QUOD4"]). \
            check_order_fields_list({"Sts": "Terminated", "Side": "Sell"},
                                    "Checking placed order AO EUR/NOK")

        actual_pos_eur_nok = get_dealing_positions_details(pos_service, case_base_request, "EUR/NOK", account_quod)
        actual_pos_usd_sek = get_dealing_positions_details(pos_service, case_base_request, "USD/SEK", account_quod)
        actual_pos_eur_usd = get_dealing_positions_details(pos_service, case_base_request, "EUR/USD", account_quod)

        compare_position('Checking positions Client QUOD4_1 EUR/NOK', case_id, "0", actual_pos_eur_nok)
        compare_position('Checking positions Client QUOD4_1 USD/SEK', case_id, "0", actual_pos_usd_sek)
        compare_position('Checking positions Client QUOD4_1 EUR/USD not equal', case_id, initial_pos_eur_usd, actual_pos_eur_usd, VerificationMethod.NOT_EQUALS)

        # # Step 3
        initial_pos_nok_sek = get_dealing_positions_details(pos_service, case_base_request, "NOK/SEK", account_client)

        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_2, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side=side,
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("OfferPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

        FXOrderBook(case_id, case_base_request).set_filter(
            ["Order ID", "AO", "Orig", "AutoHedger", "Lookup", "EUR/USD-SPO.SPO", "Client ID", "QUOD4"]). \
            check_order_fields_list({"Sts": "Terminated", "Side": "Buy"},
                                    "Checking placed order AO EUR/USD")

        actual_pos_eur_nok = get_dealing_positions_details(pos_service, case_base_request, "EUR/NOK", account_quod)
        actual_pos_usd_sek = get_dealing_positions_details(pos_service, case_base_request, "USD/SEK", account_quod)
        actual_pos_eur_usd_ = get_dealing_positions_details(pos_service, case_base_request, "EUR/USD", account_quod)
        actual_pos_nok_sek = get_dealing_positions_details(pos_service, case_base_request, "NOK/SEK", account_client)

        compare_position('Checking positions Client QUOD4_1 EUR/NOK', case_id, "0", actual_pos_eur_nok)
        compare_position('Checking positions Client QUOD4_1 USD/SEK', case_id, "0", actual_pos_usd_sek)
        compare_position('Checking positions Client QUOD4_1 EUR/USD not equal', case_id, actual_pos_eur_usd, actual_pos_eur_usd_, VerificationMethod.NOT_EQUALS)
        compare_position('Checking positions Client QUOD4_1 NOK/SEK not equal', case_id, initial_pos_nok_sek, actual_pos_nok_sek, VerificationMethod.NOT_EQUALS)

        # PostConditions
        params_spot = CaseParamsSellRfq(client, case_id, orderqty=qty_3, symbol=symbol,
                                        securitytype=security_type_spo, settldate=settle_date_spo,
                                        settltype=settle_type_spo, securityid=symbol, settlcurrency=settle_currency,
                                        currency=currency, side="2",
                                        account=account_client)
        rfq = FixClientSellRfq(params_spot)
        rfq.send_request_for_quote()
        rfq.verify_quote_pending()
        price = rfq.extract_filed("BidPx")
        rfq.send_new_order_single(price=price). \
            verify_order_pending(). \
            verify_order_filled()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
