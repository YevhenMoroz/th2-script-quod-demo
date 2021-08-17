import logging
from datetime import date
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.tenor_settlement_date import wk1, wk2
from quod_qa.fx.fx_wrapper.CaseParamsSellRfq import CaseParamsSellRfq
from quod_qa.fx.fx_wrapper.FixClientSellRfq import FixClientSellRfq
from stubs import Stubs
from win_gui_modules.client_pricing_wrappers import ModifyRatesTileRequest
from win_gui_modules.common_wrappers import BaseTileDetails
from win_gui_modules.utils import call, get_base_request
from win_gui_modules.wrappers import set_base


def create_or_get_rates_tile(base_request, service):
    call(service.createRatesTile, base_request.build())


def modify_rates_tile(base_request, service, instrument, client):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.set_instrument(instrument)
    modify_request.set_client_tier(client)
    call(service.modifyRatesTile, modify_request.build())


def press_executable(base_request, service):
    modify_request = ModifyRatesTileRequest(details=base_request)
    modify_request.press_executable()
    call(service.modifyRatesTile, modify_request.build())


def execute(report_id, session_id):
    case_name = Path(__file__).name[:-3]
    case_id = bca.create_event(case_name, report_id)

    set_base(session_id, case_id)

    cp_service = Stubs.win_act_cp_service

    case_base_request = get_base_request(session_id, case_id)
    base_details = BaseTileDetails(base=case_base_request)
    instrument = "GBP/USD-Spot"
    client_tier = "Iridium1"
    account = "Iridium1_1"
    qty = 1000000
    symbol = "GBP/USD"
    security_type_swap = "FXSWAP"
    security_type = "FXFWD"
    settle_date = wk1()
    leg2_settle_date = wk2()
    settle_type_leg1 = "W1"
    settle_type_leg2 = "W2"
    currency = "GBP"
    settle_currency = "USD"

    side = ""
    leg1_side = "1"
    leg2_side = "2"
    today = date.today()
    today = today.today().strftime('%m/%d/%Y')

    try:
        # Step 1
        create_or_get_rates_tile(base_details, cp_service)
        modify_rates_tile(base_details, cp_service, instrument, client_tier)
        press_executable(base_details, cp_service)
        # Step 2
        params = CaseParamsSellRfq(client_tier, case_id, side=side, leg1_side=leg1_side, leg2_side=leg2_side,
                                   orderqty=qty, leg1_ordqty=qty, leg2_ordqty=qty,
                                   currency=currency, settlcurrency=settle_currency,
                                   leg1_settltype=settle_type_leg1, leg2_settltype=settle_type_leg2,
                                   settldate=settle_date, leg1_settldate=settle_date, leg2_settldate=leg2_settle_date,
                                   symbol=symbol, leg1_symbol=symbol, leg2_symbol=symbol,
                                   securitytype=security_type_swap, leg1_securitytype=security_type,
                                   leg2_securitytype=security_type,
                                   securityid=symbol, account=account)

        rfq = FixClientSellRfq(params)
        rfq.send_request_for_quote_swap()
        rfq.verify_quote_pending_swap()

    except Exception:
        logging.error("Error execution", exc_info=True)
        bca.create_event('Fail test event', status='FAILED', parent_id=case_id)
    finally:
        try:
            # Close tile
            press_executable(base_details, cp_service)
            call(cp_service.closeRatesTile, base_details.build())

        except Exception:
            logging.error("Error execution", exc_info=True)
